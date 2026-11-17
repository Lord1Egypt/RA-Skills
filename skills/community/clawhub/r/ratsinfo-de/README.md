# ratsinfo-de

A skill for reading German municipal council records through the OParl API,
politely.

German municipalities publish their council papers, decisions and meeting
agendas in a *Ratsinformationssystem*. Most of these systems expose a
machine readable API called [OParl](https://oparl.org/). This skill lets an
agent ask what a town has decided about a school, a building site or a
budget, and get the actual council papers back.

```bash
python3 scripts/ratsinfo.py find Münster
python3 scripts/ratsinfo.py check https://oparl.stadt-muenster.de/system
python3 scripts/ratsinfo.py papers https://oparl.stadt-muenster.de/system \
    --term Sanierung --since 2026-01-01
```

Python 3.9 or newer. Standard library only, nothing to install.

## Why this exists

We are a small construction planning and project management firm in
Wuppertal. Our work sits on top of municipal decisions: which school gets
renovated, which budget was approved, which committee is responsible. That
information is public by law and sits in council information systems, and
we had to learn how to get at it. This is that work, given back.

The libraries that existed are unmaintained. `liboparl` last moved in 2021,
`oparl.js` in 2017. The OParl endpoint registry has around 127 entries,
contains duplicates and dead hosts, and is a lower bound rather than a
census. There was no small, dependency free client that behaves itself.

## What it does

- Finds a municipality's endpoint in the official registry
- Health checks it before crawling, because the registry lists endpoints
  that are dead, duplicated or switched off
- Lists council papers and meetings, following `links.next` rather than
  trusting `pagination`
- Prints the file URLs so the documents themselves can be fetched
- Lists every body an endpoint serves, so a Kreis endpoint is not mistaken
  for a single council
- Speaks JSON on `--json`, for use from a script or an agent
- Explains vendor URL patterns for the towns the registry does not know
- **Tracks what became of a paper** (`track`), walking Paper to Consultation
  to AgendaItem to Meeting and printing the route through the committees
  with dates, roles and results, ending in a plain status line. No council
  frontend shows that in one view.
- **Watches for change cheaply** (`watch`), using `modified_since` and a
  small state file, reporting what is new and what has been withdrawn, with
  optional iCalendar output for upcoming sittings
- Lists people and their committee memberships (`people`)
- **Searches many municipalities at once** (`scan`) and writes a market
  report grouped by town, naming the endpoints it could not read rather
  than passing over them in silence
- **Writes a real PDF dossier** (`report`), one page, with your logo, the
  status, the full committee timeline and the legal footnote. The PDF
  writer is part of the skill and uses only `zlib` and the base fourteen
  fonts, so there is still nothing to install.

## What it does not do

Stated plainly, because a tool that hides its limits wastes more time than
it saves.

- **No full text search.** OParl has no search parameter. Filtering happens
  on the client over titles and reference numbers. A paper whose subject
  appears only inside the attached PDF will not be found.
- **CC e-gov ALLRIS installations are closed to it.** They answer with an
  HTML bot check page that needs a browser session. The script recognises
  the page and stops rather than pretending.
- **Some operators disallow their own API in robots.txt.** The script
  honours that and stops. There is an override flag for the case where the
  operator has said yes in writing, and for no other case.
- **Coverage is patchy.** Many municipalities run no OParl at all.

## Manners

One request per second per host, an identifiable user agent, exponential
backoff on 429 and 503, robots.txt honoured by default, `created_since`
instead of full crawls. Throttling is per host rather than per municipality
because several municipal data centres host dozens of towns on one machine.

Set `RATSINFO_USER_AGENT` to something that names you and gives a way to
reach you.

## Legal footing

Council sessions are public by law, and the documents of the public part
are meant to be read. That is not the same as free to republish.
Attachments often carry third party copyright, and paper texts routinely
name private individuals. `references/recht-und-etikette.md` sets out the
detail with sources, in German, because the law is German.

## Tests

```bash
bash tests/run_tests.sh
```

Forty checks against two local mock servers, one well behaved and one that
reproduces the failure modes that really occur: a disabled endpoint, a bot
check page instead of JSON, a robots.txt that blocks the API path, a
malformed list, a link pointing off host, a `file://` URL, and a meeting
title containing a calendar injection. The throttle itself is tested too,
because it is the central promise. No network, no municipality touched.

## Layout

```
SKILL.md                          how an agent should use this
README.md                         this file
scripts/ratsinfo.py               the client
scripts/pdfreport.py              the dependency free PDF writer
references/vendors.md             vendors, URL patterns, prior art
references/recht-und-etikette.md  legal footing and etiquette, German
tests/                            offline mock servers and the test run
```

## Licence

MIT-0, the licence ClawHub applies to published skills. Contributed by
[Alpha Quadrat](https://alpha-quadrat.de), Wuppertal.
