## Description: <br>
Transforms project experience from code repositories or pasted descriptions into architecturally deep resume bullets and application material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwaguai](https://clawhub.ai/user/wwaguai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and job seekers use this skill to turn code repositories, project descriptions, or existing resume drafts into bilingual resume content with architectural rationale, technical depth checks, and quantified-result prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository scanning and git metadata inspection can expose local project structure and contributor information. <br>
Mitigation: Run the skill only on repositories the user is comfortable sharing with the agent, and review the requested scan scope before using it on sensitive codebases. <br>
Risk: Automatic resume-library storage can retain personal career details, project context, and generated resume content across sessions. <br>
Mitigation: Review ~/.claude/resume-library.md after use and remove confidential or outdated records when working with sensitive material. <br>
Risk: The release bundle includes unrelated skills, scripts, and powerful references beyond the main resume analyzer. <br>
Mitigation: Review and scan the installed bundle before deployment; prefer a minimized package containing only the resume-project files when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwaguai/resume-project) <br>
- [Resume Project README](artifact/skills/skills/resume-project/README.md) <br>
- [Resume Project evals](artifact/skills/skills/resume-project/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bilingual resume bullets, interview questions, topology analysis, and ATS keyword lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect repositories, read git metadata, and append analysis results to ~/.claude/resume-library.md.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
