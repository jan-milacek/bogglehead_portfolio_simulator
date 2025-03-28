import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Import the portfolio definitions and data reader functions
from portfolio_definitions import (
    portfolios,
    etf_descriptions,
    asset_categories,
    category_colors
)
from csv_data_reader import (
    get_ticker_data_for_period,
    get_portfolio_data
)

# Set page configuration
st.set_page_config(
    page_title="Bogleheads Lazy Portfolios Simulator",
    page_icon="📈",
    layout="wide"
)

# Check if historical_data folder exists
if not os.path.exists("historical_data"):
    st.error("Error: The 'historical_data' folder is missing. Please create it and add your CSV files.")
    st.stop()

def simulate_growth(portfolio_data, initial_investment, monthly_contribution):
    """Calculate growth with initial investment and monthly contributions"""
    if portfolio_data is None:
        return None
    
    # Get returns from portfolio data
    returns = portfolio_data['portfolio_return']
    
    # Create dataframe for investments
    investments = pd.DataFrame(index=returns.index)
    investments['return'] = returns
    investments['contribution'] = 0.0
    
    # Set initial investment
    investments.iloc[0, investments.columns.get_loc('contribution')] = initial_investment
    
    # Add monthly contributions
    current_date = pd.to_datetime(returns.index[0])
    end_date = pd.to_datetime(returns.index[-1])
    
    while current_date <= end_date:
        # Get the first day of next month
        next_month = pd.Timestamp(year=current_date.year, month=current_date.month, day=1)
        if current_date.month == 12:
            next_month = pd.Timestamp(year=current_date.year + 1, month=1, day=1)
        else:
            next_month = pd.Timestamp(year=current_date.year, month=current_date.month + 1, day=1)
        
        # Find dates in our data that fall within this month
        month_dates = investments.index[
            (investments.index >= next_month) & 
            (investments.index < next_month + pd.DateOffset(months=1))
        ]
        
        # Add contribution to the first day of the month (if exists in our data)
        if len(month_dates) > 0 and month_dates[0] != investments.index[0]:  # Skip first date (initial investment)
            investments.loc[month_dates[0], 'contribution'] = monthly_contribution
        
        # Move to next month
        current_date = next_month + pd.DateOffset(months=1)
    
    # Calculate total contributions
    investments['cumulative_contribution'] = investments['contribution'].cumsum()
    
    # Calculate portfolio value
    investments['portfolio_value'] = 0.0
    value = initial_investment
    
    for i in range(len(investments)):
        if i > 0:
            # Previous value grows by today's return
            value = value * (1 + investments.iloc[i]['return'])
            # Add today's contribution
            value += investments.iloc[i]['contribution']
        
        investments.iloc[i, investments.columns.get_loc('portfolio_value')] = value
    
    return investments

def main():
    st.title("Bogleheads Lazy Portfolios Simulator")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page:", ["Portfolio Simulator", "Portfolio Comparison"])
    
    if page == "Portfolio Simulator":
        st.header("Simulate Portfolio Growth")
        
        # Portfolio selection and parameters
        col1, col2 = st.columns(2)
        
        with col1:
            selected_portfolio = st.selectbox("Select a portfolio:", list(portfolios.keys()))
            
            # Display portfolio composition
            st.subheader("Portfolio Composition")
            
            # Create data for pie chart
            composition_data = []
            for ticker, weight in portfolios[selected_portfolio].items():
                composition_data.append({
                    "Ticker": ticker,
                    "Asset": etf_descriptions.get(ticker, ticker),
                    "Category": asset_categories.get(ticker, "Other"),
                    "Weight": weight * 100  # Convert to percentage
                })
            
            # Display as table
            composition_df = pd.DataFrame(composition_data)
            st.dataframe(composition_df[["Ticker", "Asset", "Weight"]])
            
            # Create pie chart
            fig = px.pie(
                composition_df, 
                values="Weight", 
                names="Category", 
                title="Asset Allocation",
                color="Category",
                color_discrete_map=category_colors
            )
            st.plotly_chart(fig)
        
        with col2:
            # Get test data to find available date range
            test_data = get_ticker_data_for_period("VT")
            
            if test_data is not None:
                min_date = test_data.index.min().date()
                max_date = test_data.index.max().date()
            else:
                min_date = datetime(2010, 1, 1).date()
                max_date = datetime.today().date()
            
            # Input parameters
            start_date = st.date_input(
                "Start Date:", 
                value=min_date + timedelta(days=90),
                min_value=min_date,
                max_value=max_date - timedelta(days=90)
            )
            
            end_date = st.date_input(
                "End Date:", 
                value=max_date,
                min_value=start_date + timedelta(days=90),
                max_value=max_date
            )
            
            initial_investment = st.number_input(
                "Initial Investment ($):", 
                min_value=1, 
                value=10000,
                step=1000
            )
            
            monthly_contribution = st.number_input(
                "Monthly Contribution ($):", 
                min_value=0, 
                value=500,
                step=100
            )
        
        # Run simulation button
        if st.button("Run Simulation"):
            with st.spinner("Calculating..."):
                # Get portfolio data
                portfolio_data = get_portfolio_data(
                    selected_portfolio,
                    start_date,
                    end_date
                )
                
                if portfolio_data is None:
                    st.error(f"Could not load data for {selected_portfolio}. Please check your CSV files.")
                else:
                    # Simulate growth
                    growth_data = simulate_growth(
                        portfolio_data,
                        initial_investment,
                        monthly_contribution
                    )
                    
                    if growth_data is not None:
                        # Display results
                        st.subheader("Portfolio Growth")
                        
                        # Create growth chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=growth_data.index,
                            y=growth_data['portfolio_value'],
                            mode='lines',
                            name='Portfolio Value',
                            line=dict(color='blue', width=2)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=growth_data.index,
                            y=growth_data['cumulative_contribution'],
                            mode='lines',
                            name='Total Contributions',
                            line=dict(color='green', width=2, dash='dash')
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_portfolio} Growth",
                            xaxis_title="Date",
                            yaxis_title="Value ($)",
                            legend=dict(x=0.01, y=0.99)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show statistics
                        final_value = growth_data['portfolio_value'].iloc[-1]
                        total_invested = growth_data['cumulative_contribution'].iloc[-1]
                        profit = final_value - total_invested
                        roi = (profit / total_invested) * 100
                        
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Final Value", f"${final_value:,.2f}")
                        col2.metric("Total Invested", f"${total_invested:,.2f}")
                        col3.metric("Profit/Loss", f"${profit:,.2f}")
                        col4.metric("ROI", f"{roi:.2f}%")
                        
                        # Show monthly data table
                        st.subheader("Monthly Data")
                        monthly_data = growth_data.resample('M').last()
                        monthly_data = monthly_data[['portfolio_value', 'cumulative_contribution']]
                        monthly_data.columns = ['Portfolio Value ($)', 'Total Invested ($)']
                        monthly_data['Profit/Loss ($)'] = monthly_data['Portfolio Value ($)'] - monthly_data['Total Invested ($)']
                        monthly_data['ROI (%)'] = (monthly_data['Profit/Loss ($)'] / monthly_data['Total Invested ($)']) * 100
                        
                        st.dataframe(monthly_data.round(2))
                    else:
                        st.error("Error running simulation. Please try different parameters.")
    
    elif page == "Portfolio Comparison":
        st.header("Compare Portfolio Performance")
        
        # Get date range from test data
        test_data = get_ticker_data_for_period("VT")
        
        if test_data is not None:
            min_date = test_data.index.min().date()
            max_date = test_data.index.max().date()
        else:
            min_date = datetime(2010, 1, 1).date()
            max_date = datetime.today().date()
        
        # Input parameters
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Start Date:", 
                value=min_date + timedelta(days=90),
                min_value=min_date,
                max_value=max_date - timedelta(days=90)
            )
        
        with col2:
            end_date = st.date_input(
                "End Date:", 
                value=max_date,
                min_value=start_date + timedelta(days=90),
                max_value=max_date
            )
        
        # Portfolio selection
        portfolios_to_compare = st.multiselect(
            "Select Portfolios to Compare:",
            list(portfolios.keys()),
            default=list(portfolios.keys())
        )
        
        if st.button("Compare Portfolios"):
            if not portfolios_to_compare:
                st.warning("Please select at least one portfolio to compare.")
            else:
                with st.spinner("Calculating..."):
                    # Create figure for comparison
                    fig = go.Figure()
                    
                    # Add each portfolio to the chart
                    for portfolio_name in portfolios_to_compare:
                        portfolio_data = get_portfolio_data(
                            portfolio_name,
                            start_date,
                            end_date
                        )
                        
                        if portfolio_data is not None:
                            fig.add_trace(go.Scatter(
                                x=portfolio_data.index,
                                y=portfolio_data['cumulative_return'],
                                mode='lines',
                                name=portfolio_name
                            ))
                    
                    fig.update_layout(
                        title="Portfolio Comparison",
                        xaxis_title="Date",
                        yaxis_title="Growth (%)",
                        legend=dict(x=0.01, y=0.99),
                        height=500,  # Taller chart
                        margin=dict(l=20, r=20, t=40, b=30)  # Adjust margins
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show statistics for each portfolio
                    st.subheader("Performance Statistics")
                    
                    stats_data = []
                    
                    for portfolio_name in portfolios_to_compare:
                        portfolio_data = get_portfolio_data(
                            portfolio_name,
                            start_date,
                            end_date
                        )
                        
                        if portfolio_data is not None:
                            # Calculate statistics
                            returns = portfolio_data['portfolio_return']
                            
                            annual_return = ((1 + returns.mean()) ** 252) - 1
                            annual_risk = returns.std() * np.sqrt(252)
                            sharpe = annual_return / annual_risk if annual_risk != 0 else 0
                            max_drawdown = (portfolio_data['cumulative_return'] / portfolio_data['cumulative_return'].cummax() - 1).min()
                            
                            stats_data.append({
                                "Portfolio": portfolio_name,
                                "Annual Return": f"{annual_return:.2%}",
                                "Annual Risk": f"{annual_risk:.2%}",
                                "Sharpe Ratio": f"{sharpe:.2f}",
                                "Max Drawdown": f"{max_drawdown:.2%}"
                            })
                    
                    if stats_data:
                        stats_df = pd.DataFrame(stats_data)
                        stats_df.set_index("Portfolio", inplace=True)
                        st.dataframe(stats_df)
                    
                    # Show individual portfolio details
                    for portfolio_name in portfolios_to_compare:
                        st.subheader(f"{portfolio_name} Details")
                        
                        # Display portfolio composition
                        composition_data = []
                        for ticker, weight in portfolios[portfolio_name].items():
                            composition_data.append({
                                "Ticker": ticker,
                                "Asset": etf_descriptions.get(ticker, ticker),
                                "Weight": weight * 100  # Convert to percentage
                            })
                        
                        composition_df = pd.DataFrame(composition_data)
                        st.dataframe(composition_df)
                        
                        # Show individual asset performance
                        for ticker, weight in portfolios[portfolio_name].items():
                            ticker_data = get_ticker_data_for_period(ticker, start_date, end_date)
                            
                            if ticker_data is not None:
                                # Calculate cumulative return in percentage if not already
                                if 'cumulative_return' not in ticker_data.columns:
                                    ticker_data['cumulative_return'] = (1 + ticker_data['daily_return']).cumprod() * 100
                                
                                # Create chart
                                fig = px.line(
                                    ticker_data,
                                    x=ticker_data.index,
                                    y='cumulative_return',
                                    title=f"{ticker} - {etf_descriptions.get(ticker, '')}"
                                )
                                
                                # Make chart wider with adjusted height
                                fig.update_layout(
                                    height=400,
                                    width=800,
                                    margin=dict(l=20, r=20, t=40, b=20)
                                )
                                
                                # Use container width to make chart responsive to page size
                                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()