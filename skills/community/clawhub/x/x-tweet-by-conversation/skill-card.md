## Description: <br>
Collects visible tweets from an X (Twitter) conversation thread by conversation id and returns normalized tweet, author, engagement, media, reply mapping, and pagination data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to collect visible replies and sub-replies from an X conversation for thread export, sentiment analysis, Q&A capture, or controversy mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in X browser session to inspect TweetDetail network responses, which may include sensitive or private account-visible content. <br>
Mitigation: Run it only in an intended browser session, review outputs before sharing them, and avoid broad batch use on sensitive accounts unless that matches the user's intent. <br>
Risk: Quote tweets are not collected by this conversation workflow even if the skill text suggests quote-chain coverage. <br>
Mitigation: Treat output as visible conversation replies and sub-replies; use a separate quote-search workflow when quote tweets are required. <br>
Risk: Temporary raw network response files may be saved locally during collection. <br>
Mitigation: Store them in a controlled temporary directory and delete raw captures after extracting the normalized tweet data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/x-tweet-by-conversation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON tweet data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's logged-in X browser session and local parsing scripts; outputs normalized tweet objects with pagination cursors.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
