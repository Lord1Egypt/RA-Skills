## Description: <br>
Fetches and summarizes recent arXiv and Hugging Face papers with Agentic Paper Digest, including JSON feed and optional local API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to configure and run a paper-digest pipeline that fetches recent arXiv and Hugging Face papers, summarizes them, and exposes results as JSON or through a local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bootstrap downloads and installs live external code from the referenced project. <br>
Mitigation: Review the downloaded repository and dependency list before running bootstrap or installing requirements. <br>
Risk: The skill requires a sensitive SkillBoss API key for LLM calls. <br>
Mitigation: Use a revocable key, keep .env private, and avoid sharing logs or outputs that may expose credentials. <br>
Risk: The stop script can forcibly terminate any local process bound to port 8000. <br>
Mitigation: Confirm port 8000 belongs to this skill before running stop_api.sh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/quincy-agentic-paper-digest-skill) <br>
- [Agentic Paper Digest repository](https://github.com/matanle51/agentic_paper_digest) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration notes, and JSON paper-digest output from the wrapped pipeline] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local SQLite data store and expose local API endpoints when the API workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
