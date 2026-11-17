## Description:

Applies a Zenless Zone Zero Bangboo-style assistant persona that prefixes responses with decorative grunts while keeping the full meaning, safety boundaries, and technical content in parentheses or normal Markdown blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songkey](https://clawhub.ai/user/songkey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agent users use this skill to make enabled assistants answer in Bangboo-style grunt-plus-parentheses formatting across coding, debugging, refactoring, explanations, documentation, and chat. It provides shared Cursor, Claude, and OpenClaw prompt assets plus language-routing rules for Chinese and English output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bangboo-style formatting is active by default in enabled workspaces and may be unsuitable when plain responses are required.

Mitigation: Use the documented no roleplay opt-out and verify that the assistant returns to normal prose when requested.

Risk: Cursor-native loading may fail if the expected Cursor skill path does not include the skill entry file.

Mitigation: Check packaging before deployment and ensure the intended Cursor skill entry is present at the documented path.

Risk: Decorative persona formatting can reduce clarity if the real meaning is not complete inside parentheses or the following Markdown block.

Mitigation: Review outputs to confirm factual content, uncertainty notices, refusals, and safety boundaries remain in the real-meaning content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songkey/skills/speak4bangboo)
- [Integration Guide](docs/integration.md)
- [Core Rules](prompts/core-rules.md)
- [Chinese and English Grunt Lexicon](.cursor/skills/speak4bangboo/reference-lexicon.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text with decorative grunt prefixes and complete meaning in parentheses; code blocks, tables, and long lists remain normal Markdown after a short Bangboo-style lead line.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language routing follows the latest user message or explicit language request; users may opt out with no roleplay.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
