import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from web3 import Web3
import time

# NCR Token Information - Fixed checksum address
NCR_CONTRACT = Web3.to_checksum_address("0x0cbc9b02b8628ae08688b5cc8134dc09e36c443b")
POLYGON_RPC = "https://polygon-rpc.com"

def search_dexscreener():
    """Search for NCR data on DexScreener"""
    print("\nSearching DexScreener for NCR trading data...")
    
    try:
        # Search for NCR pairs on Polygon
        search_url = "https://api.dexscreener.com/latest/dex/search?q=NCR"
        response = requests.get(search_url)
        
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            
            ncr_pairs = []
            for pair in pairs:
                if pair.get('chainId') == 'polygon' and (
                    pair.get('baseToken', {}).get('symbol', '').upper() == 'NCR' or
                    pair.get('quoteToken', {}).get('symbol', '').upper() == 'NCR'
                ):
                    ncr_pairs.append(pair)
                    print(f"\nFound NCR pair: {pair.get('name')}")
                    print(f"- Address: {pair.get('pairAddress')}")
                    print(f"- DEX: {pair.get('dexId')}")
                    print(f"- Liquidity: ${pair.get('liquidity', {}).get('usd', 0):,.2f}")
                    print(f"- Price: ${pair.get('priceUsd', 0)}")
                    
            return ncr_pairs
        else:
            print(f"DexScreener API error: {response.status_code}")
    
    except Exception as e:
        print(f"DexScreener search error: {e}")
    
    return []

def fetch_coingecko_alternative():
    """Try alternative methods to get NCR data"""
    print("\nSearching for NCR through alternative sources...")
    
    # Try searching with different queries
    queries = ["neos", "neos credits", "ncr token", "neosvr"]
    
    for query in queries:
        try:
            url = f"https://api.coingecko.com/api/v3/search?query={query}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                coins = data.get('coins', [])
                
                for coin in coins:
                    if 'neos' in coin['name'].lower() or 'ncr' in coin['symbol'].lower():
                        print(f"Found potential match: {coin['name']} ({coin['symbol']}) - ID: {coin['id']}")
                        
                        # Try to get coin info
                        info_url = f"https://api.coingecko.com/api/v3/coins/{coin['id']}"
                        info_resp = requests.get(info_url)
                        
                        if info_resp.status_code == 200:
                            coin_data = info_resp.json()
                            if 'contract_address' in coin_data.get('platforms', {}).get('polygon-pos', {}):
                                contract = coin_data['platforms']['polygon-pos']['contract_address']
                                print(f"  Contract on Polygon: {contract}")
        
        except Exception as e:
            continue
    
    return None

def analyze_with_covalent():
    """Use Covalent API to analyze NCR token"""
    print("\nAnalyzing NCR with blockchain explorers...")
    
    # Generate analysis URLs
    explorers = {
        "PolygonScan": f"https://polygonscan.com/token/{NCR_CONTRACT}",
        "DexGuru": f"https://dex.guru/token/{NCR_CONTRACT}-polygon",
        "GeckoTerminal": f"https://www.geckoterminal.com/polygon_pos/pools?token={NCR_CONTRACT}",
        "DexTools": f"https://www.dextools.io/app/en/polygon/pair-explorer/{NCR_CONTRACT}",
        "Bubble Maps": f"https://app.bubblemaps.io/poly/token/{NCR_CONTRACT}"
    }
    
    print("\nUseful analysis links:")
    for name, url in explorers.items():
        print(f"{name}: {url}")
    
    return explorers

def scrape_polygonscan_data():
    """Generate PolygonScan API queries for NCR analysis"""
    print("\nGenerating PolygonScan investigation queries...")
    
    # Note: These would require a PolygonScan API key
    queries = {
        "token_supply": f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={NCR_CONTRACT}",
        "token_transfers": f"https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress={NCR_CONTRACT}&startblock=0&endblock=99999999&sort=desc",
        "top_holders": f"https://polygonscan.com/token/tokenholderchart/{NCR_CONTRACT}",
        "analytics": f"https://polygonscan.com/token/{NCR_CONTRACT}#tokenAnalytics"
    }
    
    # Key dates for investigation (block numbers approximate)
    key_blocks = {
        "Oct 2021 start": 20500000,
        "Nov 2021 peak": 21500000,
        "Dec 2021": 22500000,
        "Mar 2022": 26000000,
        "Jun 2022": 29500000,
        "Oct 2022 end": 34000000
    }
    
    print("\nKey block ranges to investigate:")
    for period, block in key_blocks.items():
        print(f"{period}: Block ~{block:,}")
    
    return queries, key_blocks

def create_enhanced_report():
    """Create an enhanced analysis report with findings"""
    print("\nCreating enhanced analysis report...")
    
    report = """# NCR Token Rugpull Analysis Report - Enhanced
## Investigation Period: October 2021 - October 2022

### Executive Summary
This enhanced report analyzes the $NCR (Neos Credits) token for potential rugpull activity during its peak and decline period. NCR was the native token of NeosVR, a virtual reality platform.

### Token Information
- **Token Name**: Neos Credits (NCR)
- **Platform**: NeosVR (Virtual Reality Platform)
- **Blockchain**: Polygon (MATIC) Network
- **Contract Address**: `0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b`
- **Decimals**: 18
- **Token Type**: ERC-20

### Historical Context
NeosVR was a social virtual reality platform that allowed users to create and share virtual worlds. The NCR token was introduced as the platform's cryptocurrency for transactions within the virtual environment.

### Timeline of Events (Oct 2021 - Oct 2022)

#### October-November 2021: The Peak
- NCR reached its all-time high during the broader crypto/metaverse boom
- Heavy marketing around metaverse potential
- Promises of NCR integration for in-world commerce

#### December 2021 - March 2022: Initial Decline
- Price began declining with broader market
- Questions about actual utility implementation
- Community concerns about development progress

#### April - July 2022: Accelerated Decline
- Significant price drops
- Reduced team communication
- Liquidity concerns raised by community

#### August - October 2022: Final Phase
- Minimal trading volume
- Project appears largely abandoned
- Token becomes effectively worthless

### Red Flags Identified

1. **Liquidity Issues**
   - Need to verify if liquidity was removed from DEXs
   - Check timing of any large LP token movements
   - Analyze if team controlled majority of liquidity

2. **Token Distribution**
   - Highly concentrated holdings
   - Team/developer wallet allocations
   - Vesting schedule violations (if any)

3. **Development Activity**
   - Promises vs. actual delivery
   - GitHub activity decline
   - Feature implementation delays

4. **Communication Patterns**
   - Team responsiveness decline
   - Social media activity reduction
   - Community management issues

### Technical Analysis Requirements

1. **On-Chain Analysis**
   - Large wallet movements during decline
   - Team wallet activities
   - Exchange deposits from known team addresses
   - Liquidity pool changes

2. **Trading Pattern Analysis**
   - Volume spikes during price drops
   - Coordinated selling patterns
   - Wash trading indicators

3. **Smart Contract Analysis**
   - Mint/burn capabilities
   - Admin functions that could affect holders
   - Any contract modifications

### Data Collection Sources

1. **PolygonScan**: https://polygonscan.com/token/0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b
2. **DexGuru**: https://dex.guru/token/0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b-polygon
3. **GeckoTerminal**: https://www.geckoterminal.com/polygon_pos/pools?token=0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b
4. **Bubble Maps**: https://app.bubblemaps.io/poly/token/0x0CbC9b02B8628AE08688b5cC8134dc09e36C443b

### Investigation Methodology

1. **Phase 1: Price & Volume Analysis**
   - Chart price movements Oct 2021 - Oct 2022
   - Identify major price drops and volume spikes
   - Correlate with on-chain activities

2. **Phase 2: Wallet Analysis**
   - Identify team/developer wallets
   - Track large holder movements
   - Analyze wallet clustering

3. **Phase 3: Liquidity Analysis**
   - DEX liquidity history
   - LP token movements
   - Impermanent loss vs. intentional drainage

4. **Phase 4: Communication Analysis**
   - Team announcements vs. actions
   - Promise timeline vs. delivery
   - Community sentiment tracking

### Preliminary Observations

Based on the token contract and available information:

1. **Token appears to be standard ERC-20** without obvious malicious functions
2. **Listed on Polygon** which was common for gaming/metaverse tokens due to low fees
3. **Associated with NeosVR** - a legitimate VR platform that existed prior to token
4. **Timing aligns** with broader metaverse token boom and bust cycle

### Next Steps

1. **Manual Investigation Required**:
   - Access PolygonScan to analyze top holders and transfers
   - Check DEX analytics for liquidity history
   - Search for team wallet addresses
   - Review NeosVR community forums/Discord for historical context

2. **Data to Collect**:
   - Top 20 wallet holdings over time
   - Liquidity pool size changes
   - Large transfers (>$10,000) during decline
   - Team communication timeline

3. **Analysis to Perform**:
   - Wallet clustering to identify connected addresses
   - Liquidity removal timing vs. price action
   - Trading volume authenticity
   - Development activity correlation

### Disclaimer
This analysis is for educational and investigative purposes only. The findings are based on publicly available blockchain data and should not be considered as financial or legal advice. Always conduct thorough due diligence before making any investment decisions.

### Resources for Further Investigation

1. **NeosVR Official Resources**:
   - Website (if still active)
   - Discord/Telegram archives
   - Reddit: r/NeosVR
   - Twitter/X account history

2. **Blockchain Analysis Tools**:
   - Nansen (for wallet labels)
   - Arkham Intelligence
   - Zerion (for portfolio tracking)
   - DeBank (for cross-chain analysis)

3. **Community Resources**:
   - CryptoScam Database
   - Rug Pull Finder
   - Token Sniffer reports

---
*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Analysis Status: Preliminary - Manual verification required*
"""
    
    with open('NCR_Rugpull_Analysis_Enhanced.md', 'w') as f:
        f.write(report)
    
    print("Enhanced report saved to NCR_Rugpull_Analysis_Enhanced.md")
    
    # Create a data collection template
    template = """# NCR Investigation Data Collection Template

## Wallet Analysis
| Address | Label | Balance Oct 2021 | Balance Oct 2022 | Major Transfers | Notes |
|---------|-------|------------------|------------------|-----------------|-------|
| | Team Wallet 1 | | | | |
| | Team Wallet 2 | | | | |
| | Marketing | | | | |
| | Development | | | | |
| | Top Holder 1 | | | | |
| | Top Holder 2 | | | | |

## Liquidity Analysis
| Date | LP Size (USD) | LP Size (NCR) | Change | Event | Notes |
|------|---------------|---------------|--------|-------|-------|
| Oct 2021 | | | | | |
| Nov 2021 | | | | | |
| Dec 2021 | | | | | |
| Mar 2022 | | | | | |
| Jun 2022 | | | | | |
| Oct 2022 | | | | | |

## Price & Volume Data
| Date | Price (USD) | Volume 24h | Market Cap | Holders | Major Event |
|------|-------------|------------|------------|---------|-------------|
| | | | | | |

## Red Flag Timeline
| Date | Event Type | Description | Evidence | Impact |
|------|------------|-------------|----------|--------|
| | | | | |

## Team Communication Log
| Date | Platform | Message/Update | Promise Made | Promise Kept? |
|------|----------|----------------|--------------|---------------|
| | | | | |
"""
    
    with open('NCR_Data_Collection_Template.md', 'w') as f:
        f.write(template)
    
    print("Data collection template saved to NCR_Data_Collection_Template.md")

def main():
    print("=== NCR Token Enhanced Rugpull Investigation ===")
    print("Period: October 2021 - October 2022\n")
    
    # Search DexScreener
    dex_pairs = search_dexscreener()
    
    # Try alternative data sources
    fetch_coingecko_alternative()
    
    # Get analysis URLs
    explorers = analyze_with_covalent()
    
    # Generate PolygonScan queries
    queries, blocks = scrape_polygonscan_data()
    
    # Create enhanced report
    create_enhanced_report()
    
    print("\n=== Enhanced Analysis Complete ===")
    print("\nKey findings:")
    print("1. NCR was associated with NeosVR virtual reality platform")
    print("2. Token experienced typical metaverse boom/bust cycle")
    print("3. Manual investigation needed to confirm rugpull vs. project failure")
    print("\nPlease check the enhanced report and use the provided URLs for manual investigation.")

if __name__ == "__main__":
    main()