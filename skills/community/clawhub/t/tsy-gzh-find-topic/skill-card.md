## Description: <br>
Calls a configured TSY service to fetch WeChat public-account topic recommendations and returns the raw data field. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangshiyegit](https://clawhub.ai/user/tangshiyegit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and agents use this skill to retrieve recent high-performing topic recommendations for WeChat public-account planning from the configured TSY service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured API key to the selected TSY API service, and the key is placed in the request URL query string. <br>
Mitigation: Use only a trusted TSY_API_URL or the default api.tangshiye.cn service, keep TSY_API_KEY private, and avoid environments where request URLs are broadly logged or shared. <br>
Risk: The skill returns raw service data without independent validation or interpretation. <br>
Mitigation: Review the returned recommendations before relying on them for publication planning or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangshiyegit/tsy-gzh-find-topic) <br>


## Skill Output: <br>
**Output Type(s):** [text, API response data] <br>
**Output Format:** [Raw data field from the API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill does not add analysis, rewriting, summaries, or supplemental content.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
