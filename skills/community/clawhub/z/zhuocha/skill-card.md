## Description: <br>
Helps authorized users assess whether bid records grouped under the same reid are true duplicates before writing confirmed deduplication decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cybluesky](https://clawhub.ai/user/cybluesky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized operations or data-quality users use this skill to review groups of bid jy_id records under a shared reid, compare business fields and source text, and decide whether the records should be marked as duplicate or non-duplicate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist duplicate-review decisions to an internal result table. <br>
Mitigation: Use it only with authorization for the relevant bidding databases and require human confirmation before insert operations. <br>
Risk: The documented recovery path includes a full-table truncate operation. <br>
Mitigation: Run any truncate only with a current backup, administrator approval, and a clear plan to restore or rewrite all needed records. <br>
Risk: A mismatch between helper behavior and the documented 5200 data-source workflow can undermine automated judgments. <br>
Mitigation: Align the helper with the documented 5200 detail-field workflow before relying on automated duplicate classifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cybluesky/zhuocha) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, code, shell commands] <br>
**Output Format:** [Markdown guidance with SQL examples, Python snippets, and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be human-confirmed before any database insert.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
