# Research Notes and Methodology

## Signal Generation Approach
Developed during session with Hermes Agent.

### Data Collection Process
1. **Form Stats Retrieval**: For each player, executed web searches like:
   - `"{player}" last 5 matches chances created key passes assists {club}`
   - Variations for specific stats when needed
   - Extracted numerical values from search snippets and page content

2. **Price Fetching**: Searched for:
   - `"Simmer assist price {player}"`
   - Looked for dollar amounts in results

### Calculation Methodology
- **Weights**: Assists (0.5), Key passes (0.3), Chances created (0.2)
- **Formula**: `form_score = (assists * 0.5) + (key_passes * 0.3) + (chances_created * 0.2)`
- **Expected Price**: `form_score * SCALING_FACTOR` (currently 10.0)
- **Signal Trigger**: When Simmer price ≤ (expected price × 0.92) i.e., ≥8% below expected

### Limitations and Improvements Needed
1. **Data Quality**: Web search snippets may not contain complete or accurate stats
2. **Sample Size**: Using "last 5 matches" is arbitrary - could use season averages
3. **Weight Calibration**: Weights and scaling factor are placeholders requiring backtesting
4. **Price Accuracy**: Simmer price extraction from web search may be unreliable
5. **Missing Context**: Doesn't account for injuries, suspensions, or tactical changes

### Recommended Enhancements
1. **Direct API Access**: Use official sports stats APIs (if available) instead of web scraping
2. **Simmer Integration**: Use actual Simmer API for price data and trading
3. **Backtesting Framework**: Test strategy on historical data before live deployment
4. **Risk Management**: Implement stop-loss, position sizing based on volatility
5. **News Integration**: Factor in team news, injuries, suspensions

### Sources Consulted During Development
- Premier League official statistics
- Transfermarkt player pages
- StatMuse sports statistics
- FBref and FotMob advanced stats
- League official sites (Bundesliga, Ligue 1, La Liga)
- The Guardian for World Cup fixtures
- Various social media and news sites for supplementary info

### Next Steps for Live Deployment
1. Replace dry-run logging with actual Simmer API calls
2. Implement proper error handling and retry logic
3. Add configuration for bankroll, risk parameters, and signal thresholds
4. Create monitoring dashboard for active positions
5. Schedule regular runs (e.g., every 6 hours) via Hermes cron