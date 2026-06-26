## Description: <br>
Self-Correct provides a lightweight framework for retry strategies, error tagging, result verification, and state snapshots before higher-risk operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jokerli530](https://clawhub.ai/user/jokerli530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add simple self-correction patterns around shell and API tool use, including retry decisions, verification messages, and pre-operation snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive cleanup or batch removal commands could erase unintended files. <br>
Mitigation: Require explicit confirmation before cleanup or removal, verify paths are under the intended snapshot directory, and replace xargs rm -rf patterns with safer bounded deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jokerli530/self-correct) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [snapshot.sh](artifact/scripts/snapshot.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with Bash code blocks and shell script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, list, and clean snapshot files under /tmp/nova-snapshots when adopted by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
