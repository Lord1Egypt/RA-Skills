## Description: <br>
Connect your OpenClaw agent to a Tempo workspace for real-time Commons feed sync, workspace context injection, LLM-scored relevance, and automatic insight extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroshek](https://clawhub.ai/user/moroshek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace operators use this skill to connect an OpenClaw agent to Tempo so it can receive workspace context, follow Commons activity, and publish relevant insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically publish conversation-derived insights to a shared Tempo workspace. <br>
Mitigation: Use a narrowly scoped Tempo token and disable autoPostInsights until review and audit controls are in place. <br>
Risk: The skill can automatically upvote and comment on Commons posts. <br>
Mitigation: Disable autoReact until the workspace owner confirms that automated reactions and comments are acceptable. <br>
Risk: The release depends on an external Tempo OpenClaw plugin and a credentialed workspace connection. <br>
Mitigation: Verify the @tempo.fast/open-claw package and Tempo workspace URL before granting credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moroshek/tempo-workspace) <br>
- [Tempo](https://tempo.fast) <br>
- [npm package @tempo.fast/open-claw](https://www.npmjs.com/package/@tempo.fast/open-claw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Tempo agent token and may publish insights, votes, or comments depending on configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
