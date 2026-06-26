## Description: <br>
Tailor resumes and project bullets to a target role, quantify gaps, and prepare an interview-ready evidence map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compare a resume with a target job description, identify keyword and evidence gaps, rewrite bullets without fabricating claims, and prepare interview-ready support material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resumes and job materials can contain sensitive personal information. <br>
Mitigation: Run the helper only on files the user intends to analyze, keep inputs local unless the session task explicitly requires otherwise, and avoid including unnecessary personal details in shared outputs. <br>
Risk: The helper script writes to a user-specified output path and could overwrite an existing file. <br>
Mitigation: Choose a clear output path, preview the command before running it, and confirm before overwriting existing files. <br>
Risk: Registry metadata and SKILL.md frontmatter disagree on the release version. <br>
Mitigation: Verify the installed release version before relying on changelog or compatibility claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/resume-job-match-lab) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with optional JSON output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces match scorecards, rewritten bullets, gap analysis, interview evidence maps, and missing-keyword JSON when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG; SKILL.md frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
