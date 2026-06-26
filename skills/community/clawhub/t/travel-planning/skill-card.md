## Description: <br>
Plan trips with itineraries, multi-city routing, budget optimization, family logistics, packing lists, and visa timelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to plan personal, family, group, and multi-city travel. It helps organize trip ideas, itineraries, budgets, booking details, packing lists, traveler needs, and deadline reminders in local Markdown records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent travel preferences and trip records that may include sensitive personal details. <br>
Mitigation: Review what is saved in ~/travel-planning/, avoid storing full document numbers or images, and keep only details needed for planning. <br>
Risk: Cross-session memory and proactive reminders may preserve or surface travel context longer than a user expects. <br>
Mitigation: Enable persistent memory and proactive activation only when explicitly wanted, and remove or edit saved travel records when plans or privacy preferences change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/travel-planning) <br>
- [Skill homepage](https://clawic.com/skills/travel-planning) <br>
- [Setup guide](artifact/setup.md) <br>
- [Booking guide](artifact/booking-guide.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Multi-city planning guide](artifact/multi-city.md) <br>
- [Packing templates](artifact/packing-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and local Markdown file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update travel memory, wishlist, trip, itinerary, booking, packing, budget, traveler, and document reference files under ~/travel-planning/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
