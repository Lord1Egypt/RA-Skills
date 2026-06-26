## Description: <br>
Analyzes fixed-camera aquarium or aquaculture video to track individual fish positions, estimate school centroids, measure body-length-normalized distance from the school, and report prolonged isolation behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarists, aquarium operators, aquaculture staff, and smart-camera developers use this skill to review fixed-camera fish video for prolonged isolation or abnormal schooling patterns and to generate alerts, reports, and suggested inspection actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud analysis can expose aquarium video, report history, and an open-id or phone-like identifier to the publisher's backend. <br>
Mitigation: Install only when the publisher and backend are trusted, obtain clear consent before uploading files or submitting video URLs, and avoid using sensitive personal identifiers when a less sensitive open-id is available. <br>
Risk: Under-documented token handling, broad remote API helpers, arbitrary video URL forwarding, and a mismatched human-health API reference increase review burden before deployment. <br>
Mitigation: Review the code and configuration before installation; prefer a release that documents account and token storage, removes unrelated health references and generic mutation helpers, and narrows remote API behavior. <br>
Risk: Poor camera coverage, occlusion, low tracking reliability, or missing species baselines can produce misleading isolation alerts. <br>
Mitigation: Require stable full-tank video coverage, species and body-length calibration, and ReID tracking reliability checks; return an unreliable signal rather than an alert when tracking quality is insufficient. <br>
Risk: Behavior alerts may be mistaken for disease diagnosis or treatment instructions. <br>
Mitigation: Present outputs as position-based behavior signals only, avoid disease diagnosis and medication guidance, and direct users to inspect water quality and consult a qualified aquarium professional when needed. <br>


## Reference(s): <br>
- [Fish Isolation API Documentation](artifact/references/api_doc.md) <br>
- [SMYX Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/smyx-fish-isolation-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis report with command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fish isolation metrics, alert levels, recommended inspection actions, disclaimers, and optional output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
