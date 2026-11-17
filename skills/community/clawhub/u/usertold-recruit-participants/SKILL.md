---
name: usertold-recruit-participants
description: Plan participant recruitment for a UserTold Study and produce participant-readable recruitment copy plus canonical Invitation, Visibility, and neutral Intake inputs. Use when choosing whom to invite, comparing outreach channels, setting an honest reward, drafting an in-product launcher or direct-link invitation, screening without revealing qualifying answers, or translating an existing recruitment plan into UserTold configuration. Do not use to send outreach, source a participant panel, fulfill rewards, claim representative sampling, or provide legal advice.
---

# Recruit UserTold Participants

Turn a research question into a small, truthful recruitment plan for people the team can already reach. Recruitment is distribution into a UserTold Study, not a marketing funnel.

## Establish the participant boundary

1. State the behavior or recent experience that makes someone relevant. Prefer “attempted checkout in the last 30 days” over a persona label.
2. State exclusions that protect the research question, participant safety, conflicts, and duplicate participation. Do not add demographic filters without a study-specific reason.
3. Name the reachable population and the resulting coverage limit. Never call a convenience sample representative.
4. Record whether recontact is needed as a separate, optional consent choice.

## Choose distribution

Read [references/channel-selection.md](references/channel-selection.md), choose one primary channel, and name one meaningfully contrasting channel. Explain why each reaches the target behavior and add one explicit sampling-bias sentence.

Email and CRM are distribution only: special URL → expanded Invitation → explicit **Start**. The participant must select Start before permissions or recording. A link is never consent. Do not claim UserTold sends email, operates a CRM, or personalizes the link to an identity.

Track source with channel-level `utm_source`, `utm_medium`, and `utm_campaign` values where the host flow preserves them. Use campaign labels, not personal data. Report response and completion by source without turning the result into a representative-sample claim.

## Set the offer

Read [references/rewards.md](references/rewards.md). State all four terms exactly:

- duration;
- reward or “No reward”;
- eligibility, including gift restrictions or alternatives;
- delivery timing and method, or “Not applicable.”

About $80/hour is marketplace orientation for human-moderated consumer interviews, not a universal rate or a calculator. AI-moderated and short in-product interviews normally use a smaller fixed reward. Participant copy must show the actual promise, such as “20 minutes · $25 gift card.” UserTold records the promise; it does not fulfill payment.

## Select presentation and timing

Choose one `presentation_mode`:

- `passive`: a compact launcher the participant opens; use for voluntary feedback or a standing bug-report route.
- `contextual`: show an expanded panel on a relevant product route; use when current product context matters.
- `direct_link`: distribute the generated `recruitment_url`; use for email, CRM, community posts, or a targeted new-feature test. It does not participate in automatic page placement.

For automatic placement, define Visibility v1 with the fewest include/exclude rules needed. State when recruitment opens and closes plus any maximum-participant or contact-cadence rule as an operational timing plan. Visibility does not encode dates or display frequency; do not invent fields for them or claim UserTold enforces an outreach cadence. Respect remembered **Minimize** and **Hide** choices. Never interrupt an intake, interview, or completion flow, and never convert observed frustration into an automatic interruption.

## Draft neutral Intake

Ask only questions needed to determine the behavioral boundary. Use balanced answer options and neutral wording that does not signal which answer qualifies. Put qualification logic in `qualification_rules`, not in participant copy. Do not ask for contact details unless the workflow requires them and the participant agrees.

Provide:

- `title`, `welcome_message`, and concise `consent_text`;
- ordered `questions` using the existing Intake fields (`question_text`, `question_type`, `required`, optional `options`, numeric bounds, and `qualification_rules`);
- participation/recording consent copy plus separate optional recontact copy and the point where the host flow will ask it;
- a neutral disqualification message that does not reveal the rule.

Recontact permission is consent, not qualification. Do not put it in `qualification_rules` or claim an ordinary Intake question writes UserTold's response-level `consent_followup` value. If the discovered participant flow cannot capture separate recontact consent, flag that limitation and leave recontact off.

The public UserTold MCP surface can create or update Studies with Invitation and Visibility. It does not expose a new recruitment or Intake tool. Produce Intake inputs for the dashboard or published CLI unless the live discovered surface explicitly supports more.

## Produce configuration

Return this compact packet:

1. **Participant:** behavioral definition; exclusions; reachable population.
2. **Channels:** primary; contrasting channel; sampling-bias note; source tags.
3. **Offer:** exact duration, reward, eligibility, delivery.
4. **Copy:** launcher label; optional panel eyebrow, headline, body, and CTA; outreach copy when relevant.
5. **Presentation:** passive/contextual/direct-link rationale; Visibility and timing plan.
6. **Intake:** neutral participant-facing questions and hidden qualification intent/rules.
7. **Safeguards:** consent, optional recontact, Minimize/Hide, and non-interruption rules.
8. **Canonical JSON:** exact `invitation`, `visibility`, `intake_create`, and optional `intake_update` objects directly usable with shipped UserTold fields. Put `title`, `welcome_message`, `consent_text`, `max_participants`, and `questions` in `intake_create`; put `disqualified_message` or other post-create copy in `intake_update`. Do not emit an invented combined `intake` schema.

Use only Invitation fields and enums shown in [references/invitation-examples.md](references/invitation-examples.md). `contextual` and `direct_link` require a panel. Omit reward entirely when there is no reward. Keep one reward promise, and never add payment, email, CRM, participant-sourcing, identity, or sampling fields to the JSON.

Before writing through UserTold, discover the live MCP operations. Prefer `studies.get` to inspect an existing Study and `studies.create` or `studies.update` for supported fields. Show the packet and require explicit approval before activating a Study or Intake or changing a live Invitation/Visibility configuration.

## Check the packet

Confirm that participant copy and JSON agree on duration and reward, direct links require explicit Start, qualification answers are not telegraphed, recontact is not used as qualification, source tracking contains no identity, and the bias note names who the chosen channel misses. Read the relevant scenario in [references/invitation-examples.md](references/invitation-examples.md) when the offer is unusual or a direct link is involved.
