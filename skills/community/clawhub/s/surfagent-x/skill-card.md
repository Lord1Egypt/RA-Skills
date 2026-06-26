## Description: <br>
X platform skill for SurfAgent, covering route-aware workflows, proof rules, blockers, and when to use the X adapter over raw browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surfagentapp](https://clawhub.ai/user/surfagentapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide SurfAgent through X navigation, posting, replies, likes, account switching, community posting, and route-aware verification while avoiding unsupported assumptions about X UI state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent following this skill may post, reply, like, repost, follow, or switch X accounts in a logged-in browser session. <br>
Mitigation: Review intended public actions before execution, verify the active account and target surface, and require visible result confirmation before claiming success. <br>
Risk: X UI state can be ambiguous or stale, including disabled composers, delayed route settlement, and partial account switcher extraction. <br>
Mitigation: Prefer X adapter state checks, route-aware verification, and screenshot or visual confirmation when account, composer, or community state is unclear. <br>


## Reference(s): <br>
- [SurfAgent homepage](https://surfagent.app) <br>
- [ClawHub skill page](https://clawhub.ai/surfagentapp/surfagent-x) <br>
- [X state map](X_STATE_MAP.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code or package installation is produced by the skill itself.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
