## Description: <br>
Helps agents use SocialDataX for Xiaohongshu, XHS, and RedNote search hot lists, content research, note search, note details, comment analysis, creator profile lookup, and creator note lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and analyze Xiaohongshu / XHS / RedNote search trends, notes, comments, and creator information through SocialDataX. It requires a SocialDataX API key and Node/npm runtime access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned XHS note URLs may contain xsec_token query parameters that should be treated as sensitive. <br>
Mitigation: Avoid storing, forwarding, or sharing token-bearing note URLs unless needed; prefer note IDs or redacted links when possible. <br>
Risk: The skill depends on a third-party SocialDataX API key and npm package for Xiaohongshu data access. <br>
Mitigation: Install and use it only when the publisher, package, API key handling, and SocialDataX terms are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-xhs) <br>
- [SocialDataX API key and service homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and returned XHS identifiers or URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SocialDataX CLI commands, MCP tool names, XHS note IDs, comment IDs, creator IDs, and returned note URLs.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
