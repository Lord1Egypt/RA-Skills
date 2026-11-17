## Description:

Extracts structured data from Zight share links, including video metadata, stream URLs, AI smart summary content, chapter markers, and transcript text from captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phin](https://clawhub.ai/user/phin)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to convert Zight video share links into machine-usable JSON for reading, summarization, quoting, media processing, and follow-up workflow planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to arbitrary user-provided URLs and caption links rather than enforcing only the documented Zight hosts.

Mitigation: Use only in environments where outbound HTTP requests are acceptable, and tighten deployment controls to allow only expected Zight HTTPS domains and trusted caption hosts before use in sensitive networks.

Risk: Fetched transcript text may contain operational or step-by-step instructions that should not automatically drive external or sensitive actions.

Mitigation: Treat transcript content as candidate input and require explicit user confirmation before using extracted instructions for follow-up actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phin/skills/zight)
- [Publisher profile](https://clawhub.ai/user/phin)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON object printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes video title, share URL, media URLs when exposed, captions URL, smart summary text, chapter metadata, and transcript text; errors are returned as JSON objects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
