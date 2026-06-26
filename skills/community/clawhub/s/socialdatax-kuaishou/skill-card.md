## Description: <br>
Socialdatax Kuaishou helps agents research Kuaishou/Kwai hot lists, videos, comments, replies, creator profiles, and creator posts through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to retrieve Kuaishou/Kwai hot-search, content, comment, reply, creator profile, and creator post data through the SocialDataX CLI or matching MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party SocialDataX npm package and API service that receives requests made with SOCIALDATAX_API_KEY. <br>
Mitigation: Install and run it only in trusted environments, and provide SOCIALDATAX_API_KEY only when Kuaishou/Kwai research access is required. <br>
Risk: The artifact invokes read-only data-retrieval commands for external Kuaishou/Kwai content, so results may reflect the external service's available data. <br>
Mitigation: Treat retrieved social data as research input and review outputs before using them in decisions or reports. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-kuaishou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and SOCIALDATAX_API_KEY; direct CLI examples use the socialdatax-skills npm package.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
