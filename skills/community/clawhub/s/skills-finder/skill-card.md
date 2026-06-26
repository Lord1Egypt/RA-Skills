## Description: <br>
Intelligent skill matcher that searches multiple skill marketplaces (ClawHub & Skills.sh) in real-time. Supports ANY language for user input, multi-step skill chaining, and one-click installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welliu](https://clawhub.ai/user/welliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search ClawHub and Skills.sh for relevant skills, compare recommendations, install selected packages, and identify multi-skill chains for complex tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a recommended result can modify the user's agent environment and affect future behavior. <br>
Mitigation: Verify the exact package name, source marketplace, publisher, and permissions before running install commands. <br>
Risk: Search and install commands depend on external marketplace CLIs and may return unavailable, rate-limited, or unexpected results. <br>
Mitigation: Review the raw command output and prefer source-qualified installs from ClawHub or Skills.sh. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/welliu/skills-finder) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Skill Finder Script](artifact/scripts/skill-finder.sh) <br>
- [Evaluation Prompts](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with marketplace search output, status messages, and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke npx-based marketplace CLIs and can install persistent skills when the install command is used.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
