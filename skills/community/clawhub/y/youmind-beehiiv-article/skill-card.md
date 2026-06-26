## Description: <br>
Write and publish Beehiiv posts with AI, including topic research via the YouMind knowledge base, Beehiiv-native writing, Markdown-to-HTML conversion, and publishing through the Beehiiv account connected in YouMind. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft, adapt, preview, and publish newsletter posts for Beehiiv through YouMind-managed credentials and Beehiiv account connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, list, and potentially delete posts in a connected Beehiiv account. <br>
Mitigation: Use draft mode by default, validate the target account before publishing, and avoid delete actions unless the user intentionally names a specific post to remove. <br>
Risk: The local YouMind configuration file contains a sensitive API key. <br>
Mitigation: Protect ~/.youmind/config.yaml as a secret and avoid sharing logs or artifacts that include credential values. <br>
Risk: Source material may be sent to YouMind, Beehiiv, and web-search services during research and publishing workflows. <br>
Mitigation: Avoid confidential source material unless those transfers are acceptable for the user's workspace and publication process. <br>
Risk: Beehiiv plan or API limits may block post creation, sending, or update operations. <br>
Mitigation: Validate the Beehiiv connection and plan state first, keep drafts as the safe default, and report Send API or Enterprise caveats in the result summary. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/mindy-youmind/youmind-beehiiv-article) <br>
- [YouMind Beehiiv OpenAPI Reference](references/api-reference.md) <br>
- [Beehiiv Pipeline](references/pipeline.md) <br>
- [Beehiiv Platform DNA](references/platform-dna.md) <br>
- [Generation Playbook: Idea to Beehiiv-Native Post](references/content-generation-playbook.md) <br>
- [Adaptation Playbook: Existing Content to Beehiiv Post](references/content-adaptation-playbook.md) <br>
- [Publishing Guidelines](shared/PUBLISHING.md) <br>
- [YouMind API Keys](https://youmind.com/settings/api-keys?utm_source=youmind-beehiiv-article) <br>
- [YouMind Connector Settings](https://youmind.com/settings/connector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown drafts, Beehiiv-safe HTML payloads, CLI output, and concise result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft mode is the default; publishing requires a YouMind API key and a Beehiiv account connected in YouMind.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
