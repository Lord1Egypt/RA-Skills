## Description: <br>
Identify a track from a SoundCloud Live set screenshot and find its Apple Music and Spotify links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjanssen19](https://clawhub.ai/user/mjanssen19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to identify songs playing at a specific timestamp in a SoundCloud live set, DJ mix, or radio show screenshot and retrieve Apple Music and Spotify links for the matched track. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may include information extracted from screenshots, such as set names, timestamps, artists, or track titles. <br>
Mitigation: Avoid using screenshots that contain private information the user does not want included in public search engine or music service queries. <br>
Risk: Track matching can be uncertain near transitions or when tracklists lack exact cue times. <br>
Mitigation: State uncertainty, mention both tracks when a timestamp is within about five seconds of a transition, and ask the user how to proceed when evidence is incomplete. <br>


## Reference(s): <br>
- [iTunes Search API](https://itunes.apple.com/search?term={artist}+{track name}&entity=song&limit=5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text with set name, timestamp, track, artist, Apple Music link, Spotify link, and uncertainty notes when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for clarification when the screenshot does not clearly show the set name or timestamp.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
