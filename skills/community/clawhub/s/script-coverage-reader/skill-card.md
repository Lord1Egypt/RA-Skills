## Description: <br>
Evaluates feature screenplays or TV pilots and produces industry-standard coverage, including a logline, synopsis, character breakdown, craft grid, producibility notes, comps, and separate script and writer verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Script readers, development executives, producers, and contest readers use this skill to evaluate screenplay or TV pilot submissions and turn them into actionable development coverage. It supports intake, read-pass analysis, craft scoring, producibility review, comps, and separate script and writer verdicts. <br>

### Deployment Geography for Use: <br>
Global; defaults to US industry conventions unless the user names another market. <br>

## Known Risks and Mitigations: <br>
Risk: Submitted scripts can contain confidential writer, representation, project, or rights information. <br>
Mitigation: Keep outputs labeled for development team use only, do not disclose writer identity outside the team, avoid external services, and do not write submitted scripts to disk. <br>
Risk: Coverage can mislead a development team if plot beats, character actions, dialogue, or comparable titles are invented. <br>
Mitigation: Mark missing material as unknown, paraphrase source material, cap verbatim quotation, and use only real released comparable projects. <br>
Risk: The server security review recommends trusted-maintainer installation and least-privileged credentials for the broader release environment. <br>
Mitigation: Install only in a trusted ClawHub maintainer environment and keep GitHub, ClawHub, and Convex credentials least-privileged when related tooling is present. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/script-coverage-reader) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown coverage document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a development-team-use label, reader/date fields, fixed craft rating anchors, and separate script and writer verdicts.] <br>

## Skill Version(s): <br>
0.1.1 (source: evidence.release.version and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
