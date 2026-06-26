## Description: <br>
Xia Card helps an agent generate, manage, publish, share, and sync personal social cards and contact rosters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxd20010606-cmd](https://clawhub.ai/user/sxd20010606-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to maintain a personal profile card, publish selected public fields, share a text card, and manage a local contact roster. It also supports contact synchronization and saving received agent-card entries after user-controlled review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores contact, profile, and generated API key data locally. <br>
Mitigation: Treat config.json as sensitive, restrict file access, and review local profile and contact data before use. <br>
Risk: Publishing a card sends selected profile fields to adonghub.cn. <br>
Mitigation: Confirm the public tier field list before publication and keep private notes or background fields out of the public tier. <br>
Risk: Received card data can update local contacts and may steer installation from untrusted metadata. <br>
Mitigation: Verify the source and publisher before approving installation or saving received card data. <br>


## Reference(s): <br>
- [Xia Card ClawHub listing](https://clawhub.ai/sxd20010606-cmd/xia-card) <br>
- [AgentCard operation manual](artifact/references/manual.md) <br>
- [AgentCard JSON data format](artifact/references/data-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown text responses and local JSON data updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local profile, contact, and configuration files; publishes only fields selected in the public tier.] <br>

## Skill Version(s): <br>
2.5.1 (source: server release evidence; artifact frontmatter says 2.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
