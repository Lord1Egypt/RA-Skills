# Country module: Germany

Use this file when intake 5 and 13 are German. It sets **display labels** only.
Keys, option values (`scheduledInspection`, `defect`, `contractMaintenance`, `inspectionProtocol`,
`pass`, `occupationalSafetyCheck`, …) and tool names stay as in the rest of the
skill. This skill does not give legal advice. Intervals, kinds and who must
inspect are intake answers from the business, not a reading of German law.

## Display labels

| Key | Suggested label |
|---|---|
| `serviceOrder` | Auftrag / Prüffrist |
| `dueDate` | Fälligkeit |
| `intervalDays` | Intervall (Tage) |
| `intervalKm` | Intervall (km) |
| `lastDone` | Zuletzt geprüft |
| `kind` | Prüfart |
| `orderKind` | Auftragsart |
| `scheduledInspection` (value unchanged) | Prüffrist |
| `defect` (value unchanged, `orderKind`) | Mangel |
| `contractMaintenance` (value unchanged) | Wartungsvertrag |
| `inspectionProtocol` (value unchanged) | Prüfprotokoll |
| `result` | Ergebnis |
| `pass` (value unchanged) | Bestanden |
| `defect` (value unchanged, `result`) | Mangel |
| `inspectionNote` | Prüfnotiz |
| `orderStatus` | Auftragsstatus |
| `assignedTo` | Zugewiesen an |
| `record_inspection` | Prüfung erfassen |
| `report_defect` | Mangel melden |
| `inspections_overdue` / start card | Überfällig |
| `inspections_due_30` / start card | Fällig in 30 Tagen |
| `inspections_open` / start card | Alle offenen Prüfungen |
| `defects` / start card | Mängel |
| `team_assets` / start card | Mangel melden |
| asset column (`concerns` / `ofAsset`) | Anlage |
| `description` on a defect | Kurzbeschreibung |
| form / prompt `lastdone` | Prüfdatum (JJJJ-MM-TT) |
| form / prompt `nextduedate` | Nächste Fälligkeit (JJJJ-MM-TT) |
| form / prompt `note` | Notiz |
| form `images` | Fotos |
| form `signature` | Unterschrift |
| row action detail link | Öffnen |
| `car` | Fahrzeug |
| `device` | Gerät |
| `tool` | Werkzeug |
| `machine` | Maschine |
| `building` | Standort / Gebäude |
| `organisation` | Organisation |

## Kind labels (option values unchanged)

| Value | Suggested label |
|---|---|
| `occupationalSafetyCheck` | UVV |
| `periodicVehicleInspection` | HU |
| `electricalTest` | DGUV V3 |
| `fireExtinguisher` | Feuerlöscher |
| `ladder` | Leiter |
| `oilChange` | Ölwechsel |
| `contractMaintenance` | Wartungsvertrag |

Example calendar intervals that a German workshop may give in the intake — use
only what the business confirmed, never as a default: occupational safety check
and electrical test often 365 days, periodic vehicle inspection often 730 days,
oil change often 365 days (and optionally a kilometre interval). These figures
are not statutory advice.

## Notes

The lists show open duties and defects. They are the book the manager works
from. Keep any statutory logbook, sticker or protocol the business already uses
in the form their advisor has set; do not treat these views as a substitute
unless the customer has decided that with their advisor.
