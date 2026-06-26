# Airbnb — Short-Stay & Apartment Search

Airbnb is **optional** and runs as a **separate local MCP server** that the user installs independently.

Use it when the user wants:
- apartments, homes, villas, cabins, unique stays
- kitchen / washer / longer stay convenience
- family or group travel needing multiple rooms
- workcations / digital nomad stays
- to compare **Airbnb vs hotel** for the same destination and dates

## Install / Run

Airbnb MCP is a separate package (`@openbnb/mcp-server-airbnb`). The user must install it themselves before use. Node.js 18+ required.

**Installation (user must run manually):**
```bash
npm install -g @openbnb/mcp-server-airbnb
```

**MCP config (after installation):**
```json
{
  "mcpServers": {
    "airbnb": {
      "command": "mcp-server-airbnb"
    }
  }
}
```

Respects robots.txt by default. Do not override this.

## Tools

### `airbnb_search`

Search Airbnb listings.

Parameters:
- `location` (required) — e.g. `"Barcelona, Spain"`
- `placeId` (optional) — Google Maps Place ID, overrides location
- `checkin` / `checkout` (optional) — `YYYY-MM-DD`
- `adults`, `children`, `infants`, `pets` (optional)
- `minPrice`, `maxPrice` (optional) — nightly price range
- `cursor` (optional) — pagination

### `airbnb_listing_details`

Fetch listing details.

Parameters:
- `id` (required)
- `checkin` / `checkout` (optional)
- `adults`, `children`, `infants`, `pets` (optional)

Returns rich details such as amenities, policies, highlights, location data, and direct link.

## When Airbnb Beats Hotels

Airbnb often wins on **value** when any of these are true:
- stay is **4+ nights**
- **2+ travelers** sharing one place
- kitchen / laundry matters
- the user wants neighborhood feel over hotel services
- family / friend group wants common space
- longer stay or workcation

Hotels often win when:
- trip is short (1-3 nights)
- user wants easy check-in, daily cleaning, breakfast, concierge
- solo traveler needs convenience over space
- strict central location matters most

## Airbnb vs Hotel Comparison Workflow

```
1. Search hotels (Skiplagged + Trivago)
2. Search Airbnb listings for same location + dates
3. Compare by value, not price alone
4. Recommend ONE best-value option overall
5. Present hotel + Airbnb alternatives with trade-offs
```

## Airbnb Value Scoring

For Airbnb, score on:

- **Nightly price / total price**
- **Entire place vs room** (entire place bonus for couples/groups)
- **Location / neighborhood fit**
- **Amenities** (kitchen, washer, WiFi, AC, workspace, self check-in)
- **Space value** (bedrooms, common space, privacy)
- **Policies** (cancellation, house rules)

Heuristic:
- solo / short stay → hotels usually get a convenience bonus
- couples / 4-7 nights → balanced
- groups / families / long stay → Airbnb gets a strong value bonus

## Presentation Pattern

When comparing:

```text
🏆 BEST VALUE: [option]
- Why: [space/location/price/convenience summary]

🏨 Best hotel:
- [name] — $X/night — [key strength]
- Link: ...

🏠 Best Airbnb:
- [listing title/type] — $X/night — [key strength]
- Link: ...

Trade-off:
- Hotel = easier + more service
- Airbnb = more space + better for [group/longer stay]
```

## Defaults

If user does **not** specify accommodation style:
- **solo + short trip (1-3 nights)** → favor hotels
- **couple + 4-7 nights** → compare both equally
- **family/group + 3+ nights** → favor Airbnb in value scoring
- **digital nomad / workcation / month+** → Airbnb first, hotels as fallback

## Best Practices

- Always compare Airbnb against hotels for the same dates before recommending.
- Prefer **entire place** when privacy matters.
- Mention if Airbnb value comes from space rather than raw price.
- Flag missing essentials when relevant: WiFi, AC, kitchen, washer, self check-in.
- If user mentions pets, explicitly search with `pets` and prioritize pet-friendly stays.
- For longer stays, emphasize kitchen + laundry + workspace.
