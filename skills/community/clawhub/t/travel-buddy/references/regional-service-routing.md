# Regional service routing

Read this reference whenever selecting map, transport, hotel, flight, ticket, car-rental, or local-payment-adjacent browsing links. A global brand is never the default merely because it is familiar.

## Decide the service context

For each trip, record these fields in `regional_service_context` before rendering the final page:

- `destination_service_market`: where the route and booking will actually be used (for example `mainland_china`, `japan`, `south_korea`, `global`), not the traveller's nationality alone.
- `selection_basis`: destination coverage, traveller access without a workaround, language/currency, requested transport mode, and any explicit user preference or exclusion.
- `google_services_access`: `available`, `unavailable`, or `unknown`. It means accessible without a VPN, proxy, credential sharing, or other circumvention.
- `primary_map_provider`, any checked alternative providers, and the authoritative local transit/road sources used for decisions.
- `booking_platform_selection_note` and one `booking_access_checks` record for every booking category actually shown. A check records the local channel, access status, known non-sensitive requirements, source URL, and check time.

Ask only if the answer can change the plan. For an open-destination discovery request, retain the preference as a constraint and choose the detailed provider only after a destination is selected. Never ask for an account name, password, payment method, or device identifier.

<a id="routing-policy"></a>
## Routing policy

1. Prefer a map or transport service with reliable destination coverage and normal local access for the user's route and transport mode.
2. Prefer official transit, rail, road, venue, and tourism sources for schedule, fare, restrictions, and tickets; use mapping links for navigation, not as the sole proof of a timetable or entry rule.
3. Use a global map only when it is usable in the trip market and by the traveller without a workaround. Do not tell a user to use a VPN, proxy, sideloaded application, login workaround, or an app account.
4. Label every generated primary map button with its real provider. Offer one checked alternative only when it materially improves access or resilience; do not add a speculative fallback.
5. Do not manufacture provider deep links. Use a verified browse-only URL returned by current research, omit checkout/login/session URLs, and record the check time. A route button must contain the actual researched endpoints and a mode; a destination/POI page is never an acceptable substitute.

## Non-map service checks

Treat the ability to **open** a result and the ability to **complete a booking** as separate facts. The final page only opens browse links; it must never test a login, payment, checkout, account, or private app session.

For every live booking category included in the final page, record a `booking_access_checks` item with:

```json
{
  "category": "accommodation",
  "access_status": "available | limited | unknown",
  "provider_or_channel": "direct property plus selected comparison platform",
  "requirements_note": "non-sensitive constraints only; for example a local phone may be required",
  "source_url": "https://verified-browse-only-source.example",
  "checked_at": "ISO-8601 timestamp"
}
```

Required categories are `accommodation` for every final plan, plus `flight`, `attraction_ticket`, or `rental_car` when that option type is present. Add `rail_or_ground` whenever a rail, intercity bus, ferry, or public-transit ticket is an essential part of the plan.

- **Flights:** compare a direct airline with a suitable marketplace only after checking route coverage, displayed currency, baggage/fare conditions, and whether the traveller can normally use the channel. Do not make a flight look purchasable merely because its search result is visible.
- **Accommodation:** compare the direct property with locally suitable marketplace(s). Check tax/fee display, cancellation terms, date/guest/room prefill, and any non-sensitive local access limitation. A global marketplace is never mandatory.
- **Rail, buses, ferries, and city transport:** use the official operator for timetable, fare, disruption, ticket eligibility, and conditions; a route planner is not enough. State whether the plan is a route-only instruction, a user-opened sales browse link, or an unverified purchase step.
- **Attractions:** use the venue or authorised distributor. Verify whether a timed slot, named ticket, local phone, or identity check is material without asking the traveller to disclose document numbers or account details.
- **Rental cars:** check licence/translation eligibility, minimum age, debit/credit-deposit conditions, transmission, fuel, mileage, local restricted zones, tolls, parking, and cross-border rules. Do not infer payment-deposit compatibility from nationality or a generic marketplace listing.

`limited` is not an automatic exclusion: show the limitation, preserve an alternative direct/official browse source when possible, and ask a single targeted question only if it changes feasibility. `unknown` means the final page must say recheck before purchase; it cannot be presented as a confirmed purchasing path.

### Mainland China

- Use **Amap / 高德地图** as the primary route-link candidate for routes in mainland China unless the user requests a different accessible provider and it is verified. Use its [official URI/directions capability](https://lbs.amap.com/api/uri-api/guide/travel/route) for a normal user-opened route link; do not require an API key in the final HTML. The final navigation URI must be `https://uri.amap.com/navigation` with non-empty `from`, `to`, and `mode` parameters. A `ditu.amap.com/place/...` page is useful only as a venue reference and must never be presented as a route.
- Do not make Google Maps the primary map or only route link for mainland-China routes. Treat `google_services_access` as `unavailable` unless the user explicitly says otherwise; even then, retain an accessible local primary route link.
- When useful and verified, offer Baidu Maps or Tencent Maps as a clearly labelled alternative. For transit fare/service decisions, cross-check the relevant city metro/bus operator or rail operator rather than inferring details from a route display.
- Choose flight, hotel, train, ticket, and car platforms by the actual route, user language/currency, and the providers' legitimate local availability. A direct airline/property/operator link plus a suitable local or international comparison source is preferable to assuming a single global marketplace is best.
- For self-drive, research driver-eligibility, licence/translation rules, city restrictions, tolls, parking, and rental terms for the particular traveller and location. Do not assume that an overseas licence or IDP is accepted.

### Country patterns that require a targeted check

Do not treat this list as a permanent provider table; platform features, regulations, languages, and payment flows change. Verify the current route and channel for the user's exact itinerary.

- **South Korea:** test a Korean local map/transit provider as a primary candidate. [Kakao Map](https://www.kakaocorp.com/page/service/service/kakaomap?lang=en) officially offers car, public-transit, walking, and bicycle route functions; do not assume a global map supplies every mode without checking it for the requested route. Keep the current provider choice and route result in the source register.
- **Japan:** for rail-heavy days, test a Japan-specific route/fare planner such as [Japan Transit Planner](https://world.jorudan.co.jp/mln/en/?main_lang=en) alongside the operator source. Its route search exposes date/time, fare type, and seat-preference inputs; ticket conditions still come from the railway/operator. Do not convert a route-planner estimate into a reservable train ticket.
- **Yandex-supported markets:** test [Yandex Maps](https://yandex.com/support/maps/en/concept/rout) as a candidate only when it is normally accessible and appropriate for the destination. Its official route guidance covers driving, public transport, walking, cycling, and scooter modes; route availability and payment/booking access must still be checked locally.
- **Any market with a local-language, local-phone, local-wallet, resident-ID, or regulated-ticket flow:** do not guess around it. Mark the relevant booking check as `limited` or `unknown`, supply an official/direct browse alternative where possible, and explain the exact user-side verification needed. Never ask for credentials, payment data, document images, or a workaround.

### Other markets and cross-border trips

- Start with the destination's locally reliable map/transit service and official operator sources. A traveller from mainland China planning an overseas trip may use the destination-appropriate provider if it is normally accessible to them; a traveller visiting mainland China still receives a local Chinese primary route link.
- If a country has a locally dominant map/transit provider, verify that provider's current web or app route link before using it. Do not hard-code a provider merely from a country label.
- Cross-border or multi-country itineraries may use different providers by day or segment. State the change in the final page, preserve an overall provider where possible, and never label two incompatible links as the same live route.

<a id="final-plan-contract"></a>
## Final-plan contract

Each day route, each route segment, and the transport overview must include `map_provider`, `map_link_kind: "directions"`, `verified_map_url`, and `map_checked_at`. A route also records its primary mode, route logic, and fallback. Each segment records a single mode, service/line where relevant, walking minutes, transfers, journey and arrival instructions, fare basis, and fallback. `alternative_map_links`, when present, is a list of `{ "provider", "url", "checked_at", "map_link_kind": "directions", "note" }` records. The primary link and every alternative must be a safe HTTPS browse link and must open actual directions rather than a place page. **Every endpoint in every one of them is a coordinate pair** — including the alternatives, which were for a while the one place a caption could still hide.

The order is provider-specific and is not recoverable from the numbers: Google, Apple and OpenStreetMap read `lat,lon`; Amap reads `lon,lat,name`; OpenStreetMap packs both ends into a single `route=a;b` parameter. Note which way round this rule was learned. The mainland-China branch below has always required `from=<lon>,<lat>` in the Amap URI, so it was accidentally immune to the defect that produced this paragraph, while the global branch — where an endpoint could be any string — was not: a plan wrote its own Chinese display label into a Google `origin=`, the label geocoded to Taiwan, and the button offered a 65-hour drive to the Canary Islands. The fix generalises the China rule outward rather than inventing a new one.

Because a coordinate pair is meaningless on its own, the plan declares `trip.destination_coords` once and every endpoint is checked against it. A pair reversed *consistently* keeps its partner the right distance away — 4.73 km instead of 4.70 on a Las Palmas leg — while moving every pin to southern Africa, so a rule that compares endpoints only to each other cannot see it. One absolute reference turns "do these two agree" into "is this where the trip is".

If `destination_service_market` is `mainland_china`, validation requires Amap/高德 as the primary provider by default and rejects a Google Maps primary route URL or provider. A different verified local primary provider is allowed only with a concise, user-confirmed `primary_map_exception_reason`; Google is never that exception. If `google_services_access` is `unavailable`, validation rejects Google Maps anywhere as a primary or alternative route link. This is a usability rule, not a claim that a service is universally inaccessible.

For final HTML, expose `data-map-provider` and `data-map-kind="directions"` on every live map button. The provider name must be visible in the button label or adjacent short text; generic “open map” text is insufficient.

## Booking-platform routing

Use the same service context for booking comparison. Select one or two public, browse-only platforms after checking coverage, date/guest prefill support, language/currency, taxes/cancellation clarity, normal traveller access, and legitimate availability to the traveller. Preserve direct-provider links whenever practical. Never use an account-only, payment, checkout, affiliate, referral, session, or tracking URL. The final page remains a comparison interface, not a transaction flow.
