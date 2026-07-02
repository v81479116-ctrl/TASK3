# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration for a wide, responsive layout
st.set_page_config(
    page_title="E-Commerce & Customer Intelligence Portal",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for premium aesthetics (Clean typography, soft shadows, responsive sizing)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Main Banner Styles */
    .banner {
        background: linear-gradient(135deg, #0F4C5C 0%, #1D3557 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(15, 76, 92, 0.15);
    }
    
    .banner h1 {
        color: white !important;
        font-size: 40px !important;
        font-weight: 800 !important;
        margin: 0 0 10px 0 !important;
    }
    
    .banner p {
        font-size: 16px;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Metric Card Styling with Responsive font sizes to prevent numeric clipping */
    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(15, 76, 92, 0.05);
        border: 1px solid #E2E8F0;
        transition: all 0.25s ease-in-out;
        text-align: left;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(15, 76, 92, 0.09);
        border-color: #CBD5E1;
    }
    
    .metric-header {
        font-size: 11px;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }
    
    .metric-val {
        font-size: 25px; /* Scaled down from 32px to fit large values on small screens */
        font-weight: 800;
        margin-bottom: 6px;
        line-height: 1.1;
        white-space: nowrap;
    }
    
    .metric-sub {
        font-size: 12px;
        color: #E36414;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    /* Subsection Titles */
    .section-title {
        color: #1D3557;
        font-size: 22px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
        border-left: 5px solid #2A9D8F;
        padding-left: 12px;
    }
    
    /* Explanation Box */
    .explanation-box {
        background-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 35px;
        color: #334155;
        font-size: 14.5px;
        line-height: 1.6;
    }
    
    /* Sidebar adjustments */
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        color: #475569;
        background-color: transparent;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #0F4C5C;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0F4C5C !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to generate custom chart styling
def style_chart(ax, title, xlabel="", ylabel="", show_grid=True):
    ax.set_title(title, fontsize=12, fontweight="bold", pad=15, color="#1D3557")
    ax.set_xlabel(xlabel, fontsize=10, color="#64748B", fontweight="semibold")
    ax.set_ylabel(ylabel, fontsize=10, color="#64748B", fontweight="semibold")
    ax.tick_params(colors="#64748B", labelsize=9)
    sns.despine(ax=ax, left=True, bottom=True)
    if show_grid:
        ax.grid(axis='y', linestyle='--', alpha=0.4, color="#E2E8F0")

# KPI Card renderer
def render_kpi(label, value, subtext, color="#0F4C5C"):
    st.markdown(f"""
    <div class="metric-card" style="border-top: 4px solid {color};">
        <div class="metric-header">{label}</div>
        <div class="metric-val" style="color: {color};">{value}</div>
        <div class="metric-sub">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    transactions_path = r"C:\Users\rkvig\Downloads\Joshi\task1_wrangling\cleaned_retail.csv"
    segments_path = r"C:\Users\rkvig\Downloads\Joshi\task3_dashboard\rfm_segments.csv"
    
    tx = pd.read_csv(transactions_path)
    tx['InvoiceDate'] = pd.to_datetime(tx['InvoiceDate'])
    tx['CustomerID'] = tx['CustomerID'].astype(str)
    
    seg = pd.read_csv(segments_path)
    seg['CustomerID'] = seg['CustomerID'].astype(str)
    return tx, seg

try:
    tx_df, seg_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

if data_loaded:
    # Sidebar design
    st.sidebar.markdown("<h2 style='color:#0F4C5C; margin-bottom:10px;'>🛍️ Control Panel</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("Use filters below to query the transaction data and update metrics dynamically.")
    st.sidebar.markdown("---")
    
    # 1. Currency selector with accurate exchange conversion rates
    CURRENCIES = {
        "GBP (£)": {"symbol": "£", "rate": 1.0},
        "USD ($)": {"symbol": "$", "rate": 1.27},
        "EUR (€)": {"symbol": "€", "rate": 1.18},
        "INR (₹)": {"symbol": "₹", "rate": 106.0},
        "JPY (¥)": {"symbol": "¥", "rate": 200.0}
    }
    selected_curr = st.sidebar.selectbox("💱 Select Display Currency", list(CURRENCIES.keys()), index=0)
    curr_symbol = CURRENCIES[selected_curr]["symbol"]
    curr_rate = CURRENCIES[selected_curr]["rate"]
    curr_code = selected_curr.split()[0]
    
    st.sidebar.markdown("---")
    
    # 2. Country filter (defaults to UK)
    countries = sorted(tx_df['Country'].unique())
    selected_countries = st.sidebar.multiselect("🌍 Filter by Countries", countries, default=["United Kingdom"])
    
    # 3. Customer segment filter
    segments = sorted(seg_df['Segment'].unique())
    selected_segments = st.sidebar.multiselect("👥 Filter by Customer Segments", segments, default=segments)
    
    # 4. Date Range slider - Robust unpacking fix
    min_date = tx_df['InvoiceDate'].min().date()
    max_date = tx_df['InvoiceDate'].max().date()
    
    date_range = st.sidebar.date_input("📅 Date Range Filter", [min_date, max_date], min_value=min_date, max_value=max_date)
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = min_date
        end_date = max_date
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📅 **Active Range**:\n{start_date} to {end_date}\n\n🌍 **Countries Selected**:\n{len(selected_countries)} countries\n\n👥 **Segments Selected**:\n{len(selected_segments)} segments\n\n💱 **Exchange Rate**: 1 GBP = {curr_rate} {curr_code}")
    
    # Filtering Logic
    filtered_tx = tx_df[
        (tx_df['Country'].isin(selected_countries)) &
        (tx_df['InvoiceDate'].dt.date >= start_date) &
        (tx_df['InvoiceDate'].dt.date <= end_date)
    ].copy()
    
    # Apply currency conversion calculations
    filtered_tx['LineTotal'] = filtered_tx['LineTotal'] * curr_rate
    filtered_tx['UnitPrice'] = filtered_tx['UnitPrice'] * curr_rate
    
    tx_with_segment = pd.merge(filtered_tx, seg_df[['CustomerID', 'Segment']], on='CustomerID', how='inner')
    tx_with_segment = tx_with_segment[tx_with_segment['Segment'].isin(selected_segments)]
    
    filtered_seg = seg_df[
        (seg_df['Segment'].isin(selected_segments))
    ].copy()
    
    # Apply currency conversion to segment monetary metrics
    filtered_seg['Monetary'] = filtered_seg['Monetary'] * curr_rate
    filtered_seg = filtered_seg[filtered_seg['CustomerID'].isin(tx_with_segment['CustomerID'].unique())]
    
    # Banner Header
    st.markdown("""
    <div class="banner">
        <h1>Retail & Customer Intelligence Portal</h1>
        <p>Analyze sales metrics, track seasonal trends, and visualize buyer cohorts based on the Online Retail transaction database.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Business Overview", "👥 RFM Customer Cohorts", "🔍 Customer Deep-Dive"])
    
    # Tab 1: Business Overview
    with tab1:
        # Calculate key business metrics
        completed_tx = tx_with_segment[tx_with_segment['IsCancelled'] == 0]
        total_rev = completed_tx['LineTotal'].sum()
        total_orders = completed_tx['InvoiceNo'].nunique()
        aov = total_rev / total_orders if total_orders > 0 else 0
        total_cust = tx_with_segment['CustomerID'].nunique()
        
        # Grid of KPI Cards with dynamic currency symbols
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi("Total Net Revenue", f"{curr_symbol}{total_rev:,.2f}", f"💼 Net Sales value in {curr_code}", "#0F4C5C")
        with k2:
            render_kpi("Completed Orders", f"{total_orders:,}", "📦 Total volume shipped", "#E36414")
        with k3:
            render_kpi("Average Order Value (AOV)", f"{curr_symbol}{aov:,.2f}", f"💳 Average order in {curr_code}", "#2A9D8F")
        with k4:
            render_kpi("Active Buyers", f"{total_cust:,}", "👥 Registered & guest buyers", "#264653")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. Monthly Sales
        st.markdown("<div class='section-title'>1. Monthly Sales Trajectory</div>", unsafe_allow_html=True)
        monthly_sales = completed_tx.copy()
        monthly_sales['Month'] = monthly_sales['InvoiceDate'].dt.to_period('M').astype(str)
        monthly_trend = monthly_sales.groupby('Month')['LineTotal'].sum().reset_index()
        
        fig1, ax1 = plt.subplots(figsize=(10, 4.5))
        ax1.fill_between(monthly_trend['Month'], monthly_trend['LineTotal'], color="#2A9D8F", alpha=0.15)
        sns.lineplot(data=monthly_trend, x="Month", y="LineTotal", marker="o", color="#2A9D8F", linewidth=2.5, ax=ax1)
        style_chart(ax1, f"Gross Revenue Trend ({curr_code})", "Month", f"Revenue ({curr_symbol})")
        plt.xticks(rotation=25, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()
        
        st.markdown(f"""
        <div class="explanation-box">
            <strong>📈 Insights & Takeaways:</strong><br>
            • This trend chart highlights a strong <strong>seasonal uptick</strong> in sales starting in September, peaking in November at <strong>{curr_symbol}{1456145.8 * curr_rate:,.2f}</strong>.<br>
            • This pattern is standard in retail operations, representing B2B distributors stocking up inventory prior to the winter holiday shopping season.<br>
            • The sharp decrease in December is due to the transaction record cutting off on December 9th.
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Top Products
        st.markdown("<div class='section-title'>2. Top 10 Best Selling Products</div>", unsafe_allow_html=True)
        top_products = completed_tx.groupby('Description')['LineTotal'].sum().reset_index()
        top_products = top_products.sort_values(by='LineTotal', ascending=False).head(10)
        
        fig2, ax2 = plt.subplots(figsize=(10, 4.5))
        sns.barplot(data=top_products, x="LineTotal", y="Description", hue="Description", palette="viridis", ax=ax2, legend=False)
        style_chart(ax2, f"Revenue by Product Description ({curr_code})", f"Revenue ({curr_symbol})", "")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()
        
        st.markdown(f"""
        <div class="explanation-box">
            <strong>📦 Insights & Takeaways:</strong><br>
            • The leading product by revenue contribution is <strong>"PAPER CRAFT, LITTLE BIRDIE"</strong> generating over {curr_symbol}{168469.6 * curr_rate:,.2f}.<br>
            • Bulk catalog items and adjustments like <strong>"DOTCOM POSTAGE"</strong> and the <strong>"REGENCY CAKESTAND 3 TIER"</strong> represent high-margin revenue earners.<br>
            • Knowing your top-sellers allows warehouse operations to optimize stock placement (e.g. placing fast-moving items closer to packaging stations).
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Hour of Density
        st.markdown("<div class='section-title'>3. Hour of Day Order Density</div>", unsafe_allow_html=True)
        hourly = completed_tx.groupby('InvoiceHour')['InvoiceNo'].nunique().reset_index()
        
        fig3, ax3 = plt.subplots(figsize=(10, 4.5))
        sns.barplot(data=hourly, x="InvoiceHour", y="InvoiceNo", hue="InvoiceHour", palette="Blues_d", ax=ax3, legend=False)
        style_chart(ax3, "Unique Invoices Placed by Hour of Day", "Hour (24h format)", "Order Count")
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()
        
        st.markdown("""
        <div class="explanation-box">
            <strong>⏰ Insights & Takeaways:</strong><br>
            • Transactions are highly concentrated during office hours, specifically between <strong>10:00 AM and 3:00 PM</strong>, with the absolute peak volume occurring at <strong>12:00 PM</strong>.<br>
            • Almost no purchases occur before 7:00 AM or after 8:00 PM.<br>
            • <em>Operational Value:</em> Warehouse managers can use this layout to schedule staff shifts, aligning peak picking hours with peak incoming transaction loads.
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Countries Share
        st.markdown("<div class='section-title'>4. Revenue by Country</div>", unsafe_allow_html=True)
        country_revenue = completed_tx.groupby('Country')['LineTotal'].sum().reset_index()
        country_revenue = country_revenue.sort_values(by='LineTotal', ascending=False).head(10)
        
        fig4, ax4 = plt.subplots(figsize=(10, 4.5))
        sns.barplot(data=country_revenue, x="LineTotal", y="Country", hue="Country", palette="viridis", ax=ax4, legend=False)
        style_chart(ax4, f"Total Revenue by Country ({curr_code})", f"Revenue ({curr_symbol})", "")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()
        
        st.markdown("""
        <div class="explanation-box">
            <strong>🌍 Insights & Takeaways:</strong><br>
            • This chart shows total revenue across the selected countries, allowing for easy comparison when one or more countries are active.<br>
            • While the **United Kingdom** represents our largest overall market, international hubs like the **Netherlands** and **EIRE** show substantial spending.<br>
            • International buyers often purchase in large quantities per order, leading to a high Average Order Value (AOV).
        </div>
        """, unsafe_allow_html=True)
            
    # Tab 2: RFM Customer Cohorts
    with tab2:
        st.markdown("<div class='section-title'>Customer Segment Distribution</div>", unsafe_allow_html=True)
        
        # Calculate counts
        seg_counts = filtered_seg['Segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment', 'Customer Count']
        seg_counts['Percentage'] = (seg_counts['Customer Count'] / len(filtered_seg)) * 100
        
        # Table and Bar Chart
        st.markdown("#### **Segment Profile Table**")
        st.dataframe(
            seg_counts.style.format({'Percentage': '{:.2f}%', 'Customer Count': '{:,}'}),
            use_container_width=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        fig5, ax5 = plt.subplots(figsize=(10, 4.5))
        sns.barplot(data=seg_counts, x="Customer Count", y="Segment", hue="Segment", palette="viridis", ax=ax5, legend=False)
        style_chart(ax5, "Segment Share of Registered Customer Base", "Customer Count", "")
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()
        
        st.markdown("""
        <div class="explanation-box">
            <strong>👥 Insights & Takeaways:</strong><br>
            • <strong>Loyal Customers (26.96%)</strong> and <strong>Champions (18.61%)</strong> represent the core healthy base of our customer relationships.<br>
            • However, <strong>Lost Customers (22.70%)</strong> and <strong>About to Sleep (19.83%)</strong> account for a massive chunk of accounts that require re-engagement.<br>
            • Marketing budgets should prioritize low-cost email reactivation campaigns for the "About to Sleep" cohort rather than spending on the "Lost" cohort.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>Segment Metrics Comparison (Averages)</div>", unsafe_allow_html=True)
        segment_averages = filtered_seg.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()
        
        st.dataframe(
            segment_averages.style.format({
                'Recency': '{:.1f} days',
                'Frequency': '{:.1f} orders',
                'Monetary': f'{curr_symbol}{{:,.2f}}'
            }),
            use_container_width=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Scatterplot positioning (full width)
        st.markdown("<div class='section-title'>RFM Customer Mapping (Recency vs Frequency)</div>", unsafe_allow_html=True)
        fig6, ax6 = plt.subplots(figsize=(10, 5))
        sns.scatterplot(
            data=filtered_seg, 
            x="Recency", 
            y="Frequency", 
            hue="Segment", 
            size="Monetary", 
            sizes=(30, 600), 
            palette="viridis", 
            alpha=0.75, 
            ax=ax6
        )
        style_chart(ax6, "Positioning Matrix (Log Scale for Frequency)", "Days Since Last Purchase (Recency)", "Unique Invoices (Frequency)")
        ax6.set_yscale('log')
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.tight_layout()
        st.pyplot(fig6)
        plt.close()

        st.markdown("""
        <div class="explanation-box">
            <strong>📊 Insights & Takeaways:</strong><br>
            • This scatter plot places each customer along two axes: <strong>Recency</strong> (x-axis) and <strong>Frequency</strong> (y-axis, logarithmic scale).<br>
            • The size of each bubble corresponds to the customer's gross <strong>Monetary Spend</strong>.<br>
            • <strong>Champions</strong> cluster in the upper-left corner (highly recent, high frequency, large bubbles).<br>
            • <strong>Lost Customers</strong> lie in the lower-right corner (inactive for a long time, only 1 order, small bubbles).
        </div>
        """, unsafe_allow_html=True)

    # Tab 3: Customer Deep-Dive
    with tab3:
        st.markdown("<div class='section-title'>Interactive Customer Transaction Lookup</div>", unsafe_allow_html=True)
        cust_