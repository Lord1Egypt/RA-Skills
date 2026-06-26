## Description: <br>
Analyze URLs, YouTube videos, tweets, or text for quality, bias, and reliability using the Vajra API (vajra.to). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minhyeong112](https://clawhub.ai/user/minhyeong112) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users, developers, and analysts use this skill to submit public URLs, videos, social posts, or text to Vajra for quality, bias, reliability, key-takeaway, warning, and report-link analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs or text are sent to Vajra for analysis. <br>
Mitigation: Submit only content approved for external processing, and avoid private, proprietary, or personally identifying material. <br>
Risk: Analysis output may be cached server-side and exposed through a public permalink. <br>
Mitigation: Treat generated reports as public, review output before sharing, and avoid using the skill for sensitive material. <br>
Risk: The skill requires a Vajra API key. <br>
Mitigation: Store the key only in the VAJRA_API_KEY environment variable and avoid pasting credentials into prompts or shared logs. <br>


## Reference(s): <br>
- [Vajra Skill Page](https://clawhub.ai/minhyeong112/vajra) <br>
- [Vajra](https://www.vajra.to) <br>
- [Vajra Dashboard](https://www.vajra.to/dashboard) <br>
- [Vajra Analyze API](https://www.vajra.to/api/analyze) <br>
- [Humanity Labs](https://humanitylabs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON fields and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns quality score, bias level, verdict, key takeaways, warnings, and a public report permalink when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
