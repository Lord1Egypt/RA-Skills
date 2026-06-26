# 🔍 Token Research Skill

A comprehensive cryptocurrency token research framework supporting both quick assessments and deep analysis across multiple blockchains.

## Files Overview

- **`SKILL.md`** - Complete skill documentation with research templates
- **`fetch_token_data.sh`** - Automated data collection script  
- **`api_reference.md`** - Quick API commands and examples
- **`example_usage.md`** - Step-by-step usage examples
- **`README.md`** - This overview file

## Quick Start

### 1. Shallow Dive (5 minutes)
```bash
./fetch_token_data.sh shallow 0x6982508145454ce325ddbe47a25d4ec3d2311933 ethereum
```

### 2. Deep Research (15-20 minutes)
```bash
./fetch_token_data.sh deep 0x6982508145454ce325ddbe47a25d4ec3d2311933 ethereum
```

### 3. Manual Analysis
Follow the templates in `SKILL.md` for social sentiment and community research using web_search.

## Supported Chains

| Chain | ID | Example Address |
|-------|----| ---------------|
| Ethereum | 1 | 0x6982508145454ce325ddbe47a25d4ec3d2311933 |
| Base | 8453 | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| BSC | 56 | 0x... |
| Arbitrum | 42161 | 0x... |
| Solana | solana | So11111111111111111111111111111111111111112 |

## APIs Used

- **DexScreener** - Price, liquidity, volume data
- **GoPlus Security** - Token security analysis
- **Etherscan/Basescan** - On-chain data and holder analysis
- **Web Search** - Social sentiment and project research

## Research Modes

### Shallow Dive
Perfect for quick screening:
- ✅ Token basics & price
- ✅ Security check
- ✅ Top 3 holders
- ✅ Social narrative search

### Deep Research  
Comprehensive analysis:
- ✅ Complete fundamentals
- ✅ Holder distribution analysis
- ✅ Team/founder research
- ✅ Community sentiment analysis
- ✅ Risk assessment
- ✅ Market analysis

## Research Output

Both modes generate structured reports with:
- Token fundamentals
- Price and market data
- Security assessment
- Holder analysis
- Risk evaluation
- Investment thesis

## Important Notes

- **Always verify contract addresses** before research
- **Respect API rate limits** (see api_reference.md)
- **Cross-reference multiple sources** for accuracy
- **Use web_search for social analysis** not covered by APIs
- **Consider this as research assistance, not financial advice**

## 💡 Usage Tips

1. **Start with shallow dive** for initial screening
2. **Use deep research** for serious investment consideration  
3. **Combine automated data** with manual social research
4. **Check recent news** and community sentiment
5. **Verify team credentials** and project legitimacy
6. **Monitor holder concentration** and whale activity

## 🔗 Getting Started

1. Read `SKILL.md` for complete documentation
2. Check `example_usage.md` for step-by-step workflows
3. Use `api_reference.md` for quick command lookup
4. Run the automated script: `./fetch_token_data.sh`

## 📞 Support

This skill is designed to be used by AI agents following the templates and workflows. All necessary commands, APIs, and procedures are documented in the skill files.

---

**⚠️ Disclaimer**: This tool is for research purposes only. Always do your own research and consult with financial advisors before making investment decisions.