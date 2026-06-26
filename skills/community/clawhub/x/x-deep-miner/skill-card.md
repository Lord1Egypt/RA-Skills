## Description: <br>
X Deep Miner is a local X/Twitter discovery and archiving scaffold for collecting high-engagement posts about AI, markets, and lifestyle topics into Obsidian-style Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forvendettaw](https://clawhub.ai/user/forvendettaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to organize a personal knowledge base or daily intelligence workflow around manually or browser-assisted collected X/Twitter content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rely on a logged-in X browser profile and user-directed collection of social-media content. <br>
Mitigation: Confirm account authorization, X/Twitter policy compliance, and privacy expectations before using browser-assisted collection. <br>
Risk: An hourly cron job can repeatedly save collected content under the configured local workspace. <br>
Mitigation: Review WORKSPACE_DIR, output directories, retention expectations, and storage access before enabling scheduled execution. <br>
Risk: The implementation is a scaffold with unfinished fetching and translation behavior. <br>
Mitigation: Treat generated notes as drafts and verify collection results, translations, and summaries before relying on them. <br>


## Reference(s): <br>
- [X-Deep-Miner references](references/references.md) <br>
- [X Explore](https://x.com/explore) <br>
- [X Home](https://x.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Obsidian-style Markdown files and terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes notes under the configured local workspace output directory when collected results are available.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
