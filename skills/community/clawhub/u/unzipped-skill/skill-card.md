## Description: <br>
Create Farcaster accounts and post casts autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jozh-bit](https://clawhub.ai/user/Jozh-bit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage Farcaster identities, configure profiles, and publish casts through CLI or programmatic flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend wallet funds while registering identities, bridging, swapping, and paying API fees. <br>
Mitigation: Use a new low-value wallet and require manual approval before any bridge, swap, signer, profile, or cast action. <br>
Risk: The skill handles private keys and may store credentials as plaintext JSON by default. <br>
Mitigation: Prefer --no-save or a dedicated secret store, and restrict access to any saved credential files. <br>
Risk: The skill can post public casts and update a public Farcaster profile. <br>
Mitigation: Review cast and profile content before execution and monitor the resulting account activity. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Jozh-bit/unzipped-skill) <br>
- [Farcaster Agent Source Link](https://github.com/rishavmukherji/farcaster-agent) <br>
- [Neynar Hub API](https://hub-api.neynar.com) <br>
- [Neynar REST API](https://api.neynar.com) <br>
- [Farcaster Fname Registry](https://fnames.farcaster.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause an agent to execute wallet, bridge, swap, profile, and public posting workflows when followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
