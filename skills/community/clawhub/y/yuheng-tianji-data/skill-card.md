## Description: <br>
Collects and formats free real-time Chinese A-share, Hong Kong index, QDII ETF, commodity futures, and macro-policy market signals from public data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and market-analysis agents use this skill to collect free market snapshots, normalized data, and alert signals for Chinese equities, Hong Kong indices, commodity futures, QDII ETFs, and related macro news inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public market-data network requests and can write local market data, logs, and alert queue files. <br>
Mitigation: Approve the external data sources and storage path before execution, and run the scripts in an environment where those outbound requests and local writes are expected. <br>
Risk: The monitoring script includes Feishu notification behavior with a hard-coded recipient. <br>
Mitigation: Remove or rewrite the Feishu push helper before running or scheduling the monitor, make recipients configurable, and require explicit consent before any outbound message is sent. <br>
Risk: The security guidance flags unsafe dynamic Python execution in the notification helper. <br>
Mitigation: Replace the python3 -c subprocess call with a safe in-process or data-only API call before deployment. <br>
Risk: Market data can be delayed, unavailable, or anomalous. <br>
Mitigation: Preserve the documented freshness checks, cross-source validation, anomaly labels, and null handling before using outputs for downstream analysis. <br>


## Reference(s): <br>
- [Free Data Sources](references/free-data-sources.md) <br>
- [ClawHub Release Page](https://clawhub.ai/horizoncove/yuheng-tianji-data) <br>
- [Tencent Market Quote Endpoint](https://qt.gtimg.cn/q=hkHSI) <br>
- [Sina Futures Quote Endpoint](https://hq.sinajs.cn/list=hf_GC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance, Python code examples, JSON data snapshots, and console text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may write local data, logs, and alert queue JSON files under /workspace/data/tianji-system when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
