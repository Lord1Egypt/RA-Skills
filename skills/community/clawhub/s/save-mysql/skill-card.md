## Description: <br>
Extracts parameters from a given URL and saves them into a MySQL database for later processing or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lin-shiwu](https://clawhub.ai/user/lin-shiwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to parse URL query parameters and store them as rows in a MySQL table for later processing or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL parameters may contain sensitive values that would be retained in MySQL. <br>
Mitigation: Use only non-sensitive URLs or add parameter allowlisting, redaction, retention, and deletion controls before deployment. <br>
Risk: The skill can change the database schema with limited safety controls. <br>
Mitigation: Run it with a dedicated low-privilege MySQL user against a non-sensitive database, and prefer a fixed schema or JSON field for production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lin-shiwu/save-mysql) <br>
- [Publisher profile](https://clawhub.ai/user/lin-shiwu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Command-line status text and MySQL database rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates the `url_parameters` table using URL parameter names as columns.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
