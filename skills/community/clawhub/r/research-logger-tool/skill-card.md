## Description: <br>
Research a topic via web search, auto-match a relevant GIF, and log results as a Bear note using a configurable template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, knowledge workers, and developers use this skill to gather quick web research, pair it with a topic-relevant GIF, and save a structured Markdown-style note in Bear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and generated content may be sent to configured search and GIF tools and then saved locally in Bear. <br>
Mitigation: Use the skill only with topics appropriate for those tools, and review generated notes before storing or sharing them. <br>
Risk: Template values from user input and web results are inserted into a shell-driven template step, which can mishandle untrusted text. <br>
Mitigation: Review or patch the script before using sensitive topics; prefer escaping template values or using a safer templating method. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/research-logger-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown-style Bear note content with source links, GIF metadata, and shell status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bear on macOS, grizzly, web search access, gifgrep, jq, and a workspace template at notes/research_template.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
