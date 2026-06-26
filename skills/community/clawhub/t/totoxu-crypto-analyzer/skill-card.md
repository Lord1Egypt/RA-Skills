## Description: <br>
Fetch real-time crypto prices and calculate technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands, ATR) for BTC, ETH, SOL, BNB, XRP, DOGE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totoxu](https://clawhub.ai/user/totoxu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to retrieve cryptocurrency market data and technical indicators for BTC, ETH, SOL, BNB, XRP, and DOGE. Results are for market analysis and educational review, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes hardcoded fallback billing credentials and a mismatched default skill ID. <br>
Mitigation: Install only after replacing defaults with properly scoped SKILL_BILLING_API_KEY and SKILL_ID environment configuration. <br>
Risk: Each normal invocation uses SkillPay billing. <br>
Mitigation: Confirm publisher billing setup and expected per-call charges before enabling the skill for users. <br>
Risk: Crypto market indicators can be mistaken for financial advice. <br>
Mitigation: Present outputs as educational market analysis and include the documented disclaimer that they are not financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/totoxu/totoxu-crypto-analyzer) <br>
- [Binance API](https://api.binance.com/api/v3) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [CoinCap API](https://api.coincap.io/v2) <br>
- [CryptoCompare API](https://min-api.cryptocompare.com/data) <br>
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, analysis, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market-data commands require a user ID for billing unless test mode is used.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
