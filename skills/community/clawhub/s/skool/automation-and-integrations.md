# Automation and Integrations - Skool

## Official-Only Bias

Default to official Skool surfaces first.
Use native settings, AutoDM, Zapier, or the documented webhook plugin before proposing custom browser automation.

## Zapier Workflow Rules

- Treat the Zapier plugin as a real write surface because it can affect real members.
- Verify the current setup requirements first: exact group URL segment, approved credential source, and approved Zap owner.
- Start from the four documented use cases before inventing anything broader: export paid-member info, export membership questions, invite a member, unlock a course.
- Build the smallest working Zap before adding branches, filters, or downstream systems.
- Test against a staging-safe group, a test member, or a reversible scenario whenever possible.
- Remember the documented delay on standard Zapier accounts can be around 10 to 15 minutes, so do not debug too early.

## Webhook Plugin Rules

- The webhook plugin is the right choice when invite or course-access workflows must trigger downstream automation.
- Confirm the destination host, payload fields, retry expectations, and rollback path before enabling it.
- If the workflow affects access or payment-adjacent behavior, preview the entire member journey first.
- Treat it as narrower than a general public API. It is a developer-only plugin for specific off-platform invite and access workflows, not a blanket automation surface.

## Native Automation Rules

- Use membership questions, instant approval, AutoDM, and classroom access settings as first-class automation tools.
- Use invite-link, email-invite, and CSV-import flows when the need is admission rather than two-way automation.
- Use built-in tracking plugins when the problem is attribution or retargeting rather than member management.
- If a native setting solves the problem, do not add a second automation layer just because it feels more technical.

## Concrete Verified Workflows

- **Admission**: share About page, send direct email invites, import CSV batches, or trigger invite emails from Zapier.
- **Qualification**: collect membership questions, review answers before approval, and export answers when CRM sync is needed.
- **Activation**: send AutoDM with built-in name and group variables, add onboarding video, and route members into the first lesson or event.
- **Access**: grant or revoke course access manually, or unlock courses through Zapier when the user is already in the group.
- **Attribution**: use Google Ads, Meta pixel, or Hyros plugins when the user needs tracking instead of CRM sync.
- **Events**: use recurring calendar events, Skool Calls, or Pro webinars before adding external event tooling.

## Hard Boundaries

- No official Skool CLI is documented in the current official help content.
- Do not assume undocumented endpoints are safe enough for production writes.
- Do not automate posting, commenting, or messaging through unsupported bots when the platform or docs say otherwise.
- Do not ask the user to share Skool credentials with teammates, contractors, or external tools.

## What To Capture After a Working Automation

- trigger source
- exact group URL or environment it belongs to
- required approval level
- who the workflow can affect
- rollback or disable path
- known failure signatures
