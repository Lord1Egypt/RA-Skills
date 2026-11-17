## Description:

Plan trips end-to-end and turn them into polished static travel-guide webpages deployed to Cloudflare Pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cianweeresinghe-sudo](https://clawhub.ai/user/cianweeresinghe-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers, trip planners, and agents use this skill to design realistic trips, compare route and base options, generate itineraries, shortlist hotels and activities, and package the result as a static travel-guide microsite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable traveller profiles can retain personal or preference details that are not necessary for future planning.

Mitigation: Confirm what details will be saved, store only durable travel-planning preferences, and avoid retaining unnecessary sensitive information.

Risk: Published travel-guide microsites can expose itinerary, rooming, or traveller preference details if the agent includes them in public page content.

Mitigation: Review generated pages before deployment and remove personal, sensitive, or overly specific travel details that do not need to be public.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cianweeresinghe-sudo/skills/travel-guide-test)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated static HTML/CSS and deployment commands when publishing is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route summaries, day-by-day itineraries, hotel shortlists, booking checklists, map or leg links, image guidance, and Cloudflare Pages deployment steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
