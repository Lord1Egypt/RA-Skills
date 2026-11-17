# Form: incident-report

**Register:** `docs`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

The internal record of one failure: what broke, when, who was affected, why it happened, and what changes as a result. It routes to `docs` because of how it is read. Nobody reads an incident report front to back for pleasure. They arrive during the next incident, looking something up, which is the same posture a runbook reader is in and the reason that register relaxes what it relaxes.

`forms/technical-blog.md` covers the other document: the public writeup of an incident, narrative, written for readers outside the organization, with the internal detail removed. Same event, different form. The internal report is the one with severity, owners, and action items in it, and the one that has to be findable by somebody who was not on the call.

## Slots

- **Summary.** Two or three sentences: what broke, for how long, who was affected. Written for a reader who will read nothing else.
- **Impact.** Measured. Users, requests, revenue, data, duration. An impact section with adjectives instead of numbers is the section that gets argued about later.
- **Severity and status.** Against whatever scale the organization already uses. This form does not supply one.
- **Timeline.** Timestamped, with the timezone stated once. Detection, escalation, mitigation, resolution. What was believed at each point belongs here too, because a timeline that records only what was true reads as though the responders knew it.
- **Root cause.** The chain, not the last link. Stop when the next step leaves the system and becomes a person.
- **Detection and response.** How it was found and how long each stage took. Whether it was found by monitoring or by a customer is the single most useful line in the document.
- **What went well.** Real, and not a courtesy. The things that limited the blast radius are the things worth funding.
- **Action items.** Each with an owner, a date, and a link to wherever it is tracked. An action item that lives only in the report is a wish.
- **Supporting detail.** Logs, graphs, queries, configuration. Appended rather than inline.

## Bands

| Purpose | Band |
|---|---|
| A low-severity incident | 300 to 600 words plus the timeline |
| A significant outage | as long as the timeline, and the timeline is not padding |
| A review circulated beyond the team | add the summary and impact sections above, not more prose in the others |

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Human error" as a root cause. It names where the investigation stopped.
- "The system experienced an issue."
- "Unfortunately, a small number of users may have been affected." Count them.
- "We take reliability seriously" in an internal document.
- "This should not happen again" with no change behind it.
- A root cause that is the last thing that broke rather than the reason it could break.
- A timeline with no timezone, or with two timezones and no note saying which is which.
- Action items with owners named as teams rather than people.
- Blame anywhere. A report that costs somebody something is a report the next person writes less honestly.

## What the mechanical layer sees here

`docs` is the most relaxed register outside `chat`, and every relaxation fits this form. The vocabulary tiers run in partial mode, so the words that carry real technical meaning are not reported. Uniform paragraph length, excessive bullets, bullet-NP lists, and list-label periods are all skipped, which matters because a timeline and an action-item list are exactly those shapes and reporting them would report the genre.

What runs at full strength is the whole `safety` band, every P0 fingerprint, and the placeholder check. The placeholder check earns its place here: an incident report is written under time pressure and circulated fast, and a template field left unfilled goes out to everybody.

Ignore the paragraph and sentence spread numbers on the timeline. A timeline is a list, and the engine counts a list as one paragraph.
