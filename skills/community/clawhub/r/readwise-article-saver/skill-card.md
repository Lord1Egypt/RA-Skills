## Description: <br>
Saves article URLs to Readwise Reader and applies content-based tags, with support for WeChat Official Account articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zz123-awef](https://clawhub.ai/user/zz123-awef) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who collect articles use this skill to save one or more article URLs to Readwise Reader and receive automatic tags based on article content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically fetch and save pasted URLs with broad triggers and little user control. <br>
Mitigation: Require explicit Readwise save intent, confirm ambiguous or batch saves, and disable automatic triggering when reviewing sensitive links. <br>
Risk: Article URLs, fetched content or HTML, metadata, and generated tags may be sent to Readwise and an LLM provider. <br>
Mitigation: Use only with content acceptable for those services, strip sensitive URL parameters, and prefer URL-only handling when full content sharing is not appropriate. <br>
Risk: The skill requires a Readwise token and broad command execution to run helper scripts. <br>
Mitigation: Scope and rotate the Readwise token, restrict allowed tools to the minimum required, and review the bundled scripts before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zz123-awef/readwise-article-saver) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [Readwise Reader](https://readwise.io/read) <br>
- [Readwise Save API](https://readwise.io/api/v3/save/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON status objects from helper scripts plus concise text or Markdown user reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, READWISE_TOKEN, and OPENROUTER_API_KEY; can process multiple URLs sequentially.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
