## Description: <br>
Fetches real-time China A-share stock and market-index quotes from the Sina Finance API without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunnyfo](https://clawhub.ai/user/Sunnyfo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to query A-share indices and individual stock codes, then receive current price, change, volume, turnover, and related quote fields as text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock codes are sent to Sina Finance. <br>
Mitigation: Use only intended public stock or index codes, and avoid entering account identifiers, private notes, or unrelated sensitive data as stock-code input. <br>
Risk: Quote data may be delayed, unavailable outside trading hours, or unsuitable as investment advice. <br>
Mitigation: Treat results as informational market data and verify important decisions against an authoritative financial source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sunnyfo/sina-stock) <br>
- [Sunnyfo publisher profile](https://clawhub.ai/user/Sunnyfo) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is plain text, simplified text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stock codes are supplied as comma-separated or space-separated command arguments; no API key is required.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
