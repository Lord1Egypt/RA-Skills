## Description: <br>
Reviews SQL syntax and safety, executes candidate SQL against StarRocks or Doris, and returns query results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LoveNerverMore](https://clawhub.ai/user/LoveNerverMore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill as the final step in a SQL-generation workflow to audit candidate SQL, execute it against a configured database, and return data, row counts, retry guidance, and simplified metric candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live database execution can expose or modify sensitive systems if configured with broad credentials, and the security summary says advertised SQL safety blocks are not enforced. <br>
Mitigation: Deploy only with read-only, least-privilege database credentials in a controlled environment, and patch or verify SQL safety checks before allowing live database execution. <br>
Risk: Query results and fallback prompts may contain sensitive business data and can be sent to the configured Gemini fallback service. <br>
Mitigation: Use approved network access, disable or review the Gemini fallback before production use, and avoid sending sensitive data to external services. <br>
Risk: Credential and external-service handling requires review before production use. <br>
Mitigation: Manage database and API credentials through approved secret storage, rotate any bundled or default tokens, and limit environment variable exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LoveNerverMore/sql-audit) <br>
- [Publisher profile](https://clawhub.ai/user/LoveNerverMore) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, configuration] <br>
**Output Format:** [JSON result object with query data, status fields, row counts, errors, retry flags, and optional simplified metric candidates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 50 rows from execution and may write audit_output.json when run as a standalone workflow step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
