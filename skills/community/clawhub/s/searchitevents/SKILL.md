---
name: it_events
description: Finds new upcoming IT events worldwide based on user-selected interests and location, avoids duplicates, and helps return official registration or payment links on request.
---

# IT Events

## Purpose

This skill is used to find upcoming IT events based on the user's selected interests and location, and send only new events that were not sent before.

Supported event types include:

- conferences
- meetups
- workshops
- summits
- forums
- tech talks
- community events
- bootcamps
- hackathons
- webinars
- online events

This skill must work for both:
- regular digests
- one-time searches
- follow-up requests about a specific event

---

## Main goal

Find only future IT events that match the user's selected interests and selected location.

Core rules:

- location: a specific country or worldwide
- event type: any relevant IT event
- topics: defined by the user in the current request
- deduplication: do not resend events that were already sent before

---

## User-defined interests

The user may specify the directions they are interested in.

Examples:

- JavaScript
- TypeScript
- Frontend
- Backend
- Fullstack
- Web development
- AI
- Artificial Intelligence
- DevOps
- QA
- Cybersecurity
- Data Science
- Machine Learning
- Mobile
- iOS
- Android
- Cloud
- UI/UX
- Product
- GameDev
- Blockchain
- PHP
- Laravel
- WordPress
- Vue
- React
- Node.js
- Python
- Java
- .NET
- Rust
- Go
- general software engineering

The skill must use the interests provided by the user in the current request.

If the user gives multiple interests, include events matching at least one of them.

If the user does not specify interests, the skill must ask which IT directions or topics they want.

The assistant must not start searching until both of these are known:
- interests / topic
- location scope: a country or worldwide

---

## Interest matching rules

Include an event if:

- its title, description, tags, agenda, or organizer page clearly show relevance to at least one of the user’s selected interests
- the event is clearly IT-related

Exclude an event if:

- it is mainly non-IT
- it is mainly business, HR, recruiting, marketing, or sales and has no clear technical relevance
- topic relevance to the requested interests is weak or unclear

If relevance is doubtful, exclude it.

---

## Geographic filter

The assistant must know the location scope before searching.

Location scope may be:

- a specific country
- worldwide

If the user does not specify a country or worldwide scope, the assistant must ask before searching.

Include only events that match the selected location scope.

If a specific country was requested:
- include events clearly held in that country
- include online events only if they are clearly targeted to that country or organized from that country

If worldwide was requested:
- include relevant events from any country

If the country, audience, or location relevance is unclear, prefer excluding the event.

---

## Time filter

Only include future events.

Do not include past events.

Do not include events that already ended.

If the event date is unclear or missing, exclude it.

---

## Preferred sources

Prefer sources in this order:

1. official event website
2. official registration page
3. official organizer page
4. reliable event platform page such as Meetup, Eventbrite, Dou, Luma, or similar trusted platform

Do not rely on low-quality reposts if an official page exists.

When possible, extract both:

- official event page
- registration or payment page

---

## State file

Use this file for deduplication:

`memory/it-events-sent.json`

If the file does not exist, create it with this content:

```json
{
  "sent": []
}
```

---
## Stored format

Each sent event should be stored in memory/it-events-sent.json  like this:

```json
{
  "id": "normalized_name|date|normalized_location",
  "type": "conference",
  "name": "Conference name",
  "date": "2026-05-18",
  "location": "Berlin, Germany",
  "topics": ["JavaScript", "Frontend"],
  "matchedInterests": ["JavaScript", "Frontend"],
  "eventUrl": "https://example.com/event",
  "registrationUrl": "https://example.com/register",
  "sentAt": "2026-04-06"
}
```

Allowed values for type include:

- conference
- meetup
- workshop
- summit
- forum
- tech talk
- webinar
- hackathon
- bootcamp
- other

If registrationUrl is not available, store an empty string or reuse the official event page only when necessary.

---
## Deduplication rules

An event is considered the same if these values match in meaning:

normalized name
date
normalized location

Use this id format:

`normalized_name|date|normalized_location`

Rules:

- ignore minor punctuation differences
- ignore case differences
- ignore small URL differences
- if name, date, and location are effectively the same, treat it as the same event
- never resend an event whose id already exists in the state file

---
## Search behavior

Before searching, the assistant must know:

1. the user's requested interests
2. the location scope:
  - a specific country
  - or worldwide

If interests are missing, ask for them.

If location is missing, ask whether to search in a specific country or worldwide.

If both are missing, ask both questions before searching.

When searching for events:

1. read the user’s requested interests
2. read the selected location scope
3. search for future IT events matching those interests and location
4. remove all events already present in `memory/it-events-sent.json`
5. prepare a compact result with only new matching events
6. after producing the result, append those new events to the state file

If no new matching events are found, return:

`За вказаними темами та локацією нових IT-подій не знайшов.`

---
## Output format

Start with:

`Нові IT-події:`

Then for each event include:

- type
- name
- date
- city and country, or online
- short topic summary
- official event link

If a registration page exists, also include:
- registration link

Keep the message compact and easy to scan.

Example structure:

- Meetup - JS Kraków Community
  - Дата: 2026-05-18
  - Локація: Kraków, Poland
  - Теми: JavaScript, Frontend
  - Сайт: ...
  - Реєстрація: ...
- Workshop - Python AI Lab
  - Дата: 2026-06-02
  - Локація: Online / USA
  - Теми: Python, AI
  - Сайт: ...
  - Реєстрація: ...

---
## Follow-up behavior for payment or registration link

If the user asks something like:

- надішли посилання на оплату
- дай посилання на квиток
- де оплатити цю подію
- надішли реєстрацію на цю подію
- дай посилання на участь

Then:

- identify the requested event by name
- first check `memory/it-events-sent.json`
- if needed, open the official event page
- find the most direct official registration or payment link
- return that link

Priority:

- direct ticket or payment page
- direct registration page
- official event page if direct payment page is unavailable

If checkout requires login, selecting ticket type, or several manual steps, explain this briefly and return the nearest official registration page.

Never invent a payment link.

Never return unofficial or suspicious payment links.

---
## Behavior when user refers to "this event"

If the user says:

- ця подія
- ця конференція
- цей meetup
- цей івент
- це
- по ній
- надішли оплату на неї

Use the most recently discussed relevant event from the current conversation context.

If multiple events were discussed and the reference is ambiguous, prefer the most recent clearly mentioned event.

---
## Data quality rules

Only include an event if all of the following are clear enough:

- type
- name
- future date
- location / audience
- topic relevance to the user’s selected interests
- official or reliable source

If one of these is unclear, exclude the event.

Never guess missing important details.

---
## Safety and trust rules
- prefer official pages
- do not fabricate dates, cities, organizers, or links
- do not fabricate payment pages
- if direct payment is unavailable, clearly say so
- if the event is sold out, say that if confirmed
- if registration is closed, say that if confirmed

---
## Language handling

This skill must accept user input in any language.

The user may ask for:
- one-time event search
- weekly recurring digest
- follow-up request for registration or payment link

The skill must determine the user's intent regardless of language.

## Response language

Prefer responding in the user's language.

If global assistant or project rules require a specific language, follow those rules.

---
## Summary rule

For event searches:

- be concise
- include only new events
- avoid duplicates
- quality over quantity

For registration or payment follow-ups:

- return the most direct official link available
- keep the answer short and practical

## Script integration

This skill may use local helper scripts stored inside the skill directory.

Available scripts:

- `"$SKILL_DIR/scripts/search-events.sh" "<interests>" "<location>"`
- `"$SKILL_DIR/scripts/setup-cron.sh" "<interests>" "<location>"`

### One-time event search

If the user asks to find IT events one time, search manually, or test the skill,
run:

`"$SKILL_DIR/scripts/search-events.sh" "<interests>" "<location>"`

Use this for requests like:

- знайди нові IT-події по AI у Німеччині
- покажи нові події по Python та AI у Польщі
- знайди конференції та meetup-и по React worldwide
- перевір, які нові події є по DevOps у Чехії

If the user provides interests, pass them as a single argument string.

If the user provides a country, pass it as the second argument.

If the user wants global search, pass:

`"worldwide"`

If the user does not provide interests, ask them which IT directions they want.

If the user does not provide location, ask which country to search in or whether to search worldwide.

### Weekly digest setup

If the user asks to enable, install, configure, or set up a weekly digest of IT events,
run:

`"$SKILL_DIR/scripts/setup-cron.sh" "<interests>" "<location>"`

Use this for requests like:

- налаштуй щотижневий дайджест IT-подій по AI у Німеччині
- увімкни щопонеділковий пошук подій по React worldwide
- зроби автоматичну розсилку нових IT-подій по Python у Польщі
- налаштуй weekly digest по JavaScript та Frontend у Чехії

If the user provides interests, pass them as a single argument string.

If the user provides a country, pass it as the second argument.

If the user wants global search, pass:

`"worldwide"`

If the user does not provide interests, ask them which IT directions they want before running the setup script.

If the user does not provide location, ask which country to use or whether to search worldwide before running the setup script.

## Runtime requirements

This skill requires the local `openclaw` CLI to be installed and available in PATH.

The helper scripts rely on:

- `openclaw agent`
- `openclaw cron`

If the `openclaw` command is not available, the scripts must not run and should return a clear error message.

## Automation safety

`setup-cron.sh` creates a persistent recurring cron job through OpenClaw.

This script must run only when the user explicitly asks for recurring or weekly delivery.

Do not run `setup-cron.sh` for one-time searches.

Before creating a cron job, the assistant must ensure that:
- the user clearly wants recurring delivery
- interests are known
- location is known


### Script behavior rules

- Run `search-events.sh` for one-time searches.
- Run `setup-cron.sh` only when the user explicitly wants recurring automatic delivery.
- Do not run setup automatically without the user's request.
- Do not start searching until both interests and location are known.
- Always pass user interests as one quoted argument.
- Always pass location as a second quoted argument.
- Use `"worldwide"` when the user wants global search.
- Ensure the scripts are executable before running them.
- If needed, run: `chmod +x "$SKILL_DIR/scripts/search-events.sh" "$SKILL_DIR/scripts/setup-cron.sh"`
- `setup-cron.sh` may create `memory/it-events-sent.json` if it does not exist.
- `search-events.sh` may also create `memory/it-events-sent.json` if it does not exist.
- This skill must accept user input in any language.
