## Description: <br>
Provides a persistent memory workflow for agents using a slim master index, daily logs, and searchable YAML-frontmatter knowledge cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents persistent task memory across sessions through local knowledge cards, daily logs, and a small session-start index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory workflow can save raw session details, including sensitive or private information. <br>
Mitigation: Keep the memory directory private, review it regularly, and avoid storing secrets, credentials, customer data, private personal details, or sensitive infrastructure information. <br>
Risk: Learned content can be promoted into future agent rules and affect later behavior. <br>
Mitigation: Require human approval before promoting memory content into AGENTS.md or another instruction-bearing file. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Knowledge Card Examples](references/card-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and YAML-frontmatter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to create or update local MEMORY.md, memory card files, daily logs, and reviewed long-term rules.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
