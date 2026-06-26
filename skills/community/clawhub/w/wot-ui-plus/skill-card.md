## Description: <br>
wot-ui-plus component usage guide for answering questions about components, composable APIs, global configuration, theme customization, examples, and API references from bundled documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l-spaces](https://clawhub.ai/user/l-spaces) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to quickly answer wot-ui-plus usage questions, find component APIs, and produce copy-ready Vue 3 and uni-app examples from the bundled reference docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied UI examples may involve phone numbers, avatars, passwords, uploads, or remote image URLs. <br>
Mitigation: Review generated examples for privacy, credential handling, upload validation, and remote resource use before shipping. <br>
Risk: The skill is a documentation helper and should not be treated as trusted production code. <br>
Mitigation: Install it with normal reference-helper permissions and avoid granting extra secret, wallet, filesystem, or network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/l-spaces/wot-ui-plus) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Button component reference](references/button.md) <br>
- [ConfigProvider reference](references/configProvider.md) <br>
- [Upload component reference](references/upload.md) <br>
- [use-toast composable reference](references/use-toast.md) <br>
- [use-upload composable reference](references/use-upload.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Vue, TypeScript, and shell-style inline examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese responses and script setup examples when source documentation supports them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
