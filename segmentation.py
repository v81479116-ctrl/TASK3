import pandas as pd
import numpy as np
import os

def perform_rfm_segmentation():
    cleaned_path = r"d:\Joshi\task1_wrangling\cleaned_retail.csv"
    output_dir = r"d:\Joshi\task3_dashboard"
    output_csv = os.path.join(output_dir, "rfm_segments.csv")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading cleaned dataset...")
    df = pd.read_csv(cleaned_path)
    
    # Standardize types and parse dates
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Segment ONLY registered customers (exclude Guest checkouts)
    print("Filtering registered customers...")
    df_registered = df[~df['CustomerID'].astype(str).str.startswith('Guest_')].copy()
    print(f"Total transactions for registered customers: {len(df_registered):,}")
    
    # Establish reference date (max date + 1 day)
    ref_date = df_registered['InvoiceDate'].max() + pd.Timedelta(days=1)
    print(f"Reference Date for Recency: {ref_date}")
    
    # Group by CustomerID to calculate RFM metrics
    print("Calculating RFM metrics per customer...")
    rfm = df_registered.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (ref_date - x.max()).days, # Recency
        'InvoiceNo': 'nunique',                             # Frequency
        'LineTotal': 'sum'                                  # Monetary
    }).rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'LineTotal': 'Monetary'
    })
    
    # Filter out customers with zero or negative monetary value (can happen due to returns exceeding purchases)
    rfm = rfm[rfm['Monetary'] > 0]
    
    print(f"Calculated RFM metrics for {len(rfm):,} unique customers.")
    
    # Binning RFM scores
    # Recency: higher score for lower recency days (more recent is better)
    # Frequency & Monetary: higher score for higher values (more frequency/monetary is better)
    print("Assigning RFM scores...")
    
    # Note: Frequency can have identical bins because many customers purchase only once/twice.
    # To avoid bin duplicate edges, we use ranking/percentiles or custom cuts.
    # Recency and Monetary cuts:
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    # Frequency cut using custom logic due to non-unique quantiles
    freq_bins = [0, 1, 2, 5, 10, np.inf]
    rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=freq_bins, labels=[1, 2, 3, 4, 5]).astype(int)
    
    rfm['R_Score'] = rfm['R_Score'].astype(int)
    rfm['M_Score'] = rfm['M_Score'].astype(int)
    
    # Combine scores into a single string
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    
    # Segment definition function based on RFM rules
    def get_segment(row):
        r = row['R_Score']
        f = row['F_Score']
        m = row['M_Score']
        
        # High value recent buyers
        if r >= 4 and f >= 4:
            return "Champions"
        # Frequent buyers, but not necessarily top tier or extremely recent
        elif (r >= 3 and f >= 3) or (r >= 4 and f >= 2):
            return "Loyal Customers"
        # New buyers
        elif r >= 4 and f == 1:
            return "Recent/New Customers"
        # Potential loyalists, average recency and frequency
        elif r >= 3 and f >= 1 and m >= 3:
            return "Promising Customers"
        # Idle/slipping customer
        elif r == 2 and f >= 1:
            return "About to Sleep"
        # High value, but did not purchase in a long time
        elif r == 1 and (f >= 3 or m >= 4):
            return "At Risk"
        # Lost customer
        else:
            return "Lost"
            
    rfm['Segment'] = rfm.apply(get_segment, axis=1)
    
    print("\nSegment distribution counts:")
    counts = rfm['Segment'].value_counts()
    for seg, cnt in counts.items():
        pct = (cnt / len(rfm)) * 100
        print(f"  {seg}: {cnt:,} ({pct:.2f}%)")
        
    print(f"Saving RFM segmentation results to {output_csv}...")
    rfm.to_csv(output_csv, encoding='utf-8')
    print("Segmentation complete!")

if __name__ == "__main__":
    perform_rfm_segmentation()