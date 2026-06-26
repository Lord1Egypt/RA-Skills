## Description: <br>
Remove password protection from a PDF by uploading it with its current password to the Solutions API, polling until completion, then returning a download URL for the unlocked PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to remove known password protection from PDFs through the Cross-Service-Solutions API and receive a structured result with the unlocked file download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protected PDFs, their passwords, and unlocked outputs are sent to a third-party service. <br>
Mitigation: Use only for documents approved for Cross-Service-Solutions processing, and avoid sensitive, regulated, or confidential PDFs unless privacy, retention, deletion, and access-control practices have been separately approved. <br>
Risk: Unlocked PDF output is returned through a remote download URL. <br>
Mitigation: Share and store the download URL only in approved channels and delete or restrict access to downloaded files according to the user's document handling policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrossServiceSolutions/remove-password-from-pdf) <br>
- [Cross-Service-Solutions publisher profile](https://clawhub.ai/user/CrossServiceSolutions) <br>
- [Solutions API registration](https://login.cross-service-solutions.com/register) <br>
- [Solutions API remove-password endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions/api/33) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON result with job status, file name, and download URL; guidance may include shell commands for the bundled CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PDF file, its current password, and a Solutions API key; returns a remote download URL when processing completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
