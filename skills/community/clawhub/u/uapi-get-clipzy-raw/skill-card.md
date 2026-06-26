## Description: <br>
Helps an agent use UAPI's GET /api/raw/{id} endpoint to retrieve decrypted Clipzy clipboard text when an ID and decryption key are provided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user explicitly needs the final plaintext from a Clipzy clipboard item through the UAPI raw-text endpoint. It guides parameter checks, key handling, endpoint selection, and response-code interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retrieval may send a Clipzy decryption key to the UAPI service and return plaintext content. <br>
Mitigation: Confirm each retrieval explicitly, treat Clipzy IDs, keys, and plaintext as sensitive, and avoid secrets or private content unless the user trusts the service. <br>
Risk: The skill is under-scoped for a sensitive decryption flow and may not warn enough about key handling. <br>
Mitigation: Before calling the endpoint, restate that the key is required for server-assisted decryption and proceed only after the user provides the intended ID and key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-clipzy-raw) <br>
- [Operation reference: get-clipzy-raw](references/operations/get-clipzy-raw.md) <br>
- [Quick start](references/quick-start.md) <br>
- [Clipzy 在线剪贴板 category reference](references/resources/Clipzy-在线剪贴板.md) <br>
- [UAPI service](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands] <br>
**Output Format:** [Markdown with endpoint details, parameters, and response-code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Clipzy item ID and Base64-encoded AES decryption key before retrieving plaintext.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
