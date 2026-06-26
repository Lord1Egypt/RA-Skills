## Description: <br>
Automatically extracts and displays titles, descriptions, and favicons for shared HTTP/HTTPS URLs so users can preview webpage content without visiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingfish1949101-wq](https://clawhub.ai/user/kingfish1949101-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill to preview public HTTP/HTTPS links by seeing a page title, short description, favicon, and domain before deciding whether to visit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generating a preview sends a live request for the URL and may reveal timing, interest, or network metadata. <br>
Mitigation: Use the skill only for public links and avoid previewing private, internal, or sensitive URLs. <br>
Risk: Preview text can be incomplete or misleading because it depends on the fetched page metadata and short extracted content. <br>
Mitigation: Treat the preview as a quick triage aid and verify important information by reviewing the source page directly. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown preview with a title link, short description, and site domain or favicon.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Only public HTTP/HTTPS URLs are supported; descriptions are limited to about 200 characters and preview extraction should not exceed 5 URLs per minute.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
