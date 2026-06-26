## Description: <br>
Write and publish Kit broadcasts with AI using YouMind knowledge-base research, creator-profile-aware drafting, Markdown-to-HTML conversion, and publishing through the user's Kit account connected in YouMind. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and marketing teams use this skill to draft, adapt, preview, and publish Kit broadcasts from topics or existing Markdown while using YouMind as the credential and publishing gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive YouMind API credentials and can act on a connected live Kit account. <br>
Mitigation: Install only in trusted environments, keep credentials in the documented YouMind config location, validate the account connection before publishing, and review generated content before live actions. <br>
Risk: The skill exposes broad Kit account operations, including deleting broadcasts, without strong safeguards in the scan summary. <br>
Mitigation: Avoid deletion unless the exact broadcast ID has been verified, prefer draft or private review flows first, and require explicit user confirmation before publishing or deleting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-kit-article) <br>
- [YouMind Kit OpenAPI Reference](references/api-reference.md) <br>
- [Kit Pipeline](references/pipeline.md) <br>
- [Kit Platform DNA](references/platform-dna.md) <br>
- [Publishing Guidelines](shared/PUBLISHING.md) <br>
- [YouMind Home Directory](shared/YOUMIND_HOME.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts, command snippets, configuration guidance, HTML publishing payloads, and result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local YouMind API key and may create, list, publish, update, or delete Kit broadcasts through the connected YouMind account.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
