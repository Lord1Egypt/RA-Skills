## Description: <br>
Swap the face in an existing HTTPS video using a reference face image via WeryAI (video-face-change). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit and monitor WeryAI face-change jobs for existing public HTTPS videos when they have a separate public HTTPS reference face image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WERYAI_API_KEY for paid API calls. <br>
Mitigation: Install only from a trusted publisher, keep the key in the runtime environment, and run dry-run validation before submit or wait. <br>
Risk: Face-change workflows can process a person's likeness and source video. <br>
Mitigation: Confirm permission to use the face image and video, and verify the exact URLs with the user before submitting a job. <br>
Risk: The helper accepts only public HTTPS media URLs and does not upload local files. <br>
Mitigation: Use public HTTPS URLs only, avoid local file paths, and do not run unrelated sibling tools that have not been reviewed. <br>


## Reference(s): <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-face-change) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON CLI output from the WeryAI helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and public HTTPS video and image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
