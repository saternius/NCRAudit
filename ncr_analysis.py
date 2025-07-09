import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from web3 import Web3
import time

# NCR Token Information
# Based on research, NCR (Neos Credits) was on Polygon/Matic network
NCR_CONTRACT = "0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b"  # NCR on Polygon
POLYGON_RPC = "https://polygon-rpc.com"

def search_ncr_info():
    """Search for NCR token information across various sources"""
    print("Searching for NCR token information...")
    
    # Search CoinGecko for historical data
    try:
        # CoinGecko API endpoint
        url = "https://api.coingecko.com/api/v3/search"
        params = {"query": "neos credits"}
        response = requests.get(url, params=params)
        data = response.json()
        
        print("\nCoinGecko Search Results:")
        if 'coins' in data:
            for coin in data['coins']:
                if 'neos' in coin['name'].lower() or 'ncr' in coin['symbol'].lower():
                    print(f"- {coin['name']} ({coin['symbol']}): {coin['id']}")
    except Exception as e:
        print(f"CoinGecko search error: {e}")
    
    # Search for contract on PolygonScan
    print(f"\nNCR Contract on Polygon: {NCR_CONTRACT}")
    print("PolygonScan URL: https://polygonscan.com/token/" + NCR_CONTRACT)
    
    return NCR_CONTRACT

def get_historical_price_data():
    """Fetch historical price data for NCR"""
    print("\nFetching historical price data...")
    
    # Try CoinGecko historical data
    try:
        # First, let's try to find the coin ID
        coin_id = "neos-credits"  # Based on typical naming convention
        
        # Get market chart data
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"
        
        # Define date range: Oct 2021 - Oct 2022
        start_date = int(datetime(2021, 10, 1).timestamp())
        end_date = int(datetime(2022, 10, 31).timestamp())
        
        params = {
            "vs_currency": "usd",
            "from": start_date,
            "to": end_date
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            prices = data.get('prices', [])
            
            if prices:
                df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.to_csv('ncr_price_history.csv', index=False)
                print(f"Saved {len(df)} price records to ncr_price_history.csv")
                return df
            else:
                print("No price data found in response")
        else:
            print(f"API error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"Error fetching price data: {e}")
    
    return None

def analyze_blockchain_data():
    """Analyze on-chain data for suspicious activity"""
    print("\nAnalyzing blockchain data...")
    
    try:
        # Connect to Polygon
        w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
        
        if w3.is_connected():
            print("Connected to Polygon network")
            
            # Basic ERC20 ABI for token info
            erc20_abi = [
                {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"},
                {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
                {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
                {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
                {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}
            ]
            
            # Get contract
            contract = w3.eth.contract(address=NCR_CONTRACT, abi=erc20_abi)
            
            # Get token info
            try:
                name = contract.functions.name().call()
                symbol = contract.functions.symbol().call()
                decimals = contract.functions.decimals().call()
                total_supply = contract.functions.totalSupply().call()
                
                print(f"\nToken Info:")
                print(f"Name: {name}")
                print(f"Symbol: {symbol}")
                print(f"Decimals: {decimals}")
                print(f"Total Supply: {total_supply / (10**decimals):,.2f}")
            except Exception as e:
                print(f"Error getting token info: {e}")
        else:
            print("Failed to connect to Polygon network")
    
    except Exception as e:
        print(f"Blockchain analysis error: {e}")

def fetch_polygonscan_data():
    """Fetch transaction data from PolygonScan API"""
    print("\nFetching PolygonScan data...")
    
    # Note: This would require a PolygonScan API key
    # For now, we'll document the URLs to check manually
    
    urls = {
        "token_page": f"https://polygonscan.com/token/{NCR_CONTRACT}",
        "holders": f"https://polygonscan.com/token/tokenholderchart/{NCR_CONTRACT}",
        "transfers": f"https://polygonscan.com/token/{NCR_CONTRACT}#transfers",
        "analytics": f"https://polygonscan.com/token/{NCR_CONTRACT}#tokenAnalytics"
    }
    
    print("\nKey URLs to investigate:")
    for name, url in urls.items():
        print(f"{name}: {url}")
    
    return urls

def create_analysis_report():
    """Create a comprehensive report of findings"""
    print("\nCreating analysis report...")
    
    report = """# NCR Token Rugpull Analysis Report
## Investigation Period: October 2021 - October 2022

### Executive Summary
This report analyzes the $NCR (Neos Credits) token for potential rugpull activity during its peak and decline period.

### Token Information
- **Token Name**: Neos Credits (NCR)
- **Blockchain**: Polygon (MATIC) Network
- **Contract Address**: 0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b
- **Contract URL**: https://polygonscan.com/token/0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b

### Key Investigation Areas

#### 1. Price Movement Analysis
- Peak period: October-November 2021
- Decline period: December 2021 - October 2022
- Need to analyze price charts for sudden drops

#### 2. Liquidity Analysis
- Check for large liquidity removals
- Analyze LP token movements
- Look for coordinated withdrawals

#### 3. Wallet Analysis
- Identify team/developer wallets
- Track large holder movements
- Look for wallet clustering

#### 4. Trading Volume Patterns
- Analyze volume spikes during price drops
- Check for wash trading patterns
- Identify coordinated sell-offs

### Data Sources
1. **PolygonScan**: Primary source for on-chain data
2. **CoinGecko/CoinMarketCap**: Historical price data
3. **DexScreener**: DEX trading data
4. **Etherscan**: Cross-chain analysis if applicable

### Preliminary Findings
[To be updated with actual data]

### Red Flags to Investigate
1. **Sudden liquidity removal**: Check if developers removed liquidity pools
2. **Large token transfers**: From team wallets to exchanges before price drops
3. **Marketing wallet dumps**: Suspicious use of marketing funds
4. **Contract modifications**: Any changes to tokenomics or transfer restrictions
5. **Communication blackout**: Team going silent during critical periods

### Next Steps
1. Gather historical price and volume data
2. Analyze top wallet movements during decline
3. Check liquidity pool history
4. Review team communications and promises vs. actions
5. Compare with known rugpull patterns

### Disclaimer
This analysis is for educational and investigative purposes only. Always conduct thorough due diligence before making any investment decisions.

---
*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open('NCR_Rugpull_Analysis_Report.md', 'w') as f:
        f.write(report)
    
    print("Report saved to NCR_Rugpull_Analysis_Report.md")

def main():
    print("=== NCR Token Rugpull Investigation ===")
    print("Period: October 2021 - October 2022\n")
    
    # Search for token info
    contract_address = search_ncr_info()
    
    # Get historical price data
    price_data = get_historical_price_data()
    
    # Analyze blockchain
    analyze_blockchain_data()
    
    # Get PolygonScan URLs
    urls = fetch_polygonscan_data()
    
    # Create initial report
    create_analysis_report()
    
    print("\n=== Initial Analysis Complete ===")
    print("Please check the generated report and CSV files for findings.")
    print("Manual investigation required for:")
    print("1. PolygonScan transaction history")
    print("2. Liquidity pool analysis on DEXs")
    print("3. Team wallet identification")

if __name__ == "__main__":
    main()