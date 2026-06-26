## Description: <br>
Headless-detection-resistant browser automation in Docker for authorized QA, compatibility testing, and defensive security research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and defensive security testers use this skill to run authorized browser automation against owned or written-authorized targets where standard headless browsers trigger false-positive detection. It helps test anti-bot controls, compatibility behavior, and human-like interaction flows while preserving explicit authorization boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-power browser automation can be misused against unauthorized third-party services. <br>
Mitigation: Use only for owned systems or targets with written authorization, and avoid scraping, access-control evasion, account abuse, rate-limit abuse, or unauthorized CAPTCHA bypass. <br>
Risk: An exposed browser API or noVNC viewer can let others control the browser and any active sessions. <br>
Mitigation: Bind services to localhost, require a strong AUTH_TOKEN for any non-local deployment, avoid query-string tokens, and do not expose noVNC beyond localhost. <br>
Risk: Persistent profiles can retain live cookies, credentials, fingerprints, and other sensitive session data. <br>
Mitigation: Use isolated test accounts, treat profile volumes as secrets, avoid sharing them across environments, delete them after testing, and rotate exercised test credentials. <br>
Risk: Mutable container tags or unreviewed compose files can change deployed behavior. <br>
Mitigation: Pin reviewed Docker image digests, inspect compose files before use, and upgrade only after conscious review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/psyb0t/stealthy-auto-browse) <br>
- [Setup](references/setup.md) <br>
- [Project homepage](https://github.com/psyb0t/docker-stealthy-auto-browse) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser API requests, structured JSON responses, screenshots, page text, HTML, cookies, storage data, and script-mode result JSON when used against an authorized running service.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
