import matplotlib.pyplot as plt
import os
import pandas as pd

# Set style
plt.style.use('dark_background')
asset_dir = '/home/mihir/portfolio_reports/assets'
os.makedirs(asset_dir, exist_ok=True)

def save_plot(name):
    plt.tight_layout()
    plt.savefig(os.path.join(asset_dir, name), dpi=150)
    plt.close()

# 1. HUBB vs ETN vs EMR: AI Power Infrastructure Growth Projections
def hubb_comp():
    labels = ['HUBB', 'Eaton (ETN)', 'Emerson (EMR)']
    growth = [60, 17, 15] # DC related growth %
    margins = [23, 21, 19] # Operating margins
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    
    ax1.bar(labels, growth, color='#38bdf8', alpha=0.7, label='Data Center Growth %')
    ax2.plot(labels, margins, color='#fbbf24', marker='o', linewidth=3, label='Op Margin %')
    
    ax1.set_title('AI Power Infra: HUBB Outperforms on Vertical Growth', fontsize=16, color='#38bdf8')
    ax1.set_ylabel('DC Growth %', color='#38bdf8')
    ax2.set_ylabel('Operating Margin %', color='#fbbf24')
    save_plot('hubb_comparison.png')

# 2. HOOD: The "Stickiness" Chart (Gold Subscription Growth)
def hood_growth():
    years = ['2023', '2024', '2025', '2026E']
    subs = [1.4, 2.6, 4.2, 5.5] # Millions
    deposits = [20, 45, 68, 85] # $B Net Deposits
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    
    ax1.fill_between(years, subs, color='#22c55e', alpha=0.3, label='Gold Subscribers (M)')
    ax1.plot(years, subs, color='#22c55e', marker='s', linewidth=3)
    
    ax2.bar(years, deposits, color='#38bdf8', alpha=0.4, width=0.4, label='Net Deposits ($B)')
    
    ax1.set_title('HOOD: Hyper-Growth in High-LTV Assets', fontsize=16, color='#22c55e')
    ax1.set_ylabel('Subscribers (Millions)', color='#22c55e')
    ax2.set_ylabel('Net Deposits ($Billions)', color='#38bdf8')
    save_plot('hood_stickiness.png')

# 3. UBER: High-Margin Ad Revenue Trajectory
def uber_ads():
    quarters = ['Q1-25', 'Q2-25', 'Q3-25', 'Q4-25', '2026E']
    ad_rev = [0.9, 1.1, 1.3, 1.5, 2.5] # $B run rate
    
    plt.figure(figsize=(10, 6))
    plt.plot(quarters, ad_rev, color='#818cf8', marker='o', linewidth=4, markersize=12)
    plt.fill_between(quarters, ad_rev, color='#818cf8', alpha=0.2)
    plt.title('UBER: The High-Margin Ad Pivot ($B Run Rate)', fontsize=16, color='#818cf8')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    save_plot('uber_ads_growth.png')

# 4. VST: Nuclear Baseload vs. Oil Shock (Correlation)
def vst_energy():
    oil_prices = [70, 85, 100, 110]
    vst_val = [40, 65, 95, 120] # Representative value mapping
    
    plt.figure(figsize=(10, 6))
    plt.scatter(oil_prices, vst_val, s=200, color='#fbbf24', alpha=0.8)
    plt.plot(oil_prices, vst_val, '--', color='#fbbf24', alpha=0.5)
    plt.xlabel('Crude Oil Price ($)', fontsize=12)
    plt.ylabel('VST Relative Value Index', fontsize=12)
    plt.title('VST: Positive Correlation to Energy Scarcity', fontsize=16, color='#fbbf24')
    save_plot('vst_correlation.png')

# 5. ASML: 2nm EUV Backlog Dominance
def asml_moat():
    tech = ['DUV (Old)', 'EUV (Std)', 'High-NA (New)']
    backlog = [13, 20, 6] # $B estimates
    
    plt.figure(figsize=(10, 6))
    plt.barh(tech, backlog, color=['#94a3b8', '#a78bfa', '#c084fc'])
    plt.title('ASML: €38B Backlog Focused on 2nm Mastery', fontsize=16, color='#a78bfa')
    plt.xlabel('Order Backlog (€ Billions)', fontsize=12)
    save_plot('asml_backlog.png')

if __name__ == "__main__":
    hubb_comp()
    hood_growth()
    uber_ads()
    vst_energy()
    asml_moat()
    print("Individual visuals generated successfully.")
