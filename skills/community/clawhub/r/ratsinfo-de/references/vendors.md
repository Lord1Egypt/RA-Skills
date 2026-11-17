# RIS vendors and their OParl URL patterns

The registry at <https://dev.oparl.org/api/endpoints> is a lower bound, not
a census. Many municipalities run an OParl endpoint and never reported it.
The URL patterns below are stable per vendor, so guessing along the pattern
finds endpoints the registry does not know.

Try one candidate, run `ratsinfo.py check` on it, and stop. Do not sweep a
range of guesses at a municipal data centre.

| Product | Vendor | Typical OParl URL |
|---|---|---|
| Session / SessionNet | SOMACOS GmbH & Co. KG, Salzwedel | `https://<host>/oparl/system` or `https://<host>/system` |
| SD.NET RIM | STERNBERG Software | `https://<town>.ratsinfomanagement.net/webservice/oparl/v1.1/system` |
| more! rubin | more! software GmbH & Co. KG, Montabaur | `https://<town>.gremien.info/oparl/system` |
| ALLRIS, ALLRIS net | CC e-gov GmbH, Hamburg (PDV.group) | `https://<host>/bi/oparl/1.0/system.asp`, `https://<host>/oi/oparl/1.1/system.asp` |
| regisafe | regisafe GmbH, Waiblingen (PDV.group) | OParl support unconfirmed |
| PV-Rat.net / Provox IIP | PROVOX Systemplanung GmbH | no OParl implementation confirmed |
| Rats-Manager | Bartelsoft | unknown |
| KOMMUNE-AKTIV, govgó | various | unknown |

Verified live while building this skill: Köln
(`https://buergerinfo.stadt-koeln.de/oparl/system`, Session 1.6.1, OParl
1.1), Münster (`https://oparl.stadt-muenster.de/system`, Session 1.6.0,
OParl 1.1), Montabaur (`https://montabaur.gremien.info/oparl/system`, more!
rubin, OParl 1.0).

## Shared hosts

Several municipal data centres host many towns on one machine. Throttle per
host, not per town, or a single run multiplies the load on one server:

- `rim.ekom21.de/<town>/webservice/oparl/v1.1/system` (Hesse)
- `sdnetrim.kdvz-frechen.de/rim<NNNN>/webservice/oparl/v1.1/system`
- `sitzungsdienst.kdz-ws.net/gkz<NNN>/webservice/oparl/v1.1/system`
- `sessionnet-oparl.krz.de/oparl/...`

## Fingerprinting

SOMACOS puts the module version into the `vendor` field as a query
parameter, for example `https://www.somacos.de?oparl=v1.6.1`. That is the
cleanest way to identify an installation and its version from the System
object alone.

## Aggregators

Endpoints that carry several municipalities at once:

- `https://oparl.politik-bei-uns.de/system` (Open Knowledge Foundation, OParl 1.0, alive)
- `https://www.muenchen-transparent.de/oparl/v1.0`
- `https://mirror.oparl.org/system` is dead, the host no longer resolves

## Known traps

- The registry contains duplicates, `http://` URLs and hosts that no longer
  exist. Health check first.
- `https://edenkoben.gremien.info/oparl/system` answers with a valid HTTP
  response carrying `"message": "OParl is not active."` An endpoint can be
  present and switched off at the same time.
- more! rubin in its OParl 1.0 form uses `.../oparl/Body` with a capital B.
  Follow the URL out of the System object rather than assembling it.
- ALLRIS installations answer with an HTML bot check page instead of JSON.
  There is no way around that from a script, and there should not be.

## Prior art

Worth reading before extending this skill:

- `meine-stadt-transparent` (MIT, archived November 2023) is the most mature
  code base in this field.
- `mandari` (AGPL-3.0, active) aggregates more than a hundred OParl systems.
- `oparl-bridge` (MIT, active) puts an OParl facade in front of ALLRIS
  installations by driving their frontend with a browser. Note that its
  README attributes ALLRIS to the wrong vendor.
- `scrape-a-ris` scrapes SOMACOS SessionNet HTML without OParl, from the
  days before the API existed.
