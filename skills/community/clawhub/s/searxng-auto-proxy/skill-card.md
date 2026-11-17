## Description:

SearXNG 自适应代理检测技能，自动检测 Clash 代理可用性，智能切换搜索引擎，支持性能监控和自动优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengong101](https://clawhub.ai/user/pengong101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure SearXNG with adaptive proxy rules, dynamic engine reachability checks, and Clash proxy node optimization for mixed domestic and global search deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The adapter can run as a long-lived process using root-scoped paths.

Mitigation: Run it as a dedicated unprivileged user with narrowly scoped write access for configuration, cache, and logs.

Risk: The skill can automatically change Clash proxy routing.

Mitigation: Protect the Clash controller with authentication and network restrictions, and configure switching only for a SearXNG-specific proxy group.

Risk: Dependency and container updates can change runtime behavior.

Mitigation: Pin Python dependencies and container image versions before deployment.

Risk: Search quality and latency can vary when engines timeout or return poor results.

Mitigation: Monitor adapter logs and cache state, tune engine rules and timeouts, and disable low-quality engines when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengong101/skills/searxng-auto-proxy)
- [README.md](artifact/README.md)
- [Release notes v3.0.0](artifact/RELEASE-v3.0.0.md)
- [Final test report v3.0](artifact/FINAL-TEST-REPORT-v3.0.md)
- [Proxy rules configuration](artifact/proxy-rules.yml)
- [ClawHub manifest](artifact/clawhub.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce configuration and operational steps for a long-running SearXNG proxy adapter.]

## Skill Version(s):

3.0.0 (source: server release evidence, clawhub.json, release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
