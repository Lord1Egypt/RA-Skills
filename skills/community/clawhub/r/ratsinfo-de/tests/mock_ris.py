#!/usr/bin/env python3
"""A minimal, well behaved OParl 1.1 server for offline tests.

Serves a System object, one Body, a paginated Paper list across two pages
and a Meeting list, so the client's pagination, filtering and field
handling can be exercised without touching a real municipality.

    python3 tests/mock_ris.py &
    python3 scripts/ratsinfo.py check http://127.0.0.1:8799/system
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import os

PORT = int(os.environ.get("MOCK_PORT", "8799"))
TOWN = os.environ.get("MOCK_TOWN", "Stadt Musterhausen")
AGS = os.environ.get("MOCK_AGS", "05124000")
BASE = f"http://127.0.0.1:{PORT}"

PAPERS = [
    {
        "id": f"{BASE}/paper/{i}",
        "type": "https://schema.oparl.org/1.1/Paper",
        "created": "2026-01-01T00:00:00+00:00",
        "modified": "2026-01-01T00:00:00+00:00",
        "name": name,
        "reference": reference,
        "paperType": "Beschlussvorlage",
        "date": "2026-03-01",
        "mainFile": {
            "id": f"{BASE}/file/{i}-main",
            "type": "https://schema.oparl.org/1.1/File",
            "name": "Beschlussvorlage der Verwaltung",
            "fileName": f"vorlage-{i}.pdf",
            "mimeType": "application/pdf",
            "size": 428317,
            "accessUrl": f"{BASE}/files/{i}.pdf",
        },
        "auxiliaryFile": [
            {
                "id": f"{BASE}/file/{i}-a1",
                "type": "https://schema.oparl.org/1.1/File",
                "name": "Anlage 1: Kostenberechnung nach DIN 276",
                "mimeType": "application/pdf",
                "size": 1142880,
                "accessUrl": f"{BASE}/files/{i}-a1.pdf",
            },
            {
                "id": f"{BASE}/file/{i}-a2",
                "type": "https://schema.oparl.org/1.1/File",
                "name": "Anlage 2: Schadstoffgutachten Bestandsgebaeude",
                "mimeType": "application/pdf",
                "size": 3310992,
                "accessUrl": f"{BASE}/files/{i}-a2.pdf",
            },
            {
                "id": f"{BASE}/file/{i}-a3",
                "type": "https://schema.oparl.org/1.1/File",
                "name": "Anlage 3: Terminplan Bauabschnitte",
                "mimeType": "application/pdf",
                "size": 220160,
                "accessUrl": f"{BASE}/files/{i}-a3.pdf",
            },
        ],
        "keyword": ["Schulbau", "Sanierung", "Schadstoffe", "Ganztag"],
        "underDirectionOf": [f"{BASE}/org/fb65"],
        "originatorPerson": [f"{BASE}/person/1"],
        "location": {
            "id": f"{BASE}/location/1",
            "type": "https://schema.oparl.org/1.1/Location",
            "description": "Erich-Kaestner-Schule, Schulstrasse 14",
        },
        "relatedPaper": [f"{BASE}/paper/2"],
        "consultation": [f"{BASE}/consultation/{i}a", f"{BASE}/consultation/{i}b"],
    }
    for i, (name, reference) in enumerate(
        [
            ("Sanierung Erich-Kaestner-Schule", "27/2026"),
            ("Neubau Feuerwache Mitte", "28/2026"),
            ("Sanierung kommunaler Sportstaetten", "29/2026"),
        ]
    )
]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep test output clean
        pass

    def _json(self, payload):
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]

        if path == "/robots.txt":
            body = b"User-agent: *\nAllow: /\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/system":
            return self._json(
                {
                    "id": f"{BASE}/system",
                    "type": "https://schema.oparl.org/1.1/System",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "oparlVersion": "https://schema.oparl.org/1.1/",
                    "name": "Mock Ratsinformationssystem",
                    "product": "Mock",
                    "vendor": "https://example.org",
                    "contactEmail": "info@example.org",
                    "license": "https://www.govdata.de/dl-de/by-2-0",
                    "body": f"{BASE}/body",
                }
            )

        if path == "/body":
            return self._json(
                {
                    "data": [
                        {
                            "id": f"{BASE}/body/1",
                            "type": "https://schema.oparl.org/1.1/Body",
                            "created": "2026-01-01T00:00:00+00:00",
                            "modified": "2026-01-01T00:00:00+00:00",
                            "name": TOWN,
                            "paper": f"{BASE}/papers",
                            "meeting": f"{BASE}/meetings",
                            "person": f"{BASE}/people",
                            "ags": AGS,
                            "rgs": AGS + "0000",
                        }
                    ],
                    "links": {"self": f"{BASE}/body"},
                }
            )

        # deliberately paginated, so the client has to follow links.next
        if path == "/papers":
            return self._json(
                {
                    "data": PAPERS[:2],
                    "links": {"self": f"{BASE}/papers", "next": f"{BASE}/papers2"},
                }
            )

        if path == "/papers2":
            return self._json({"data": PAPERS[2:], "links": {"self": f"{BASE}/papers2"}})

        if path == "/meetings":
            return self._json(
                {
                    "data": [
                        {
                            "id": f"{BASE}/meeting/1",
                            "type": "https://schema.oparl.org/1.1/Meeting",
                            "created": "2026-01-01T00:00:00+00:00",
                            "modified": "2026-01-01T00:00:00+00:00",
                            "name": "Rat der Stadt Musterhausen",
                            "start": "2026-03-10T17:00:00+01:00",
                        }
                    ],
                    "links": {"self": f"{BASE}/meetings"},
                }
            )

        # deliberately hostile and malformed responses, for the guard tests
        if path == "/evil-system":
            return self._json(
                {
                    "id": f"{BASE}/evil-system",
                    "type": "https://schema.oparl.org/1.1/System",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "oparlVersion": "https://schema.oparl.org/1.1/",
                    "name": "Hostile",
                    "body": f"{BASE}/evil-body",
                }
            )

        if path == "/evil-body":
            # a link pointing at a different host
            return self._json(
                {
                    "data": [],
                    "links": {"next": "http://127.0.0.1:8798/dead"},
                }
            )

        if path == "/dirty-system":
            return self._json(
                {
                    "id": f"{BASE}/dirty-system",
                    "type": "https://schema.oparl.org/1.1/System",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "oparlVersion": "https://schema.oparl.org/1.1/",
                    "name": "Malformed",
                    "body": f"{BASE}/dirty-body",
                }
            )

        if path == "/dirty-body":
            # data as an object instead of a list
            return self._json({"data": {"not": "a list"}})

        if path == "/relative":
            return self._json(
                {
                    "data": [],
                    "links": {"self": f"{BASE}/relative", "next": "relative2"},
                }
            )

        if path == "/relative2":
            return self._json({"data": []})

        if path == "/nasty-meetings":
            return self._json(
                {
                    "data": [
                        {
                            "id": f"{BASE}/meeting/x",
                            "type": "https://schema.oparl.org/1.1/Meeting",
                            "created": "2026-01-01T00:00:00+00:00",
                            "modified": "2026-01-01T00:00:00+00:00",
                            "name": "Boese\nATTENDEE:mailto:x@y\nX-EVIL:1; komma, ende",
                            "start": "2026-03-10T18:00:00+02:00",
                        }
                    ],
                    "links": {"self": f"{BASE}/nasty-meetings"},
                }
            )

        if path.startswith("/paper/"):
            index = path.rsplit("/", 1)[1]
            if index.isdigit() and int(index) < len(PAPERS):
                return self._json(PAPERS[int(index)])
            self.send_response(404)
            self.end_headers()
            return

        # the consultation chain, so track can be exercised offline
        if path.startswith("/consultation/"):
            key = path.rsplit("/", 1)[1]
            index, stage = key[:-1], key[-1]
            return self._json(
                {
                    "id": f"{BASE}{path}",
                    "type": "https://schema.oparl.org/1.1/Consultation",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "paper": f"{BASE}/paper/{index}",
                    "role": "Vorberatung" if stage == "a" else "Entscheidung",
                    "authoritative": stage == "b",
                    "organization": [f"{BASE}/org/{stage}"],
                    "agendaItem": f"{BASE}/agenda/{key}",
                }
            )

        if path.startswith("/agenda/"):
            key = path.rsplit("/", 1)[1]
            stage = key[-1]
            return self._json(
                {
                    "id": f"{BASE}{path}",
                    "type": "https://schema.oparl.org/1.1/AgendaItem",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "number": "4.1" if stage == "a" else "7.2",
                    "name": "Sanierung Erich-Kaestner-Schule, Bauabschnitt 1",
                    "public": True,
                    "result": "zur Kenntnis genommen und zur Entscheidung "
                    "an den Rat verwiesen"
                    if stage == "a"
                    else "einstimmig beschlossen",
                    "resolutionText": (
                        "Der Bauausschuss nimmt die Kostenberechnung nach DIN 276 "
                        "mit Gesamtkosten von 8.430.000 Euro zur Kenntnis und "
                        "empfiehlt dem Rat, den Bauabschnitt 1 zu beschliessen. "
                        "Die Verwaltung wird gebeten, das Schadstoffgutachten bis "
                        "zur Ratssitzung fortzuschreiben."
                        if stage == "a"
                        else "Der Rat beschliesst die Sanierung der "
                        "Erich-Kaestner-Schule im Bauabschnitt 1 mit Gesamtkosten "
                        "von 8.430.000 Euro. Die Mittel werden im Haushalt 2026 "
                        "bei Produkt 21-101 bereitgestellt. Die Verwaltung wird "
                        "beauftragt, die Vergabe der Planungsleistungen nach "
                        "VgV einzuleiten und dem Ausschuss halbjaehrlich zu "
                        "berichten."
                    ),
                    "resolutionFile": {
                        "name": "Beschlussausfertigung",
                        "accessUrl": f"{BASE}/files/beschluss-{stage}.pdf",
                        "mimeType": "application/pdf",
                    }
                    if stage == "b"
                    else None,
                    "meeting": f"{BASE}/meeting/{stage}",
                }
            )

        if path.startswith("/meeting/"):
            stage = path.rsplit("/", 1)[1]
            return self._json(
                {
                    "id": f"{BASE}{path}",
                    "type": "https://schema.oparl.org/1.1/Meeting",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "name": "Bauausschuss" if stage == "a" else "Rat der Stadt",
                    "start": "2026-02-11T17:00:00+01:00"
                    if stage == "a"
                    else "2026-03-10T17:00:00+01:00",
                    "end": "2026-02-11T19:40:00+01:00"
                    if stage == "a"
                    else "2026-03-10T21:15:00+01:00",
                    "location": {
                        "description": "Rathaus, Ratssaal, Am Markt 1",
                    },
                    "participant": [f"{BASE}/person/{n}" for n in range(1, 18)]
                    if stage == "b"
                    else [f"{BASE}/person/{n}" for n in range(1, 12)],
                    "invitation": {
                        "name": "Einladung mit Tagesordnung",
                        "accessUrl": f"{BASE}/files/einladung-{stage}.pdf",
                    },
                    "resultsProtocol": {
                        "name": "Ergebnisprotokoll",
                        "accessUrl": f"{BASE}/files/protokoll-{stage}.pdf",
                    },
                    "verbatimProtocol": {
                        "name": "Wortprotokoll",
                        "accessUrl": f"{BASE}/files/wortprotokoll-{stage}.pdf",
                    }
                    if stage == "b"
                    else None,
                }
            )

        if path.startswith("/org/"):
            stage = path.rsplit("/", 1)[1]
            names = {
                "a": "Bauausschuss",
                "b": "Rat der Stadt",
                "fb65": "Fachbereich 65 Gebaeudewirtschaft",
            }
            return self._json(
                {
                    "id": f"{BASE}{path}",
                    "type": "https://schema.oparl.org/1.1/Organization",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "name": names.get(stage, "Gremium"),
                }
            )

        if path.startswith("/person/"):
            return self._json(
                {
                    "id": f"{BASE}{path}",
                    "type": "https://schema.oparl.org/1.1/Person",
                    "created": "2026-01-01T00:00:00+00:00",
                    "modified": "2026-01-01T00:00:00+00:00",
                    "name": "Maria Beispiel",
                }
            )

        if path == "/people":
            return self._json(
                {
                    "data": [
                        {
                            "id": f"{BASE}/person/1",
                            "type": "https://schema.oparl.org/1.1/Person",
                            "created": "2026-01-01T00:00:00+00:00",
                            "modified": "2026-01-01T00:00:00+00:00",
                            "name": "Maria Beispiel",
                            "familyName": "Beispiel",
                            "membership": [
                                {
                                    "id": f"{BASE}/membership/1",
                                    "type": "https://schema.oparl.org/1.1/Membership",
                                    "organization": f"{BASE}/org/a",
                                    "role": "Vorsitzende",
                                    "votingRight": True,
                                    "startDate": "2025-11-01",
                                }
                            ],
                        }
                    ],
                    "links": {"self": f"{BASE}/people"},
                }
            )

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
