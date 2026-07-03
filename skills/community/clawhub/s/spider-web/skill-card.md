## Description: <br>
Spider Web Trigger Network indexes installed skill trigger words and routes natural-language queries to likely matching skills through exact, semantic, logical, and fuzzy matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inventory installed skill triggers, test user queries against a trigger database, and choose which skill should handle a request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and expose the installed skill inventory through its trigger database and dashboard. <br>
Mitigation: Run the dashboard only on localhost in a trusted browser session and review exported trigger data before sharing it. <br>
Risk: Broad routing rules may select the wrong skill from generic words or bare file extensions. <br>
Mitigation: Rebuild or edit the trigger database before relying on routing decisions, and remove generic triggers that create ambiguous matches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/spider-web) <br>
- [Source repository](https://github.com/bettermen/spider-web) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local JSON/API outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce ranked skill matches, skill names, trigger database JSON, dashboard responses, and reindexing instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
