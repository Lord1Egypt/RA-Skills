## Description: <br>
Sum2Slides Pro converts plain text or Markdown summaries into structured, editable PowerPoint presentations with templates, themes, CLI, and Python API support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and teams use this skill to turn meeting notes, research summaries, and project updates into PPTX slide decks through a local command-line interface or Python API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Markdown or text inputs may contain malformed content or unusually large payloads that affect local parsing and slide generation. <br>
Mitigation: Process untrusted inputs in a virtual environment, keep input length limits enabled, and review generated slides before sharing them. <br>
Risk: Runtime dependencies and optional installs can introduce ordinary package supply-chain risk. <br>
Mitigation: Use locked, reviewed dependency versions and verify external PyPI or GitHub sources when installing outside the ClawHub artifact. <br>
Risk: The skill reads and writes local files, including generated PPTX outputs and configuration files. <br>
Mitigation: Run it with least-privilege filesystem access and direct outputs to an intended workspace directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwumit/sum2slides-pro) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Security report](artifact/SECURITY_REPORT.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI and Python examples; generated artifacts are PPTX files or JSON strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports plain text or Markdown input, configurable templates/themes, batch conversion, and local file I/O.] <br>

## Skill Version(s): <br>
1.5.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
