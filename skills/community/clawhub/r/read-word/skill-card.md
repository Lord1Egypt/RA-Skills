## Description: <br>
Read Microsoft Word documents in .docx and legacy .doc formats with Chinese support, keyword search, document analysis, and optional UTF-8 text export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vincent-Big-fish](https://clawhub.ai/user/Vincent-Big-fish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract, inspect, search, and export text from user-selected Microsoft Word documents without requiring Microsoft Word. It is useful for local document review workflows that need Chinese text handling and simple document statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected local Word documents and can write extracted text to a user-provided output path. <br>
Mitigation: Use it only on documents and output locations the user intends to expose to the agent, and review output paths before execution. <br>
Risk: Legacy .doc extraction is partial text-only parsing and may miss content or produce imperfect text for complex files. <br>
Mitigation: Prefer .docx when accuracy matters, or convert legacy .doc files to .docx before extraction. <br>
Risk: Dependency behavior may vary if packages are installed without version control. <br>
Mitigation: Pin and review dependency versions in stricter environments before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vincent-Big-fish/read-word) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [requirements.txt](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [Plain text, UTF-8 text files, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on user-selected local Word documents; preview and search output may be limited by command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
