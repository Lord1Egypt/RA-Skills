## Description: <br>
Ubuntu Encyclopedia guides agents through documentation-first Ubuntu administration, troubleshooting, package, service, networking, storage, release, and diagnostics work using Ubuntu manpages, official docs, and workspace-local cache notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and system administrators use this skill to answer Ubuntu-specific questions and plan or perform maintenance and troubleshooting after consulting Ubuntu manpages, official documentation, and local cache notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make Ubuntu documentation network requests and write a workspace-local .Ubuntu-Encyclopedia cache and notes tree. <br>
Mitigation: Install only when that network and workspace-write behavior is acceptable, and keep cache and notes scoped to consulted Ubuntu documentation and operational learnings. <br>
Risk: Live Ubuntu administration guidance can affect package state, services, networking, storage, boot behavior, or access. <br>
Mitigation: Review proposed live admin commands before execution, especially upgrades, package repair, networking, storage, boot, service, or security changes. <br>
Risk: Workspace notes could accidentally retain sensitive operational details. <br>
Mitigation: Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes or inventory tree. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kklouzal/ubuntu-encyclopedia) <br>
- [Ubuntu Manpages](https://manpages.ubuntu.com/manpages/) <br>
- [Ubuntu Encyclopedia Workflow](references/workflow.md) <br>
- [Ubuntu Topic Map](references/topic-map.md) <br>
- [Ubuntu Encyclopedia Cache Layout](references/cache-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local cache or note file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch approved Ubuntu documentation URLs and write cached documentation or operational notes under .Ubuntu-Encyclopedia/.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
