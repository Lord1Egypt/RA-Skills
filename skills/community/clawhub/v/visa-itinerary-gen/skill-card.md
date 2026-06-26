## Description: <br>
Generate consulate-grade visa itinerary documents from natural language using flyai travel search data, with PDF travel plans and Fliggy booking-link pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zephryve](https://clawhub.ai/user/zephryve) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and visa-preparation agents use this skill to turn trip details into a consulate-facing itinerary, including a Markdown travel plan, a rendered PDF, booking-link HTML pages, and supporting booking data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip search details are sent to external travel services through flyai and Fliggy. <br>
Mitigation: Install and run the skill only when external travel search is acceptable, and avoid entering unnecessary sensitive personal data. <br>
Risk: Generated itinerary, hotel, flight, and attraction details may be unsuitable for a visa filing or travel purchase if source results are incomplete or stale. <br>
Mitigation: Review generated booking links and itinerary details before using them for a visa application or booking travel. <br>
Risk: The skill depends on the flyai CLI plus Playwright/Chromium in the local environment. <br>
Mitigation: Approve dependency installation only after reviewing the requested tools and run the skill in an environment appropriate for travel-search automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zephryve/visa-itinerary-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zephryve) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, configuration, shell commands] <br>
**Output Format:** [Markdown itinerary, PDF file, JSON booking data, and bilingual HTML booking-link files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided travel details and flyai/Fliggy search results; generated travel and booking details should be reviewed before visa submission or travel booking.] <br>

## Skill Version(s): <br>
1.7.4 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
