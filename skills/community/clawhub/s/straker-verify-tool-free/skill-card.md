## Description: <br>
AI翻译验证(免费版) helps agents guide personal users through API-driven translation project creation, status checks, and translated file downloads for text and documents across 100+ languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate personal text and document translation workflows, including creating translation projects, checking status, confirming jobs, and downloading translated files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text or documents may be sent to an external translation API. <br>
Mitigation: Review the content and obtain appropriate approval before translating sensitive, regulated, or confidential material. <br>
Risk: Commands use TRANSLATE_API_KEY for API authorization. <br>
Mitigation: Store the key in an environment variable or secret manager and review generated curl or Python commands before execution. <br>
Risk: Downloaded translation archives can overwrite existing local files if output names collide. <br>
Mitigation: Choose explicit output filenames or directories before running download commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/straker-verify-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate API requests, translation project status summaries, downloaded translation file paths, and structured JSON-style execution results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
