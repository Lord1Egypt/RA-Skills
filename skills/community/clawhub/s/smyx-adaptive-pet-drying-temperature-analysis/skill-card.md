## Description: <br>
Analyzes pet images or videos through server-side APIs to identify breed or body type and fur density, then returns a non-medical drying temperature and time curve for pet drying equipment or grooming workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process pet full-body images, videos, or media URLs and obtain structured breed or body-type recognition, fur-density estimates, and drying temperature/time recommendations. It is intended for pet drying boxes, grooming salons, and smart pet care devices, not for medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet media or media URLs are sent to remote services and cloud history may be queried. <br>
Mitigation: Use only media appropriate for the service, avoid sensitive household content, and confirm that the service's retention and access practices are acceptable before installation. <br>
Risk: The skill can silently create or reuse an internal identity, authenticate with a remote service, and store returned tokens locally. <br>
Mitigation: Review the account and credential flow before use, run the skill in an isolated environment, and manage or remove local token storage after testing when appropriate. <br>
Risk: Drying recommendations are care guidance rather than medical advice and may be unsuitable for vulnerable pets without review. <br>
Mitigation: Treat the generated temperature curve as a recommendation for human or device-side review, especially for young, elderly, or heat-sensitive pets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-adaptive-pet-drying-temperature-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Error Reference](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured report as Markdown or JSON, including drying temperature/time recommendations and report links when returned by the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud history report tables and supports basic, standard, and json detail modes.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
