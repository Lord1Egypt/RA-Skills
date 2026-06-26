## Description: <br>
Identifies plant growth stages from plant media and returns structured reports for precision agriculture decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agricultural producers, greenhouse operators, researchers, and smart-farming developers use this skill to analyze plant images or videos, classify growth stages, and retrieve account-linked report history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant media, media URLs, and supplied username/phone/open-id values are sent to the publisher's cloud service. <br>
Mitigation: Use only with user consent, avoid sensitive media, and review the publisher's authentication, retention, and data handling terms before deployment. <br>
Risk: Report history is account-linked and authentication tokens may be handled or persisted locally. <br>
Mitigation: Run the skill in a controlled environment, restrict account privileges, protect local runtime storage, and clear stored tokens when the skill is no longer needed. <br>
Risk: The scanner summary reports mismatched human-health or face-analysis artifacts in a plant-analysis release. <br>
Mitigation: Review the installed artifact before use and prefer an updated version that removes stale references and clearly documents the plant-analysis workflow. <br>
Risk: The scanner guidance flags the `yaml` dependency for review or correction. <br>
Mitigation: Verify dependencies during installation and replace or pin the YAML parser dependency to a valid, trusted package before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-plant-growth-stage-recognition-analysis) <br>
- [API interface documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Network video recognition demo](https://www.coze.cn/s/EGesE1qiHM8/) <br>
- [Uploaded video recognition demo](https://www.coze.cn/s/CiyhsWLkihc/) <br>
- [Historical report demo](https://www.coze.cn/s/MJ-xy1q_M7w/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON-like structured text, with optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report export links and history tables; can write output to a file when --output is provided.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
