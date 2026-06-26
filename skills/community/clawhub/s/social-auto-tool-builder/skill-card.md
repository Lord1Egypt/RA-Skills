## Description: <br>
Standardizes building local AI and Playwright social media auto-reply tools, including dry-run checks, Windows EXE delivery, and selector templates for Xiaohongshu, Douyin, and Kuaishou. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cruciata](https://clawhub.ai/user/cruciata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to turn a social platform auto-reply requirement into a local Python, Playwright, and Ollama workflow with selector mapping, safety checks, packaging steps, and user-facing run instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tools may retain authority through a logged-in browser session. <br>
Mitigation: Use only accounts and content you control, isolate the browser profile used for saved sessions, and inspect generated code and build scripts before running them. <br>
Risk: Automated social-platform replies can send unintended public messages or trigger account restrictions. <br>
Mitigation: Keep dry-run as the default, set very small reply limits, and require manual approval before any live send. <br>
Risk: Platform selector drift or incomplete DOM mapping can target the wrong content or fail silently. <br>
Mitigation: Calibrate selectors from current screenshots or DOM snippets, verify dry-run candidates against manual expectations, and require a success signal for live sends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cruciata/social-auto-tool-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks and command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers platform, interval, recency, reply limit, once, and interactive parameters for generated tools.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
