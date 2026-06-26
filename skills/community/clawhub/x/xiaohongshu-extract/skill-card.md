## Description: <br>
Extract metadata from Xiaohongshu (XHS) share or discovery URLs by parsing window.__INITIAL_STATE__ and returning note details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jovijovi](https://clawhub.ai/user/jovijovi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to extract structured metadata, engagement statistics, user details, tags, and video information from public Xiaohongshu share or discovery links for downstream review or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extractor makes outbound web requests to user-provided Xiaohongshu URLs, which can expose requested URLs and network metadata to the remote service. <br>
Mitigation: Use public Xiaohongshu links only, avoid private or internal URLs, and review links before execution. <br>
Risk: The --output option writes extracted metadata, including user details and engagement data, to a local file path selected by the user. <br>
Mitigation: Choose an appropriate output path and handle generated JSON files according to the sensitivity of the source content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jovijovi/xiaohongshu-extract) <br>
- [Publisher profile](https://clawhub.ai/user/jovijovi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [JSON metadata or flattened JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write extracted metadata or error details to a user-selected local file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
