## Description: <br>
Analyzes fixed-camera reptile feeding videos to identify prey attack, swallowing, feeding refusal, vomiting or regurgitation, unreliable footage, and alert-level guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External reptile keepers, vivarium operators, and developers use this skill to analyze feeding-session video or video URLs and produce behavior records, refusal or vomiting alerts, recommendations, and report links. The skill is intended to support monitoring and escalation to a reptile veterinarian, not to diagnose disease or prescribe treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reptile videos or video URLs are sent to a vendor cloud service for analysis. <br>
Mitigation: Use the skill only for media that is appropriate to share with the vendor cloud and confirm cloud processing is acceptable for the deployment. <br>
Risk: The skill automatically creates or reuses an account-linked identity and may keep authentication or profile data locally. <br>
Mitigation: Run it in an environment where local data can be inspected and deleted, and use cloud-history access only when explicitly intended. <br>
Risk: Behavior analysis may be mistaken for medical diagnosis or treatment advice. <br>
Mitigation: Treat outputs as visual behavior records and escalation guidance only; use a professional reptile veterinarian for diagnosis, medication, dosing, force-feeding, or treatment decisions. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown or JSON structured analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include event fields, alert levels, recommendations, report links, and saved output files when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
