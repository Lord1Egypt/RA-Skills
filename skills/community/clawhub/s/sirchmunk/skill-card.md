## Description: <br>
Sirchmunk provides local file search through the Sirchmunk API for natural-language file and content queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxingjun778](https://clawhub.ai/user/wangxingjun778) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to submit natural-language searches against a local Sirchmunk service for files or content in configured paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may include sensitive terms and are sent to the local Sirchmunk API. <br>
Mitigation: Use only with an intentional Sirchmunk deployment, review indexed folders and logging behavior, and avoid sensitive workspaces unless approved. <br>
Risk: Results can be incomplete when search paths are not configured or passed to the wrapper. <br>
Mitigation: Confirm SIRCHMUNK_SEARCH_PATHS or pass explicit paths before relying on search results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxingjun778/sirchmunk) <br>
- [Sirchmunk project homepage](https://github.com/modelscope/sirchmunk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime search results are formatted as JSON when the local API returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running local Sirchmunk service and configured search paths; search terms are sent to the localhost API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
