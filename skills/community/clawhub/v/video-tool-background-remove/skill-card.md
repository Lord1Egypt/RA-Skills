## Description: <br>
Remove or replace a video background with a solid color via WeryAI for an existing public HTTPS video URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to validate, submit, and poll a WeryAI background-removal job for an existing public HTTPS video, optionally choosing a flat background color. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan reports a suspicious verdict for the release context because a review helper can run tests, inspect repository diffs, and share diffs with fallback reviewer tools. <br>
Mitigation: Install only after review; avoid full-access review mode and disable automatic fallback reviewers when working with private code or secrets. <br>
Risk: Paid WeryAI processing is not idempotent, so repeated submit or wait calls may consume credits. <br>
Mitigation: Use dry-run first and require explicit user confirmation for the video URL and any non-default background color before submitting. <br>
Risk: The workflow requires WERYAI_API_KEY and sends a public HTTPS video URL to WeryAI. <br>
Mitigation: Keep the API key only in the runtime environment, never write it to files, and use only public HTTPS media URLs intended for this external processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-background-remove) <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown instructions with shell commands and JSON CLI responses; completed videos are shared as Markdown links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access to WeryAI, and a public https:// video_url; paid submit and wait calls require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
