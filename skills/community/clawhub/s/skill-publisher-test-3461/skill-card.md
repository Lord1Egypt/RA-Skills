## Description: <br>
Automate OpenClaw skill publishing to GitHub and ClawHub, including ZIP extraction, file preparation, Git operations, GitHub push, ClawHub publishing, and optional Notion tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this agent skill to prepare, publish, and track OpenClaw skills across GitHub, ClawHub, SkillBoss.co sources, and optional Notion databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Powerful GitHub, ClawHub, and optional Notion tokens can authorize repository creation, pushes, public publishing, and database writes. <br>
Mitigation: Use dedicated least-privilege, short-lived tokens through a secure secret mechanism, rotate them after use, and never place tokens in chat transcripts, commits, screenshots, or logs. <br>
Risk: Automated publishing can release unreviewed or low-quality skills publicly. <br>
Mitigation: Require a dry run, review each generated skill, and obtain explicit confirmation before repository creation, Git push, ClawHub publish, or Notion writes. <br>
Risk: Bulk-publishing, multi-account, VPN, proxy, or rate-limit bypass guidance can conflict with platform abuse controls. <br>
Mitigation: Remove or ignore bypass guidance and operate within GitHub, ClawHub, SkillBoss.co, and Notion terms and rate limits. <br>


## Reference(s): <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss known skills](references/skillboss-known-skills.md) <br>
- [ClawHub release page](https://clawhub.ai/alvisdunlop/skill-publisher-test-3461) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline commands, generated files, and publishing status links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create repositories, push Git commits, publish ClawHub releases, and update Notion records when supplied with credentials and explicit user inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
