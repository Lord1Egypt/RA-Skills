## Description: <br>
Plans trips and produces verified, day-by-day travel itineraries as a polished standalone HTML page with maps, budgets, transport details, checklists, and source-labeled facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric6286](https://clawhub.ai/user/eric6286) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to gather trip requirements, research current travel facts, and assemble a phone-friendly itinerary page. It is intended for query-only planning and leaves booking, login, CAPTCHA, and payment actions to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read travel or social-site pages in an already logged-in browser session. <br>
Mitigation: Use it only with the specific travel tabs and accounts needed for the itinerary, and close unrelated sensitive tabs before running it. <br>
Risk: Travel prices, schedules, reviews, and page selectors can change or become unavailable during research. <br>
Mitigation: Treat unavailable data as unavailable, keep source labels near facts, and verify booking-critical details directly on the provider site before purchase. <br>
Risk: The workflow touches booking sites while researching fares and hotels. <br>
Mitigation: Keep booking, payment, credential entry, login completion, and CAPTCHA handling manual and user-controlled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eric6286/trip-planner) <br>
- [README](artifact/README.md) <br>
- [Design System](artifact/references/design-system.md) <br>
- [Research Playbook](artifact/references/research-playbook.md) <br>
- [Scraping Method](artifact/references/scraping-method.md) <br>
- [Benchmark](artifact/evals/benchmark.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Standalone HTML file with embedded CSS and JavaScript, plus concise status or validation notes when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve source labels for researched facts and avoid booking, payment, credential entry, or CAPTCHA handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
