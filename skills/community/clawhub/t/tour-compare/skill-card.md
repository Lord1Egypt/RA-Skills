## Description:

Tour Compare helps users compare OTA package-tour products from links, screenshots, or JSON and produces structured recommendations, comparison summaries, and travel-risk reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangnex](https://clawhub.ai/user/liangnex)

### License/Terms of Use:

MIT-0

## Use Case:

Travel shoppers and agents use this skill to compare package-tour options across OTA platforms, identify price, itinerary, hotel, shopping-stop, and cancellation-policy differences, and choose an option that fits a traveler persona. Developers can also run it as a CLI tool for JSON-based comparison, URL-assisted extraction, recommendation, filtering, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL crawling gives the skill network and browser execution authority when users provide links.

Mitigation: Prefer JSON input or --no-fetch, and only use trusted OTA URLs until strict hostname validation, redirect checks, private-network blocking, and Chromium sandboxing are in place.

Risk: Screenshots may include sensitive booking, identity, or payment-adjacent information.

Mitigation: Use screenshots that exclude personal data and avoid sharing or retaining sensitive screenshots.

Risk: Optional crawler, OCR, and export dependencies expand the local execution surface.

Mitigation: Review the crawler and dependency setup, then install dependencies explicitly in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangnex/skills/tour-compare)
- [README](artifact/README.md)
- [Input guide](artifact/docs/INPUT_GUIDE.md)
- [Output flow](artifact/docs/OUTPUT_FLOW.md)
- [Supported OTA platforms](artifact/docs/PLATFORMS.md)
- [Usage examples](artifact/examples/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, image files, guidance]

**Output Format:** [Markdown or plain text summaries, optional JSON output, local HTML report links, and optional PNG exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include comparison tables, recommendation rankings, persona-specific guidance, follow-up questions, and warnings about low-price tours, shopping stops, hidden costs, or cancellation policies.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
