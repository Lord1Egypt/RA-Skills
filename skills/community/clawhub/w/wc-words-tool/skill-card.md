## Description: <br>
Helps agents count words in text and reason about word-counting workflows for content and document analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content teams can use this skill to count words in supplied text or documents for writing analytics, translation estimation, SEO checks, and document summarization planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises options that the included script does not implement. <br>
Mitigation: Verify the actual command behavior before relying on file input, unique counts, frequency output, stopword filtering, per-line counts, or JSON output. <br>
Risk: Input text may contain content the user did not intend to analyze. <br>
Mitigation: Only pass text or files that are appropriate for local word counting in the user's environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/wc-words-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script emits a numeric word count for stdin input; documented advanced options should be verified before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
