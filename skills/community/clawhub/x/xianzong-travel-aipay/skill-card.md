## Description:

Creates tailored, day-by-day travel itineraries with itemized budgets, transport and lodging advice, practical contingencies, and Markdown and PDF delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveljack](https://clawhub.ai/user/liveljack)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and trip planners use the skill to turn requirements for one destination and date range into a practical itinerary, with budgets, booking checks, rest pacing, and contingency options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags an unpinned package installation command, and only part of the artifact was analyzed.

Mitigation: Before installing, pin and independently verify the package version and review the complete artifact, following the security guidance.

Risk: Trip details and the email address are sent to an external service as part of consultation and delivery.

Mitigation: Review what information is sent and when, and provide only the trip and contact details needed for the service.

## Reference(s):

- [Publisher's travel service site](https://xianzongwendao.com)
- [ClawHub release page](https://clawhub.ai/liveljack/skills/xianzong-travel-aipay)
- [Beijing itinerary sample (PDF)](https://ai-agency-dev.oss-cn-beijing.aliyuncs.com/static_files/samples/aipay/%E6%97%85%E8%A1%8C%E5%92%A8%E8%AF%A2%E6%96%B9%E6%A1%88_%E5%8C%97%E4%BA%AC.pdf)
- [UK itinerary sample (PDF)](https://ai-agency-dev.oss-cn-beijing.aliyuncs.com/static_files/samples/aipay/%E6%97%85%E8%A1%8C%E5%92%A8%E8%AF%A2%E6%96%B9%E6%A1%88_%E8%8B%B1%E5%9B%BD.pdf)
- [Travel service endpoint](https://api.riyuexinzhu.com/aipay/travel_consultant)
- [402 travel flow reference](references/402-travel-flow.md)
- [Installation and packaging reference](references/install-and-pack.md)

## Skill Output:

**Output Type(s):** [Markdown, PDF, Travel guidance]

**Output Format:** [Day-by-day itinerary with itemized budget and practical checklists; PDF is delivered by email with a download link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One trip per consultation. The PDF cover and email are Chinese-only; travelers should verify prices, opening hours, and booking rules with official sources before acting.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
