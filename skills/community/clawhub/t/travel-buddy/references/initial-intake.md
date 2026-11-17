# Initial intake and preference map

Use this reference after the first response is gathered or when the user asks for a detailed intake. The goal is a sufficiently reliable decision profile, not exhaustive personal data.

**This file describes the questions, not a licence to ask them in chat.** The loopback HTML form asks them; the conversation design below is what the form encodes and what a chat fallback must cover when the traveller has declined the form. Chat is theirs to choose, not yours — see SKILL.md section 1, and note that `save_trip_deliverables.py` refuses any plan whose `intake_context` does not say which route was taken, with the traveller's own declining words when it was `chat_fallback`.

<a id="conversation-design"></a>
## Conversation design

Collect information in descending order of decision impact:

1. Origin and travel window determine what is reachable at all.
2. Duration, party, budget scope, and destination scope determine the realistic candidate set.
3. Experience direction chooses the type of trip, not merely attractions.
4. Entry, health, climate, transport, and avoid-list constraints eliminate false positives.
5. Comfort and pace refine trade-offs among otherwise feasible options.

For a first-time user, or a user without a valid reusable profile, use `python scripts/start_intake_workflow.py --assistant auto`, adding `--language en` when the conversation is in English. It first opens `assets/traveler-profile-intake.html` for one-time consented stable preferences, then automatically opens `assets/trip-intake-form.html` for this trip. When one valid profile already exists, it skips the profile form and pre-fills stable values in the trip form. Both forms speak Chinese or English and carry a switch: they open in `--language` when given, else in the saved profile's preferred output language, else in Chinese, and a first-time traveller's trip form follows the profile they have just saved. Only the words change — every stored value is identical in both languages — and the saved intake records `form_language` and `preferred_output_language`, which `new_plan_skeleton.py --from-intake` uses as the plan's language. The trip form's entry question is a yes/no, described in the next two paragraphs: does this trip need a visa the traveller does not already hold? Only "yes" collects identity — each traveller's passport nationality, residence country, and residence-status category, never document identifiers, images, or validity dates. It always captures one-way transport tolerance, current-window climate preferences, and the actual usable modes: high-speed rail, conventional/night rail, intercity bus, ferry, flight, and self-drive. The server also rejects saved payloads with document, payment, password, or exact-address fields. After submission, the terminal writes a `trip-profile.json`-compatible intake and a `next-action-*.json` workflow event naming the next step (`trip_construction` for a fixed destination, otherwise `destination_discovery`), then prints `TRAVEL BUDDY TRIP INPUT: <path>`; you read that intake and continue in the session you are already in. Under `--assistant auto` it never launches a second assistant, on any harness and from any terminal. Two earlier versions tried to detect when spawning was safe — first by recognising assistant names, then by a tty test — and each let an unattended planner start beside the one already working: opencode, Cursor and Cline set none of the recognised variables and allocate a full pty, so neither test recognised an assistant already at work. That produced two divergent plans in one workspace, the unattended one built from the un-clarified intake this form hands over. Start the workflow as a **background/non-blocking** command, or with `--detach`: it blocks in `serve_forever()` until the traveller submits, so a foreground run withholds the link and then dies on the harness's command timeout. It never resumes an arbitrary most-recent CLI conversation. Continuation is opt-in: `--assistant codex` or `--assistant claude` (or `TRAVEL_BUDDY_ASSISTANT=codex|claude`) starts one anyway, and `--assistant none` says so explicitly.

The scope question is a yes/no on whether this trip needs a visa the traveller does not already hold (`no_new_visa_needed`, `any_including_visa`), not whether the trip is domestic or cross-border, and not how much visa effort is acceptable. Intakes saved with the older `domestic` / `cross_border` / `domestic_or_cross_border` / `home_country_only` / `visa_free_only` values are still accepted and mapped forward.

`no_new_visa_needed` collects two fields — `feasibility.held_entry_documents`, a free-text note on what the traveller enters on, and `passport_validity_status`, which is still required because a held visa does not rescue an expired passport and this answer also covers people who are leaving the country. Its `not_applicable_domestic` value must be selected, never inferred. It sets `entry_status: traveler_asserts_can_enter`. Treat that string as a hard destination filter: candidates are limited to what the named document actually admits them to. `any_including_visa` is the only answer that opens the effort sub-question and the per-traveller identity panel; identity is prefilled from the profile's nationality, residence country, and residence-status category.

The current-trip form asks for exact `start_date`/`end_date` when the traveller has them and falls back to month plus duration otherwise; it cross-checks the two so a stated date range and a stated day count cannot disagree. It also collects trip purpose, any fixed commitment the trip must fit around, dietary or religious food restrictions, and — only when the trip may leave the country of residence — a `valid_through_trip` / `not_sure` / `needs_renewal` passport-validity status, never a number or an expiry date. A `fixed` or `anchored` destination scope must name at least one place: a fixed scope with no destination used to start a Construction handoff with nothing to construct. Detail that only matters after a destination is chosen (rooms, breakfast, cancellation, cabin, baggage, rail/bus comfort, map and platform preferences) sits in collapsed optional blocks so the discovery questions stay legible.

Treat form choices as this trip’s source of truth. Prefill only compatible stable profile values (for example home city, airports, usual currency, pace, recurring interests, accessibility, dietary needs, `never_recommend` exclusions, avoid-list and normal service access), and let an edited form field win. Do not use profile language, currency, or map app to guess how far the traveller wants to go: require the explicit scope selection. Profile nationality, residence country, and residence-status category are used for the separate question of what entry each candidate destination needs — never to infer scope. Use the selected modes—not a profile’s generic flight or self-drive habit—to decide whether flight, rail, bus, ferry, or rental-car research is needed. Resolve any conflict between a selected scope and a named destination before ranking.

Use a compact chat card only when the user cannot or explicitly does not want to use the local form. Present choices as examples, not a closed form. If the user answers only part of the card, acknowledge it and ask the one or two omitted fields that most affect their request. Do not repeat information already supplied.

## Origin and access

Capture:

- home/departure city and country;
- acceptable airports, including nearby airports only if the extra ground travel is acceptable;
- maximum door-to-door or flight-only travel time; transfer and overnight tolerance;
- ability/willingness to drive, use rail, or cross a nearby border for an airport;
- whether departure is constrained by work, school, or a fixed event.

Do not infer an airport solely from a city. For example, a traveler in a metropolitan area may prioritize a low-cost secondary airport, rail, a direct flight, or minimal ground transfer differently.

<a id="budget-model"></a>
## Budget model

Capture the **per-person** number, currency, and scope before using it to rank destinations. Compute a party total only as a separately labeled multiplication by traveler count.

| Ask | Normalize as | Why it matters |
| --- | --- | --- |
| “€1,500” | per-person amount + currency + confidence | The standard intake basis is per person. |
| “For both of us” | traveler count for a separately labeled derived total | Prevents per-person/all-party errors. |
| “Including flights and hotels” | included categories | Makes candidate totals comparable. |
| “Could stretch a little” | target + hard ceiling | Enables honest trade-offs. |
| “I want comfort, not luxury” | lodging/comfort preference | Prevents an unrealistic lodging assumption. |

Default only after disclosure: use an all-in, per-person estimate including that traveler’s share of round-trip transport, accommodation, local transport, food, activities, insurance/entry costs where material, and a modest contingency. State categories that cannot yet be estimated.

## Destination scope

Use one explicit state:

| Scope | Interpretation | Next action |
| --- | --- | --- |
| `fixed` | The traveler has chosen a specific country, region, or city. | Validate feasibility; do not replace it without invitation. |
| `anchored` | A country/region is strongly preferred but alternatives are welcome. | Compare it with relevant alternatives and explain the trade-off. |
| `continent` | A broad geography is intended. | Search across that geography; check entry and travel-time variation. |
| `open` | No geography selected. | Start globally, then curate a diverse, feasible short list. |

Ask whether a named place is a must, a wish, or inspiration. A country-sized choice is not enough to start a city-level itinerary: retain room to compare its regions and arrival airports.

<a id="experience-taxonomy"></a>
## Experience and scenery taxonomy

Start with the high-level direction, then ask the user to pick up to four items, rank the top two, and say whether each is a trip centerpiece or a bonus. Let the user add an unlisted item.

### Natural

- coast, islands, beaches, swimming, sailing, surfing, or diving;
- mountains, viewpoints, hiking, alpine landscapes, cable cars, or scenic trains;
- lakes, forests, rivers, waterfalls, and slow nature stays;
- desert, volcanoes, caves, dramatic geology, or road-trip scenery;
- wildlife, birding, marine life, safari, or seasonal migration;
- snow sports, aurora, autumn color, spring flowers, or other seasonal phenomena;
- tropical forest, jungle, hot springs, or wellness-in-nature;
- cycling, paddling, climbing, photography, or other activity-led nature travel.

Clarify intensity: “view from a comfortable base,” “short walks,” “day hikes,” or “multi-day physical activity.” Never infer hiking tolerance from an interest in mountains.

### Human / cultural

- history, archaeology, heritage sites, old towns, architecture, or religious sites;
- museums, art, design, literature, film, or creative neighborhoods;
- local food, markets, cooking, wine/coffee/tea, or regional specialties;
- everyday street life, villages, crafts, language, and local community encounters;
- music, dance, nightlife, festivals, sport, or live performance;
- fashion, shopping, contemporary city energy, or technology/design scenes;
- wellness, slow living, spa, meditation, or retreat-style experiences;
- specific interests such as genealogy, photography, train travel, or a personal event.

Clarify depth: “see landmark highlights,” “one or two deep experiences,” or “make this the main purpose of the trip.” Do not equate cultural interest with crowded capital cities; offer quieter regional options where appropriate.

### Balance, pace, and negatives

For a balanced trip, ask for the intended split (for example, primarily nature with two culture/food days). Also record what reduces enjoyment: extreme crowds, resorts, heavy nightlife, long drives, repeated hotel changes, organized tours, heat, humidity, rain, altitude, or tourist traps.

## Feasibility and dignity

Ask sensitively and only when relevant. In particular, first establish whether cross-border travel is in scope:

- only when the trip may leave the country of residence: passport nationality, residence country, residence-status category, and a yes/not-sure/needs-renewal answer on whether every passport stays valid six months past the trip—never a document identifier, image, or expiry date, and never when the traveller is staying home. Acceptable visa effort follows from the scope answer and is not asked again;
- mobility, injury, pregnancy, sensory needs, and medical logistics only to adapt the plan;
- dietary, religious, family, safety, language, connectivity, and privacy needs;
- realistic tolerance for transfers, red-eye flights, self-driving, crowds, and isolation.

<a id="machine-readable-values"></a>
### Two answers must leave the interview as machine-readable values

Most of what the intake collects can stay in the traveller's own words. Two cannot, because the
gates measure them rather than read them, and nothing converts a sentence into either:

- **The walking limit** becomes `trip.traveler_constraints.max_continuous_walking_minutes`, a
  number of minutes. "I can't walk far" is not one. Ask for the figure directly — *"roughly how
  many minutes can you walk at a stretch before you'd want to sit down?"* — and accept a rough
  answer, because 30 is a usable constraint and "not far" is not. Left as prose the field stays
  null, and every per-leg and per-activity walking check silently passes on a plan built around
  a limit nobody measured.
- **A dietary restriction's severity** becomes `allergy_severity`, one of `none`, `preference`,
  `intolerance`, `anaphylactic`. Ask which it is rather than inferring it: the enum decides
  whether the trip gets the light or the full verification tier, and "I avoid dairy" covers both
  a preference and a hospital visit.

`new_plan_skeleton.py --from-intake` copies the prose lists across and says on stderr that it has
left both of these at their defaults, because a script cannot turn a sentence into a severity or a
number. Type them in yourself before delivering, or the plan asserts in its own prose that a
constraint is severe while its fields say there is nothing to avoid.

Phrase the reason for every sensitive question: “This affects entry options” or “I can choose low-walking alternatives.” Treat a non-answer as an unknown, not consent to assume.

## Profile completeness thresholds

Proceed to a **tentative inspiration list** when origin, approximate window/duration, rough budget, destination scope, and broad experience direction are known. Mark it exploratory.

Proceed to a **ranked recommendation** only when the preceding fields plus party and the relevant high-impact filters (usually entry, travel-time, weather, and major mobility constraints) are known or explicitly assumed.

Proceed to a **bookable trip plan** only when dates, traveler count, entry status and passport validity, budget scope, accommodation expectations, and mobility requirements are confirmed. Verify volatile facts immediately before the user acts.
