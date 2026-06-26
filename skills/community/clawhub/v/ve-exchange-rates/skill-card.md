## Description: <br>
Gets Venezuelan exchange rates, including the BCV official USD rate, Binance P2P USDT averages, and the gap between official and parallel rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jehg814](https://clawhub.ai/user/jehg814) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer questions about Venezuelan USD/VES rates, compare the BCV official rate with Binance P2P USDT prices, and estimate the exchange-rate gap and a 100 USD conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exchange-rate output may be stale, estimated, or based on fallback data when BCV or Binance data is unavailable. <br>
Mitigation: Check the reported source, Fecha Valor, and any fallback, respaldo, or estimado warning before relying on the rate. <br>
Risk: The skill contacts external public market-data services and requires local python3 and bc to run. <br>
Mitigation: Install only in environments where those outbound requests and local command dependencies are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jehg814/ve-exchange-rates) <br>
- [BCV official exchange-rate source](https://www.bcv.org.ve/) <br>
- [Binance P2P API endpoint](https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search) <br>
- [ExchangeRate API fallback endpoint](https://api.exchangerate-api.com/v4/latest/USD) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal output with rates, warnings, and conversion calculations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and bc; contacts BCV, Binance P2P, and a fallback exchange-rate API for public market data.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
