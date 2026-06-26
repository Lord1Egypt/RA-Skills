## Description: <br>
Offline-first workflow for extracting Chinese web page video or audio, transcribing it locally with SenseVoice, and exporting TXT or DOCX deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to turn authorized Chinese web page video, direct media URLs, or local media files into raw transcripts, refined text, and Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow downloads user-supplied or page-discovered media and model files, then writes transcripts and manifests to disk. <br>
Mitigation: Use only public or authorized media, choose an appropriate local output directory, and review generated transcripts before sharing. <br>
Risk: Manual header support could expose sensitive Cookie or Authorization values if a user supplies them. <br>
Mitigation: Avoid authenticated or private pages and do not pass Cookie, Authorization, access-token, or account credential headers. <br>
Risk: Browser-based extraction may fail for DRM, login-gated, geo-restricted, or unsupported playback flows. <br>
Mitigation: Stop at the supported boundary, do not attempt bypasses, and continue only with a direct media URL the user is authorized to use. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Cleanup Guidelines](references/cleanup-guidelines.md) <br>
- [Publishing](references/publishing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated outputs may include TXT transcripts, DOCX documents, JSON media manifests, and downloaded media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps raw transcripts separate from refined reading copies when refinement is requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter metadata says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
