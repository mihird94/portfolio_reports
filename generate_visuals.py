import matplotlib.pyplot as plt
import os

# Set style
plt.style.use('dark_background')
colors = ['#38bdf8', '#fbbf24', '#ef4444', '#22c55e', '#818cf8']
asset_dir = '/home/mihir/portfolio_reports/assets'

# 1. Barbell Architecture Chart
def create_barbell():
    labels = ['Core (VOO)', 'Gold (GLD)', 'Alpha (Atoms)', 'Digital Alpha', 'Energy (XLE)']
    weights = [44, 21, 18, 13, 8]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, weights, color=colors)
    ax.set_title('Portfolio Strategic Barbell Posture', fontsize=16, color='#38bdf8', pad=20)
    ax.set_ylabel('Allocation (%)', fontsize=12)
    
    # Add values on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(asset_dir, 'barbell_posture.png'))
    plt.close()

# 2. Recovery Timeline (Historical Script)
def create_timeline():
    stages = ['Panic Gap', 'Price Discovery', 'Settlement', 'True Bottom', 'Recovery']
    days = [1, 3, 5, 10, 23] # Accumulative days for visual spacing
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.step(days, stages, where='post', color='#38bdf8', linewidth=3)
    ax.plot(days, stages, 'o', color='#fbbf24', markersize=10)
    
    ax.set_title('The Geopolitical "3-Week Script" Recovery', fontsize=16, color='#38bdf8', pad=20)
    ax.set_xlabel('Trading Days Post-Shock', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(asset_dir, 'recovery_timeline.png'))
    plt.close()

# 3. Regime Rotation Meter
def create_rotation():
    labels = ['Atoms (Physical/Infra)', 'Bits (Software/SaaS)']
    sizes = [75, 25]
    explode = (0.1, 0)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
           shadow=True, startangle=140, colors=['#38bdf8', '#94a3b8'],
           textprops={'fontsize': 14, 'fontweight': 'bold'})
    ax.set_title('Regime Rotation: Atoms vs. Bits', fontsize=18, color='#38bdf8', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(asset_dir, 'regime_rotation.png'))
    plt.close()

if __name__ == "__main__":
    create_barbell()
    create_timeline()
    create_rotation()
    print("Visuals generated successfully in assets/")
