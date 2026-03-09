import os
import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Add the project src to path
sys.path.append('/home/mihir/context_files/trading/src')

from trading_suite.risk.risk_engine import RiskEngine
from trading_suite.config import settings

def run_custom_mc():
    print("--- Initializing Large-Scale Monte Carlo Simulation ---")
    
    # 1. Define Portfolios
    # CURRENT (From portfolio.toml)
    curr_port = {
        'VOO': 44.82, 'GLD': 20.96, 'GOOGL': 7.70, 'ASML': 6.53, 
        'SOXX': 4.55, 'VGT': 4.54, 'XLI': 3.77, 'AMAT': 1.71, 'UBER': 5.42 # Balanced UBER
    }
    
    # TARGET (The "Atoms" Barbell suggest in our discussion)
    target_port = {
        'VOO': 40.0, 'GLD': 21.0, 'XLE': 8.0, 'VST': 4.0, 
        'HUBB': 4.0, 'AMAT': 4.0, 'ASML': 6.5, 'UBER': 4.0, 
        'GOOGL': 5.5, 'HOOD': 3.0
    }

    # Normalize weights
    def norm(p):
        s = sum(p.values())
        return {k: v/s for k, v in p.items()}

    curr_tickers, curr_weights = list(curr_port.keys()), list(norm(curr_port).values())
    target_tickers, target_weights = list(target_port.keys()), list(norm(target_port).values())

    engine = RiskEngine()
    
    # Parameters requested: Larger lookback and num simulations
    NUM_SIMS = 50000
    LOOKBACK_YEARS = 10 
    PROJECTION_YEARS = 5

    # Override the fetch_data lookback inside run_monte_carlo logic (by proxy)
    # The current run_monte_carlo has a hardcoded 4-year lookback. 
    # I will modify the call or simulate the internal logic here for the requested 10-year lookback.
    
    from trading_suite.data.data_provider import fetch_data
    
    all_tickers = list(set(curr_tickers + target_tickers))
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365*LOOKBACK_YEARS)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    print(f"Fetching {LOOKBACK_YEARS} years of data for {len(all_tickers)} tickers...")
    prices = fetch_data(all_tickers, start_date, end_date)
    returns = prices.pct_change().dropna()
    
    def simulate(tickers, weights, initial_val=100000.0):
        # Extract subset returns
        sub_returns = returns[tickers]
        mean_r = sub_returns.mean()
        cov = sub_returns.cov()
        num_assets = len(tickers)
        current_prices = prices[tickers].iloc[-1].values
        days = PROJECTION_YEARS * 252
        
        # Cholesky / SVD for correlation
        try:
            L = np.linalg.cholesky(cov.values)
        except np.linalg.LinAlgError:
            u, s, vh = np.linalg.svd(cov.values)
            L = u @ np.diag(np.sqrt(s))
            
        drift = (mean_r.values - 0.5 * np.diag(cov.values))
        
        final_values = []
        # Batch simulation for 50k sims
        for _ in range(NUM_SIMS):
            uncorrelated = np.random.normal(0, 1, (num_assets, days))
            correlated = np.dot(L, uncorrelated)
            daily_log_returns = drift[:, np.newaxis] + correlated
            cum_log_returns = np.sum(daily_log_returns, axis=1)
            final_p = current_prices * np.exp(cum_log_returns)
            shares = (initial_val * np.array(weights)) / current_prices
            final_values.append(np.dot(shares, final_p))
            
        return np.array(final_values)

    print(f"Running {NUM_SIMS} simulations for Current Portfolio...")
    res_curr = simulate(curr_tickers, curr_weights)
    
    print(f"Running {NUM_SIMS} simulations for Target Portfolio...")
    res_target = simulate(target_tickers, target_weights)

    # 3. Generate Visuals
    plt.figure(figsize=(12, 7))
    plt.style.use('dark_background')
    sns.kdeplot(res_curr, fill=True, label='Current (Legacy-Heavy)', color='#fbbf24', alpha=0.4)
    sns.kdeplot(res_target, fill=True, label='Target (Atoms Barbell)', color='#38bdf8', alpha=0.4)
    
    plt.axvline(np.median(res_curr), color='#fbbf24', linestyle='--', label=f'Curr Median: ${np.median(res_curr):,.0f}')
    plt.axvline(np.median(res_target), color='#38bdf8', linestyle='--', label=f'Target Median: ${np.median(res_target):,.0f}')
    
    plt.title(f'Stress Test: {NUM_SIMS} Simulations ({LOOKBACK_YEARS}yr Lookback)', fontsize=16, color='#38bdf8', pad=20)
    plt.xlabel('Projected Value in 5 Years (Initial $100k)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    
    report_asset_dir = '/home/mihir/portfolio_reports/assets'
    plot_path = os.path.join(report_asset_dir, "large_scale_mc_10yr.png")
    plt.savefig(plot_path, dpi=200)
    print(f"Plot saved to {plot_path}")

    # Output Stats
    stats = f"""
## 🧮 Large-Scale Monte Carlo Results
- **Lookback Period:** {LOOKBACK_YEARS} Years
- **Total Simulations:** {NUM_SIMS:,}
- **Horizon:** 5 Years

### **Current Portfolio (Legacy Heavy)**
- **Median Projected Value:** ${np.median(res_curr):,.0f}
- **95% VaR (Worst Case):** ${np.percentile(res_curr, 5):,.0f}
- **Probability of Loss:** {np.sum(res_curr < 100000) / NUM_SIMS:.1%}

### **Target Portfolio (Atoms Barbell)**
- **Median Projected Value:** ${np.median(res_target):,.0f}
- **95% VaR (Worst Case):** ${np.percentile(res_target, 5):,.0f}
- **Probability of Loss:** {np.sum(res_target < 100000) / NUM_SIMS:.1%}

**Verdict:** The Target "Atoms" portfolio shows a **{(np.median(res_target)/np.median(res_curr)-1)*100:+.1f}%** relative improvement in median outcome with a {('lower' if np.percentile(res_target, 5) > np.percentile(res_curr, 5) else 'higher')} risk profile.
    """
    print(stats)
    
    # Save to report
    with open('/home/mihir/portfolio_reports/investment_thesis/Monte_Carlo_Audit.md', 'w') as f:
        f.write("# 🧪 Stress Test: Large-Scale Monte Carlo Audit\n")
        f.write(f"![MC Plot](../assets/large_scale_mc_10yr.png)\n\n")
        f.write(stats)

if __name__ == "__main__":
    run_custom_mc()
