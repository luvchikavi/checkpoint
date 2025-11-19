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
    initial_sidebar_state="collapsed"
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
    h1, h2, h3 {
        color: #000000;
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

# Header with logo
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    try:
        st.image("checkpiont_logo.png", width=200)
    except:
        st.markdown("### 🔒 Check Point")
with col2:
    st.markdown('<div class="main-header" style="text-align: center;">Environmental Compliance Platform</div>', unsafe_allow_html=True)
with col3:
    st.markdown("")

st.markdown("---")

# Top navigation using tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🔬 LCA Calculator",
    "📄 EPD Generator",
    "⚙️ Operations Decision Tool",
    "💰 Financial Analysis"
])

# ============================================
# TAB 1: DASHBOARD
# ============================================
with tab1:
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

    # GHG Emissions by Scope
    st.subheader("GHG Emissions by Scope (GHG Protocol)")

    col1, col2, col3 = st.columns(3)

    # Calculate emissions by scope from current month data
    current_month = historical_data.iloc[-1]

    # Scope 1: Direct emissions (company-owned sources) - minimal for software company
    scope1_emissions = 500  # Estimated company vehicles, generators, etc.

    # Scope 2: Indirect emissions from purchased energy
    scope2_emissions = (current_month['Data Centers'] +
                       current_month['Cloud Infrastructure'] +
                       current_month['Office Buildings'])

    # Scope 3: Other indirect emissions
    scope3_emissions = (current_month['Employee Commute'] +
                       current_month['Business Travel'] +
                       current_month['Software Development'])

    with col1:
        st.markdown("#### Scope 1: Direct Emissions")
        st.metric(
            "Company-Owned Sources",
            f"{scope1_emissions:,.0f} tons CO₂e",
            help="Direct GHG emissions from sources owned or controlled by the company"
        )
        st.caption("🚗 Fleet vehicles, emergency generators, refrigerants")

    with col2:
        st.markdown("#### Scope 2: Energy Indirect")
        st.metric(
            "Purchased Energy",
            f"{scope2_emissions:,.0f} tons CO₂e",
            help="Indirect emissions from purchased electricity, heat, and cooling"
        )
        st.caption("⚡ Data centers, offices, cloud infrastructure")

    with col3:
        st.markdown("#### Scope 3: Other Indirect")
        st.metric(
            "Value Chain Emissions",
            f"{scope3_emissions:,.0f} tons CO₂e",
            help="All other indirect emissions in the value chain"
        )
        st.caption("✈️ Business travel, commute, supply chain")

    # Scope breakdown chart
    st.markdown("#### Emissions Breakdown by Scope")

    scope_data = pd.DataFrame({
        'Scope': ['Scope 1\nDirect', 'Scope 2\nEnergy', 'Scope 3\nOther Indirect'],
        'Emissions (tons CO₂e)': [scope1_emissions, scope2_emissions, scope3_emissions],
        'Percentage': [
            scope1_emissions / (scope1_emissions + scope2_emissions + scope3_emissions) * 100,
            scope2_emissions / (scope1_emissions + scope2_emissions + scope3_emissions) * 100,
            scope3_emissions / (scope1_emissions + scope2_emissions + scope3_emissions) * 100
        ]
    })

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            scope_data,
            x='Scope',
            y='Emissions (tons CO₂e)',
            color='Scope',
            title='',
            color_discrete_map={
                'Scope 1\nDirect': '#E4002B',
                'Scope 2\nEnergy': '#FFA07A',
                'Scope 3\nOther Indirect': '#4ECDC4'
            }
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=scope_data['Scope'],
            values=scope_data['Emissions (tons CO₂e)'],
            hole=0.4,
            marker=dict(colors=['#E4002B', '#FFA07A', '#4ECDC4']),
            textinfo='label+percent'
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
        
        fig = px.bar(
            products,
            x='Product',
            y='GWP_per_unit',
            color='Status',
            title='',
            labels={'GWP_per_unit': 'kg CO₂e per unit'},
            color_discrete_map={
                'Compliant': '#4ECDC4',
                'In Progress': '#FFA07A',
                'Pending': '#FF6B6B'
            }
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Product Portfolio Table
    st.subheader("Product Portfolio Overview")
    
    products_display = products.copy()
    products_display['Total Annual Impact (tons CO₂e)'] = (
        products_display['Annual_Units'] * products_display['GWP_per_unit'] / 1000
    ).round(2)
    
    st.dataframe(
        products_display[['Product', 'Category', 'Annual_Units', 'GWP_per_unit', 
                         'Total Annual Impact (tons CO₂e)', 'Status']],
        use_container_width=True,
        height=250
    )
    
    st.markdown("---")
    
    # Action items
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**🎯 Next Actions**\n- Update Harmony Endpoint EPD\n- Schedule Q2 audit\n- Review supplier data")
    
    with col2:
        st.warning("**⚠️ Attention Required**\n- 2 products pending EPD\n- CBAM submission due in 14 days")
    
    with col3:
        st.success("**✅ Achievements**\n- 12% emissions reduction YoY\n- 3 new EPDs published\n- 94% CBAM compliance")

# ============================================
# TAB 2: LCA CALCULATOR
# ============================================
with tab2:
    st.markdown('<div class="main-header">Life Cycle Assessment Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculate environmental impacts across product lifecycle</div>', unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.lca_step / 5
    st.progress(progress)
    st.markdown(f"**Step {st.session_state.lca_step} of 5**")
    
    st.markdown("---")
    
    # Step 1: Product Information
    if st.session_state.lca_step == 1:
        st.subheader("Step 1: Product Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input(
                "Product Name",
                value=st.session_state.lca_data.get('product_name', 'Quantum Firewall 5800'),
                help="Enter the name of the product for LCA"
            )
            
            product_category = st.selectbox(
                "Product Category",
                ['Network Security Hardware', 'Cloud Security Service', 'Endpoint Software', 
                 'Unified Security Platform', 'Mobile Security App'],
                index=0
            )
            
            functional_unit = st.text_input(
                "Functional Unit",
                value="1 unit (hardware appliance)",
                help="Define how the product is measured (e.g., '1 unit', '1 license', '1000 users')"
            )
        
        with col2:
            reference_flow = st.number_input(
                "Reference Flow Quantity",
                min_value=1,
                max_value=1000000,
                value=1000,
                help="Number of units for this assessment"
            )
            
            product_lifetime = st.number_input(
                "Expected Product Lifetime (years)",
                min_value=1,
                max_value=20,
                value=5,
                help="How long the product is expected to be used"
            )
            
            geography = st.selectbox(
                "Primary Manufacturing Location",
                ['Israel', 'USA', 'Singapore', 'Germany', 'China', 'Global Average'],
                index=0
            )
        
        st.info("""
        **💡 Tip:** For hardware products, specify physical materials. For software/cloud services, focus on infrastructure.
        """)
        
        if st.button("Next: Materials & Components", use_container_width=True):
            st.session_state.lca_data.update({
                'product_name': product_name,
                'product_category': product_category,
                'functional_unit': functional_unit,
                'reference_flow': reference_flow,
                'product_lifetime': product_lifetime,
                'geography': geography
            })
            st.session_state.lca_step = 2
            st.rerun()
    
    # Step 2: Materials & Components - WITH NEW DROPDOWN FEATURE
    elif st.session_state.lca_step == 2:
        st.subheader("Step 2: Materials & Components")
        
        st.info("""
        For hardware products, specify physical materials. For software/cloud services, focus on infrastructure.
        """)
        
        st.markdown("### Search Material Database")
        
        # Material category dropdown - NEW FEATURE
        material_categories = [
            "All Categories",
            "🔩 Metals (Steel, Aluminum, Copper)",
            "🧪 Plastics & Polymers",
            "💾 Electronics & PCB Components",
            "🏗️ Concrete & Cement",
            "🪟 Glass & Ceramics",
            "🌳 Wood & Natural Materials",
            "⚗️ Chemicals & Compounds",
            "📦 Packaging Materials",
            "🧵 Textiles & Fabrics"
        ]
        
        selected_category = st.selectbox(
            "Filter by Material Category",
            material_categories,
            key="material_category",
            help="Select a category to filter materials, or choose 'All Categories' to search everything"
        )
        
        # Show category description
        if selected_category != "All Categories":
            st.caption(f"📋 Showing materials in: **{selected_category.split(' ', 1)[1]}**")
        
        # Search materials
        search_query = st.text_input(
            "Search materials (e.g., 'steel', 'printed circuit board', 'aluminum')",
            key="material_search",
            help="Type to search across thousands of materials from Ecoinvent, ELCD, and US LCI databases"
        )
        
        # Sample materials database with categories
        sample_materials = {
            "🔩 Metals (Steel, Aluminum, Copper)": [
                {'name': 'Steel, low-alloyed, hot rolled', 'gwp': 2.1, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'Aluminum, primary, ingot', 'gwp': 11.5, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'Copper, primary, at refinery', 'gwp': 3.8, 'unit': 'kg', 'database': 'Ecoinvent'},
            ],
            "🧪 Plastics & Polymers": [
                {'name': 'Polystyrene, high impact', 'gwp': 3.2, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'Polyethylene, high density', 'gwp': 1.9, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'ABS copolymer', 'gwp': 3.5, 'unit': 'kg', 'database': 'Ecoinvent'},
            ],
            "💾 Electronics & PCB Components": [
                {'name': 'Printed circuit board, surface mounted', 'gwp': 15.2, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'Integrated circuit, logic type', 'gwp': 0.45, 'unit': 'piece', 'database': 'Ecoinvent'},
                {'name': 'Capacitor, surface mounted', 'gwp': 0.02, 'unit': 'piece', 'database': 'Ecoinvent'},
            ],
            "🏗️ Concrete & Cement": [
                {'name': 'Concrete, normal, at plant', 'gwp': 0.15, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'Portland cement', 'gwp': 0.92, 'unit': 'kg', 'database': 'US LCI'},
            ],
            "📦 Packaging Materials": [
                {'name': 'Corrugated board', 'gwp': 0.55, 'unit': 'kg', 'database': 'Ecoinvent'},
                {'name': 'Polyethylene film', 'gwp': 2.1, 'unit': 'kg', 'database': 'Ecoinvent'},
            ]
        }
        
        # Filter materials based on category and search
        filtered_materials = []
        
        for cat, materials in sample_materials.items():
            # Filter by category
            if selected_category == "All Categories" or selected_category == cat:
                for mat in materials:
                    # Filter by search query
                    if not search_query or search_query.lower() in mat['name'].lower():
                        filtered_materials.append({
                            'Category': cat,
                            'Material': mat['name'],
                            'GWP': f"{mat['gwp']} kg CO₂e/{mat['unit']}",
                            'Database': mat['database'],
                            'gwp_value': mat['gwp'],
                            'unit': mat['unit']
                        })
        
        if filtered_materials:
            st.markdown(f"**Found {len(filtered_materials)} materials**")
            
            # Display materials as expandable sections
            for idx, mat in enumerate(filtered_materials):
                with st.expander(f"**{mat['Material']}** - {mat['GWP']}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Category:** {mat['Category']}")
                        st.write(f"**Database:** {mat['Database']}")
                    
                    with col2:
                        quantity = st.number_input(
                            "Quantity",
                            min_value=0.0,
                            value=1.0,
                            key=f"qty_{idx}",
                            help=f"Enter quantity in {mat['unit']}"
                        )
                    
                    with col3:
                        st.write(f"**Unit:** {mat['unit']}")
                        if st.button("Add", key=f"add_{idx}"):
                            if 'materials' not in st.session_state.lca_data:
                                st.session_state.lca_data['materials'] = []
                            st.session_state.lca_data['materials'].append({
                                'name': mat['Material'],
                                'quantity': quantity,
                                'unit': mat['unit'],
                                'gwp': mat['gwp_value'],
                                'total_gwp': mat['gwp_value'] * quantity
                            })
                            st.success(f"Added {quantity} {mat['unit']} of {mat['Material']}")
                            st.rerun()
        else:
            st.warning("No materials found. Try adjusting your search or category filter.")
        
        # Display selected materials
        if 'materials' in st.session_state.lca_data and st.session_state.lca_data['materials']:
            st.markdown("---")
            st.markdown("### Selected Materials")
            
            materials_df = pd.DataFrame(st.session_state.lca_data['materials'])
            st.dataframe(materials_df, use_container_width=True)
            
            total_gwp = materials_df['total_gwp'].sum()
            st.metric("Total Materials Impact", f"{total_gwp:.2f} kg CO₂e")
            
            if st.button("Clear All Materials"):
                st.session_state.lca_data['materials'] = []
                st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous: Product Info", use_container_width=True):
                st.session_state.lca_step = 1
                st.rerun()
        
        with col2:
            if st.button("Next: Energy & Manufacturing →", use_container_width=True):
                st.session_state.lca_step = 3
                st.rerun()
    
    # Step 3: Energy & Manufacturing
    elif st.session_state.lca_step == 3:
        st.subheader("Step 3: Energy & Manufacturing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Electricity Consumption")
            
            electricity_kwh = st.number_input(
                "Manufacturing Electricity (kWh per unit)",
                min_value=0.0,
                value=150.0,
                help="Total electricity used in manufacturing per unit"
            )
            
            grid_emission_factor = st.number_input(
                "Grid Emission Factor (kg CO₂e/kWh)",
                min_value=0.0,
                value=0.45,
                help="Depends on location. Israel: ~0.55, EU avg: ~0.3, US avg: ~0.4"
            )
            
            renewable_percent = st.slider(
                "Renewable Energy %",
                min_value=0,
                max_value=100,
                value=25,
                help="Percentage of electricity from renewable sources"
            )
        
        with col2:
            st.markdown("#### Other Energy Sources")
            
            natural_gas_kwh = st.number_input(
                "Natural Gas (kWh per unit)",
                min_value=0.0,
                value=50.0
            )
            
            diesel_liters = st.number_input(
                "Diesel/Fuel (liters per unit)",
                min_value=0.0,
                value=2.0
            )
            
            process_heat = st.number_input(
                "Process Heat/Steam (MJ per unit)",
                min_value=0.0,
                value=500.0
            )
        
        # Calculate energy impacts
        electricity_impact = electricity_kwh * grid_emission_factor * (1 - renewable_percent/100)
        gas_impact = natural_gas_kwh * 0.2  # ~0.2 kg CO₂e/kWh for natural gas
        diesel_impact = diesel_liters * 2.7  # ~2.7 kg CO₂e/liter
        heat_impact = process_heat * 0.06  # ~0.06 kg CO₂e/MJ
        
        total_energy_impact = electricity_impact + gas_impact + diesel_impact + heat_impact
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Electricity Impact", f"{electricity_impact:.2f} kg CO₂e")
        with col2:
            st.metric("Natural Gas", f"{gas_impact:.2f} kg CO₂e")
        with col3:
            st.metric("Diesel/Fuel", f"{diesel_impact:.2f} kg CO₂e")
        with col4:
            st.metric("Process Heat", f"{heat_impact:.2f} kg CO₂e")
        
        st.metric("**Total Energy Impact**", f"{total_energy_impact:.2f} kg CO₂e", 
                 delta=f"{(total_energy_impact/300)*100:.1f}% of typical product")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous: Materials", use_container_width=True):
                st.session_state.lca_step = 2
                st.rerun()
        
        with col2:
            if st.button("Next: Transport & Distribution →", use_container_width=True):
                st.session_state.lca_data['energy_impact'] = total_energy_impact
                st.session_state.lca_step = 4
                st.rerun()
    
    # Step 4: Transport & Distribution
    elif st.session_state.lca_step == 4:
        st.subheader("Step 4: Transport & Distribution")
        
        st.info("Specify transportation from manufacturing to end customer")
        
        # Inbound logistics (materials to factory)
        st.markdown("#### Inbound Logistics (Materials → Factory)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inbound_distance = st.number_input(
                "Average Distance (km)",
                min_value=0,
                value=500,
                key="inbound_dist"
            )
        
        with col2:
            inbound_mode = st.selectbox(
                "Transport Mode",
                ['Truck', 'Rail', 'Ship', 'Air'],
                key="inbound_mode"
            )
        
        with col3:
            inbound_weight = st.number_input(
                "Total Weight (kg)",
                min_value=0.0,
                value=50.0,
                key="inbound_weight"
            )
        
        # Emission factors (kg CO₂e per ton-km)
        emission_factors = {
            'Truck': 0.062,
            'Rail': 0.022,
            'Ship': 0.008,
            'Air': 0.602
        }
        
        inbound_impact = (inbound_distance * inbound_weight / 1000) * emission_factors[inbound_mode]
        
        st.markdown("---")
        
        # Outbound logistics (factory to customer)
        st.markdown("#### Outbound Logistics (Factory → Customer)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            outbound_distance = st.number_input(
                "Average Distance (km)",
                min_value=0,
                value=2000,
                key="outbound_dist"
            )
        
        with col2:
            outbound_mode = st.selectbox(
                "Transport Mode",
                ['Truck', 'Rail', 'Ship', 'Air'],
                index=3,
                key="outbound_mode"
            )
        
        with col3:
            outbound_weight = st.number_input(
                "Product Weight (kg)",
                min_value=0.0,
                value=25.0,
                key="outbound_weight"
            )
        
        outbound_impact = (outbound_distance * outbound_weight / 1000) * emission_factors[outbound_mode]
        
        total_transport_impact = inbound_impact + outbound_impact
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Inbound Transport", f"{inbound_impact:.2f} kg CO₂e")
        with col2:
            st.metric("Outbound Transport", f"{outbound_impact:.2f} kg CO₂e")
        with col3:
            st.metric("**Total Transport**", f"{total_transport_impact:.2f} kg CO₂e")
        
        st.info(f"""
        **💡 Transport Optimization:**
        - Switching outbound from {outbound_mode} to Ship could save {outbound_impact - (outbound_distance * outbound_weight / 1000) * emission_factors['Ship']:.2f} kg CO₂e
        - Rail transport is 65% lower emissions than truck
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous: Energy", use_container_width=True):
                st.session_state.lca_step = 3
                st.rerun()
        
        with col2:
            if st.button("Calculate Results →", use_container_width=True):
                st.session_state.lca_data['transport_impact'] = total_transport_impact
                st.session_state.lca_step = 5
                st.rerun()
    
    # Step 5: Results
    elif st.session_state.lca_step == 5:
        st.subheader("Step 5: LCA Results")
        
        # Calculate total impacts
        materials_impact = sum(m['total_gwp'] for m in st.session_state.lca_data.get('materials', []))
        energy_impact = st.session_state.lca_data.get('energy_impact', 0)
        transport_impact = st.session_state.lca_data.get('transport_impact', 0)
        
        # Estimate use phase and end-of-life (simplified)
        use_phase_impact = energy_impact * 0.3  # Rough estimate
        eol_impact = materials_impact * 0.05  # Rough estimate
        
        total_impact = materials_impact + energy_impact + transport_impact + use_phase_impact + eol_impact
        
        # Display results
        st.markdown("### Global Warming Potential (GWP)")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Materials (A1-A3)", f"{materials_impact:.2f}", 
                     f"{(materials_impact/total_impact*100):.1f}%")
        
        with col2:
            st.metric("Manufacturing (A3)", f"{energy_impact:.2f}",
                     f"{(energy_impact/total_impact*100):.1f}%")
        
        with col3:
            st.metric("Transport (A4)", f"{transport_impact:.2f}",
                     f"{(transport_impact/total_impact*100):.1f}%")
        
        with col4:
            st.metric("Use Phase (B1)", f"{use_phase_impact:.2f}",
                     f"{(use_phase_impact/total_impact*100):.1f}%")
        
        with col5:
            st.metric("End of Life (C)", f"{eol_impact:.2f}",
                     f"{(eol_impact/total_impact*100):.1f}%")
        
        st.markdown("---")
        
        st.metric("**Total Product Carbon Footprint**", 
                 f"{total_impact:.2f} kg CO₂e per {st.session_state.lca_data.get('functional_unit', 'unit')}")
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Impact by Life Cycle Stage")
            
            stages_df = pd.DataFrame({
                'Stage': ['Materials\n(A1-A3)', 'Manufacturing\n(A3)', 'Transport\n(A4)', 'Use Phase\n(B1)', 'End of Life\n(C)'],
                'Impact (kg CO₂e)': [materials_impact, energy_impact, transport_impact, use_phase_impact, eol_impact]
            })
            
            fig = px.bar(stages_df, x='Stage', y='Impact (kg CO₂e)', 
                        color='Impact (kg CO₂e)',
                        color_continuous_scale='Reds')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Impact Distribution")
            
            fig = go.Figure(data=[go.Pie(
                labels=['Materials', 'Manufacturing', 'Transport', 'Use Phase', 'End of Life'],
                values=[materials_impact, energy_impact, transport_impact, use_phase_impact, eol_impact],
                hole=0.4
            )])
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Industry benchmark
        st.markdown("#### Industry Benchmarking")
        
        benchmarks = {
            'Your Product': total_impact,
            'Industry Average': 320,
            'Best in Class': 180,
            'Regulatory Limit': 400
        }
        
        for label, value in benchmarks.items():
            st.markdown(f"**{label}:** {value:.1f} kg CO₂e")
            progress_val = min(value / 500, 1.0)
            st.progress(progress_val)
        
        if total_impact < benchmarks['Industry Average']:
            st.success(f"✅ Your product performs {((benchmarks['Industry Average'] - total_impact)/benchmarks['Industry Average']*100):.1f}% better than industry average!")
        else:
            st.warning(f"⚠️ Your product is {((total_impact - benchmarks['Industry Average'])/benchmarks['Industry Average']*100):.1f}% above industry average")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate EPD Document", use_container_width=True):
                st.success("EPD document generated! (Would download in production)")
        
        with col2:
            if st.button("Submit for Verification", use_container_width=True):
                st.info("Submitted to verification body (Would integrate with EPD Hub API)")
        
        with col3:
            if st.button("Export Results (Excel)", use_container_width=True):
                st.success("Results exported to Excel!")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous: Transport", use_container_width=True):
                st.session_state.lca_step = 4
                st.rerun()
        
        with col2:
            if st.button("Start New Assessment", use_container_width=True):
                st.session_state.lca_step = 1
                st.session_state.lca_data = {}
                st.rerun()

# ============================================
# TAB 3: EPD GENERATOR
# ============================================
with tab3:
    st.markdown('<div class="main-header">EPD Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create Environmental Product Declarations</div>', unsafe_allow_html=True)
    
    st.info("""
    **Environmental Product Declaration (EPD)** is a standardized document that communicates 
    transparent and comparable information about the life-cycle environmental impact of products.
    """)
    
    # EPD Project Selection
    st.markdown("### Active EPD Projects")
    
    epd_projects = pd.DataFrame({
        'Project': ['Quantum 5800 Firewall', 'CloudGuard Platform', 'Harmony Endpoint v5', 'Infinity Gateway'],
        'Status': ['In Progress', 'Verified', 'Draft', 'Pending Review'],
        'Progress': [75, 100, 30, 60],
        'PCR': ['UN CPC 452 - Hardware', 'UN CPC 8441 - Cloud', 'UN CPC 8441 - Software', 'UN CPC 452 - Hardware'],
        'Verifier': ['EPD Hub', 'IBU', 'EPD International', 'UL'],
        'Due Date': ['2024-03-15', '2024-01-20', '2024-04-30', '2024-02-28']
    })
    
    for idx, row in epd_projects.iterrows():
        with st.expander(f"**{row['Project']}** - {row['Status']} ({row['Progress']}%)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**PCR:** {row['PCR']}")
                st.write(f"**Verifier:** {row['Verifier']}")
            
            with col2:
                st.write(f"**Due Date:** {row['Due Date']}")
                st.progress(row['Progress'] / 100)
            
            with col3:
                if st.button(f"Open Project", key=f"open_{idx}"):
                    st.info("Opening EPD project...")
    
    st.markdown("---")
    
    # Create new EPD
    st.markdown("### Create New EPD")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_product = st.selectbox(
            "Select Product",
            ['Quantum Firewall 5800', 'CloudGuard', 'Harmony Endpoint', 'Infinity Platform', 'Mobile Security']
        )
        
        pcr_selection = st.selectbox(
            "Product Category Rules (PCR)",
            ['UN CPC 452 - Network Hardware', 'UN CPC 8441 - Cloud Services', 
             'UN CPC 8441 - Software Products', 'EN 15804 - Construction Products']
        )
    
    with col2:
        program_operator = st.selectbox(
            "EPD Program Operator",
            ['EPD Hub (Fastest, Digital)', 'EPD International (Most Recognized)', 
             'IBU (European Focus)', 'UL Solutions (North America)']
        )
        
        verification_type = st.selectbox(
            "Verification Type",
            ['Third-party verified', 'Self-declared (Type II)', 'Industry-average']
        )
    
    if st.button("Create EPD Project", use_container_width=True):
        st.success(f"EPD project created for {new_product}! Starting data collection...")
    
    st.markdown("---")
    
    # EPD Template Preview
    st.markdown("### EPD Document Structure Preview")
    
    with st.expander("📄 View Standard EPD Template"):
        st.markdown("""
        **EPD Document Sections (ISO 14025, EN 15804):**
        
        1. **General Information**
           - Product name and description
           - Manufacturer details
           - Declaration number and validity
           
        2. **Product Information**
           - Technical specifications
           - Declared/functional unit
           - Reference service life
           
        3. **LCA Information**
           - PCR used
           - System boundaries
           - Data quality
           - Cut-off rules
           
        4. **LCA Results**
           - Global Warming Potential (GWP)
           - Ozone Depletion Potential (ODP)
           - Acidification Potential (AP)
           - Eutrophication Potential (EP)
           - Photochemical Ozone Creation Potential (POCP)
           - Abiotic Depletion Potential (ADP)
           
        5. **Life Cycle Stages**
           - A1-A3: Product stage
           - A4-A5: Construction
           - B1-B7: Use stage
           - C1-C4: End of life
           - D: Benefits beyond system boundary
           
        6. **Additional Information**
           - Material composition
           - Hazardous substances
           - Environmental management
           
        7. **Verification Statement**
           - Verifier information
           - Independence statement
           - Date and signature
        """)
    
    st.markdown("---")
    
    # Integration with verification
    st.markdown("### Verification Partners (API Integrated)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### EPD Hub")
        st.image("https://via.placeholder.com/150x80/E4002B/FFFFFF?text=EPD+Hub", use_container_width=True)
        st.write("✅ Digital workflow")
        st.write("✅ 2-3 week turnaround")
        st.write("✅ Pre-verification tools")
        
    with col2:
        st.markdown("#### EPD International")
        st.image("https://via.placeholder.com/150x80/4ECDC4/FFFFFF?text=EPD+Intl", use_container_width=True)
        st.write("✅ Most recognized")
        st.write("✅ 100+ PCRs")
        st.write("✅ Global verifier network")
    
    with col3:
        st.markdown("#### IBU Germany")
        st.image("https://via.placeholder.com/150x80/45B7D1/FFFFFF?text=IBU", use_container_width=True)
        st.write("✅ European focus")
        st.write("✅ EN 15804 compliant")
        st.write("✅ ECO Platform member")

# ============================================
# TAB 4: OPERATIONS DECISION TOOL
# ============================================
with tab4:
    st.markdown('<div class="main-header">Operations Decision Support Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Scenario analysis for emissions reduction initiatives</div>', unsafe_allow_html=True)
    
    st.info("""
    **AI-Powered Decision Support:** Evaluate and compare different operational scenarios 
    to optimize both environmental impact and business outcomes.
    """)
    
    # Current baseline
    st.markdown("### Current Baseline")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Annual Emissions", "234,560 tons CO₂e")
    with col2:
        st.metric("Energy Cost", "€28.5M/year")
    with col3:
        st.metric("Carbon Cost (€100/ton)", "€23.5M/year")
    with col4:
        st.metric("Total Cost", "€52M/year")
    
    st.markdown("---")

    # Scenario selection with radio buttons
    st.markdown("### Select Scenario")

    # Define predefined scenarios
    scenarios = {
        'Conservative (Low Risk)': {
            'initiatives': ['Remote Work Policy (40% WFH)', 'Sustainable Procurement', 'EV Fleet Transition'],
            'description': 'Low investment, proven technologies, minimal operational disruption',
            'total_reduction': 18700,
            'total_cost': 4500000,
            'risk_level': 'Low'
        },
        'Balanced (Recommended)': {
            'initiatives': ['Renewable Energy (50% of grid)', 'Data Center Efficiency Upgrade',
                           'Remote Work Policy (40% WFH)', 'EV Fleet Transition'],
            'description': 'AI-recommended optimal balance of cost, impact, and feasibility',
            'total_reduction': 67500,
            'total_cost': 20500000,
            'risk_level': 'Medium'
        },
        'Aggressive (High Impact)': {
            'initiatives': ['Renewable Energy (50% of grid)', 'Data Center Efficiency Upgrade',
                           'Cloud Migration (30% workloads)', 'EV Fleet Transition',
                           'Remote Work Policy (40% WFH)', 'Sustainable Procurement'],
            'description': 'Maximum emissions reduction, requires significant investment and change management',
            'total_reduction': 83700,
            'total_cost': 29000000,
            'risk_level': 'High'
        },
        'Energy Focus': {
            'initiatives': ['Renewable Energy (50% of grid)', 'Data Center Efficiency Upgrade'],
            'description': 'Focused on energy efficiency and renewable sources',
            'total_reduction': 53000,
            'total_cost': 17000000,
            'risk_level': 'Medium'
        },
        'Operational Efficiency': {
            'initiatives': ['Data Center Efficiency Upgrade', 'Cloud Migration (30% workloads)',
                           'Remote Work Policy (40% WFH)'],
            'description': 'Optimize operations and infrastructure without major capital investments',
            'total_reduction': 36500,
            'total_cost': 13500000,
            'risk_level': 'Low'
        },
        'Custom Scenario': {
            'initiatives': [],
            'description': 'Build your own scenario by selecting individual initiatives',
            'total_reduction': 0,
            'total_cost': 0,
            'risk_level': 'Custom'
        }
    }

    # Radio button for scenario selection
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Choose Scenario")
        selected_scenario = st.radio(
            "Select one scenario:",
            list(scenarios.keys()),
            index=1,  # Default to "Balanced (Recommended)"
            key='scenario_radio'
        )

    with col2:
        st.markdown("#### Scenario Details")
        scenario = scenarios[selected_scenario]

        st.markdown(f"**{selected_scenario}**")
        st.write(f"_{scenario['description']}_")

        if selected_scenario != 'Custom Scenario':
            st.markdown("**Included Initiatives:**")
            for initiative in scenario['initiatives']:
                st.markdown(f"- {initiative}")

            # Risk indicator
            risk_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
            st.markdown(f"**Risk Level:** {risk_colors[scenario['risk_level']]} {scenario['risk_level']}")

    st.markdown("---")

    # Initiative details for selected scenario
    initiative_details = {
        'Renewable Energy (50% of grid)': {'reduction': 35000, 'cost': 12000000, 'payback': 6},
        'Data Center Efficiency Upgrade': {'reduction': 18000, 'cost': 5000000, 'payback': 4},
        'Cloud Migration (30% workloads)': {'reduction': 12000, 'cost': 8000000, 'payback': 8},
        'EV Fleet Transition': {'reduction': 8000, 'cost': 3000000, 'payback': 5},
        'Remote Work Policy (40% WFH)': {'reduction': 6500, 'cost': 500000, 'payback': 1},
        'Sustainable Procurement': {'reduction': 4200, 'cost': 1000000, 'payback': 3}
    }

    # Custom Scenario Builder
    if selected_scenario == 'Custom Scenario':
        st.markdown("### 🛠️ Build Your Custom Scenario")
        st.markdown("Select the initiatives you want to include in your scenario:")

        col1, col2, col3 = st.columns(3)

        custom_selections = {}

        with col1:
            st.markdown("#### 💡 Energy Initiatives")
            custom_selections['Renewable Energy (50% of grid)'] = st.checkbox(
                '🌱 Renewable Energy (50% of grid)',
                value=False,
                key='custom_renewable',
                help='€12M investment, 35,000 tons reduction, 6 year payback'
            )
            custom_selections['Data Center Efficiency Upgrade'] = st.checkbox(
                '🖥️ Data Center Efficiency Upgrade',
                value=False,
                key='custom_datacenter',
                help='€5M investment, 18,000 tons reduction, 4 year payback'
            )

        with col2:
            st.markdown("#### 🚀 Operational Initiatives")
            custom_selections['Cloud Migration (30% workloads)'] = st.checkbox(
                '☁️ Cloud Migration (30% workloads)',
                value=False,
                key='custom_cloud',
                help='€8M investment, 12,000 tons reduction, 8 year payback'
            )
            custom_selections['Remote Work Policy (40% WFH)'] = st.checkbox(
                '🏠 Remote Work Policy (40% WFH)',
                value=False,
                key='custom_remote',
                help='€0.5M investment, 6,500 tons reduction, 1 year payback'
            )

        with col3:
            st.markdown("#### 🚗 Transportation & Supply")
            custom_selections['EV Fleet Transition'] = st.checkbox(
                '⚡ EV Fleet Transition',
                value=False,
                key='custom_ev',
                help='€3M investment, 8,000 tons reduction, 5 year payback'
            )
            custom_selections['Sustainable Procurement'] = st.checkbox(
                '📦 Sustainable Procurement',
                value=False,
                key='custom_procurement',
                help='€1M investment, 4,200 tons reduction, 3 year payback'
            )

        # Build selected initiatives dict from custom selections
        selected_initiatives = {
            name: {**initiative_details[name], 'selected': True}
            for name, selected in custom_selections.items()
            if selected
        }

        if not selected_initiatives:
            st.info("👆 Select at least one initiative above to build your custom scenario")
    else:
        # Build selected initiatives dict for predefined scenarios
        selected_initiatives = {
            name: {**details, 'selected': True}
            for name, details in initiative_details.items()
            if name in scenario['initiatives']
        }
    
    if selected_initiatives:
        st.markdown("### Scenario Results")
        
        total_reduction = sum(init['reduction'] for init in selected_initiatives.values())
        total_cost = sum(init['cost'] for init in selected_initiatives.values())
        
        new_emissions = 234560 - total_reduction
        reduction_percent = (total_reduction / 234560) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "New Annual Emissions",
                f"{new_emissions:,} tons",
                f"-{reduction_percent:.1f}%",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Total Investment",
                f"€{total_cost/1000000:.1f}M"
            )
        
        with col3:
            annual_savings = (total_reduction * 100) / 1000000  # Assuming €100/ton carbon price
            st.metric(
                "Annual Savings",
                f"€{annual_savings:.1f}M"
            )
        
        with col4:
            simple_payback = total_cost / (annual_savings * 1000000) if annual_savings > 0 else 0
            st.metric(
                "Simple Payback",
                f"{simple_payback:.1f} years"
            )
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Emissions Reduction by Initiative")
            
            init_df = pd.DataFrame([
                {'Initiative': k, 'Reduction (tons CO₂e)': v['reduction']}
                for k, v in selected_initiatives.items()
            ])
            
            fig = px.bar(init_df, x='Initiative', y='Reduction (tons CO₂e)', 
                        color='Reduction (tons CO₂e)',
                        color_continuous_scale='Greens')
            fig.update_layout(height=350, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Cost vs. Reduction")
            
            scatter_df = pd.DataFrame([
                {
                    'Initiative': k,
                    'Investment (€M)': v['cost'] / 1000000,
                    'Reduction (tons)': v['reduction'],
                    'Payback (years)': v['payback']
                }
                for k, v in selected_initiatives.items()
            ])
            
            fig = px.scatter(scatter_df, 
                           x='Investment (€M)', 
                           y='Reduction (tons)',
                           size='Reduction (tons)',
                           color='Payback (years)',
                           hover_data=['Initiative'],
                           color_continuous_scale='RdYlGn_r')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Timeline projection
        st.markdown("### 5-Year Impact Projection")
        
        years = list(range(2024, 2029))
        baseline_emissions = [234560 * (0.98 ** i) for i in range(5)]  # 2% natural reduction
        scenario_emissions = [(234560 - total_reduction) * (0.98 ** i) for i in range(5)]
        
        projection_df = pd.DataFrame({
            'Year': years,
            'Baseline Scenario': baseline_emissions,
            'With Selected Initiatives': scenario_emissions
        })
        
        fig = px.line(projection_df, x='Year', y=['Baseline Scenario', 'With Selected Initiatives'],
                     title='', markers=True)
        fig.update_layout(height=350, yaxis_title='Annual Emissions (tons CO₂e)')
        st.plotly_chart(fig, use_container_width=True)
        
        cumulative_reduction = sum(baseline_emissions[i] - scenario_emissions[i] for i in range(5))
        st.success(f"**Cumulative 5-year reduction:** {cumulative_reduction:,.0f} tons CO₂e")
        
        st.markdown("---")
        
        # Export scenario
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Scenario Report", use_container_width=True):
                st.success("Scenario report exported!")
        
        with col2:
            if st.button("Send to Management", use_container_width=True):
                st.info("Scenario sent to management team")
        
        with col3:
            if st.button("Save Scenario", use_container_width=True, key="save_scenario_operations"):
                st.success("Scenario saved!")

    else:
        st.warning("Select at least one initiative to see scenario results")

# ============================================
# TAB 5: FINANCIAL ANALYSIS
# ============================================
with tab5:
    st.markdown('<div class="main-header">Financial Analysis & ROI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive financial modeling for sustainability initiatives</div>', unsafe_allow_html=True)
    
    st.info("""
    **Financial Decision Support:** Calculate NPV, IRR, payback period, and sensitivity analysis 
    for environmental investments.
    """)
    
    # Initiative selection
    st.markdown("### Select Initiatives for Financial Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        initiatives = {
            'Renewable Energy (50% of grid)': {
                'reduction': 35000,
                'cost': 12000000,
                'payback': 6,
                'selected': st.checkbox('Renewable Energy (50% of grid)', value=True, key='fin_renewable')
            },
            'Data Center Efficiency Upgrade': {
                'reduction': 18000,
                'cost': 5000000,
                'payback': 4,
                'selected': st.checkbox('Data Center Efficiency Upgrade', value=True, key='fin_datacenter')
            },
            'Cloud Migration (30% workloads)': {
                'reduction': 12000,
                'cost': 8000000,
                'payback': 8,
                'selected': st.checkbox('Cloud Migration (30% workloads)', value=False, key='fin_cloud')
            },
            'EV Fleet Transition': {
                'reduction': 8000,
                'cost': 3000000,
                'payback': 5,
                'selected': st.checkbox('EV Fleet Transition', value=True, key='fin_ev')
            }
        }
    
    with col2:
        st.markdown("#### Financial Parameters")
        
        carbon_price = st.number_input(
            "Carbon Price (€/ton CO₂e)",
            min_value=0,
            max_value=500,
            value=100,
            step=10,
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
            if st.button("Save Scenario", use_container_width=True, key="save_scenario_financial"):
                st.success("Financial scenario saved!")
    
    else:
        st.warning("Please select at least one initiative to analyze")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>🛡️ Check Point Software Technologies Environmental Compliance Platform</strong></p>
        <p style='font-size: 0.9em;'>© 2025 Climaterix Technologies Ltd. | Demo Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)
