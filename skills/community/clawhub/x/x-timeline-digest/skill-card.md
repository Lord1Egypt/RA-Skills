## Description: <br>
Build a deduplicated digest from X (Twitter) For You and Following timelines using bird, then output a payload for upstream delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seandong](https://clawhub.ai/user/seandong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to collect recent X timeline items through an authenticated local bird session, filter duplicates and low-signal posts, and prepare a digest payload for later summarization or delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads authenticated X timelines through the local bird CLI and stores digest history on disk. <br>
Mitigation: Install only with a trusted bird binary and an intended authenticated X session; review any upstream delivery workflow and delete ~/.openclaw/state/x-timeline-digest.json to reset stored digest history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seandong/x-timeline-digest) <br>
- [Publisher profile](https://clawhub.ai/user/seandong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON payload plus optional Markdown digest prompt and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The payload includes a time window, fetch and filtering counts, digest text, ranked tweet items, sources, scores, and X status URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
