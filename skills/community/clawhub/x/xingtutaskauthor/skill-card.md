## Description: <br>
Queries the registered influencer list for a XingTu recruitment task, validates cookie-based access, paginates through the task author API, and exports the results to a formatted Excel workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanjuan2538](https://clawhub.ai/user/juanjuan2538) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and e-commerce operators use this skill to retrieve all registered influencers for a XingTu recruitment task and package the results for review. It is intended for workflows where the user can provide an authorized XingTu task ID and session cookie. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide an active XingTu browser cookie and stores it in plaintext for reuse. <br>
Mitigation: Use only with authorized accounts, prefer a browser-mediated or secure credential flow, remove the local cookie file after use, and avoid sharing long-lived session cookies in chat. <br>
Risk: The exported workbook can contain creator and contact data such as WeChat IDs and recruitment notes. <br>
Mitigation: Confirm that the data export is permitted, mask or exclude contact fields when they are not needed, and store or share the workbook only in approved locations. <br>
Risk: The workflow records task metadata, including task ID, author count, and output path, in memory. <br>
Mitigation: Ask before retaining task metadata and avoid keeping sensitive task identifiers or output paths longer than necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juanjuan2538/xingtutaskauthor) <br>
- [XingTu login](https://sso.oceanengine.com/xingtu/login?role=7) <br>
- [XingTu task author list API](https://www.xingtu.cn/gw/api/challenge/provider_get_task_author_list) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, terminal progress text, a JSON summary, and an Excel workbook (.xlsx) file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workbook includes author profile, pricing, recruitment status, contact, and task response fields when returned by the XingTu API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
