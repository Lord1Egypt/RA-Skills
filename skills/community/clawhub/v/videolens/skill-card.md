## Description: <br>
AI video reviews for creators and teams that return timestamped feedback from prompts for pacing, clarity, hook, retention, structure, proof, CTA, and publish-readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadoprizm](https://clawhub.ai/user/shadoprizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, teams, and agent developers use VideoLens.io to review videos with custom prompts and produce timestamped feedback, summaries, bug reports, and QA artifacts before publishing or handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OpenAI API key for local video analysis. <br>
Mitigation: Provide credentials only in trusted environments and use the preflight action to confirm key availability before analysis. <br>
Risk: Bootstrap and analysis clone and execute the external VideoLens CLI locally. <br>
Mitigation: Review the upstream repository and use the default OCC data paths, especially when processing sensitive videos. <br>
Risk: Analysis can spend model or API credits. <br>
Mitigation: The wrapper refuses analysis unless allow_credit_spend is explicitly set to true. <br>


## Reference(s): <br>
- [VideoLens.io](https://videolens.io) <br>
- [VideoLens source repository](https://github.com/shadoprizm/videolens) <br>
- [ClawHub release page](https://clawhub.ai/shadoprizm/videolens) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured JSON, status metadata, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis writes report.md and analysis.json under the OCC data directory for each run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
