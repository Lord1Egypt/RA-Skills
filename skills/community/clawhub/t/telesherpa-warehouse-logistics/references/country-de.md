# Country module: Germany

Use this file when intake 18 is German. It sets **display labels** only. Keys,
option values (`frei`, `gebunden`, `gesperrt`, `putaway`, `pick`, `relocate`,
`count`) and tool names stay as in the rest of the skill. This skill does not
give legal advice; working rules appear as intake answers (who may bind, who may
book, which units such as `kg` or `Stk`).

## Display labels

| Key | Suggested label |
|---|---|
| `label` | Etikett |
| `package` | Gebinde |
| `storage` | Lagerplatz |
| `stockMovement` | Lagerbewegung |
| `labelStatus` | Etikett-Status |
| `frei` (value unchanged) | Frei |
| `gebunden` (value unchanged) | Gebunden |
| `gesperrt` (value unchanged) | Gesperrt |
| `code` | Code |
| `charge` | Charge (Druckcharge) |
| `menge` | Menge |
| `einheit` | Einheit |
| `lot` | Charge (Los) |
| `bestBefore` | Mindesthaltbar bis |
| `movementType` | Art der Bewegung |
| `putaway` (value unchanged) | Einlagern |
| `pick` (value unchanged) | Entnehmen |
| `relocate` (value unchanged) | Umlagern |
| `count` (value unchanged) | Inventur |
| `grund` | Grund |
| `bookingTime` | Zeitpunkt |
| `bookedBy` | Gebucht von |
| `label_bind` | Etikett binden |
| `label_rebind` | Etikett umhängen |
| `stock_putaway` | Einlagern |
| `stock_pick` | Entnehmen |
| `stock_relocate` | Umlagern |
| `stock_count` | Inventur zählen |

## Print

The sheet is Avery Zweckform 3475 (70 × 36 mm, 24 per A4). The charge id and the
readable code stay on the sheet so staff can talk about a sticker without opening
the app.

## Notes

A list of packages with `menge` is the book quantity per package. It is the
figure the bookings maintain. Keep food-hygiene or customs records in the form
the business already uses; do not treat the package list as a substitute for a
statutory stock book unless the customer has decided that with their advisor.
