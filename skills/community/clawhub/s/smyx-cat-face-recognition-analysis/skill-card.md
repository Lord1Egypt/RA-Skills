## Description: <br>
Identifies specific cats by comparing cat images or videos against a registered cat-face database, supporting individual recognition in multi-cat households. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit cat images, videos, or media URLs for cat-face recognition and to retrieve prior cat-recognition reports. It is suited to multi-cat household workflows such as pet monitoring, feeder identity checks, activity logging, and lost-pet review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cat images, videos, or media URLs are sent to the LifeEmergence/SMYX cloud service for recognition. <br>
Mitigation: Use only media the user is comfortable sending to that provider, and avoid sensitive household footage unless the provider's retention and account model are acceptable. <br>
Risk: The skill can silently create or reuse a local identity and store service tokens in workspace-local state. <br>
Mitigation: Run it in a controlled workspace, limit workspace sharing, and clear local identity or token state when the workflow no longer needs it. <br>
Risk: Recognition quality depends on the submitted media and may be unreliable when faces are obstructed, poorly lit, blurred, or not registered in the database. <br>
Mitigation: Use clear frontal cat-face media with sufficient lighting and verify important identity matches against the registered cat database or source media. <br>


## Reference(s): <br>
- [Cat Face Recognition API Documentation](references/api_doc.md) <br>
- [Common AI Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text containing recognition results, report-list entries, report links, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an output file when the caller provides an output path; cloud API calls may return structured report data and export links.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
