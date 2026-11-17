## Description:

XiaoChi helps agents review public Meituan Waimai merchant and product pages and summarize ratings, prices, delivery details, and sales signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect lightweight summaries and comparisons from public Meituan Waimai merchant, product, and activity pages for internal analysis and reminders.

### Deployment Geography for Use:

Global, subject to Meituan Waimai service availability and local platform rules.

## Known Risks and Mitigations:

Risk: Prices, delivery windows, promotions, and availability can vary by time and region.

Mitigation: Capture collection time, region, and source links when summarizing merchant or product details.

Risk: Browsing automation could be misused for ordering, logged-in account actions, bulk scraping, or bypassing platform controls.

Mitigation: Limit use to public pages, avoid account actions and high-volume collection, and follow platform and location authorization rules.

## Reference(s):

- [Meituan Waimai](https://waimai.meituan.com/)
- [XiaoChi on ClawHub](https://clawhub.ai/codekungfu/skills/xiaochi)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and comparison notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links and should note collection time and region when prices or delivery details are summarized.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
