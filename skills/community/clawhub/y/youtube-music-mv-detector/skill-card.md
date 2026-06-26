## Description: <br>
Detect YouTube Music links as MV (music video) or song (audio). Use when user shares YouTube Music links (music.youtube.com/watch?v=...) and you need to classify them as MV or audio track. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicowu07](https://clawhub.ai/user/nicowu07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify user-provided YouTube Music or YouTube links as music videos or audio tracks by checking public oEmbed title and author metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided YouTube or YouTube Music links are sent to YouTube's oEmbed service to retrieve public metadata. <br>
Mitigation: Only use the skill with links that are acceptable to check against YouTube's service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicowu07/youtube-music-mv-detector) <br>
- [YouTube oEmbed endpoint](https://www.youtube.com/oembed?url={youtube_music_url}&format=json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown or concise text classification with title, author, and MV/song result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided YouTube or YouTube Music link and uses public oEmbed metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
