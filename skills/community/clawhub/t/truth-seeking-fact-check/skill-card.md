## Description: <br>
Truth Seeking Fact Check checks text for possible hallucinations or misinformation, assigns credibility and confidence scores, flags problematic sentences, and supports batch checks, configurable scoring weights, optional timed rechecks, advisory blockchain-hash checks, and configured external search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangtaozhanshen](https://clawhub.ai/user/tangtaozhanshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users can use this skill to review claims in supplied text, receive a credibility score with confidence information, and identify statements that may need additional verification. It is suited for fact-checking drafts, summaries, and recurring monitored text where advisory results are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privacy claims may be overstated because configured external datasources can send checked text to Brave Search. <br>
Mitigation: Disable external datasources or avoid submitting sensitive and confidential text unless sharing the query text with the configured provider is acceptable. <br>
Risk: Verification and blockchain results are advisory and may not prove that content is authentic or accurate. <br>
Mitigation: Treat scores, confidence values, and blockchain checks as signals for review, and cross-check important claims with authoritative sources. <br>
Risk: Timed checks keep text available for background rechecking when the scheduler is enabled. <br>
Mitigation: Enable timed checks only for text that is appropriate to retain and reprocess in the running agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangtaozhanshen/truth-seeking-fact-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON objects or Markdown summaries with credibility scores, meta-confidence, flagged sentences, suggestions, and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-text and batch results; timed checks can report score changes when enabled.] <br>

## Skill Version(s): <br>
1.5.0 (source: evidence.json release, CHANGELOG.md, manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
