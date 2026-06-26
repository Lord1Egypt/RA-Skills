## Description: <br>
Second Brain is a personal knowledge base powered by Ensue for capturing, organizing, retrieving, and extending durable knowledge from conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christinetyip](https://clawhub.ai/user/christinetyip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn conversations into an Ensue-backed knowledge base, including concepts, toolbox entries, patterns, references, and retrievable notes. It supports drafting, confirming, saving, searching, updating, and deleting knowledge entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Knowledge entries are stored in a cloud-backed Ensue service. <br>
Mitigation: Install only when cloud-backed persistent memory is intended, and avoid saving secrets, credentials, highly sensitive personal data, private paths, or system details. <br>
Risk: Incorrect or low-quality drafts could become durable knowledge if saved without review. <br>
Mitigation: Review every draft before saving and confirm that entries include context, examples, and the reason the knowledge matters. <br>
Risk: The skill requires an API key with access to the user's knowledge base. <br>
Mitigation: Use an ENSUE_API_KEY the user is comfortable granting to this skill and never log or display the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/christinetyip/second-brain) <br>
- [Ensue homepage](https://ensue-network.ai?utm_source=clawdbot&utm_medium=workflow) <br>
- [Ensue API endpoint](https://api.ensue-network.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON arguments for shell API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ENSUE_API_KEY and stores approved knowledge in the Ensue cloud service.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
