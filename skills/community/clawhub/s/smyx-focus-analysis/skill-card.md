## Description: <br>
Analyzes video for gaze direction and facial pose to estimate focus, distraction, or mind-wandering in classroom, office, or driving scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run cloud-backed focus analysis on video files or public video URLs, then review structured attention scores, distraction statistics, trend details, and report links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos and report queries are sent to the provider's cloud service. <br>
Mitigation: Use only with footage you are authorized to upload, and avoid sensitive classroom, workplace, driving, or biometric videos unless consent, retention, and account-linking behavior are understood. <br>
Risk: A persistent workspace identity may be silently created or reused, with tokens stored locally. <br>
Mitigation: Review local storage and account-linking behavior before deployment, restrict workspace access, and remove stored credentials or tokens when the skill is decommissioned. <br>
Risk: Focus scores and attention classifications may be incomplete or context-dependent. <br>
Mitigation: Treat outputs as decision support and keep human review in place before using results for safety, classroom, employment, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/18072937735/skills/smyx-focus-analysis) <br>
- [API Documentation](artifact/references/api_doc.md) <br>
- [Shared API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report; optional saved text or JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return historical report lists with report links; supports local video files or public video URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub server release evidence; artifact frontmatter reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
