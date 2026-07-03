## Description: <br>
Analyzes reptile enclosure images or video frames to identify urate size, color, and texture alongside feces morphology, then returns a structured visual health assessment with alerts and recommended next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External reptile keepers, breeding facilities, and app developers use this skill to analyze enclosure images or video frames before cleaning, classify urate and feces signals, and generate structured reports, alerts, and non-diagnostic care prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reptile enclosure images, videos, submitted media URLs, reports, and an internal identity are handled by the publisher's cloud service. <br>
Mitigation: Install only when this cloud handling is acceptable, avoid private or third-party media without permission, and review the publisher's retention and deletion practices. <br>
Risk: The skill creates or reuses an internal account identity and may rely on locally stored service tokens. <br>
Mitigation: Run it in an environment where local token storage is acceptable and restrict access to the workspace and generated reports. <br>
Risk: Visual excrement assessment can be mistaken for a veterinary diagnosis or prescription guidance. <br>
Mitigation: Treat outputs as visual screening only; avoid medication names, dosages, or medical procedures, and contact a reptile veterinarian for abnormal or urgent findings. <br>
Risk: Poor image quality or missing species, feeding, brumation, gravid, substrate, or size-reference context can produce unreliable classifications. <br>
Mitigation: Require clear pre-cleaning images or frames and mark results unreliable when quality or required context is insufficient. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-reptile-excrement-analysis-analysis) <br>
- [API Reference](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON report with structured reptile excrement observations, alert level, recommended actions, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include urate and feces classifications, image-quality status, context exclusions, history report tables, and cloud report links.] <br>

## Skill Version(s): <br>
1.0.3 (source: skill frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
