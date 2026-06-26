## Description: <br>
Find contact details for accommodation listings (Airbnb, Booking.com, VRBO, Expedia). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel, hospitality, or support agents use this skill when a user provides an accommodation listing URL and wants publicly available direct contact methods for that property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an undeclared local `travel-concierge` CLI discovered on the user's PATH. <br>
Mitigation: Install only if the CLI is known and trusted, and review proposed commands before execution. <br>
Risk: Collecting accommodation contact details can raise privacy expectations and booking-platform terms concerns. <br>
Mitigation: Use the skill only for specific user-selected listings, respect platform terms and privacy expectations, and use a restricted, quota-limited Google Places API key if configured. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a contact dossier with property details, contact methods, sources, and confidence levels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
