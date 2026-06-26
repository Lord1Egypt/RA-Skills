## Description: <br>
Analyzes store Excel data against an existing warehouse and distribution network to support warehouse placement, delivery routing, transfer planning, order-cycle planning, and trunk shipping plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqianfei](https://clawhub.ai/user/jinqianfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Logistics, operations, and planning teams use this skill to analyze customer store distribution and existing warehouse resources, then produce warehouse-network recommendations, delivery-cycle guidance, and trunk-shipping plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided Excel files that may contain customer, store, address, or business-planning data. <br>
Mitigation: Use only approved input files, remove unnecessary sensitive fields where practical, and prefer copies of business-critical datasets. <br>
Risk: Warehouse recommendations may be inaccurate if built-in city coordinates, straight-line distance estimates, or logistics assumptions do not match real operations. <br>
Mitigation: Validate coordinates, warehouse constraints, route distances, and service-level assumptions against operational data before relying on recommendations. <br>
Risk: Outputs can be incomplete or misleading when required constraints such as warehouse limits, coverage targets, time requirements, required warehouses, or excluded warehouses are missing. <br>
Mitigation: Confirm planning constraints before analysis and review generated plans with logistics stakeholders before implementation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance, Python command output, and Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided .xlsx store data and can produce an analysis workbook with distribution statistics, warehouse assignments, delivery-cycle recommendations, shipping plans, and path-planning sheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
