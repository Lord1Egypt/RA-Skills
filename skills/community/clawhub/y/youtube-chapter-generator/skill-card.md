## Description: <br>
Auto-generate YouTube video chapters from subtitles by parsing VTT/SRT files, identifying topic transitions, and producing timestamped chapter markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzxiatian-crypto](https://clawhub.ai/user/dzxiatian-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn YouTube subtitle files into timestamped chapter lists that can be pasted into video descriptions or editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may fetch subtitles for the wrong YouTube URL or write files to an unintended path. <br>
Mitigation: Confirm the YouTube URL and output path before running the suggested commands. <br>
Risk: The referenced generate_chapters.py script is not included as a standalone artifact file. <br>
Mitigation: Create or review the script contents before executing it locally. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces timestamped chapter text from local VTT/SRT subtitle input; users should verify YouTube chapter requirements before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
