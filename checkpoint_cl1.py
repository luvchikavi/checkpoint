"""
Check Point Software Technologies - Environmental Compliance Dashboard
A comprehensive demo for LCA, EPD, CBAM, and GHG emissions management
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Check Point Environmental Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #000000;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #E4002B;
    }
    .stButton>button {
        background-color: #E4002B;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #c50025;
    }
    .scenario-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample data for Check Point
def get_checkpoint_data():
    """Generate sample environmental data for Check Point"""
    
    # Historical emissions data (last 12 months)
    months = pd.date_range(end=datetime.now(), periods=12, freq='M')
    historical_data = pd.DataFrame({
        'Month': months,
        'Data Centers': np.random.uniform(8500, 9500, 12),
        'Cloud Infrastructure': np.random.uniform(3500, 4200, 12),
        'Office Buildings': np.random.uniform(2800, 3200, 12),
        'Employee Commute': np.random.uniform(1200, 1500, 12),
        'Business Travel': np.random.uniform(2500, 3500, 12),
        'Software Development': np.random.uniform(1800, 2200, 12)
    })
    
    # Product portfolio
    products = pd.DataFrame({
        'Product': ['Quantum Firewall', 'CloudGuard', 'Harmony Endpoint', 'Infinity Platform', 'Mobile Security'],
        'Category': ['Network Security', 'Cloud Security', 'Endpoint Security', 'Unified Platform', 'Mobile Security'],
        'Annual_Units': [50000, 75000, 120000, 30000, 45000],
        'GWP_per_unit': [45.2, 12.8, 8.5, 156.3, 6.2],
        'Status': ['Compliant', 'Compliant', 'In Progress', 'Compliant', 'Pending']
    })
    
    # Facility data
    facilities = pd.DataFrame({
        'Location': ['Tel Aviv HQ', 'California Office', 'Singapore DC', 'Frankfurt DC', 'Tokyo Office'],
        'Type': ['Office/R&D', 'Office/R&D', 'Data Center', 'Data Center', 'Office'],
        'Size_sqm': [15000, 12000, 8000, 6500, 5000],
        'Employees': [1500, 800, 50, 40, 300],
        'Annual_Energy_MWh': [8500, 6200, 15000, 12000, 2800],
        'Renewable_Percent': [35, 60, 25, 45, 40]
    })
    
    return historical_data, products, facilities

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'
if 'lca_step' not in st.session_state:
    st.session_state.lca_step = 1
if 'lca_data' not in st.session_state:
    st.session_state.lca_data = {}

# Load data
historical_data, products, facilities = get_checkpoint_data()

# Sidebar navigation
st.sidebar.image("/Users/aviluvchik/app/CLIMATERIX/Checkpiont/streamlit/checkpiont_logo.png", 
                 width=200)
st.sidebar.markdown("---")
st.sidebar.markdown("### Environmental Compliance Platform")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "LCA Calculator", "EPD Generator", "Operations Decision Tool", "Financial Analysis"],
    key='navigation'
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Check Point Software Technologies**  
Leading Cybersecurity Solutions Provider

100,000+ Organizations Protected  
7,000+ Employees Worldwide  
60+ Countries  
""")

# ============================================
# PAGE 1: DASHBOARD
# ============================================
if "Dashboard" in page:
    st.markdown('<div class="main-header">Check Point Environmental Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Real-time GHG Emissions Tracking & Compliance Monitoring</div>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total CO₂ Emissions (YTD)",
            "234,560 tons CO₂e",
            "-12.3%",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Active EPDs",
            "15",
            "+3"
        )
    
    with col3:
        st.metric(
            "CBAM Compliance",
            "94%",
            "+6%"
        )
    
    with col4:
        st.metric(
            "Carbon Intensity",
            "2.8 kg CO₂e/user",
            "-8.5%",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly GHG Emissions by Source")
        
        # Prepare data for stacked area chart
        emissions_melted = historical_data.melt(
            id_vars=['Month'], 
            var_name='Source', 
            value_name='Emissions_tCO2e'
        )
        
        fig = px.area(
            emissions_melted,
            x='Month',
            y='Emissions_tCO2e',
            color='Source',
            title='',
            color_discrete_map={
                'Data Centers': '#E4002B',
                'Cloud Infrastructure': '#FF6B6B',
                'Office Buildings': '#4ECDC4',
                'Employee Commute': '#45B7D1',
                'Business Travel': '#FFA07A',
                'Software Development': '#98D8C8'
            }
        )
        fig.update_layout(height=350, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Emissions by Category (Current Month)")
        
        current_month = historical_data.iloc[-1]
        categories = ['Data Centers', 'Cloud Infrastructure', 'Office Buildings', 
                     'Employee Commute', 'Business Travel', 'Software Development']
        values = [current_month[cat] for cat in categories]
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=values,
            hole=0.4,
            marker=dict(colors=['#E4002B', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
        )])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Facility Energy Consumption")
        
        fig = px.bar(
            facilities,
            x='Location',
            y='Annual_Energy_MWh',
            color='Renewable_Percent',
            title='',
            labels={'Annual_Energy_MWh': 'Energy (MWh/year)', 'Renewable_Percent': 'Renewable %'},
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Product Carbon Footprint")
        
        fig = px.scatter(
            products,
            x='Annual_Units',
            y='GWP_per_unit',
            size='Annual_Units',
            color='Status',
            hover_data=['Product'],
            title='',
            labels={'Annual_Units': 'Annual Units Sold', 'GWP_per_unit': 'GWP (kg CO₂e/unit)'},
            color_discrete_map={'Compliant': '#4CAF50', 'In Progress': '#FFA726', 'Pending': '#EF5350'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Product Performance Table
    st.subheader("Product Environmental Performance")
    
    products['Total_GWP'] = products['Annual_Units'] * products['GWP_per_unit']
    products_display = products.copy()
    products_display['Total_GWP'] = products_display['Total_GWP'].apply(lambda x: f"{x:,.0f} kg CO₂e")
    products_display['GWP_per_unit'] = products_display['GWP_per_unit'].apply(lambda x: f"{x:.1f}")
    products_display['Annual_Units'] = products_display['Annual_Units'].apply(lambda x: f"{x:,}")
    
    st.dataframe(products_display, use_container_width=True, height=250)

# ============================================
# PAGE 2: LCA CALCULATOR
# ============================================
elif "LCA Calculator" in page:
    st.markdown('<div class="main-header">Life Cycle Assessment Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculate environmental impact of cybersecurity products</div>', unsafe_allow_html=True)
    
    # Progress indicator
    steps = ['Product Info', 'Materials & Components', 'Energy & Cloud', 'Transport & Logistics', 'Results']
    current_step = st.session_state.lca_step
    
    # Progress bar
    progress_cols = st.columns(5)
    for i, step in enumerate(steps, 1):
        with progress_cols[i-1]:
            if i < current_step:
                st.success(f"COMPLETED: {step}")
            elif i == current_step:
                st.info(f"CURRENT: {step}")
            else:
                st.text(f"PENDING: {step}")
    
    st.markdown("---")
    
    # Step 1: Product Information
    if current_step == 1:
        st.subheader("Step 1: Product Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("Product Name", placeholder="e.g., Quantum 6500 Firewall")
            product_category = st.selectbox(
                "Product Category",
                ["Network Security Appliance", "Cloud Security Service", "Endpoint Security Software", 
                 "Mobile Security App", "Security Management Platform"]
            )
            functional_unit = st.selectbox(
                "Functional Unit",
                ["1 device", "1 license", "1000 users/year", "1 rack unit", "1 software instance"]
            )
        
        with col2:
            production_location = st.selectbox(
                "Primary Production/Deployment Location",
                ["Israel", "United States", "Singapore", "Europe (Germany)", "Global Distribution"]
            )
            expected_lifetime = st.number_input("Expected Lifetime (years)", min_value=1, max_value=20, value=5)
            annual_volume = st.number_input("Annual Volume/Licenses", min_value=1, value=10000)
        
        st.markdown("---")
        
        if st.button("Next: Materials & Components", use_container_width=True):
            st.session_state.lca_data['step1'] = {
                'product_name': product_name,
                'category': product_category,
                'functional_unit': functional_unit,
                'location': production_location,
                'lifetime': expected_lifetime,
                'volume': annual_volume
            }
            st.session_state.lca_step = 2
            st.rerun()
    
    # Step 2: Materials & Components
    elif current_step == 2:
        st.subheader("Step 2: Materials & Components")
        
        st.info("For hardware products, specify physical materials. For software/cloud services, focus on infrastructure.")
        
        # Material database search
        st.markdown("#### Search Material Database")
        material_search = st.text_input("Search materials (e.g., 'steel', 'printed circuit board', 'aluminum')")
        
        # Sample materials database
        materials_db = {
            'Steel, low-alloyed': {'gwp': 2.1, 'unit': 'kg', 'source': 'Ecoinvent'},
            'Aluminum, primary': {'gwp': 11.5, 'unit': 'kg', 'source': 'Ecoinvent'},
            'Printed Circuit Board (PCB)': {'gwp': 15.8, 'unit': 'kg', 'source': 'Ecoinvent'},
            'Plastic, ABS': {'gwp': 3.4, 'unit': 'kg', 'source': 'Ecoinvent'},
            'Copper': {'gwp': 4.2, 'unit': 'kg', 'source': 'Ecoinvent'},
            'Glass fiber': {'gwp': 2.8, 'unit': 'kg', 'source': 'Ecoinvent'},
            'Server (average)': {'gwp': 1200, 'unit': 'unit', 'source': 'ICT Sector'},
            'Network Switch': {'gwp': 450, 'unit': 'unit', 'source': 'ICT Sector'},
        }
        
        if material_search:
            filtered = {k: v for k, v in materials_db.items() if material_search.lower() in k.lower()}
            if filtered:
                st.success(f"Found {len(filtered)} materials")
                for material, data in filtered.items():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.text(material)
                    with col2:
                        st.text(f"{data['gwp']} kg CO₂e")
                    with col3:
                        st.text(f"per {data['unit']}")
                    with col4:
                        if st.button("Add", key=f"add_{material}"):
                            if 'materials' not in st.session_state.lca_data:
                                st.session_state.lca_data['materials'] = []
                            st.session_state.lca_data['materials'].append({
                                'name': material,
                                'gwp': data['gwp'],
                                'quantity': 1,
                                'unit': data['unit']
                            })
                            st.rerun()
        
        st.markdown("---")
        
        # Display added materials
        if 'materials' in st.session_state.lca_data and st.session_state.lca_data['materials']:
            st.markdown("#### Added Materials")
            for i, material in enumerate(st.session_state.lca_data['materials']):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.text(material['name'])
                with col2:
                    quantity = st.number_input(
                        f"Quantity ({material['unit']})",
                        min_value=0.1,
                        value=float(material['quantity']),
                        key=f"qty_{i}"
                    )
                    st.session_state.lca_data['materials'][i]['quantity'] = quantity
                with col3:
                    impact = material['gwp'] * quantity
                    st.metric("Impact", f"{impact:.1f} kg CO₂e")
                with col4:
                    if st.button("Delete", key=f"del_{i}"):
                        st.session_state.lca_data['materials'].pop(i)
                        st.rerun()
            
            total_materials = sum(m['gwp'] * m['quantity'] for m in st.session_state.lca_data['materials'])
            st.info(f"**Total Materials Impact: {total_materials:.1f} kg CO₂e**")
        else:
            st.warning("No materials added yet. Search and add materials above.")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back", use_container_width=True):
                st.session_state.lca_step = 1
                st.rerun()
        with col2:
            if st.button("Next: Energy & Cloud", use_container_width=True):
                st.session_state.lca_step = 3
                st.rerun()
    
    # Step 3: Energy & Cloud Infrastructure
    elif current_step == 3:
        st.subheader("Step 3: Energy & Cloud Infrastructure")
        
        st.info("Specify energy consumption for manufacturing, operation, and cloud services.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Manufacturing Energy")
            manufacturing_energy = st.number_input("Manufacturing Energy (kWh)", min_value=0.0, value=150.0)
            energy_grid_factor = st.selectbox(
                "Grid Emission Factor",
                ["Israel (0.52 kg CO₂e/kWh)", "EU Average (0.38 kg CO₂e/kWh)", 
                 "US Average (0.42 kg CO₂e/kWh)", "Renewable (0.05 kg CO₂e/kWh)"]
            )
            
            st.markdown("#### Operational Energy (per year)")
            operational_energy = st.number_input("Device/Service Energy Consumption (kWh/year)", min_value=0.0, value=500.0)
            use_phase_years = st.number_input("Use Phase Duration (years)", min_value=1, max_value=20, value=5)
        
        with col2:
            st.markdown("#### Cloud Infrastructure")
            cloud_based = st.checkbox("Cloud-based service?", value=True)
            
            if cloud_based:
                cloud_provider = st.selectbox(
                    "Cloud Provider",
                    ["AWS", "Azure", "Google Cloud", "Private Cloud"]
                )
                cloud_region = st.selectbox(
                    "Primary Region",
                    ["US East", "EU West", "Asia Pacific", "Middle East"]
                )
                compute_hours = st.number_input("Annual Compute Hours", min_value=0, value=8760)
                storage_tb = st.number_input("Storage (TB)", min_value=0.0, value=10.0)
                
                # Calculate cloud emissions
                cloud_emission_factor = 0.25  # kg CO₂e per compute hour (average)
                storage_emission_factor = 0.02  # kg CO₂e per TB per year
                
                cloud_emissions = (compute_hours * cloud_emission_factor) + (storage_tb * storage_emission_factor)
                st.metric("Estimated Cloud Emissions", f"{cloud_emissions:.1f} kg CO₂e/year")
        
        # Calculate energy emissions
        grid_factors = {
            "Israel (0.52 kg CO₂e/kWh)": 0.52,
            "EU Average (0.38 kg CO₂e/kWh)": 0.38,
            "US Average (0.42 kg CO₂e/kWh)": 0.42,
            "Renewable (0.05 kg CO₂e/kWh)": 0.05
        }
        
        factor = grid_factors[energy_grid_factor]
        manufacturing_emissions = manufacturing_energy * factor
        operational_emissions = operational_energy * factor * use_phase_years
        
        st.session_state.lca_data['energy'] = {
            'manufacturing': manufacturing_emissions,
            'operational': operational_emissions,
            'cloud': cloud_emissions if cloud_based else 0
        }
        
        st.markdown("---")
        
        st.success(f"""
        **Energy Impact Summary:**
        - Manufacturing: {manufacturing_emissions:.1f} kg CO₂e
        - Operational ({use_phase_years} years): {operational_emissions:.1f} kg CO₂e
        - Cloud Infrastructure: {cloud_emissions if cloud_based else 0:.1f} kg CO₂e/year
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back", use_container_width=True):
                st.session_state.lca_step = 2
                st.rerun()
        with col2:
            if st.button("Next: Transport & Logistics", use_container_width=True):
                st.session_state.lca_step = 4
                st.rerun()
    
    # Step 4: Transport & Logistics
    elif current_step == 4:
        st.subheader("Step 4: Transport & Logistics")
        
        st.info("Specify transportation for materials, products, and distribution.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Supply Chain Transport")
            supplier_distance = st.number_input("Average Supplier Distance (km)", min_value=0, value=2000)
            transport_mode_supply = st.selectbox(
                "Transport Mode (Suppliers)",
                ["Air Freight", "Sea Freight", "Road (Truck)", "Rail"]
            )
            
            st.markdown("#### Product Distribution")
            distribution_distance = st.number_input("Average Distribution Distance (km)", min_value=0, value=1500)
            transport_mode_dist = st.selectbox(
                "Transport Mode (Distribution)",
                ["Air Freight", "Sea Freight", "Road (Truck)", "Rail"],
                key="dist_mode"
            )
        
        with col2:
            st.markdown("#### Emission Factors (kg CO₂e per ton-km)")
            
            emission_factors = {
                "Air Freight": 1.2,
                "Sea Freight": 0.015,
                "Road (Truck)": 0.12,
                "Rail": 0.03
            }
            
            # Calculate transport emissions
            product_weight = st.number_input("Product Weight (kg)", min_value=0.1, value=5.0)
            
            supply_emissions = (supplier_distance * (product_weight/1000) * emission_factors[transport_mode_supply])
            dist_emissions = (distribution_distance * (product_weight/1000) * emission_factors[transport_mode_dist])
            
            st.metric("Supply Chain Transport", f"{supply_emissions:.2f} kg CO₂e")
            st.metric("Distribution Transport", f"{dist_emissions:.2f} kg CO₂e")
            
            total_transport = supply_emissions + dist_emissions
            st.info(f"**Total Transport Emissions: {total_transport:.2f} kg CO₂e**")
        
        st.session_state.lca_data['transport'] = {
            'supply_chain': supply_emissions,
            'distribution': dist_emissions,
            'total': total_transport
        }
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back", use_container_width=True):
                st.session_state.lca_step = 3
                st.rerun()
        with col2:
            if st.button("Calculate Results", use_container_width=True):
                st.session_state.lca_step = 5
                st.rerun()
    
    # Step 5: Results
    elif current_step == 5:
        st.subheader("Step 5: LCA Results")
        
        # Calculate total impact
        materials_total = sum(m['gwp'] * m['quantity'] for m in st.session_state.lca_data.get('materials', []))
        energy_total = sum(st.session_state.lca_data.get('energy', {}).values())
        transport_total = st.session_state.lca_data.get('transport', {}).get('total', 0)
        
        total_gwp = materials_total + energy_total + transport_total
        
        # Display results
        st.success(f"## Total Global Warming Potential: {total_gwp:.1f} kg CO₂e")
        
        # Results breakdown
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Materials", f"{materials_total:.1f} kg CO₂e", 
                     f"{(materials_total/total_gwp*100):.1f}%")
        
        with col2:
            st.metric("Energy", f"{energy_total:.1f} kg CO₂e",
                     f"{(energy_total/total_gwp*100):.1f}%")
        
        with col3:
            st.metric("Transport", f"{transport_total:.1f} kg CO₂e",
                     f"{(transport_total/total_gwp*100):.1f}%")
        
        with col4:
            # Compare to benchmark
            benchmark = 250  # kg CO₂e (industry average)
            diff = ((total_gwp - benchmark) / benchmark * 100)
            st.metric("vs Industry Avg", f"{abs(diff):.1f}%",
                     f"{'Better' if diff < 0 else 'Worse'}")
        
        st.markdown("---")
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Impact Breakdown by Life Cycle Stage")
            
            stages_data = pd.DataFrame({
                'Stage': ['Raw Materials', 'Manufacturing', 'Transport', 'Use Phase', 'End of Life'],
                'Impact': [
                    materials_total * 0.7,
                    st.session_state.lca_data.get('energy', {}).get('manufacturing', 0),
                    transport_total,
                    st.session_state.lca_data.get('energy', {}).get('operational', 0),
                    materials_total * 0.1
                ]
            })
            
            fig = px.bar(stages_data, x='Stage', y='Impact', 
                        title='', 
                        color='Impact',
                        color_continuous_scale='RdYlGn_r')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Benchmarking")
            
            benchmark_data = pd.DataFrame({
                'Category': ['Your Product', 'Industry Average', 'Best in Class', 'Regulatory Limit'],
                'GWP': [total_gwp, 250, 180, 400],
                'Type': ['You', 'Reference', 'Reference', 'Reference']
            })
            
            fig = px.bar(benchmark_data, x='Category', y='GWP',
                        title='',
                        color='Type',
                        color_discrete_map={'You': '#E4002B', 'Reference': '#CCCCCC'})
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate EPD Document", use_container_width=True):
                st.success("EPD document generated! Check EPD Generator tab.")
        
        with col2:
            if st.button("Submit for Verification", use_container_width=True):
                st.info("Submission sent to EPD Hub for verification.")
        
        with col3:
            if st.button("Export Results (Excel)", use_container_width=True):
                st.success("Results exported to checkpoint_lca_results.xlsx")
        
        st.markdown("---")
        
        if st.button("Start New Calculation", use_container_width=True):
            st.session_state.lca_step = 1
            st.session_state.lca_data = {}
            st.rerun()

# ============================================
# PAGE 3: EPD GENERATOR
# ============================================
elif "EPD Generator" in page:
    st.markdown('<div class="main-header">EPD Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create Environmental Product Declarations</div>', unsafe_allow_html=True)
    
    # EPD Project Management
    st.markdown("### Active EPD Projects")
    
    epd_projects = pd.DataFrame({
        'Project ID': ['EPD-001', 'EPD-002', 'EPD-003', 'EPD-004', 'EPD-005'],
        'Product': ['Quantum 6500', 'CloudGuard SaaS', 'Harmony Endpoint', 'Mobile Security', 'Infinity Platform'],
        'Status': ['Verified', 'In Verification', 'Draft', 'Verified', 'In Progress'],
        'Progress': [100, 75, 30, 100, 60],
        'Created': ['2024-01-15', '2024-08-20', '2024-10-01', '2023-11-10', '2024-09-15'],
        'Valid Until': ['2029-01-15', '2029-08-20', '-', '2028-11-10', '-']
    })
    
    # Color code status
    def color_status(val):
        if val == 'Verified':
            return 'background-color: #d4edda'
        elif val == 'In Verification':
            return 'background-color: #fff3cd'
        elif val == 'In Progress':
            return 'background-color: #cce5ff'
        else:
            return 'background-color: #f8f9fa'
    
    styled_df = epd_projects.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, height=250)
    
    st.markdown("---")
    
    # Create New EPD
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Create New EPD")
        
        new_product = st.selectbox(
            "Select Product",
            ["Quantum 6500 Firewall", "Quantum 9800", "CloudGuard Posture", "Harmony Email", "New Product..."]
        )
        
        pcr_standard = st.selectbox(
            "PCR Standard",
            ["EN 15804+A2 (Construction Products)",
             "ISO 14025 (General Products)",
             "ITU-T L.1410 (ICT Goods & Services)",
             "Custom PCR"]
        )
        
        verification_body = st.selectbox(
            "Verification Body",
            ["EPD Hub", "EPD International", "IBU (Germany)", "UL Solutions", "NSF International"]
        )
    
    with col2:
        st.markdown("### EPD Statistics")
        st.metric("Total EPDs", "15", "+3 this year")
        st.metric("Verified EPDs", "8", "53%")
        st.metric("Avg. Verification Time", "3.2 weeks")
    
    if st.button("Create EPD Project", use_container_width=True):
        st.success(f"EPD project created for {new_product}!")
        st.info("Next steps: Complete LCA calculation → Upload supporting documents → Submit for verification")
    
    st.markdown("---")
    
    # EPD Template Preview
    st.markdown("### EPD Document Preview")
    
    with st.expander("View Sample EPD Structure"):
        st.markdown("""
        **Environmental Product Declaration**
        
        **Product:** Quantum 6500 Network Security Appliance  
        **Manufacturer:** Check Point Software Technologies Ltd.  
        **Declaration Number:** EPD-CHKP-001-2024  
        **Valid Until:** January 2029  
        
        ---
        
        **1. Product Information**
        - Product Name: Quantum 6500
        - Category: Network Security Appliance
        - Functional Unit: 1 device (5-year lifetime)
        - Production Location: Israel & Global Assembly
        
        **2. LCA Information**
        - PCR Used: ITU-T L.1410 (ICT Equipment)
        - LCA Method: ISO 14040/14044
        - System Boundary: Cradle-to-gate + Use phase
        - Data Quality: Primary data (85%), Secondary data (15%)
        
        **3. Environmental Impacts**
        
        | Impact Category | Value | Unit |
        |----------------|-------|------|
        | Global Warming Potential (GWP) | 245.5 | kg CO₂e |
        | Acidification Potential (AP) | 1.24 | kg SO₂e |
        | Eutrophication Potential (EP) | 0.89 | kg PO₄e |
        | Ozone Depletion Potential (ODP) | 0.0012 | kg CFC-11e |
        | Water Use | 450 | m³ |
        
        **4. Life Cycle Stages (A1-C4)**
        - A1-A3 (Production): 120 kg CO₂e
        - A4 (Transport): 30 kg CO₂e
        - B1-B7 (Use Phase): 85 kg CO₂e
        - C1-C4 (End of Life): 10.5 kg CO₂e
        
        **5. Additional Information**
        - Hazardous Substances: Compliant with RoHS
        - Recyclability: 78% by weight
        - Energy Efficiency: ENERGY STAR certified
        
        **6. Verification**
        - Verified by: EPD Hub
        - Verification Date: January 15, 2024
        - Program Operator: EPD International
        """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download EPD Template", use_container_width=True):
            st.success("EPD template downloaded!")
    
    with col2:
        if st.button("Upload Supporting Docs", use_container_width=True):
            st.info("Document upload interface opened")
    
    with col3:
        if st.button("Sync with EPD Hub API", use_container_width=True):
            st.success("Synced with EPD Hub!")

# ============================================
# PAGE 4: OPERATIONS DECISION TOOL
# ============================================
elif "Operations Decision Tool" in page:
    st.markdown('<div class="main-header">Operations Decision Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">GHG Reduction Scenario Modeling & Strategic Planning</div>', unsafe_allow_html=True)
    
    # Baseline emissions
    st.markdown("### Current Baseline (2024)")
    
    baseline = {
        'Data Centers': 106000,
        'Cloud Infrastructure': 45000,
        'Office Buildings': 36000,
        'Employee Commute': 15600,
        'Business Travel': 35000,
        'Software Development': 23000
    }
    
    baseline_total = sum(baseline.values())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Emissions", f"{baseline_total:,} tons CO₂e")
    with col2:
        st.metric("Per Employee", f"{baseline_total/7000:.1f} tons CO₂e")
    with col3:
        st.metric("Per Revenue ($M)", f"{baseline_total/2500:.1f} tons CO₂e/$M")
    with col4:
        st.metric("Target Reduction", "30% by 2030")
    
    st.markdown("---")
    
    # Scenario Builder
    st.markdown("### Build Your Reduction Scenario")
    st.info("Adjust the sliders below to model different emission reduction strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Energy Transition")
        
        renewable_data_centers = st.slider(
            "Renewable Energy for Data Centers (%)",
            min_value=0, max_value=100, value=35, step=5,
            help="Transition to renewable energy sources"
        )
        
        renewable_offices = st.slider(
            "Renewable Energy for Offices (%)",
            min_value=0, max_value=100, value=45, step=5
        )
        
        server_efficiency = st.slider(
            "Server Efficiency Improvement (%)",
            min_value=0, max_value=50, value=15, step=5,
            help="Upgrade to more efficient servers"
        )
        
        cooling_optimization = st.slider(
            "Cooling System Optimization (%)",
            min_value=0, max_value=40, value=20, step=5,
            help="Improve PUE (Power Usage Effectiveness)"
        )
    
    with col2:
        st.markdown("#### Transportation & Travel")
        
        flight_reduction = st.slider(
            "Business Flight Reduction (%)",
            min_value=0, max_value=70, value=30, step=5,
            help="Replace with virtual meetings"
        )
        
        ev_fleet = st.slider(
            "Company Fleet EV Transition (%)",
            min_value=0, max_value=100, value=25, step=5,
            help="Replace combustion vehicles with EVs"
        )
        
        public_transport = st.slider(
            "Employees Using Public Transport (%)",
            min_value=0, max_value=80, value=40, step=5,
            help="Incentivize public transportation"
        )
        
        remote_work = st.slider(
            "Remote Work Days per Week",
            min_value=0, max_value=5, value=2, step=1,
            help="Reduce commuting emissions"
        )
    
    st.markdown("---")
    
    # Calculate scenario impact
    st.markdown("### Scenario Impact Analysis")
    
    # Calculate reductions
    reductions = {
        'Data Centers': baseline['Data Centers'] * (
            (renewable_data_centers/100 * 0.9) + 
            (server_efficiency/100 * 0.15) + 
            (cooling_optimization/100 * 0.10)
        ),
        'Cloud Infrastructure': baseline['Cloud Infrastructure'] * (renewable_data_centers/100 * 0.8),
        'Office Buildings': baseline['Office Buildings'] * (renewable_offices/100 * 0.85),
        'Employee Commute': baseline['Employee Commute'] * (
            (public_transport/100 * 0.7) + 
            (remote_work/5 * 0.5) +
            (ev_fleet/100 * 0.3)
        ),
        'Business Travel': baseline['Business Travel'] * (flight_reduction/100),
        'Software Development': baseline['Software Development'] * (renewable_offices/100 * 0.6)
    }
    
    new_emissions = {k: baseline[k] - reductions[k] for k in baseline}
    total_reduction = sum(reductions.values())
    new_total = sum(new_emissions.values())
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Reduction",
            f"{total_reduction:,.0f} tons CO₂e",
            f"-{(total_reduction/baseline_total*100):.1f}%"
        )
    
    with col2:
        st.metric(
            "New Total Emissions",
            f"{new_total:,.0f} tons CO₂e",
            f"{new_total:,.0f}"
        )
    
    with col3:
        target_2030 = baseline_total * 0.7  # 30% reduction
        progress = (baseline_total - new_total) / (baseline_total - target_2030) * 100
        st.metric(
            "Progress to 2030 Target",
            f"{min(progress, 100):.1f}%",
            "On Track" if progress >= 80 else "Below Target"
        )
    
    st.markdown("---")
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Emissions Comparison")
        
        comparison_data = pd.DataFrame({
            'Category': list(baseline.keys()) * 2,
            'Emissions': list(baseline.values()) + list(new_emissions.values()),
            'Scenario': ['Baseline']*6 + ['With Reductions']*6
        })
        
        fig = px.bar(
            comparison_data,
            x='Category',
            y='Emissions',
            color='Scenario',
            barmode='group',
            title='',
            color_discrete_map={'Baseline': '#CCCCCC', 'With Reductions': '#E4002B'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Reduction by Initiative")
        
        reduction_breakdown = pd.DataFrame({
            'Initiative': ['Renewable Energy (DC)', 'Renewable Energy (Offices)', 
                          'Server Efficiency', 'Cooling Optimization',
                          'Flight Reduction', 'EV Fleet', 'Public Transport', 'Remote Work'],
            'Reduction': [
                baseline['Data Centers'] * (renewable_data_centers/100 * 0.9),
                baseline['Office Buildings'] * (renewable_offices/100 * 0.85),
                baseline['Data Centers'] * (server_efficiency/100 * 0.15),
                baseline['Data Centers'] * (cooling_optimization/100 * 0.10),
                baseline['Business Travel'] * (flight_reduction/100),
                baseline['Employee Commute'] * (ev_fleet/100 * 0.3),
                baseline['Employee Commute'] * (public_transport/100 * 0.7),
                baseline['Employee Commute'] * (remote_work/5 * 0.5)
            ]
        }).sort_values('Reduction', ascending=True)
        
        fig = px.bar(
            reduction_breakdown,
            x='Reduction',
            y='Initiative',
            orientation='h',
            title='',
            color='Reduction',
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("### Strategic Recommendations")
    
    recommendations = []
    
    if renewable_data_centers < 50:
        recommendations.append({
            'Priority': 'HIGH',
            'Action': 'Increase Renewable Energy for Data Centers',
            'Impact': f'+{((50-renewable_data_centers)/100 * baseline["Data Centers"] * 0.9):,.0f} tons CO₂e reduction',
            'Timeframe': '12-18 months'
        })
    
    if flight_reduction < 40:
        recommendations.append({
            'Priority': 'MEDIUM',
            'Action': 'Reduce Business Flights by 40%',
            'Impact': f'+{((40-flight_reduction)/100 * baseline["Business Travel"]):,.0f} tons CO₂e reduction',
            'Timeframe': '6-12 months'
        })
    
    if remote_work < 3:
        recommendations.append({
            'Priority': 'MEDIUM',
            'Action': 'Implement 3-day Remote Work Policy',
            'Impact': f'+{((3-remote_work)/5 * baseline["Employee Commute"] * 0.5):,.0f} tons CO₂e reduction',
            'Timeframe': '3-6 months'
        })
    
    if server_efficiency < 30:
        recommendations.append({
            'Priority': 'HIGH',
            'Action': 'Upgrade to High-Efficiency Servers',
            'Impact': f'+{((30-server_efficiency)/100 * baseline["Data Centers"] * 0.15):,.0f} tons CO₂e reduction',
            'Timeframe': '18-24 months'
        })
    
    if recommendations:
        rec_df = pd.DataFrame(recommendations)
        st.dataframe(rec_df, use_container_width=True, height=200)
    else:
        st.success("Excellent! Your scenario meets or exceeds all recommended targets.")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Save Scenario", use_container_width=True):
            st.success("Scenario saved!")
    
    with col2:
        if st.button("Generate Report", use_container_width=True):
            st.success("Detailed report generated!")
    
    with col3:
        if st.button("Share with Leadership", use_container_width=True):
            st.info("Scenario emailed to stakeholders")

# ============================================
# PAGE 5: FINANCIAL ANALYSIS
# ============================================
elif "Financial Analysis" in page:
    st.markdown('<div class="main-header">Financial Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Cost-Effective GHG Reduction Analysis & ROI Calculator</div>', unsafe_allow_html=True)
    
    # Investment scenarios
    st.markdown("### Reduction Investment Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Select Initiatives")
        
        initiatives = {
            'Renewable Energy (Data Centers)': {
                'cost': 2500000,
                'reduction': 50000,
                'payback': 5,
                'selected': st.checkbox('Renewable Energy for Data Centers', value=True)
            },
            'Server Efficiency Upgrade': {
                'cost': 1800000,
                'reduction': 15000,
                'payback': 4,
                'selected': st.checkbox('Upgrade to Efficient Servers', value=True)
            },
            'EV Fleet Transition': {
                'cost': 3200000,
                'reduction': 4500,
                'payback': 7,
                'selected': st.checkbox('Transition to Electric Vehicles', value=False)
            },
            'Remote Work Infrastructure': {
                'cost': 500000,
                'reduction': 7800,
                'payback': 2,
                'selected': st.checkbox('Remote Work Technology', value=True)
            },
            'Building Energy Efficiency': {
                'cost': 1200000,
                'reduction': 18000,
                'payback': 6,
                'selected': st.checkbox('Office Building Upgrades', value=False)
            },
            'Carbon Offsets (Credits)': {
                'cost': 200000,
                'reduction': 20000,
                'payback': 1,
                'selected': st.checkbox('Purchase Carbon Offsets', value=False)
            }
        }
    
    with col2:
        st.markdown("#### Cost Parameters")
        
        carbon_price = st.number_input(
            "Carbon Price (€/ton CO₂e)",
            min_value=0,
            max_value=200,
            value=75,
            step=5,
            help="Current EU ETS price or internal carbon price"
        )
        
        electricity_price = st.number_input(
            "Electricity Price (€/MWh)",
            min_value=0,
            max_value=500,
            value=120,
            step=10
        )
        
        discount_rate = st.slider(
            "Discount Rate (%)",
            min_value=0,
            max_value=15,
            value=5,
            step=1,
            help="For NPV calculations"
        )
        
        analysis_period = st.slider(
            "Analysis Period (years)",
            min_value=5,
            max_value=20,
            value=10,
            step=1
        )
    
    st.markdown("---")
    
    # Calculate financial metrics
    selected_initiatives = {k: v for k, v in initiatives.items() if v['selected']}
    
    if selected_initiatives:
        st.markdown("### Financial Analysis Results")
        
        total_investment = sum(init['cost'] for init in selected_initiatives.values())
        total_reduction = sum(init['reduction'] for init in selected_initiatives.values())
        
        # Annual savings
        carbon_cost_savings = total_reduction * carbon_price
        energy_cost_savings = total_reduction * 0.4 * electricity_price / 1000  # Assuming 40% from energy
        total_annual_savings = carbon_cost_savings + energy_cost_savings
        
        # Simple payback
        simple_payback = total_investment / total_annual_savings if total_annual_savings > 0 else float('inf')
        
        # NPV calculation
        npv = -total_investment
        for year in range(1, analysis_period + 1):
            npv += total_annual_savings / ((1 + discount_rate/100) ** year)
        
        # IRR approximation
        irr = (total_annual_savings / total_investment) * 100 if total_investment > 0 else 0
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Investment",
                f"€{total_investment/1000000:.2f}M"
            )
        
        with col2:
            st.metric(
                "Annual Savings",
                f"€{total_annual_savings/1000:.0f}K",
                f"{total_reduction:,.0f} tons CO₂e"
            )
        
        with col3:
            st.metric(
                "Simple Payback",
                f"{simple_payback:.1f} years",
                "✅ Good" if simple_payback < 7 else "⚠️ Long"
            )
        
        with col4:
            st.metric(
                f"NPV ({analysis_period}yr)",
                f"€{npv/1000000:.2f}M",
                "✅ Positive" if npv > 0 else "❌ Negative"
            )
        
        st.markdown("---")
        
        # Detailed breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Cost-Effectiveness Ranking")
            
            cost_effectiveness = []
            for name, data in selected_initiatives.items():
                cost_per_ton = data['cost'] / data['reduction'] if data['reduction'] > 0 else float('inf')
                cost_effectiveness.append({
                    'Initiative': name,
                    'Cost per ton CO₂e': f"€{cost_per_ton:.0f}",
                    'Total Reduction': f"{data['reduction']:,} tons",
                    'Investment': f"€{data['cost']/1000000:.2f}M",
                    'Payback': f"{data['payback']} years"
                })
            
            ce_df = pd.DataFrame(cost_effectiveness)
            st.dataframe(ce_df, use_container_width=True, height=250)
        
        with col2:
            st.markdown("#### Investment vs. Reduction")
            
            investment_data = pd.DataFrame([
                {'Initiative': name, 
                 'Investment (€M)': data['cost']/1000000,
                 'Reduction (tons CO₂e)': data['reduction']}
                for name, data in selected_initiatives.items()
            ])
            
            fig = px.scatter(
                investment_data,
                x='Investment (€M)',
                y='Reduction (tons CO₂e)',
                size='Reduction (tons CO₂e)',
                color='Investment (€M)',
                hover_data=['Initiative'],
                title='',
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Cash flow projection
        st.markdown("#### 10-Year Cash Flow Projection")
        
        years = list(range(0, analysis_period + 1))
        cumulative_cashflow = [-total_investment]
        
        for year in range(1, analysis_period + 1):
            discounted_savings = total_annual_savings / ((1 + discount_rate/100) ** year)
            cumulative_cashflow.append(cumulative_cashflow[-1] + discounted_savings)
        
        cashflow_df = pd.DataFrame({
            'Year': years,
            'Cumulative Cash Flow (€M)': [cf/1000000 for cf in cumulative_cashflow]
        })
        
        fig = px.line(
            cashflow_df,
            x='Year',
            y='Cumulative Cash Flow (€M)',
            title='',
            markers=True
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        # Break-even analysis
        breakeven_year = next((i for i, cf in enumerate(cumulative_cashflow) if cf > 0), None)
        if breakeven_year:
            st.success(f"Break-even achieved in Year {breakeven_year}")
        else:
            st.warning(f"Break-even not achieved within {analysis_period} years")
        
        st.markdown("---")
        
        # Sensitivity analysis
        st.markdown("#### Sensitivity Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Impact of Carbon Price**")
            
            carbon_prices = [50, 75, 100, 125, 150]
            npvs = []
            
            for cp in carbon_prices:
                annual_savings = total_reduction * cp + energy_cost_savings
                npv_temp = -total_investment
                for year in range(1, analysis_period + 1):
                    npv_temp += annual_savings / ((1 + discount_rate/100) ** year)
                npvs.append(npv_temp / 1000000)
            
            sens_df = pd.DataFrame({
                'Carbon Price (€/ton)': carbon_prices,
                'NPV (€M)': npvs
            })
            
            fig = px.line(sens_df, x='Carbon Price (€/ton)', y='NPV (€M)', markers=True)
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Impact of Discount Rate**")
            
            discount_rates = [0, 3, 5, 7, 10]
            npvs = []
            
            for dr in discount_rates:
                npv_temp = -total_investment
                for year in range(1, analysis_period + 1):
                    npv_temp += total_annual_savings / ((1 + dr/100) ** year)
                npvs.append(npv_temp / 1000000)
            
            sens_df = pd.DataFrame({
                'Discount Rate (%)': discount_rates,
                'NPV (€M)': npvs
            })
            
            fig = px.line(sens_df, x='Discount Rate (%)', y='NPV (€M)', markers=True)
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Financial Model", use_container_width=True):
                st.success("Financial model exported to Excel!")
        
        with col2:
            if st.button("Send to CFO", use_container_width=True):
                st.info("Financial analysis emailed to CFO")
        
        with col3:
            if st.button("Save Scenario", use_container_width=True):
                st.success("Financial scenario saved!")
    
    else:
        st.warning("Please select at least one initiative to analyze")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong> 🛡️ Check Point Software Technologies Environmental Compliance Platform</strong></p>
    <p style='font-size: 0.9em;'>© 2025 Climaterix Technologies Ltd. | Demo Version 1.0</p>
</div>
""", unsafe_allow_html=True)
