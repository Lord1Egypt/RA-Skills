## Description:

Turn an already-written script into a video with voiceover, auto-cut stock visuals, and captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn a prepared script into a Revid video workflow with voiceover, stock visuals, captions, music, and rendering status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided script text and the Revid API key are sent to Revid's service for rendering.

Mitigation: Use only with scripts approved for third-party processing and avoid confidential, regulated, or proprietary content unless organizational policy permits it.

Risk: Long scripts may exceed practical rendering limits or need summarization.

Mitigation: Keep scripts within the documented practical limit or split them into smaller render jobs.

Risk: Generated stock visuals, captions, or voiceover may not match niche topics, brand pronunciations, or audio balance expectations.

Mitigation: Review rendered output before publication and adjust script wording, voice settings, media workflow, or music settings as needed.

## Reference(s):

- [Script to Video ClawHub Page](https://clawhub.ai/api00/skills/revid-script-to-video)
- [Revid Render API Endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid Status API Endpoint](https://www.revid.ai/api/public/v3/status?pid=$PID)
- [Example payload](artifact/examples/honey-script.json)
- [Example run script](artifact/examples/run.sh)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and sends user-provided script text to Revid for video rendering.]

## Skill Version(s):

1.4.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
