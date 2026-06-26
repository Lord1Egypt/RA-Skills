## Description: <br>
Connect your agent to Airbnb, Booking.com & VRBO via Vanio AI, giving OpenClaw access to vacation-rental tools for reservations, guests, messaging, smart locks, payments, workflows, and related property operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivannikolovbg](https://clawhub.ai/user/ivannikolovbg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Vacation-rental operators and their agents use this skill to connect OpenClaw to Vanio AI for natural-language management of reservations, guest communication, listings, smart locks, payments, tasks, calendars, analytics, and automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language commands can affect bookings, guest messages, payments, smart locks, and automation settings. <br>
Mitigation: Require human review before charges, refunds, cancellations, guest messages, smart-lock actions, or broad automation changes. <br>
Risk: The skill relies on Vanio access to rental operations and connected platform data. <br>
Mitigation: Install only if you trust Vanio with those accounts and data, and limit use to rental operations intended for agent access. <br>
Risk: API keys may be stored locally when users configure the CLI on shared machines. <br>
Mitigation: Prefer VANIO_API_KEY for sensitive environments, protect local config files, and rotate keys if exposed. <br>


## Reference(s): <br>
- [Vanio AI homepage](https://www.vanio.ai) <br>
- [ClawHub Vanio AI skill page](https://clawhub.ai/ivannikolovbg/vanio) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Vanio CLI and VANIO_API_KEY; responses may include operational guidance or CLI-driven actions against connected rental accounts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
