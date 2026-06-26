## Description: <br>
Fetch, summarize, and save YouTube transcripts with timestamp navigation, chapter detection, and searchable content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, researchers, students, and content creators use this skill to extract readable YouTube transcripts, find timestamped moments, summarize videos, and export transcript content for notes or downstream work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches YouTube transcript and metadata content and may save transcripts or preferences locally. <br>
Mitigation: Use it for videos the user is allowed to access, ask before caching, disclose saved file locations, and delete saved data when requested. <br>
Risk: Using browser cookies or private video access can expose account-scoped data to local tooling. <br>
Mitigation: Avoid cookies or private-video workflows unless the user explicitly authorizes them, and review any dependency installation prompt before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/youtube-video-transcript) <br>
- [Skill homepage](https://clawic.com/skills/youtube-video-transcript) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with timestamped transcript text, deep links, shell commands, and optional local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can export transcripts as Markdown, SRT, plain text, or JSON; cached transcripts are stored locally only with user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
