## Description: <br>
Repo Analysis helps agents read, explain, and evaluate software repositories or GitHub projects through engineering-oriented summaries, architecture analysis, adoption review, and lightweight GitHub health context when relevant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[9penny](https://clawhub.ai/user/9penny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand unfamiliar repositories, map structure and key flows, and evaluate maintainability or adoption risk. It supports quick reads, architecture analysis, and takeover reviews, with optional lightweight GitHub health signals for public projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository files as part of its purpose, which can expose unrelated private code if the target scope is too broad. <br>
Mitigation: Use it only on repositories or subdirectories that are appropriate to share with the agent, and specify the intended target scope when a workspace contains unrelated code. <br>
Risk: Repository health and adoption guidance can be incomplete when documentation, tests, or public project metadata are sparse. <br>
Mitigation: Treat the analysis as review input and verify critical runtime behavior, security posture, and operational assumptions before adopting or modifying a project. <br>


## Reference(s): <br>
- [Signals for Repo Analysis](references/signals.md) <br>
- [Repo Analysis Output Templates](references/output-template.md) <br>
- [Lightweight GitHub health layer](references/github-health.md) <br>
- [Adapted notes from surveyed skills](references/adapted-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown engineering analysis with evidence labels and file-path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depth varies by selected mode: quick read, architecture analysis, or takeover review.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
