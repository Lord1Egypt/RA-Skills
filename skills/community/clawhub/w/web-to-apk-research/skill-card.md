## Description:

Provides decision support and actionable workflows for converting web apps or websites into Android install experiences using PWA, Capacitor with CI, Trusted Web Activity, or WebView options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to choose and execute a practical path for turning a web app into an Android install experience, especially from Termux where native Android build tooling is unavailable locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Capacitor or TWA workflows may introduce normal JavaScript supply-chain risk through npm tooling and CI execution.

Mitigation: Pin dependencies, commit a lockfile, use npm ci, avoid dynamic npx downloads where possible, and run CI with minimal permissions and secrets.

Risk: Attempting native Android builds inside Termux can fail because Java, Gradle, Android SDK, and Rust tooling are unavailable or unsupported locally.

Mitigation: Use PWA/WebAPK for local-first installation or move native APK builds to a configured CI environment.

Risk: PWA installation, service workers, and Play Store-oriented TWA distribution can fail when HTTPS or Digital Asset Links requirements are skipped.

Mitigation: Deploy the web app over HTTPS before PWA installation and complete Digital Asset Links verification before promising Play Store distribution.

## Reference(s):

- [Web-to-APK Options Analysis](references/options-analysis.md)
- [ClawHub Skill Page](https://clawhub.ai/pmuhammadagus-byte/skills/web-to-apk-research)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
