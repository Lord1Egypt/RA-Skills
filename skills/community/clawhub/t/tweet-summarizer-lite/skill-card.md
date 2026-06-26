## Description: <br>
Fetch and summarize single tweets from Twitter/X. Basic search and single tweet fetching. Lightweight version perfect for quick tweet lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FranciscoBuiltDat](https://clawhub.ai/user/FranciscoBuiltDat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill through an agent to fetch, save, summarize, and search individual Twitter/X posts from URLs or saved local tweet data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Twitter/X session cookies through AUTH_TOKEN and CT0, which are sensitive account credentials. <br>
Mitigation: Use only an account whose session cookies are acceptable to expose to the skill and bird CLI; keep credentials in environment variables and rotate them if exposure is suspected. <br>
Risk: Fetched tweets are stored locally under tweets-lite, and saved content may reveal private research, protected-account content, or sensitive interests. <br>
Mitigation: Review or delete the local workspace data when saved tweets contain sensitive content, and do not share stored tweet files without checking them first. <br>
Risk: The declared storage permission names a tweets directory while the scripts store data under tweets-lite. <br>
Mitigation: Review local data paths before installation and cleanup so storage expectations match the files the skill actually writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FranciscoBuiltDat/tweet-summarizer-lite) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/FranciscoBuiltDat) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text responses with inline shell commands and local file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch tweet text through the bird CLI, summarize text, and write or search locally stored tweet records.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; package.json lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
