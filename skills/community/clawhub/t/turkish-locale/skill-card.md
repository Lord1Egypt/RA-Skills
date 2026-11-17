## Description:

Turkish locale skill pack for Turkish news sources, BIST100 market tracking, daily brief automation, and a Turkish personality template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erhnysr](https://clawhub.ai/user/erhnysr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to localize Hermes-style agent interactions for Turkish language, news, market summaries, and scheduled daily brief delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring Telegram or Discord delivery can send summaries to an unintended destination or continue after the user expects it to stop.

Mitigation: Confirm the target chat or channel, document how to remove the scheduled delivery, and avoid routing sensitive summaries through outbound channels.

Risk: Market tracking behavior and documentation are inconsistent, including BIST100 naming alongside crypto price tooling.

Mitigation: Review market outputs before relying on them, show timestamps and data sources, and avoid treating generated market summaries as financial advice.

Risk: Bundled scripts depend on network data sources and third-party Python packages when executed.

Mitigation: Run scripts in an isolated environment with pinned dependencies and review network destinations before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erhnysr/skills/turkish-locale)
- [Publisher Profile](https://clawhub.ai/user/erhnysr)
- [Bloomberg HT BIST100](https://www.bloomberght.com/borsa/endeksler/bist-100)
- [Bigpara Live Borsa](https://bigpara.hurriyet.com.tr/borsa/canli-borsa/)
- [Hürriyet RSS](https://www.hurriyet.com.tr/rss/anasayfa)
- [NTV Breaking News RSS](https://www.ntv.com.tr/son-dakika.rss)
- [Bloomberg HT RSS](https://www.bloomberght.com/rss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and Turkish text with inline shell commands, configuration snippets, and optional JSON or generated image outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live news, market data, daily brief content, Telegram or Discord delivery setup, and Turkish locale guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
