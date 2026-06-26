## Description: <br>
Bidirectional sync with reMarkable tablet via Cloud API (rmapi). Fetch handwritten notes/sketches, process with AI, and push content back. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolmanns](https://clawhub.ai/user/coolmanns) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to move handwritten notes, sketches, PDFs, and generated images between a reMarkable tablet and local AI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External tools and Python packages used for sync and conversion can access local files and reMarkable cloud content. <br>
Mitigation: Install only trusted rmapi and package versions, prefer pinned releases with verified checksums, and run the workflow on a trusted machine. <br>
Risk: The rmapi authentication token stored in ~/.rmapi can grant access to tablet content. <br>
Mitigation: Treat ~/.rmapi as sensitive credential material, restrict local access, and re-authenticate only on trusted systems. <br>
Risk: Bulk sync or AI processing can expose private notes, journals, sketches, or documents. <br>
Mitigation: Use a dedicated sync folder, tag, or starred-item workflow, review bulk upload and download targets, and process private content only when explicitly intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/coolmanns/remarkable-sync) <br>
- [rmapi releases](https://github.com/ddvk/rmapi/releases) <br>
- [reMarkable desktop connection](https://my.remarkable.com/connect/desktop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers rmapi setup, authentication, tablet fetch and upload commands, and file conversion workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
