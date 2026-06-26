## Description: <br>
Automatically detects oversized tool results, writes them to compressed local files when they exceed a threshold, and returns file metadata to preserve the conversation context window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suda6632](https://clawhub.ai/user/suda6632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to prevent very large tool outputs from flooding the active conversation. It wraps Python tool results, spills large strings, dictionaries, or lists to local gzip files, and returns concise metadata with a preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Oversized tool outputs may contain secrets, private records, or regulated data that are written to local disk and exposed in previews. <br>
Mitigation: Use the skill only with appropriate local permissions, retention settings, and redaction practices; avoid sensitive data unless those controls are in place. <br>
Risk: Result files can accumulate on disk after repeated use. <br>
Mitigation: Run the cleanup function regularly and tune retention for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suda6632/tool-result-size-controller) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python API guidance and JSON-like result metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Oversized results are represented by local file path, character and byte size, content hash, and preview metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
