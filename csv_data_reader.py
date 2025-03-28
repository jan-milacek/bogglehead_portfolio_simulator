import pandas as pd
import os
from portfolio_definitions import file_mapping, portfolios

def load_ticker_data(ticker, data_dir="historical_data"):
    """
    Load data for a ticker from CSV file
    
    Args:
        ticker (str): The ticker symbol to load data for
        data_dir (str): Directory where CSV files are stored
    
    Returns:
        pandas.DataFrame or None: DataFrame with price data or None if error
    """
    if ticker not in file_mapping:
        print(f"No data file for {ticker}")
        return None
    
    filename = file_mapping[ticker]
    filepath = os.path.join(data_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    try:
        # Load CSV file
        df = pd.read_csv(filepath)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert date
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
        
        # Set Date as index
        df.set_index('Date', inplace=True)
        
        # Sort by date
        df = df.sort_index()
        
        # Calculate daily returns
        df['daily_return'] = df['Close'].pct_change()
        
        return df
    
    except Exception as e:
        print(f"Error loading {ticker} data: {str(e)}")
        return None

def get_ticker_data_for_period(ticker, start_date=None, end_date=None):
    """
    Get data for a ticker within a date range
    
    Args:
        ticker (str): The ticker symbol
        start_date: Start date (str or datetime)
        end_date: End date (str or datetime)
    
    Returns:
        pandas.DataFrame or None: DataFrame with price data or None if error
    """
    # Load all data for the ticker
    df = load_ticker_data(ticker)
    
    if df is None:
        return None
    
    # Filter by date range
    if start_date is not None:
        df = df[df.index >= pd.to_datetime(start_date)]
    
    if end_date is not None:
        df = df[df.index <= pd.to_datetime(end_date)]
    
    return df

def get_portfolio_data(portfolio_name, start_date, end_date):
    """
    Get historical data for a portfolio
    
    Args:
        portfolio_name (str): Name of the portfolio
        start_date: Start date (str or datetime)
        end_date: End date (str or datetime)
    
    Returns:
        pandas.DataFrame or None: DataFrame with portfolio returns or None if error
    """
    if portfolio_name not in portfolios:
        print(f"Portfolio not found: {portfolio_name}")
        return None
    
    # Get the portfolio definition
    portfolio = portfolios[portfolio_name]
    
    # Dataframe to store results
    result = None
    
    # For each ticker in the portfolio
    for ticker, weight in portfolio.items():
        # Get data for this ticker
        ticker_data = get_ticker_data_for_period(ticker, start_date, end_date)
        
        if ticker_data is None:
            print(f"Missing data for {ticker}")
            continue
        
        # Apply portfolio weight
        ticker_data[f'{ticker}_weighted'] = ticker_data['daily_return'] * weight
        
        if result is None:
            result = ticker_data[[f'{ticker}_weighted']].copy()
        else:
            # Join with existing data
            result = result.join(ticker_data[[f'{ticker}_weighted']])
    
    if result is None:
        return None
    
    # Calculate portfolio return
    result['portfolio_return'] = result.filter(like='_weighted').sum(axis=1)
    
    # Calculate cumulative return in percentage (100% = no change)
    result['cumulative_return'] = (1 + result['portfolio_return']).cumprod() * 100
    
    return result