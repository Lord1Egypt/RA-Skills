## Description: <br>
Accurately identifies cat and dog breeds and supports distinguishing between different individuals in multi-pet households; an essential assistant for intelligent pet butlers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit pet images or videos for cat and dog breed recognition, individual pet distinction, and retrieval of prior pet analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet images or videos and a username or phone-based open-id are sent to remote LifeEmergence/Open API services for analysis. <br>
Mitigation: Use the skill only when the user is comfortable sending that media and identifier to the remote service, and avoid submitting sensitive or unrelated media. <br>
Risk: History lookup accesses cloud account report data tied to the provided open-id. <br>
Mitigation: Treat history-list requests as account data access and confirm the open-id with the user before querying prior reports. <br>
Risk: The security evidence notes that the skill may create or log into an account and store returned tokens locally in the workspace data area. <br>
Mitigation: Run the skill in a trusted workspace, restrict workspace access, and remove local token/account data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-pet-breed-individual-recognition-analysis) <br>
- [Pet Breed Individual Recognition API Documentation](artifact/references/api_doc.md) <br>
- [Common Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report text, JSON-style structured results, history report tables, and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis requires a user-provided open-id and a local media path or public media URL; results can be printed or written to an output file.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
