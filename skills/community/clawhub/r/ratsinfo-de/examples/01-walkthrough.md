# Walkthrough: what did this town decide about its schools

A full run, in the order the skill is meant to be used. All output below is
real, produced against the local mock server so that anyone can reproduce
it without touching a municipality.

Start the mock:

```bash
python3 tests/mock_ris.py &
export RATSINFO_MIN_INTERVAL=0     # only for the mock, never in the field
```

## 1. Health check before anything else

```console
$ python3 scripts/ratsinfo.py check http://127.0.0.1:8799/system
endpoint      http://127.0.0.1:8799/system
oparlVersion  https://schema.oparl.org/1.1/
name          Mock Ratsinformationssystem
product       Mock
vendor        https://example.org
contactEmail  info@example.org
license       https://www.govdata.de/dl-de/by-2-0
body          Stadt Musterhausen
  paper        http://127.0.0.1:8799/papers
  meeting      http://127.0.0.1:8799/meetings
```

Three things to take from this before crawling anything:

- `oparlVersion` proves this really is an OParl endpoint and not a
  redirected frontend.
- `license` says the documents are DL-DE/BY-2.0, so they may be reused with
  attribution. When this line is missing, nothing has been said, and the
  law applies rather than an assumption.
- `contactEmail` is the operator. If anything is blocked later, that address
  is the cheap way in.

## 2. Search the papers

```console
$ python3 scripts/ratsinfo.py papers http://127.0.0.1:8799/system --term Sanierung
27/2026              Sanierung Erich-Kaestner-Schule
  date 2026-03-01   type Beschlussvorlage
  http://127.0.0.1:8799/paper/0
  main http://127.0.0.1:8799/files/0.pdf
29/2026              Sanierung kommunaler Sportstaetten
  date 2026-03-01   type Beschlussvorlage
  http://127.0.0.1:8799/paper/2
  main http://127.0.0.1:8799/files/2.pdf

2 matching of 3 scanned. OParl has no full text
search, so this is a client side filter over titles and reference
numbers. A document whose subject only appears inside the PDF will
not be found here. Narrow with --since, widen with --max-pages.
```

The three papers are served across two pages by the mock, deliberately. The
client followed `links.next` to reach the third. Do not trust
`pagination.totalPages`; several real systems omit it or get it wrong.

## 3. Follow the object

```bash
python3 scripts/ratsinfo.py get http://127.0.0.1:8799/paper/0
```

Prints the raw OParl JSON with `mainFile.accessUrl` and any
`auxiliaryFile`, so the PDF itself can be fetched and read.

## In the field

Against a real municipality the same three steps look like this, and the
throttle stays at one request per second:

```bash
python3 scripts/ratsinfo.py find Münster
python3 scripts/ratsinfo.py check https://oparl.stadt-muenster.de/system
python3 scripts/ratsinfo.py papers https://oparl.stadt-muenster.de/system \
    --term Schule --term Sanierung --since 2026-01-01 --limit 25
```

Always give a big city a date floor. Without `--since` you are paging
through years of records one second at a time, which is rude and slow in
equal measure.

## The question the list does not answer

A list of papers always provokes the same follow up: what became of it?

```console
$ python3 scripts/ratsinfo.py track http://127.0.0.1:8799/paper/0
27/2026  Sanierung Erich-Kaestner-Schule
  type Beschlussvorlage   tabled 2026-03-01
  status: decided on 2026-03-10: beschlossen

  2026-02-11   Bauausschuss
               Vorberatung   result: zur Kenntnis genommen
* 2026-03-10   Rat der Stadt
               Entscheidung   result: beschlossen

* marks the authoritative consultation, the one that decides.
```

That timeline comes from the chain Paper to Consultation to AgendaItem to
Meeting. It costs no PDF reading, and no council frontend shows it in one
view. When a paper has been tabled but never decided, the status line says
`pending since <date>` instead, which is usually the more interesting
answer.

## Watching without crawling

```console
$ python3 scripts/ratsinfo.py watch http://127.0.0.1:8799/system --term Sanierung
since 2026-08-12T12:22:48
NEW  27/2026              Sanierung Erich-Kaestner-Schule
     http://127.0.0.1:8799/paper/0
NEW  29/2026              Sanierung kommunaler Sportstaetten
     http://127.0.0.1:8799/paper/2

2 new, 0 withdrawn, 2 matching in window.
```

Run it again and it reports `0 new`, because it stored the timestamp and
asks the server only for what changed since. That is the only server side
filter OParl offers, and the specification obliges every server to support
it. Add `--kind meeting --ics rat.ics` and the upcoming sittings land in a
calendar.
