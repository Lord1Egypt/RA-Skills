## Description: <br>
Read and display recent trade history from local JSONL log file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newbienodes](https://clawhub.ai/user/newbienodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to inspect locally recorded trade history, recap recent trades, filter by symbol, and review stored trade counts without modifying the log file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private financial trading history from a local log file. <br>
Mitigation: Invoke it only for explicit trade-history requests and treat returned trades as private financial information. <br>
Risk: The submitted artifact references a local read.py helper that is not included in the artifact. <br>
Mitigation: Before running the skill, verify that the helper exists and only reads the stated trades.jsonl file without modifying or deleting data. <br>


## Reference(s): <br>
- [ClawHub Trade History release page](https://clawhub.ai/newbienodes/trade-history) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/newbienodes) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Text] <br>
**Output Format:** [JSON from the local helper script, summarized for the user as readable text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional limit and symbol filters; default output is newest trades first with up to 20 records.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
