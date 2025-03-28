"""
Portfolio and ETF definitions for the Boggleheads Lazy Portfolios Simulator.
"""

# Define mapping from ETFs to CSV files
file_mapping = {
    "VT": "HistoricalPrices_VT.csv",
    "BND": "HistoricalPrices_VBTLX.csv",
    "VTI": "HistoricalPrices_VTSAX.csv",
    "VXUS": "HistoricalPrices_VTIAX.csv",
    "TIP": "HistoricalPrices_VAIPX.csv",
    "ITOT": "HistoricalPrices_VTSAX.csv",  # Using VTSAX as proxy for ITOT
    "IXUS": "HistoricalPrices_VTIAX.csv"   # Using VTIAX as proxy for IXUS
}

# Define portfolio mappings
portfolios = {
    "Two-fund Portfolio": {
        "VT": 0.60,    # Total World Stock Market
        "BND": 0.40,   # Total Bond Market
    },
    "Taylor Larimore's Three-Fund Portfolio": {
        "VTI": 0.34,   # Total US Stock Market
        "VXUS": 0.33,  # Total International Stock Market
        "BND": 0.33,   # Total Bond Market
    },
    "Scott Burns' Margarita Portfolio": {
        "ITOT": 0.34,  # Total US Stock Market (iShares)
        "IXUS": 0.33,  # Total International Stock Market (iShares)
        "TIP": 0.33,   # Inflation-Protected Securities
    },
    "Rick Ferri's Lazy Three-Fund Portfolio": {
        "VTI": 0.40,   # Total US Stock Market
        "VXUS": 0.20,  # Total International Stock Market
        "BND": 0.40,   # Total Bond Market
    }
}

# Define ETF descriptions for better display
etf_descriptions = {
    "VT": "Vanguard Total World Stock ETF",
    "BND": "Vanguard Total Bond Market Fund",
    "VTI": "Vanguard Total Stock Market Fund",
    "VXUS": "Vanguard Total International Stock Fund",
    "ITOT": "iShares Total US Stock Market Fund",
    "IXUS": "iShares International Stock Fund",
    "TIP": "Inflation-Protected Securities Fund"
}

# Define asset categories for better visualization
asset_categories = {
    "VT": "Global Stocks",
    "VTI": "US Stocks",
    "VXUS": "International Stocks",
    "BND": "Bonds",
    "ITOT": "US Stocks",
    "IXUS": "International Stocks",
    "TIP": "TIPS Bonds"
}

# Define colors for asset categories
category_colors = {
    "US Stocks": "blue",
    "International Stocks": "orange",
    "Global Stocks": "green",
    "Bonds": "red",
    "TIPS Bonds": "purple"
}