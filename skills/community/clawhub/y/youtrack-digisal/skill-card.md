## Description: <br>
Interact with YouTrack via REST API to read projects and issues, create or update work items, generate invoices from time tracking data, and manage knowledge base articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[digiSal](https://clawhub.ai/user/digiSal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, project managers, and operations teams use this skill to work with YouTrack projects, issues, time entries, knowledge base articles, and client invoice exports from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTrack API tokens can expose project management data if passed through command-line history or stored carelessly. <br>
Mitigation: Use a least-privileged token and prefer the YOUTRACK_TOKEN environment variable over command-line token arguments. <br>
Risk: Write operations can create or update issues and knowledge base articles in the configured YouTrack instance. <br>
Mitigation: Verify the YouTrack instance URL, project identifier, and intended action before running scripts that modify data. <br>
Risk: Generated invoices may include internal issue details, worker names, dates, rates, rounding, or project scope that should not be shared externally without review. <br>
Mitigation: Manually review invoice exports for scope, dates, rate, rounding, personnel names, and internal issue details before sending them to clients. <br>


## Reference(s): <br>
- [YouTrack API References](REFERENCES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python and bash examples; scripts produce plain text invoices or JSON API output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an authenticated YouTrack token and may produce invoice exports containing project, worker, time, rate, and billing details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
