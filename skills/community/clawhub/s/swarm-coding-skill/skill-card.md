## Description: <br>
Autonomous multi-agent code generation that plans, implements, tests, and packages complete software projects from plain-English prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to generate full project scaffolds and implementation files from a prompt, including coordinated backend, frontend, QA, and DevOps outputs. It is suited for hackathon-style prototyping and should be reviewed before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model-generated file paths may write outside the intended project directory. <br>
Mitigation: Run the skill only in an isolated workspace and add strict path containment before routine use. <br>
Risk: Prompts, agent reasoning, and generated outputs may contain secrets or confidential project details. <br>
Mitigation: Use a scoped OpenRouter key, avoid sensitive prompts, and review and clean DECISIONS.md, .learnings, raw.txt, and generated files. <br>
Risk: Generated application code may include unsafe or unsuitable auth, blockchain, Docker, or CI behavior. <br>
Mitigation: Inspect generated code and configuration before running, publishing, or deploying it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arunnadarasa/swarm-coding-skill) <br>
- [OpenRouter API Keys](https://openrouter.ai/keys) <br>
- [Privy Integration Skill](https://clawhub.ai/tedim52/privy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Project files, Markdown decision logs, shell commands, and configuration files written under the generated project workspace.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create swarm.yaml, tasks.json, README files, tests, Docker assets, CI configuration, DECISIONS.md, SWARM_SUMMARY.md, and .learnings logs.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
