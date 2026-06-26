## Description: <br>
Intelligent information triage system based on Tiago Forte's PARA method (Projects/Areas/Resources/Archive) for automatic categorization and priority scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to organize notes, tasks, bookmarks, and exported content into PARA categories, assign urgency scores, detect related items, and produce triage reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private notes, tasks, bookmarks, or exported content can be processed locally and included in generated reports. <br>
Mitigation: Review selected inputs and output destinations before running the CLI, and treat generated reports as containing the same sensitivity as the source material. <br>
Risk: Automatic PARA categories, urgency scores, and relatedness suggestions may be incomplete or incorrect for user-specific workflows. <br>
Mitigation: Review triage results before acting on them or importing them into a knowledge-management system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/second-brain-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance] <br>
**Output Format:** [Structured triage summaries and optional JSON, Markdown, or CSV reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes PARA category labels, urgency scores, recommended actions, metadata, category statistics, and relatedness summaries when enabled.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence; artifact frontmatter states v1.0.0 and package metadata states 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
