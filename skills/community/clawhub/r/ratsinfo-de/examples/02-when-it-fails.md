# When it fails, and what the failure means

Three quarters of the work in this field is recognising a dead end quickly.
All three cases below are real and all three are reproducible offline:

```bash
python3 tests/mock_broken.py &
```

## The endpoint exists and is switched off

```console
$ python3 scripts/ratsinfo.py check http://127.0.0.1:8798/dead
error: http://127.0.0.1:8798/dead answers with an OParl error: OParl is not
active.. The endpoint exists but is switched off. This is common in the
public registry.
```

A real example is `https://edenkoben.gremien.info/oparl/system`. The host
answers, the URL is right, the software is installed, and the interface is
simply turned off. The registry does not know that. This is why the health
check comes before the crawl.

What to tell the user: this town has a council system with an OParl
interface that is not switched on. The documents are still on the web
frontend for a human to read.

## A bot check page instead of JSON

```console
$ python3 scripts/ratsinfo.py check http://127.0.0.1:8798/botcheck
error: http://127.0.0.1:8798/botcheck did not return JSON (Content-Type: unset).
  First characters: 'Zugriff pruefen Zum Schutz vor automatisierten Zugriffen
  ist die folgende Pruefung einmalig notwendig'
  A bot check page here usually means CC e-gov ALLRIS. Those
  endpoints need a browser session and are out of scope.
```

CC e-gov puts this page in front of its installations. It is not a bug and
it is not something to defeat. Treat ALLRIS towns as unavailable through
this route and say so.

## robots.txt forbids the API path

```console
$ python3 scripts/ratsinfo.py check http://127.0.0.1:8798/blocked
error: robots.txt on 127.0.0.1:8798 disallows this path.
  Several council systems block their own OParl endpoint with a
  blanket rule aimed at search engines. Ask the operator (the
  contactEmail in the System object) for permission, then repeat
  with --ignore-robots.
```

This is the strangest case in the whole field: an interface built for
machines, closed to machines. It is almost never deliberate. Somebody wrote
`Disallow: /` to keep the council frontend out of search results, and the
API path sits underneath it.

The correct response is a short mail to the address in `contactEmail`, not
a flag. `--ignore-robots` is for after the answer comes back, and for
nothing else.
