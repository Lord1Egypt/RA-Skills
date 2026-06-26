## Description: <br>
Render X (Twitter) posts, long articles, and mobile reading pages into mobile-style long screenshots and optional single-page PDFs using Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content archivists use this skill to generate phone-like dark-mode PNG captures and optional single-page PDFs for X posts, long articles, or mobile reading pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted output file paths may cause local code execution through the renderer's Python path handling. <br>
Mitigation: Use only simple, trusted output filenames inside a dedicated folder, and do not allow untrusted text to choose --out-png or --out-pdf values. <br>
Risk: X overlays or DOM changes may leave visual artifacts in very long captures. <br>
Mitigation: Re-run with longer waits or a larger top replacement height, and update overlay patterns or use segmented capture when X changes its page structure. <br>


## Reference(s): <br>
- [x-mobile-longshot notes](references/notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/spyfree/x-mobile-longshot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated PNG files and optional single-page PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Playwright mobile emulation with dark mode and configurable device, wait time, and top-region replacement settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
