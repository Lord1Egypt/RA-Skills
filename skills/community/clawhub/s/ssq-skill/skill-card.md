## Description:

A Chinese-language Shuangseqiu lottery education skill that produces probability reports, randomness checks, entertainment-only number references, draw verification, and anti-fraud guidance emphasizing that no selection method improves lottery odds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmily741963](https://clawhub.ai/user/hmily741963)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate responsible-play lottery analysis, debunk paid prediction claims, compare methods against random baselines, and verify Shuangseqiu draw data. It is intended for entertainment and education, not betting, investment, or income decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill asks for privileged scheduled execution and can read or write across local user profiles.

Mitigation: Run it under a normal user account and avoid creating SYSTEM or highest-privilege scheduled tasks unless the deployment has been reviewed.

Risk: The security review calls out WorkBuddy integration, peer-install mirroring, and the optional local server as high-impact features.

Mitigation: Prefer offline or manual use with `python run_ssq.py`; disable or review those integrations before installation.

Risk: Lottery reports can be misused as betting or income guidance despite the artifact's stated no-edge conclusion.

Mitigation: Keep responsible-play warnings visible and treat all generated number references as entertainment-only analysis, not financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmily741963/skills/ssq-skill)
- [README](artifact/README.md)
- [Methodology and mathematical basis](artifact/methodology.md)
- [Operations and self-check workflow](artifact/operations.md)
- [Responsible play guidance](artifact/responsible_play_2026.md)
- [FAQ](artifact/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; local runs may produce HTML and JSON report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python standard-library scripts and may reference generated desktop report paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.1.36)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
