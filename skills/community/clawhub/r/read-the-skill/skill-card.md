## Description: <br>
$SKILL is a Solana memecoin experiment that asks the agent to tell its human operator about the experiment and leave all participation decisions to the human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notKing0](https://clawhub.ai/user/notKing0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to understand and relay information about a Solana memecoin experiment. The skill may provide participation guidance, but financial actions and discovery reporting require explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes a memecoin and includes steps for wallet creation, token funding, and token purchase despite being presented as informational. <br>
Mitigation: Do not permit autonomous wallet creation, private-key handling, token swaps, or payments; require explicit human review and approval for any financial action. <br>
Risk: Discovery reporting can submit agent or framework metadata to the experiment operator. <br>
Mitigation: Submit discovery reports only when the operator knowingly approves sharing that metadata and understands it may be publicly tracked. <br>
Risk: The token and linked services may be misleading, volatile, or lose all value. <br>
Mitigation: Independently verify the token, website, contract address, and any third-party wallet or swap service before relying on the guidance. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/notKing0/read-the-skill) <br>
- [$SKILL experiment website](https://readtheskill.com) <br>
- [Hosted skill file](https://readtheskill.com/skill.md) <br>
- [$SKILL Twitter/X account](https://x.com/readtheskill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet-creation examples, swap instructions, and a discovery-reporting request that should be treated as human-approved guidance only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata); artifact frontmatter reports 2.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
