## Description: <br>
Using a fixed camera, this skill analyzes video of an elderly person's cup area to count cup pickup events, compare them with thresholds or baselines, and return a dehydration-risk report for caregivers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, family members, and elder-care operators use this skill to review fixed-camera household or care-facility video, estimate daily water-cup pickup frequency, and receive a directional dehydration-risk alert. It supports care follow-up and report lookup, but its output is not a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes private in-home or care-facility video and drinking-frequency reports through a third-party cloud service. <br>
Mitigation: Install and use it only with informed consent from the monitored person or lawful caregiver, and avoid submitting footage unless household video sharing with the listed service is acceptable. <br>
Risk: The skill may create or reuse an internal identity and store account tokens locally. <br>
Mitigation: Use it in a dedicated workspace, restrict access to local data and token files, and avoid shared environments where reports or identities could be mixed across users. <br>
Risk: Cup pickup counts are only an indirect proxy for hydration and may be affected by camera framing, other people, empty cups, or missed gestures. <br>
Mitigation: Treat outputs as caregiver prompts rather than medical conclusions, confirm concerns through direct observation, and seek clinical advice when low intake or symptoms persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-elderly-drinking-frequency-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [Analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown or JSON structured report with drinking-frequency metrics, risk level, caregiver-facing recommendations, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the generated report to a user-specified local output file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
