## Description: <br>
Helps agents retrieve and analyze Kuaishou/Kwai comments and replies through SocialDataX for audience feedback, sentiment themes, pain points, FAQs, and discussion summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Kuaishou/Kwai first-level comments and replies with a SocialDataX API key, then summarize observed themes, sentiment, objections, pain points, FAQs, and discussion patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided SocialDataX API key for comment retrieval. <br>
Mitigation: Install and use it only when you intend to access SocialDataX with your own API key, and provide the key through SOCIALDATAX_API_KEY. <br>
Risk: Using npx with @latest runs the current npm package version. <br>
Mitigation: Review the package before use in sensitive environments or pin a package version when reproducibility is required. <br>
Risk: Broad pagination options such as --all or --include-replies may fetch many comments or replies through the API. <br>
Mitigation: Use --pages or --max-items to bound retrieval when only a sample or limited analysis is needed. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-kuaishou-comments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; SocialDataX CLI and MCP calls return JSON comment data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY plus node and npm when using the direct CLI.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
