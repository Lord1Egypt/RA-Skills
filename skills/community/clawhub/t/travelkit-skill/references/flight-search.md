# flight-search ref

Use `flight_search` when the user describes route/date needs. If they provide complete flight number + airports + date + cabin, use `flight_pricing`.

## Inputs

Collect only route/date, passenger counts, cabin, and preferences. Defaults: 1 adult, economy, no airline restriction, no baggage guarantee. Do not collect name, birthday, ID/passport, phone, or email during search. Convert relative dates to `YYYY-MM-DD`.

## Requirement Parsing

Before calling `flight_search`, lightly normalize the user's flight requirement into query parameters. Use this only as internal reasoning for search; do not output JSON or a full parsed-field list unless the user explicitly asks.

- Parse trip type: one-way, explicit round-trip, continuous multi-city, or open-jaw. Keep unsupported or ambiguous itinerary shapes as clarification candidates instead of inventing a bookable route.
- Parse route, dates, date ranges, stay length, passenger counts, cabin, airline/flight preferences, airport preferences, direct/transfer preference, baggage preference, cheapest/fastest/time-window goals, and fallback strategies.
- Defaults stay aligned with Inputs: if cabin is missing, use economy; if passenger count is missing, use 1 adult; missing airline, baggage, direct/transfer, or flight-number preferences do not block search.
- Stay length to return date: count the departure date as day 1, so `returnDate = departureDate + stayDays - 1`. Example: departing 8/10 for 8 days returns 8/17.
- Phrase handling: `或者`, `也可以`, and `都可以` mean alternatives; `改成`, `换成`, and `以这个为准` mean corrections; `这个必须是` means a hard constraint; `如果没有...就...` and `先查...没有再...` mean fallback search strategy.
- Do not promise unsupported actions such as holding seats, group fares, or locked inventory unless a TravelKit tool explicitly supports and returns that capability.

## Clarification Rules

Ask only when a required search field such as origin, destination, or departure date cannot be reasonably inferred, or when a conflict cannot be classified as a correction, alternative, fallback, or hard constraint.

- Ask one concise question at a time, focused on the smallest blocking ambiguity.
- Do not ask only because passenger count, cabin, airline, baggage, or direct/transfer preference is missing; use defaults or omit optional filters.
- City names without airports are searchable as city-level routes; do not ask for airport unless the user set an airport-specific constraint or multiple same-name places make the route unsafe.
- If the user gives several alternatives, search or present them according to the stated priority instead of asking which one is valid unless priority is impossible to infer.

## Tool Use

- Airport constraints: pass specified airport codes such as PEK/PKX/PVG/SHA, then hard-filter by actual route.
- Airline constraints: pass `includeAirlines` / `excludeAirlines` when clear, then hard-filter by IATA code.
- Nonstop: use `maxSegments: 1`; otherwise omit stop limit unless requested.
- Continuous multi-city routes become one `flight_search` with up to 5 `journeys[]`.
- Explicit round-trip requests use one `flight_search` call with two `journeys[]` by default: outbound `origin -> destination` on the departure date, and return `destination -> origin` on the return date.
- Do not split an explicit round-trip request into two independent one-way searches unless the user explicitly asks for separate one-way options, or the multi-journey round-trip search returns no usable result and you explain the fallback.
- Cheapest among multiple candidate dates: search one-way candidates and combine locally only for flexible-date comparison. When the user needs one round-trip fare/order, prefer a multi-journey round trip.

## Fast Path

For user-facing lists, filtering, sorting, recommendation, and option mapping, use only `data.displayOptions`.

- Do not parse raw MCP JSON, `data.solutions`, or `solutions[].segments` for search display.
- Default ranking: hard-filter first, then sort by `displayOptions[].priceTotal` low to high.
- Keep private option mapping from `displayOptions[].solutionId` for later `flight_verify_solution`.
- Never expose internal IDs, filtered-out IDs, raw JSON, or MCP fields.

## Lowest-Price Integrity（最低价完整性）

- Do not deduplicate by flight number, route, or time in a way that drops cheaper fare options.
- If the same flight combination / itinerary has multiple prices, cabin codes, or fare codes, keep the lowest-price option by default and recommend it.
- Default 10 options are selected from all displayable fare options sorted by `priceTotal`, not from folded flight combinations.
- If you collapse duplicate-looking flight combinations for readability, collapse only to the lowest `priceTotal` option and keep that exact option's `solutionId` private mapping.
- If showing multiple fare options for the same flight, every visible option number must map to its own `solutionId`; never reuse another fare option's mapping.

## Filtering And Ranking

- Hard filters: specified airport, airline include/exclude, max stops, and other explicit constraints.
- If hard filtering leaves no options, ask whether to relax constraints; do not silently show same-city alternatives.
- Default display: first 10 filtered/sorted options; if fewer than 10, show all and say only these matched.
- If user asks for N options, show N. If user asks for more, show the next 10. If user asks for all, explain there may be many and display in batches of 10.
- Default recommendation: lowest price, explicitly say it is lowest. If user asks for fastest/time window/airport/airline/baggage/fewer stops, recommend by that goal after hard filters.
- If a cheaper option violates a soft preference, mention briefly only when useful.

## Display

Use exactly 6 columns. Do not merge, omit, or add columns, even for long international or multi-segment itineraries:

```markdown
| 选项 | 航班 | 行程 | 时间 | 舱位 | 价格 |
|---|---|---|---|---|---:|
| 1 | CA1714 | 北京首都 PEK T3 → 杭州 HGH T4 | 12:30-14:40｜直飞约2小时10分 | 经济舱 | ¥790 |
```

Rules:

- Option labels are plain numbers; recommendation stays outside the table.
- `航班` shows only complete flight numbers, no airline names.
- `行程` shows only the route chain and terminals when returned; do not put segment times in this column. For multi-segment itineraries, use a compact route chain such as `北京大兴 PKX → 上海浦东 PVG T2 → 新加坡 SIN T4`.
- Expand common airport names when only IATA is returned. If an IATA code is not in the known mapping, keep the IATA code and do not guess the city or airport name.
- `舱位` may include returned cabin/fare code, e.g. `经济舱 / PP9`; do not invent codes.
- `价格` must be the current displayed option's `priceTotal`.
- Direct time format: `18:55-23:00｜直飞约5小时05分`.
- `时间` for multi-segment rows lists every segment time, e.g. `PEK→HKG 07:25-10:55；HKG→BKK 14:30-16:30｜中转1次约10小时05分`.
- For transfer count, trust the actual number of route segments first: if `route.length > 1`, display `中转{route.length - 1}次` even when `transferNum` is `0` or missing. Never display `直飞` for a multi-segment itinerary.
- Cross-date times show dates on affected times, e.g. `5/20 22:15-5/21 00:10`.
- If a segment time is missing, show `{origin}→{destination} 时间未返回`; do not invent it.
- Do not add baggage column; mention baggage only if user asks or verified result returns it.
- For complex international routes with cross-date transfers or very long travel times, keep the table as the default display and add a short note after the table when helpful, e.g. `最低价方案需隔天中转/到达。`

## Footer And Handoff

End search results with:

> 你回复 1、2 等选项号，我先帮你确认实时价格。确认后如果继续预订，我再收集乘机人信息。你也可以继续补充筛选需求，比如航程偏好、航司、机场、时间段、价格上限或行李要求。

If more filtered options exist, add: `如需我也可以继续展示更多航班。`

When user selects an option, use the private option-to-`solutionId` mapping with `flight_verify_solution`. Say you will confirm real-time price first; do not call it "下单" or "付款".
