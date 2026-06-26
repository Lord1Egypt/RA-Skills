## Description: <br>
Checks whether delayed Power BI data appears complete by comparing a late-night baseline with a morning value before reports are sent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirowangl-ops](https://clawhub.ai/user/mirowangl-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and reporting teams use this skill to decide whether delayed T+1 data has finished backfilling before sending scheduled reports. It guides users to compare a sentinel metric across two time points and escalate when values are unchanged or below the expected range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business metrics used for completeness checks may be sensitive if the workflow is later automated against Power BI or databases. <br>
Mitigation: Use minimal-scope credentials and approved storage and access controls before automating metric retrieval. <br>
Risk: Experience-based sentinel thresholds can become stale and may misclassify data completeness. <br>
Mitigation: Review sentinel metrics and threshold ranges periodically, and confirm with the data owner before sending reports when values are unchanged or below range. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirowangl-ops/xiaozhua-data-completeness-check) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
