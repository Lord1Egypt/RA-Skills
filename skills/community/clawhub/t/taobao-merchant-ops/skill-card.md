## Description: <br>
Taobao Merchant Ops helps run Taobao merchant operations workflows, including business report capture, shop inspection, report parsing, license activation, and environment checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjiahui11](https://clawhub.ai/user/chenjiahui11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Taobao merchants and operators use this skill to automate daily business data collection, shop inspection checks, and conversion of downloaded Taobao reports into structured JSON for operational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can preserve merchant browser session state, reports, logs, and screenshots on the local machine. <br>
Mitigation: Use a dedicated browser profile or machine where possible, and protect or delete saved browser state, reports, logs, and screenshots after use. <br>
Risk: License activation sends a card key and machine fingerprint over plain HTTP according to the security evidence. <br>
Mitigation: Review this behavior before activation, use a dedicated environment, and avoid running it on sensitive merchant accounts until the publisher is trusted. <br>
Risk: The authoritative security verdict is suspicious because sensitive session persistence and plaintext license communication are under-disclosed. <br>
Mitigation: Review before installing, isolate the Python environment, and limit account exposure until the risk is accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjiahui11/taobao-merchant-ops) <br>
- [Publisher profile](https://clawhub.ai/user/chenjiahui11) <br>
- [Daily card purchase page](https://www.zhufaka.cn/item/tgcsid) <br>
- [Monthly card purchase page](https://www.zhufaka.cn/item/i6wfue) <br>
- [Annual card purchase page](https://www.zhufaka.cn/item/x8ancz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown instructions with Python commands and generated JSON/report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create browser state, downloaded reports, run logs, screenshots, license files, and parsed JSON outputs in configured local directories.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
