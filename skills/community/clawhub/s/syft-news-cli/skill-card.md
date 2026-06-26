## Description: <br>
Help users access Syft News for AI pre-recalled by-topic news pools, keyword search, and news extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solatrader](https://clawhub.ai/user/solatrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve personalized and global Syft News pools, build profile-aware briefings, search recent stories, and organize news into reusable profiles, briefings, and storylines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Syft CLI uses the user's Syft account, followed topics, and personalized news access. <br>
Mitigation: Install only when comfortable using Syft account data for personalized news workflows, and run account commands such as syft status, syft login, and syft logout intentionally. <br>
Risk: Generated profiles, briefings, storylines, or guidance files may reveal interests or editorial preferences. <br>
Mitigation: Review generated artifacts before sharing or persisting them, especially profile and guidance files. <br>
Risk: Some retrieval features require a paid Syft account. <br>
Mitigation: Check account status and plan before relying on paid commands such as syft global-search or reranked search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solatrader/syft-news-cli) <br>
- [Publisher profile](https://clawhub.ai/user/solatrader) <br>
- [Syft news skills repository](https://github.com/Solatrader/syft-news-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline CLI commands and optional Markdown, HTML, or JSON artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local profile, briefing, storyline, and guidance files when the user asks for reusable artifacts.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
