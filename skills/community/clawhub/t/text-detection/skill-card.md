## Description: <br>
Analyzes text using NLP, GPT pattern detection, regex matching, classification, hashing, sentiment analysis, and fact-checking options to help identify AI-generated content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content integrity teams use this skill as guidance for assembling text-analysis stacks that detect likely AI-generated content, tune accuracy and speed, and troubleshoot false positives or slow analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Referenced npm packages and integrations may be untrusted or change over time. <br>
Mitigation: Verify package publishers before installation and pin trusted package versions before use. <br>
Risk: Caching or fact-checking APIs may store or send private, proprietary, or regulated text to third-party services. <br>
Mitigation: Do not enable result caching or external fact-checking for sensitive text unless storage and data-sharing behavior is understood and approved. <br>
Risk: AI-text detection can produce false positives or miss generated text when thresholds and methods are poorly matched to the content. <br>
Mitigation: Use multiple detection methods, calibrate confidence thresholds on known human and AI text, and review results before taking enforcement action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/text-detection) <br>
- [Source skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples reference optional npm packages, configurable thresholds, caching, and third-party fact-checking integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
