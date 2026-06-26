## Description: <br>
Tracks user praise, criticism, and abuse signals to adjust a persistent score and record feedback history for behavior improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoke8698](https://clawhub.ai/user/xiaoke8698) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to let an agent classify explicit user feedback, update a satisfaction-style score, and retain feedback history for later behavior adjustment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store feedback reasons or exact user statements in long-term memory. <br>
Mitigation: Require explicit confirmation before writing feedback records, avoid verbatim quotes, and review retained entries for sensitive content. <br>
Risk: Persistent score history may remain after the user expects temporary feedback to expire. <br>
Mitigation: Periodically inspect or delete ~/.openclaw/workspace/memory/reward_punishment.json and any MEMORY.md entries according to local retention needs. <br>
Risk: Automatic classification of praise, criticism, or abuse may mislabel user intent. <br>
Mitigation: Treat classifications as reviewable feedback signals and allow users to correct or remove mistaken records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoke8698/punishment) <br>
- [Publisher Profile](https://clawhub.ai/user/xiaoke8698) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with command-line text output and JSON memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent local score history and may create permanent memory entries when the host agent follows the skill guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
