## Description:

Analyzes acoustic features of livestock and poultry vocalizations to identify abnormal sounds such as coughing, wheezing, painful screams, and hoarse calls, then returns respiratory health risk hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as farm operators and livestock health teams use this skill to submit barn audio or audio-bearing video for non-contact screening of abnormal livestock and poultry vocalizations. It returns respiratory health risk hints and report links for follow-up review; it is not a veterinary diagnosis tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends supplied livestock audio/video files or media URLs to the LifeEmergence cloud service.

Mitigation: Use only recordings approved for external cloud processing, and review retention and deletion expectations before using sensitive farm media or media that may contain people.

Risk: The skill can silently create or reuse a cloud-linked identity and store returned authentication tokens plus report-history state in the workspace data directory.

Mitigation: Run it in a controlled workspace, protect the workspace data directory, and clear local state when account linkage or report history should not persist.

Risk: Respiratory health risk hints may be mistaken for formal diagnosis.

Mitigation: Treat results as screening signals and confirm health decisions with veterinary review and appropriate laboratory testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-vocalization-health-analysis-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)
- [smyx_analysis API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown text containing structured analysis results, respiratory risk levels, abnormal-event details, and report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save analysis output to a user-specified file; history queries return a structured report list.]

## Skill Version(s):

1.0.10 (source: ClawHub release evidence; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
