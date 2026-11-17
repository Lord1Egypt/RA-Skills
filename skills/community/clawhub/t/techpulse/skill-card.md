## Description:

TechPulse monitors public Reddit hot posts across IoT, electric vehicles, games, DIY, and emerging technology to produce concise trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:


## Use Case:

Developers, entrepreneurs, and technology watchers use TechPulse to generate quick category-specific snapshots of public Reddit activity for technology trend discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Reddit's public API, so reports may be incomplete when Reddit is unavailable, rate-limited, or blocked by the runtime environment.

Mitigation: Run it only in environments where public Reddit access is permitted, and treat empty categories as missing source data rather than proof that no trend exists.

Risk: Trend summaries are based on public community posts and scores, which may be noisy, promotional, or misleading.

Mitigation: Review the linked source posts before using the output for product, investment, or business decisions.

## Reference(s):

- [TechPulse ClawHub skill page](https://clawhub.ai/voronindenis5/skills/techpulse)
- [voronindenis5 ClawHub profile](https://clawhub.ai/user/voronindenis5)
- [Reddit public API documentation](https://www.reddit.com/dev/api/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text trend report with category headings and Reddit post titles and scores; installation and usage guidance may be Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report all categories or one selected category: iot, ev, games, diy, or tech.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
