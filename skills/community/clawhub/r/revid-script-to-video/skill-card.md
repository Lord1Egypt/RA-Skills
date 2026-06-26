## Description: <br>
Turn an already-written script into a video with voiceover, auto-cut stock visuals, and captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to turn a finished script into a Revid-generated video with voiceover, captions, stock visuals, music, and render polling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Script text and rendering options are sent to Revid for external video rendering. <br>
Mitigation: Do not submit secrets, confidential business material, personal data, or regulated content unless Revid's privacy and retention terms have been reviewed. <br>
Risk: The workflow requires a Revid API key. <br>
Mitigation: Store REVID_API_KEY securely and avoid exposing it in prompts, logs, examples, or shared shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-script-to-video) <br>
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Example video payload](examples/honey-script.json) <br>
- [Example run script](examples/run.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY and sends script text plus rendering options to Revid.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
