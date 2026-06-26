## Description: <br>
Write and publish tweets and X threads with AI-assisted topic research from YouMind, local preview support, and publishing through a YouMind-connected X account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, developers, and other users can use this skill to draft, adapt, preview, and optionally publish single tweets or numbered X threads through YouMind. It is useful when an agent needs to turn a topic, article, or raw post text into X-native content and return result links after publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly through the user's connected X account. <br>
Mitigation: Preview generated content and require explicit user approval before publishing; use local draft mode when approval or account readiness is unclear. <br>
Risk: The skill requires a YouMind API key and uses shared ~/.youmind storage plus local post metadata files. <br>
Mitigation: Keep credentials in the documented YouMind config files, do not commit them, restrict local file access, and rotate the API key if exposure is suspected. <br>
Risk: Security evidence reports under-disclosed delete capability and broader YouMind account access than a tweet-writing workflow requires. <br>
Mitigation: Review the toolkit commands before installation and only run deletion or broader account actions when the user explicitly requests and confirms them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-x-article) <br>
- [YouMind X OpenAPI reference](artifact/references/api-reference.md) <br>
- [Publishing pipeline](artifact/references/pipeline.md) <br>
- [X platform and content constraints](artifact/references/platform-dna.md) <br>
- [Content generation playbook](artifact/references/content-generation-playbook.md) <br>
- [Content adaptation playbook](artifact/references/content-adaptation-playbook.md) <br>
- [YouMind API key settings](https://youmind.com/settings/api-keys?utm_source=youmind-x-article) <br>
- [YouMind connector settings](https://youmind.com/settings/connector) <br>
- [YouMind pricing](https://youmind.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with tweet text, numbered thread drafts, command snippets, configuration paths, and result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown drafts under the YouMind home directory and can publish externally to X when the user has configured YouMind credentials, connected X, and approved publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
