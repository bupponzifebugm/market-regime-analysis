# Market Regime Analysis: S&P 500 Distribution & Tail Risk
# Author: Buffon
# Description: Validates the existence of "Fat Tails" in market returns.

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def fetch_data(ticker, start_date):
    """Fetches historical data from Yahoo Finance."""
    data = yf.download(ticker, start=start_date)
    return data['Close']

def calculate_returns(prices):
    """Calculates daily percentage returns."""
    return prices.pct_change().dropna() * 100

def analyze_distribution(returns):
    """Calculates key statistical moments (Mean, Std Dev)."""
    mean = returns.mean()
    std_dev = returns.std()
    return mean.iloc[0], std_dev.iloc[0]

def plot_distribution(returns, mean, std_dev, ticker):
    """Plots the empirical histogram vs. theoretical Normal distribution."""
    plt.figure(figsize=(14, 7))
    
    # 1. Plot Real Data (Histogram)
    plt.hist(returns, bins=200, density=True, color='blue', alpha=0.6, label=f'Actual {ticker} Returns')
    
    # 2. Plot Theoretical Data (Normal Bell Curve)
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
    perfect_bell_curve = norm.pdf(x, mean, std_dev)
    plt.plot(x, perfect_bell_curve, color='red', linewidth=2, label='Normal Distribution (Theory)')
    
    plt.title(f'{ticker} Daily Returns vs. Normal Distribution (Fat Tail Analysis)')
    plt.xlabel('Daily Return (%)')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save the chart
    plt.savefig('fat_tail_analysis.png')
    print("Chart saved as 'fat_tail_analysis.png'")
    plt.show()

if __name__ == "__main__":
    TICKER = 'SPY'
    START_DATE = '2000-01-01'
    
    print(f"--- Starting Analysis for {TICKER} ---")
    
    prices = fetch_data(TICKER, START_DATE)
    returns = calculate_returns(prices)
    mean, std = analyze_distribution(returns)
    
    print(f"Mean Return: {mean:.4f}%")
    print(f"Volatility: {std:.4f}%")
    
    plot_distribution(returns, mean, std, TICKER)