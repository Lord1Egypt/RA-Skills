## Description: <br>
Analyzes X/Twitter profiles by collecting tweets, followings, and followers with tweety-ns, then producing a Chinese-language dossier with thematic content classification, style analysis, and network insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to build structured profile reports for public X/Twitter accounts, including tweet collection, LLM-assisted topic classification, Chinese summary reports, and social network analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Twitter/X session cookies. <br>
Mitigation: Use only a dedicated low-privilege Twitter/X account, treat cookies as passwords, and do not paste them into chats or commit them to files. <br>
Risk: The workflow can broaden collection beyond X/Twitter through external-link exploration. <br>
Mitigation: Confirm the intended collection scope before running and avoid off-platform collection unless that data is explicitly wanted. <br>
Risk: The security verdict is suspicious due to cookie handling and insufficient collection boundaries. <br>
Mitigation: Review the skill before installation and run it only in a controlled workspace with the minimum account privileges needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lovensky1992-wk/x-profile-deep-dive) <br>
- [README](artifact/README.md) <br>
- [Data analysis reference](artifact/references/data-analysis.md) <br>
- [Profile README template](artifact/references/readme-template.md) <br>
- [Network analysis template](artifact/references/network-template.md) <br>
- [With-skill evaluation](artifact/evals/results/deepdive-with-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown profile files, JSON collection data, and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a profile directory with a README summary, topic category files, and network.md; uses Twitter/X cookies and may include external-link exploration when the workflow calls for it.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
