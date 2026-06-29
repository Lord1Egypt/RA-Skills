## Description: <br>
Analyzes pet side-view walking videos or URLs to produce vision-based gait findings such as stride, stance and swing timing, symmetry indicators, lameness signals, mobility limits, and report links without providing a veterinary diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners, veterinary staff, and rehabilitation teams can use this skill to screen gait videos for lameness, arthritis-related mobility concerns, post-operative recovery tracking, and historical report review. Results are intended as vision-based screening support, not a substitute for veterinary examination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos, media URLs, and report-history requests are sent to the publisher's cloud service. <br>
Mitigation: Use only with media approved for external processing and confirm the publisher's service terms before deployment. <br>
Risk: The skill may silently create or reuse a local identity and store service tokens locally. <br>
Mitigation: Run only in trusted environments, review local state handling, and clear local credentials when decommissioning the skill. <br>
Risk: Gait findings are screening information and may be incorrect or incomplete. <br>
Mitigation: Do not rely on the output as a veterinary diagnosis; escalate concerning results to a qualified veterinarian. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-gait-analysis-lameness-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Shared API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON-style structured analysis results, report links, and command-line invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media files or public media URLs and can query cloud-hosted historical reports associated with the local identity.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
