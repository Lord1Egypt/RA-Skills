## Description: <br>
Analyzes high-performing content from URLs and builds a swipe file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentchan](https://clawhub.ai/user/vincentchan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, marketers, and content strategists use this skill to fetch and deconstruct articles, tweets, videos, and similar content into reusable structural, psychological, and writing frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches URLs supplied by the user, including possible Twitter/X requests through FxTwitter. <br>
Mitigation: Review the source URLs before running the skill and only provide URLs the user is comfortable having fetched. <br>
Risk: The skill creates or updates files under swipe-file/, which could overwrite or mix with manually edited swipe-file content. <br>
Mitigation: Review existing swipe-file content before execution and keep a backup when manual edits need to be preserved. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text] <br>
**Output Format:** [Markdown swipe-file analyses, JSON processing registry entries, and a concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates files under swipe-file/ and reports processed URLs, titles, failures, and the updated swipe file location.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
