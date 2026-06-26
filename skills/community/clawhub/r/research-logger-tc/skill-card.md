## Description: <br>
Research a topic via web search, auto-match a GIF, and log structured notes to Bear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to research a topic, collect source-backed notes, match supporting media, and prepare a Bear-ready Markdown note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a local code-execution bug when handling untrusted or unusual topic strings. <br>
Mitigation: Avoid untrusted or unusual topic strings until the quoting issue is fixed, and review command inputs before running the script. <br>
Risk: The skill may send topic data to external search or GIF tools and saves generated notes locally or in Bear. <br>
Mitigation: Avoid sensitive topics unless external lookup and local note storage are acceptable, and review generated notes before saving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/research-logger-tc) <br>
- [Research note template](references/research_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown note with source links, supporting media, and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the generated note to /tmp/research_note.md and prints it for review before saving to Bear.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
