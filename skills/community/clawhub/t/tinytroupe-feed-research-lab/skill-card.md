## Description: <br>
Run bounded synthetic audience research for draft posts and X-style feed experiments inspired by TinyTroupe and public xai-org/x-algorithm architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and research teams use this skill to compare draft posts with synthetic audience personas, identify likely objections, and generate bounded rewrite guidance before real posting or user research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may overread synthetic persona reactions as predictions of X reach, ranking, virality, revenue, or account status. <br>
Mitigation: Keep the required boundary statement with user-facing reports and treat outputs as qualitative hypotheses for real posting or user research. <br>
Risk: Draft content and generated reports are written to local files and may contain sensitive unpublished messaging. <br>
Mitigation: Use a private output directory, review generated files before sharing them, and avoid supplying confidential drafts unless the local environment is appropriate. <br>


## Reference(s): <br>
- [Research Boundaries](references/research-boundaries.md) <br>
- [Project homepage](https://github.com/zack-dev-cm/open-feed-recsys-lab) <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/tinytroupe-feed-research-lab) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, CSV, Files, Guidance] <br>
**Output Format:** [Local report files including Markdown, JSON, CSV, and SVG outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Python script on user-provided draft content and writes reports to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
