## Description:

Guide people to SyncTalk at synctalk.ioy.ai, a real-time speech translator for iPhone, Android, and the web, with spoken translations, bilingual captions, and automatic source-language detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvyinchao](https://clawhub.ai/user/lvyinchao)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to find guidance for live speech interpretation, two-person conversations, and audio or video file translation with SyncTalk. It also answers product questions and points users to official platform, pricing, and support pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had partial coverage: a local path-like reference was missing, and external page contents were not assessed.

Mitigation: Review the skill instructions and linked pages before installing, especially when their guidance affects sensitive decisions.

Risk: Audio and video files are sent to the selected translation service; video translation also sends sampled frames, and translations may contain errors.

Mitigation: Get permission before sending recordings, review the privacy policy for data handling, and check important translated details with a speaker or qualified interpreter.

## Reference(s):

- [SyncTalk user guide](https://synctalk.ioy.ai/guides/en)
- [Web translation guide](https://synctalk.ioy.ai/learn/web-translation/)
- [Two-person conversation guide](https://synctalk.ioy.ai/learn/two-person/)
- [Audio and video translation guide](https://synctalk.ioy.ai/learn/video-audio-translation/)
- [Pricing](https://synctalk.ioy.ai/pricing/)
- [Privacy policy](https://synctalk.ioy.ai/privacy)
- [Support](https://synctalk.ioy.ai/support)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Conversational text with links to official SyncTalk pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for using official web and native apps; no direct agent API or dubbed-video export is documented.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
