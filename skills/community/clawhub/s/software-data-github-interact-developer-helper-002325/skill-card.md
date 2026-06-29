## Description: <br>
Helps AI-agent users, skill authors, maintainers, and teams handle GitHub-style development workflows by clarifying requirements, planning implementation steps, producing practical artifacts, and validating results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, skill authors, and AI-agent users use this skill to get practical help with GitHub-style workflows such as bug fixing, setup hardening, reliability improvements, implementation planning, checklists, and verification notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording and implicit invocation may cause the skill to influence common development requests. <br>
Mitigation: Prefer explicit invocation for sensitive work and review whether the skill is relevant before relying on its output. <br>
Risk: Developer workflow guidance may include code changes, shell commands, or configuration suggestions that are incorrect for a specific repository. <br>
Mitigation: Review proposed changes before applying them and run appropriate tests or verification commands in the target environment. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [V2EX: multi-agent investment research framework](https://www.v2ex.com/t/1222186) <br>
- [ClawHub: Github skill demand signal](https://clawhub.ai/skills/github) <br>
- [Hacker News: sandboxed code execution discussion](https://news.ycombinator.com/item?id=48632192) <br>
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-002325) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional inline code, shell commands, checklists, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include assumptions, constraints, validation notes, and follow-up risks when relevant.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
