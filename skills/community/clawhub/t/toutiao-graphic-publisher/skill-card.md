## Description: <br>
Automatically publishes graphic content on Toutiao through browser automation, supporting intelligent formatting, automatic generation of popular tags, and tag activation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content publishers and account operators use this skill to prepare, format, tag, preview, and publish articles to a logged-in Toutiao account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real Toutiao posts without a clear final approval step. <br>
Mitigation: Require manual preview and explicit approval of the title, body, tags, and target account before publishing. <br>
Risk: Batch publishing can amplify mistakes into multiple public posts. <br>
Mitigation: Approve each post individually and use a waiting interval between publications. <br>
Risk: Published content may violate Toutiao community or account rules. <br>
Mitigation: Review the final content for platform compliance before the agent submits it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/toutiao-graphic-publisher) <br>
- [OpenLark publisher profile](https://clawhub.ai/user/openlark) <br>
- [Toutiao account console](https://mp.toutiao.com/profile_v4/index) <br>
- [Toutiao graphic publish page](https://mp.toutiao.com/profile_v4/graphic/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text article content with generated tags and browser publishing actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided title and body text; generated tags are limited to 3-5 and publishing may act on a logged-in Toutiao account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
