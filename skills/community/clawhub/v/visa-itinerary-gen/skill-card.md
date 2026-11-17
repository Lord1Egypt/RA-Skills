## Description:

Generate consulate-grade visa itinerary documents from natural language using flyai travel data, producing a PDF travel plan and Fliggy booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zephryve](https://clawhub.ai/user/zephryve)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents use this skill to turn a natural-language visa trip request into a clean consulate itinerary package. It gathers flight, hotel, and attraction data, then produces an editable Markdown itinerary, a PDF, and booking-link HTML files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries flyai/Fliggy online with trip details.

Mitigation: Use it only when sharing the required travel search details with those services is acceptable.

Risk: The skill installs mutable third-party npm and Python packages.

Mitigation: Install in an isolated environment and review or pin package versions before operational use.

Risk: Generated HTML/PDF outputs and booking links may contain untrusted destinations or unvalidated travel data.

Mitigation: Verify link destinations and avoid rendering Markdown or JSON supplied by another party unless URL validation and field escaping have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zephryve/skills/visa-itinerary-gen)
- [Publisher profile](https://clawhub.ai/user/zephryve)
- [Skill homepage](https://github.com/zephryve/visa-itinerary-gen)
- [flyai CLI package](https://www.npmjs.com/package/@fly-ai/flyai-cli)
- [Playwright package](https://pypi.org/project/playwright/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown itinerary, PDF document, JSON booking data, and local HTML booking-link pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, python3, flyai, and Playwright; outputs are generated from travel data returned during execution.]

## Skill Version(s):

1.7.4 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
