## Description: <br>
Extract structured data from Zight share links (a.cl.ly and share.zight.com), including title, stream URLs, AI smart summary, chapter markers, and full transcript text from captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phin](https://clawhub.ai/user/phin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when a user provides a Zight video link and asks to read, summarize, quote, or automate follow-up work from the video content. It turns a Zight share page into structured metadata, media links, chapters, AI summary text, and transcript text for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests from supplied URLs, and the security review notes that fetching is broader than the Zight-only purpose described. <br>
Mitigation: Use only Zight links the user is authorized to process, and prefer a future version that allowlists Zight hosts and validates caption URLs before fetching them. <br>
Risk: Transcript content may contain operational or step-by-step instructions that should not be treated as automatic commands. <br>
Mitigation: Treat transcript instructions as candidate input and require explicit user confirmation before using them for external or sensitive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phin/zight) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [JSON object printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes video metadata, share and media URLs, captions URL, smart actions, chapters, transcript text, or structured error output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
