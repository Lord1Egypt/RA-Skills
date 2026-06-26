## Description: <br>
Read and summarize X/Twitter links with low-token routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuolicong](https://clawhub.ai/user/zuolicong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to read, summarize, and inspect X/Twitter tweets, explicit threads, t.co links, and X article pages without requiring official X API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local X auth_token and ct0 cookies, which can expose or reuse an authenticated X session. <br>
Mitigation: Use a secondary X account, keep ~/.config/xreader/session.json private, and delete that file when the skill should no longer reuse the account session. <br>
Risk: Article extraction uses browser automation and may return partial or noisy content for some X article pages. <br>
Mitigation: Check warnings and fallback fields in the structured JSON before relying on article summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuolicong/xlink-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON with summarized text, metadata, warnings, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary mode truncates cleaned text for lower-token responses; full mode can include complete text or markdown when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
