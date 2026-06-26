## Description: <br>
Provides A-share market data guidance and a Python router for selecting among Tencent quotes, ftshare announcements, Wind data, AkShare, and web-search fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolfjkd](https://clawhub.ai/user/wolfjkd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent builders use this skill to configure A-share quote, announcement, news, financial, technical, and macro-data retrieval workflows. It helps agents run health checks, route requests to the best available source, and emit human-readable or JSON market-data results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wind API keys and similar credentials can be exposed if pasted into chats, logs, screenshots, or repositories. <br>
Mitigation: Store credentials only in the local tool configuration or another approved secret store, and rotate any key that may have been disclosed. <br>
Risk: Optional third-party data tools such as Wind, ftshare, or AkShare may introduce external code and service dependencies. <br>
Mitigation: Review the tool source and publisher before installing it into an active agent skill folder, and install only versions you trust. <br>
Risk: Financial data sources can be unavailable, delayed, quota-limited, or inconsistent across providers. <br>
Mitigation: Run the router health check, preserve source labels in reports, and verify important market data before using it for trading or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wolfjkd/wolfjkd-trader-data) <br>
- [Tencent quote endpoint](https://qt.gtimg.cn/) <br>
- [Wind financial data service](https://www.wind.com.cn/) <br>
- [AkShare documentation](https://akshare.akfamily.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash and Python examples, plus optional JSON output from data_router.py commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [data_router.py uses the Python standard library; optional Wind and ftshare integrations require separately installed trusted tools and, for Wind, a sensitive API key.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
