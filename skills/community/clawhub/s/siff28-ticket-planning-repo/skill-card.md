## Description:

用于根据任意影片清单与偏好规划 SIFF 2026 买票和观影行程；优先使用内置官方排片数据，并评估片长、散场缓冲、跨影院驾车时间与备选场次。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fffonion](https://clawhub.ai/user/fffonion)

### License/Terms of Use:

MIT-0

## Use Case:

Festival attendees and agent users can turn film lists, preferences, and rough location anchors into SIFF 2026 ticket-buying priorities, daily viewing plans, transfer risk notes, and backup screenings. The skill is especially suited to comparing official schedule data with estimated driving and metro travel times across Shanghai cinemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use approximate home, workplace, or stopover anchors to improve itinerary comfort.

Mitigation: Use rough landmarks when possible, avoid exact private addresses, and anonymize any anchors in outputs as home point A, work point B, or stopover point C.

Risk: Screenshots, local files, or account pages used as film-list inputs may contain sensitive personal information.

Mitigation: Prefer plain film-title lists or redacted files, and avoid submitting private account pages or unnecessary personal data.

Risk: Schedule, driving, and metro data are static or estimated and may not reflect sold-out screenings, last trains, crowding, weather, or live traffic.

Mitigation: Verify final showtimes, ticket availability, last-train constraints, and tight transfers against current official or map sources before purchasing tickets.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fffonion/skills/siff28-ticket-planning-repo)
- [SIFF 2026 official schedule page](https://www.siff.com/page/paipian)
- [SIFF 2026 official schedule data snapshot](references/siff2026/siff2026-official-cndata-20260603-001.json)
- [SIFF 2026 scrape summary](references/siff2026/siff2026-scrape-summary.json)
- [SIFF 2026 reference manifest](references/siff2026/manifest.json)
- [Cinema driving routing manifest](references/siff2026/siff2026-cinema-routing-manifest.json)
- [Cinema metro routing manifest](references/siff2026/siff2026-cinema-metro-routing-manifest.json)
- [MetroFlow station data collection](https://figshare.com/collections/ARIZONA_Sun/4209384)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files, Configuration]

**Output Format:** [Markdown itinerary and ticket-priority guidance with optional CSV or iCal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label assumptions, estimated travel times, transfer buffers, and screening risk levels.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter and changelog report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
