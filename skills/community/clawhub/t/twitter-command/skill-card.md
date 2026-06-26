## Description: <br>
Use twitter-cli for Twitter/X operations including reading tweets, posting, replying, quoting, liking, retweeting, following, searching, and user lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingtimes](https://clawhub.ai/user/flyingtimes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to operate Twitter/X from a terminal, including timeline reading, search, account lookup, and account-changing actions such as posts, likes, retweets, bookmarks, and follows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access highly sensitive Twitter/X session cookies. <br>
Mitigation: Use a dedicated browser profile or throwaway account, avoid pasting full Cookie headers into chat or public issues, and treat cookie values as secrets. <br>
Risk: The skill can perform account-changing actions such as posting, liking, retweeting, following, bookmarking, and deleting content. <br>
Mitigation: Review every write action before allowing it and avoid accounts where unintended activity would create serious impact. <br>
Risk: Artifact metadata and server release evidence disagree on license and version. <br>
Mitigation: Confirm release terms and intended version before publication; this context uses server release evidence for the public release card. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flyingtimes/twitter-command) <br>
- [Publisher Profile](https://clawhub.ai/user/flyingtimes) <br>
- [Structured Output Schema](SCHEMA.md) <br>
- [PyPI Project](https://pypi.org/project/twitter-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, YAML] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI results may be rich text, compact text, JSON, or YAML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured CLI output uses an ok/schema_version/data envelope for success and ok/schema_version/error for errors.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
