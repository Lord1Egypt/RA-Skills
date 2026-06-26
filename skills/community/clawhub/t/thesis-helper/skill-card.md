## Description: <br>
Thesis Helper supports thesis outline generation, literature review framing, abstract drafting, citation formatting, style checks, and defense preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and writing assistants use this skill to generate thesis planning templates, citation-format examples, abstract structures, formatting checklists, and defense-preparation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes local shell scripts and local storage behavior, so generic add or run commands may write user-provided text to local logs. <br>
Mitigation: Use the thesis-specific template commands for generated guidance, avoid entering sensitive unpublished text into generic storage commands, and set THESIS_HELPER_DIR to a sandbox directory when cleanup or isolation is needed. <br>
Risk: The package documentation and available command scripts do not fully match, which may confuse users about which commands produce thesis-specific output. <br>
Mitigation: Prefer the thesis-specific commands shown by the thesis script help, and review command output before relying on it in academic work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/thesis-helper) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text emitted by shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; outputs are template-based writing and formatting guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
