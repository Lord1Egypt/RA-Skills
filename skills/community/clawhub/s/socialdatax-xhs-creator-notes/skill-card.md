## Description: <br>
Retrieves and summarizes Xiaohongshu / XHS / RedNote creator note lists and related creator content signals through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to fetch creator post lists and recent publishing activity for Xiaohongshu / XHS / RedNote accounts, then summarize titles, publish times, engagement counts, media links, and content types for content research or creator analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SocialDataX API key and may invoke the socialdatax-skills npm package to retrieve creator data. <br>
Mitigation: Install and use it only after trusting SocialDataX and the npm package, and keep SOCIALDATAX_API_KEY in the environment rather than pasting it into prompts or logs. <br>
Risk: Creator-list retrieval can be incomplete or inconsistent if pagination tokens are changed or truncated. <br>
Mitigation: Pass returned next_page_token values back unchanged when continuing a creator content list, and review page counts before relying on analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-xhs-creator-notes) <br>
- [SocialDataX API access](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summaries and shell command guidance, with JSON returned by SocialDataX CLI or MCP tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY and node/npm; read-only behavior according to the security evidence.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
