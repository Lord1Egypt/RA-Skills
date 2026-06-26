## Description: <br>
TrendProof queries trendproof.dev to score keyword trend velocity and return direction, volume, CPC, peak timing, action hints, batch rankings, and related keyword suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akvise](https://clawhub.ai/user/akvise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and content teams use this skill to check whether keywords or niches are rising, stable, or falling before planning content, ads, or product work. Agents can analyze a single keyword, compare batches, or request related keyword ideas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if pasted into chat or stored in the local plaintext configuration file. <br>
Mitigation: Prefer TRENDPROOF_API_KEY through an environment variable or secret manager, avoid sharing keys in chat, and rotate any key that may have been exposed. <br>
Risk: Keyword queries and batch-file contents are sent to trendproof.dev for analysis. <br>
Mitigation: Review keywords for sensitive terms before use and keep batch files limited to the terms intended for the service. <br>


## Reference(s): <br>
- [TrendProof service](https://trendproof.dev) <br>
- [TrendProof API analyze endpoint](https://trendproof.dev/api/analyze) <br>
- [TrendProof API related endpoint](https://trendproof.dev/api/related) <br>
- [ClawHub TrendProof listing](https://clawhub.ai/akvise/trendproof) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/akvise) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-formatted summaries, terminal tables, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call trendproof.dev with user-provided keywords and optional location or language parameters.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
