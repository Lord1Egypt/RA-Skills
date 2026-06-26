## Description: <br>
RateLint scans codebases for rate limiting and API throttling anti-patterns, including missing rate limits, brute force exposure, missing backoff strategies, unbounded queues, retry storm vulnerability, and flow control gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-minded engineering teams use RateLint to audit repositories for rate limiting, throttling, brute force, backoff, queue overflow, and abuse-prevention gaps before release or during CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans selected repository files and may report findings that affect local development or CI decisions. <br>
Mitigation: Run it only against intended files or repositories, review findings before acting on them, and treat regex-based results as guidance that may need human confirmation. <br>
Risk: Passing a paid-tier license key on the command line can expose it in shell history or process listings. <br>
Mitigation: Store the license key in RATELINT_LICENSE_KEY or OpenClaw configuration instead of passing it as a command argument. <br>
Risk: Enabling lefthook integration adds persistent git hooks that can block commits or pushes. <br>
Mitigation: Review lefthook.yml before enabling hooks and keep a documented bypass or removal path for local development emergencies. <br>


## Reference(s): <br>
- [RateLint ClawHub listing](https://clawhub.ai/suhteevah/ratelint) <br>
- [RateLint homepage](https://ratelint.pages.dev) <br>
- [RateLint git hooks documentation](https://ratelint.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Text, Markdown, JSON, or HTML scan reports with file, line, severity, check ID, description, recommendation, score, and grade details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against selected files or directories; supports tiered pattern sets, category filtering, verbose output, and optional lefthook integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
