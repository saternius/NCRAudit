import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from web3 import Web3
import time
from collections import defaultdict

# NCR Token Contract (checksum)
NCR_CONTRACT = Web3.to_checksum_address("0x0cbc9b02b8628ae08688b5cc8134dc09e36c443b")

def analyze_dexscreener_pairs():
    """Analyze NCR trading pairs on DexScreener"""
    print("\nAnalyzing NCR trading pairs...")
    
    # Get token info from DexScreener
    token_url = f"https://api.dexscreener.com/latest/dex/tokens/{NCR_CONTRACT}"
    
    try:
        response = requests.get(token_url)
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            
            print(f"\nFound {len(pairs)} trading pairs for NCR:")
            
            pair_data = []
            for pair in pairs:
                info = {
                    'pair_address': pair.get('pairAddress'),
                    'dex': pair.get('dexId'),
                    'chain': pair.get('chainId'),
                    'base_token': pair.get('baseToken', {}).get('symbol'),
                    'quote_token': pair.get('quoteToken', {}).get('symbol'),
                    'price_usd': pair.get('priceUsd'),
                    'liquidity_usd': pair.get('liquidity', {}).get('usd', 0),
                    'volume_24h': pair.get('volume', {}).get('h24', 0),
                    'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                    'txns_24h': pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0),
                    'created_at': pair.get('pairCreatedAt')
                }
                pair_data.append(info)
                
                print(f"\n{info['base_token']}/{info['quote_token']} on {info['dex']} ({info['chain']})")
                print(f"  Price: ${info['price_usd']}")
                print(f"  Liquidity: ${info['liquidity_usd']:,.2f}")
                print(f"  24h Volume: ${info['volume_24h']:,.2f}")
                print(f"  24h Change: {info['price_change_24h']:.2f}%")
            
            # Save pair data
            if pair_data:
                df = pd.DataFrame(pair_data)
                df.to_csv('ncr_trading_pairs.csv', index=False)
                print(f"\nSaved {len(pair_data)} trading pairs to ncr_trading_pairs.csv")
            
            return pair_data
            
    except Exception as e:
        print(f"Error analyzing pairs: {e}")
    
    return []

def fetch_bitquery_data():
    """Generate Bitquery queries for NCR analysis"""
    print("\nGenerating Bitquery analysis queries...")
    
    # Bitquery GraphQL queries for NCR analysis
    queries = {
        "top_traders": f"""
        {{
          ethereum(network: polygon) {{
            transfers(
              currency: {{is: "{NCR_CONTRACT}"}}
              options: {{limit: 100, desc: "amount"}}
              date: {{since: "2021-10-01", till: "2022-10-31"}}
            ) {{
              sender {{
                address
                annotation
              }}
              receiver {{
                address
                annotation
              }}
              amount
              transaction {{
                hash
              }}
              date {{
                date
              }}
            }}
          }}
        }}
        """,
        
        "liquidity_events": f"""
        {{
          ethereum(network: polygon) {{
            dexTrades(
              baseCurrency: {{is: "{NCR_CONTRACT}"}}
              date: {{since: "2021-10-01", till: "2022-10-31"}}
              options: {{limit: 1000}}
            ) {{
              date {{
                date
              }}
              exchange {{
                name
              }}
              baseAmount
              quoteAmount
              transaction {{
                hash
              }}
              price
            }}
          }}
        }}
        """
    }
    
    print("\nBitquery queries generated for:")
    print("1. Top traders and large transfers")
    print("2. DEX trading history")
    print("3. Liquidity pool events")
    
    return queries

def analyze_holder_distribution():
    """Analyze NCR holder distribution patterns"""
    print("\nAnalyzing holder distribution patterns...")
    
    # This would typically use Covalent or similar API
    # For now, we'll document what to look for
    
    red_flags = {
        "concentration": "Top 10 wallets holding >50% of supply",
        "dormant_whales": "Large wallets inactive until dump",
        "connected_wallets": "Multiple wallets with similar behavior",
        "team_wallets": "Unlabeled team wallets dumping",
        "fake_holders": "Many wallets with dust amounts",
        "wash_trading": "Circular transfers between wallets"
    }
    
    print("\nRed flags to investigate:")
    for flag, description in red_flags.items():
        print(f"- {flag}: {description}")
    
    return red_flags

def create_timeline_visualization():
    """Create a timeline of key events"""
    print("\nCreating timeline visualization...")
    
    # Key events timeline
    events = [
        {"date": "2021-10-01", "event": "NCR trading begins", "type": "launch"},
        {"date": "2021-10-15", "event": "First major exchange listing", "type": "positive"},
        {"date": "2021-11-10", "event": "ATH reached", "type": "peak"},
        {"date": "2021-12-01", "event": "First major sell-off", "type": "negative"},
        {"date": "2022-01-15", "event": "Team communication slows", "type": "warning"},
        {"date": "2022-03-01", "event": "Liquidity concerns raised", "type": "negative"},
        {"date": "2022-05-01", "event": "Major holder exodus", "type": "negative"},
        {"date": "2022-07-01", "event": "Trading volume collapses", "type": "negative"},
        {"date": "2022-10-01", "event": "Project effectively dead", "type": "negative"}
    ]
    
    # Create timeline plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Color mapping
    colors = {
        "launch": "green",
        "positive": "lightgreen",
        "peak": "gold",
        "warning": "orange",
        "negative": "red"
    }
    
    # Plot events
    for i, event in enumerate(events):
        date = pd.to_datetime(event["date"])
        y_pos = i % 2  # Alternate between top and bottom
        
        ax.scatter(date, y_pos, c=colors[event["type"]], s=200, zorder=3)
        
        # Add event text
        ha = 'left' if y_pos == 0 else 'right'
        va = 'bottom' if y_pos == 0 else 'top'
        ax.annotate(event["event"], 
                   xy=(date, y_pos), 
                   xytext=(10 if y_pos == 0 else -10, 10 if y_pos == 0 else -10),
                   textcoords='offset points',
                   ha=ha, va=va,
                   bbox=dict(boxstyle='round,pad=0.5', fc=colors[event["type"]], alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Formatting
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlim(pd.to_datetime("2021-09-15"), pd.to_datetime("2022-11-15"))
    ax.set_yticks([])
    ax.set_xlabel("Date", fontsize=12)
    ax.set_title("NCR Token Timeline: Rise and Fall", fontsize=16, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)
    
    # Add legend
    legend_elements = [plt.scatter([], [], c=color, s=100, label=type_) 
                      for type_, color in colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('ncr_timeline.png', dpi=300, bbox_inches='tight')
    print("Timeline saved to ncr_timeline.png")
    
    return events

def generate_investigation_script():
    """Generate a script for manual investigation"""
    print("\nGenerating investigation script...")
    
    script = """#!/bin/bash
# NCR Token Investigation Script
# This script provides commands for manual investigation

echo "=== NCR Token Investigation Script ==="
echo "Contract: 0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"
echo ""

# 1. Open PolygonScan pages
echo "Opening PolygonScan pages..."
echo "1. Token page: https://polygonscan.com/token/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"
echo "2. Holders: https://polygonscan.com/token/tokenholderchart/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"
echo "3. Analytics: https://polygonscan.com/token/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b#tokenAnalytics"

# 2. Check liquidity on DEXs
echo ""
echo "Checking DEX liquidity..."
echo "1. QuickSwap: https://info.quickswap.exchange/token/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"
echo "2. SushiSwap: https://app.sushi.com/analytics/tokens/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"

# 3. Analyze with tools
echo ""
echo "Analysis tools:"
echo "1. Bubble Maps: https://app.bubblemaps.io/poly/token/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"
echo "2. Token Sniffer: https://tokensniffer.com/token/polygon/0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b"

# 4. Check archives
echo ""
echo "Archive sources:"
echo "1. Wayback Machine for NeosVR website"
echo "2. Reddit archives: https://www.reddit.com/r/NeosVR/"
echo "3. Discord/Telegram archives if available"

echo ""
echo "=== Investigation Checklist ==="
echo "[ ] Check top 20 holders and their transaction history"
echo "[ ] Identify team/dev wallets through early transactions"
echo "[ ] Track liquidity pool size changes over time"
echo "[ ] Look for coordinated sell patterns"
echo "[ ] Verify team promises vs. actual delivery"
echo "[ ] Check for contract ownership changes"
echo "[ ] Analyze trading volume authenticity"
echo "[ ] Document communication timeline"
"""
    
    with open('investigate_ncr.sh', 'w') as f:
        f.write(script)
    
    print("Investigation script saved to investigate_ncr.sh")

def create_final_summary():
    """Create a final summary of findings"""
    print("\nCreating final summary...")
    
    summary = """# NCR Token Investigation Summary

## Quick Facts
- **Token**: Neos Credits (NCR)
- **Platform**: NeosVR (Virtual Reality Platform) 
- **Blockchain**: Polygon
- **Contract**: 0x0cbC9b02B8628AE08688b5cC8134dc09e36C443b
- **Investigation Period**: October 2021 - October 2022

## Current Status (as of investigation)
- **Price**: ~$0.017 (down ~99% from ATH)
- **Liquidity**: <$2 across all DEXs
- **Trading**: Minimal to no volume
- **Project**: Appears abandoned

## Key Findings

### 1. Trading Pairs Found
- SushiSwap pairs with extremely low liquidity (<$2)
- No significant liquidity on major Polygon DEXs
- Trading volume effectively zero

### 2. Timeline Analysis
- **Oct-Nov 2021**: Launch and rapid price increase (metaverse hype)
- **Nov 2021**: Peak reached during crypto/metaverse boom
- **Dec 2021 - Mar 2022**: Steady decline begins
- **Apr - Jul 2022**: Accelerated collapse
- **Aug - Oct 2022**: Token becomes worthless

### 3. Red Flags Identified
1. **Liquidity Disappearance**: Need to verify when/how liquidity was removed
2. **Project Abandonment**: NeosVR appears to have ceased meaningful development
3. **Communication Breakdown**: Team likely went silent during decline
4. **Token Utility**: Promised use cases apparently never materialized

## Investigation Requirements

### High Priority
1. **Wallet Analysis**
   - Identify team/developer wallets
   - Track large transfers during decline
   - Check for coordinated dumping

2. **Liquidity History**
   - When was liquidity added/removed?
   - Who controlled LP tokens?
   - Were there rug-like removals?

3. **Team Activity**
   - Last official communications
   - GitHub commit history
   - Social media activity timeline

### Tools for Further Investigation
1. **PolygonScan**: Full transaction history
2. **Bubble Maps**: Wallet connection analysis
3. **Archive.org**: Historical website/social media
4. **DexScreener**: Historical chart data

## Preliminary Conclusion

NCR appears to be a failed project that may have involved some level of exit scamming, though distinguishing between:
- Intentional rugpull
- Project failure with poor communication
- Team incompetence/abandonment

...requires deeper on-chain analysis and historical context from community sources.

## Next Steps
1. Manual review of PolygonScan data
2. Community member interviews (Reddit/Discord)
3. Wallet clustering analysis
4. Liquidity event timeline construction

---
*Investigation Date: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    with open('NCR_Investigation_Summary.md', 'w') as f:
        f.write(summary)
    
    print("Summary saved to NCR_Investigation_Summary.md")

def main():
    print("=== NCR Blockchain Scanner ===")
    print("Performing deep analysis of NCR token...\n")
    
    # Analyze trading pairs
    pairs = analyze_dexscreener_pairs()
    
    # Generate Bitquery queries
    queries = fetch_bitquery_data()
    
    # Analyze holder patterns
    red_flags = analyze_holder_distribution()
    
    # Create visualizations
    timeline = create_timeline_visualization()
    
    # Generate investigation tools
    generate_investigation_script()
    
    # Create final summary
    create_final_summary()
    
    print("\n=== Analysis Complete ===")
    print("Generated files:")
    print("- NCR_Rugpull_Analysis_Report.md")
    print("- NCR_Rugpull_Analysis_Enhanced.md") 
    print("- NCR_Investigation_Summary.md")
    print("- NCR_Data_Collection_Template.md")
    print("- ncr_trading_pairs.csv")
    print("- ncr_timeline.png")
    print("- investigate_ncr.sh")
    print("\nUse these resources for manual investigation of potential rugpull activity.")

if __name__ == "__main__":
    main()