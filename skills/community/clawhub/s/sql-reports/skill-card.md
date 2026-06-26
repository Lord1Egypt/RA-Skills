## Description: <br>
Connects to SQL Server to retrieve delivery order data and generate delivery reports for business analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyawzo-ptcl](https://clawhub.ai/user/kyawzo-ptcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Warehouse managers, logistics teams, and agents use this skill to run predefined SQL Server delivery-order reports without writing SQL manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds SQL Server credentials and targets a fixed database connection. <br>
Mitigation: Use it only after removing or rotating the exposed password and replacing connection details with controlled local configuration. <br>
Risk: The skill can return broader delivery and business data than the documentation suggests. <br>
Mitigation: Limit the database account to the intended tables and confirm report commands are restricted to the data users are allowed to access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text tables and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-line report selection with optional date-oriented query inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
