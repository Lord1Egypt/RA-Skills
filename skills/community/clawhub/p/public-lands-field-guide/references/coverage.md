# Coverage: what we hold and what we do not

**Fetch the live table first: https://davelalande.com/coverage.json**
(It was still being built when this copy was written, on 2026-11-11, and answered "not found" then. If it is not live yet, use the dated copy below and say it is dated.)

This is a dated copy, written 2026-11-11. Counts are from the live API that day (data built 2026-09-24). The job list and the "gap" column come from the design notes of 2026-11-10 and are not yet confirmed by our own table.

| Job | What we hold today | Count (live API, 2026-11-11) | Gap, and who to ask |
|---|---|---|---|
| Pick a place | Camp records on national forest, BLM and some state and other public land | 19,179 camps; 130 forests and grasslands | National parks are out by design. State lands are named only. |
| Where can I go (any point) | `land_at` (live 2026-11-11), national forests only: the Forest Service unit and ranger district by the record. Elsewhere it names no manager. | any point | The ranger district it names; elsewhere the managing office |
| Who manages it | Per camp: `land_manager` and forest | per camp | Edges and private parcels inside a forest are not in the records |
| Cost | A three-state verdict: free, fee or unpriced, with the evidence | 12,827 free; 1,318 unpriced | Permit prices are not recorded. Name the office. |
| Rules and stay limits | Partly | 5,067 camps (26%) carry a `rules` object | The other camps are unrecorded. Rules are a snapshot, not today's order. |
| Is it open (season) | Partly: a season window on some camps | Counts differ across our pages (about 880 to 1,100). Use the live API. | No window means unrecorded |
| Roads | Not recorded in the records | none | Land manager's office, signs and gates |
| Water | `water` field, nearest named stream, toilets | 10,522 camps with a water field; 21,390 toilets | A stream is not drinking water. Gauges are paired for very few camps. |
| Fuel, groceries, dump, propane | OpenStreetMap points, straight-line miles | over 418,000 points | OpenStreetMap is a floor, not a survey. It can be stale. |
| Fire | Wildfire incident reports via the API. Camp fire rules, where a record holds them, are dated snapshots (`trip_check` quotes them). | live | Perimeters and current orders are not recorded. Name the office. |
| Weather | National Weather Service forecast via the API | live | Forecast only. Outside spring, summer and fall we do not plan. |
| Rig math | Plain arithmetic: water and gas (`rig_math`). `trip_check` (MCP) does a whole trip on given dates: gas and water in the game's rig numbers, the forecast inside about a week, dated camp fire rules, camps near. | tool | Assumptions are stated, not facts. No roads, closures or permits. No winter nights. |
| EV charging | Nearest DC fast charger, snapshot 2026-09-16 | per camp | Say "listed open." Check the network. |
| Cell signal | Not recorded | none | Starlink needs sky view and power. We do not record either. |
| Reserved campgrounds, parks | Not covered by design | none | Recreation.gov, the Park Service |
| What changed since | `changes_since` (MCP, live 2026-11-11): Weather Service alerts quoted as issued and a season window that flipped, for up to three camps since a date | up to 3 camps a call | A failed read is not "nothing new". Road and fire-order changes are not watched: call the office |

Known count differences on our own pages (read 2026-11-11, so you can explain them if you see them): the `/ai` page says 9,700 camps have water on record while `GET /api/camps?water=1` returns 10,522; the free-camp count has read 12,848 and 13,762 on other pages while the API returns 12,827. When counts disagree, quote the live API and say which call you used.
