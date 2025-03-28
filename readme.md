# Bogleheads Lazy Portfolios Simulator

This is a simple simulator for analyzing and comparing popular "lazy portfolios" recommended in the Bogleheads investment community. The simulator uses historical price data from CSV files to show the performance of different portfolio strategies over time.

## Project Structure

- `portfolio_definitions.py` - Contains definitions for portfolios, ETFs, and file mappings
- `csv_data_reader.py` - Functions for reading and processing CSV data
- `app.py` - Main Streamlit application

## Setup

1. Create a folder named `historical_data` in the same directory as the program files
2. Put your CSV files in the historical_data folder:
   - HistoricalPrices_VT.csv
   - HistoricalPrices_VBTLX.csv  
   - HistoricalPrices_VTSAX.csv
   - HistoricalPrices_VTIAX.csv
   - HistoricalPrices_VAIPX.csv

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Run the program:
```
streamlit run app.py
```

## How It Works

This program simulates the growth of different "lazy portfolio" strategies popularized in the Bogleheads community:

- Two-fund Portfolio (60% VT, 40% BND)
- Taylor Larimore's Three-Fund Portfolio (34% VTI, 33% VXUS, 33% BND)
- Scott Burns' Margarita Portfolio (34% ITOT, 33% IXUS, 33% TIP)
- Rick Ferri's Lazy Three-Fund Portfolio (40% VTI, 20% VXUS, 40% BND)

You can:
- Simulate growth with different initial investments and monthly contributions
- Compare the performance of different portfolios
- See portfolio statistics like annual return, risk, Sharpe ratio, and maximum drawdown

## CSV File Format

Your CSV files should have these columns:
- Date (in MM/DD/YY format)
- Open
- High
- Low
- Close
- Volume (optional)

## Fund Mapping

The program uses these mappings from fund tickers to CSV files:
- VT → HistoricalPrices_VT.csv
- BND → HistoricalPrices_VBTLX.csv
- VTI → HistoricalPrices_VTSAX.csv
- VXUS → HistoricalPrices_VTIAX.csv
- TIP → HistoricalPrices_VAIPX.csv
- ITOT → HistoricalPrices_VTSAX.csv (as a proxy)
- IXUS → HistoricalPrices_VTIAX.csv (as a proxy)