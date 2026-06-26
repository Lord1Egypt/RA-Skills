## Description: <br>
Record video proof of implemented features after coding tasks complete, using Playwright walkthroughs to capture recordings, screenshots, console logs, and proof summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rikisann](https://clawhub.ai/user/rikisann) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and coding agents use this skill after implementation work to create a reproducible browser or API proof that demonstrates the changed feature and records reviewable artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated proof specs can execute broad start commands and make browser or API requests against configured targets. <br>
Mitigation: Review proof specs before execution and run them only in trusted repositories and non-production environments. <br>
Risk: Recorded videos, screenshots, logs, and API results can capture sensitive page content, credentials, or response data. <br>
Mitigation: Avoid secret-bearing or authenticated pages when possible, and inspect or redact proof-artifacts before committing or sharing them. <br>
Risk: Setup installs npm packages, Playwright browser dependencies, Chromium, and may attempt system package installation for ffmpeg. <br>
Mitigation: Run setup only on machines where those dependency and package-manager changes are acceptable. <br>


## Reference(s): <br>
- [Proof Spec Reference](artifact/references/proof-spec.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rikisann/video-proof-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown, Files] <br>
**Output Format:** [Markdown guidance with YAML proof specs and shell commands; generated proof artifacts may include WebM or MP4 video, PNG screenshots, console logs, Markdown summaries, and JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pass/fail proof summaries and exits nonzero when proof steps or API assertions fail.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
