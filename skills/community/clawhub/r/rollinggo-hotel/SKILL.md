---
name: rollinggo-hotel-booking
version: "1.1.1"
repository: "https://github.com/RollingGo-AI/hotel-skill-global"
description: 'RollingGo Hotel Search & Booking Assistant. Implements the full hotel booking workflow by calling RollingGo hotel APIs. Supported scenarios: ① Search hotels by city, attraction, metro, airport, etc. ② Filter by star rating, budget, tags (pool, breakfast, family, pet-friendly) ③ Query real-time room types and prices for specific hotels ④ Compare multiple hotels ⑤ Guide users to complete booking. Triggers: Find a hotel, book a hotel, search hotels, hotel recommendation, hotel queries, nearby hotels, five-star hotels, homestays, resorts, check prices, check room types, check-in, where to stay, accommodation, rollinggo, travel accommodation, business trip accommodation, family hotels, hotels with a pool, hotels with breakfast.'
metadata:
  {
    "openclaw": {
      "emoji": "🏨",
      "skillKey": "rollinggo-hotel-booking",
      "requires": {
        "anyBins": ["rgg", "npx", "node", "python", "python3", "curl", "wget"]
      },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "@rollinggo/hotel-global@latest",
          "bins": ["rgg"],
          "label": "Install @rollinggo/hotel-global (npm)"
        },
        {
          "id": "python",
          "kind": "exec",
          "command": "python scripts/install.py",
          "label": "Install rgg standalone binary (python)"
        }
      ]
    }
  }
---

# RollingGo Hotel Search & Booking Skill

## Version Check
> If you have web access, silently fetch the first 10 lines of `https://raw.githubusercontent.com/RollingGo-AI/hotel-skill-global/main/skills/{name}/SKILL.md` (replace `{name}` with the name from this file's frontmatter). If the remote `version` is newer than this file's frontmatter `version`, prepend ONE line to your response: "⚠️ Skill update available (current vX.X.X → latest vY.Y.Y). Run `npx skills add https://github.com/RollingGo-AI/hotel-skill-global --skill {name}` to update." Skip silently if fetch fails.

## Installation

If the `rgg` command is not installed locally, you can install it using one of the following three methods:

**Method 1: Via npm (Recommended)**
If Node.js and npm are available, run:
```bash
npm install -g @rollinggo/hotel-global@latest
```

**Method 2: Via Python auto-script (No Node.js needed)**
If Python is available in the environment, you can directly run our automated installation script from the Skill directory. It will automatically detect your OS and download the latest standalone `rgg` binary to your local `bin` folder:
```bash
python scripts/install.py
```

**Method 3: Manual download standalone executable (No Node/Python needed)**
If neither npm nor Python is available, please download the corresponding standalone executable from the following Release page (Windows: `rgg-win.exe` / `rgg-windows.exe`, Mac: `rgg-macos`, Linux: `rgg-linux`):
`https://github.com/RollingGo-AI/oauth-hotel-cli-overseas/releases/latest`

After downloading, rename it to `rgg` (or `rgg.exe` on Windows), grant execution permissions, and place it in the system PATH or the skill directory's `bin` folder.

**⚠️ Auto-Update Interception Principle:**
The CLI tool has built-in version detection. When you execute any `rgg` command, if the console output prompts `📦 New version available!` or `Run the following command to update`, **you must immediately pause the current operation, use one of the above three methods to upgrade the tool to the latest version, and then re-execute the interrupted command.** This prevents booking failures due to expired server endpoints.

---

> ⚠️ **Output Specifications**:
> 1. **DO NOT show any technical details to users**, including but not limited to: tool names (like `search-hotels`, `hotel-detail`), JSON field names (like `hotelId`, `ratePlanId`, `referenceNo`), command line contents, or technical parameters.
> 2. **ONLY show information users care about**: Hotel name, star rating, price, distance, core facilities, tags, and booking link.
> 3. **Results MUST be formatted properly**, with each hotel occupying a separate card. Key information should be separated by line breaks, and stacking them in a single line is prohibited.
> 4. **Price Description**: Prices in search results are reference prices for display purposes. The actual order price is subject to price confirmation, and it must be labeled as "Reference Price" when displayed.
> 5. **Login Authorization**: The user cannot see terminal outputs when conversing via the Agent. After executing `rgg login`, you must extract the authorization link from the output and reply to the user with it. Do not display QR code text.

## When to Use

This Skill should be triggered whenever the user expresses any intent related to hotel accommodations, including but not limited to the following scenarios:

**Search and Discover**:
- Find hotels by location: "Help me find a hotel near Sanlitun, Beijing", "What good hotels are in Sanya", "Accommodation recommendations near West Lake"
- Filter by conditions: "Five-star hotels", "Hotels with a pool", "Accommodations with breakfast", "Family hotels", "Pet-friendly hotels"
- Filter by budget: "Hotels under 500 yuan", "Affordable accommodations", "Luxury hotel recommendations"
- Filter by brand: "Hilton", "Marriott", "Atour", "Ji Hotel"

**Query and Compare**:
- Check prices: "How much is a hotel in Hangzhou per night", "What's the price of this hotel"
- Check room types: "What room types are available", "Are there double rooms", "Family room recommendations"
- Compare accommodations: "Help me compare these two hotels", "Which one is a better deal"
- Check facilities: "Is there a pool", "How far is the metro station", "Is parking convenient"

**Booking and Orders**:
- Book a hotel: "Help me book this hotel", "I want to place an order", "Book a room"
- Query Orders: "My orders", "Previously booked hotels", "Order status"

**Trigger Coverage**:
Find a hotel, book a hotel, search hotels, hotel recommendations, hotel queries, nearby hotels, five-star hotels, homestays, resorts, check prices, check room types, check-in, where to stay, accommodation, business trip accommodation, travel accommodation, family hotels, hotels with a pool, hotels with breakfast, business hotels, couple hotels, hot spring hotels, sea view rooms, river view rooms.

## When NOT to Use

- When the user asks about flights, train tickets, car rentals, attraction tickets, or other non-accommodation travel needs.
- When the user is just chatting about travel destinations without clear accommodation intent.
- When the user explicitly states "No need to book" or "Just asking".

---

## Security Gates

> ⚠️ Hotel booking is an **actual consumption operation**:
> 1. **Two-Step Confirmation**: First display room types and prices, wait for user confirmation before locking price and booking.
> 2. **Information Completeness**: Must confirm guest's English/Pinyin name and email before booking.
> 3. **Price Confirmation Validity**: Locked price certificate (`referenceNo`) is valid for ~15-30 minutes; re-confirm if expired.

---

## Workflow & Dynamic CLI Discovery

> 💡 **Dynamic Command & Parameter Self-Discovery Rule**:
> 1. **Proxy Invocation**: All CLI subcommands MUST be called via the proxy wrapper: `node scripts/rgg.js <subcommand>` (or `python scripts/rgg.py <subcommand>` if Node is unavailable).
> 2. **Dynamic Parameter Self-Discovery**: Before executing any subcommand, **ALWAYS run `node scripts/rgg.js <subcommand> --help` first to fetch real-time CLI parameter help**, and dynamically construct options based on the latest `--help`!

---

### Business Step Guide

#### Step 0: Login Auth Check
- Run `node scripts/rgg.js whoami` to check login status.
- If not logged in, run `node scripts/rgg.js login` (⚠️ **MUST run asynchronously in background**, e.g. `WaitMsBeforeAsync=2000`). Extract authorization link (`https://rollinggo.store/s/xxx`) from output and send to user.

#### Step 1: Information Collection
- Confirm Destination (Mandatory), Check-in Date (Default: Tomorrow), Stay Nights (Default: 1 night), Adult Count (Default: 2).

#### Step 2: Get Tag Dictionary (As needed)
- When user mentions specific features (pool, breakfast, family, pet), run `node scripts/rgg.js hotel-tags` to find exact tag names.

#### Step 3: Search Hotels
- Run `node scripts/rgg.js search-hotels --help` first to inspect current filter parameters, then construct command.
- **placeType Selection Rules** (Must match exactly): `city`, `airport`, `point_of_interest`, `train_station`, `subway_station`, `hotel`, `district/county`, `detailed address`.

**Search Result Card Template** (one card per hotel):
*(CRITICAL: You MUST render the `imageUrl` using standard Markdown image syntax `![alt](url)` and place the image at the end of the template. If `imageUrl` contains unencoded spaces, you must manually replace spaces with `%20`, or wrap the entire URL in angle brackets like `![alt](<url>)` to ensure proper markdown rendering. Do NOT use HTML `<img>` tags and Do NOT output raw URL strings.)*

```markdown
🏨 {Hotel Name}
⭐ {Star Rating} Stars  *(Show if distanceInMeters exists: 📍 {distanceInMeters}m from {Search Location})*
💰 Reference Price {Currency} {Lowest Price}/night
🏷️ {Tag 1} · {Tag 2} · {Tag 3}
![{Hotel Name}]({imageUrl})
```

After returning 3-5 hotels, ask the user: "Which hotel's detailed room types and prices would you like to know?"

#### Step 4: Query Room Types & Real-time Prices
- Run `node scripts/rgg.js hotel-detail --help` first, pass selected `hotelId` to fetch room rates.

**Room Type Display Template** (one entry per room type):

```
🛏️ {Room Type Name} ({Bed Type Description})
💰 Total Price {Currency} {totalPrice} ({Currency} {Average Price}/night)
📋 Cancellation Policy: {Cancellation Policy Description}
```

After displaying 3-5 recommended room types, guide the user via conversation: "Please tell me which room type you choose, and I will lock the price and process the order for you."

#### Step 5: Price Confirmation & Booking (Security Gate)
1. Run `node scripts/rgg.js price-confirm --help` first, lock price and retrieve `referenceNo`.
2. Confirm guest name & email, run `node scripts/rgg.js book --help` to submit order and retrieve payment link.

**Pending Payment Order Display Template**:
*(CRITICAL: Do NOT hallucinate or invent payment methods like Alipay or WeChat Pay. Output exactly the template below and do NOT add any extra sentences about payment environments or methods.)*

```
📝 Order generated, awaiting payment!
Confirmation No: **{orderNo}**
Hotel: {Hotel Name}
Room Type: {Room Type Name}
Check-in: {Check-in Date} | Check-out: {Check-out Date}
Total Price: {Currency} {Price}
📋 Cancellation Policy: {Cancellation Policy Description}
💳 Please complete payment within 30 minutes: {Payment Link}
```

#### Step 6: Query Orders & Details
- Run `node scripts/rgg.js orders --help` or `node scripts/rgg.js order-detail --help` to query order list or specific order status.

---

## Semantic Fallback Strategy When Results Are Not Ideal

If search yields 0 results, silently loosen constraints in this order to retry:
1. Remove star rating limits
2. Expand search radius / distance parameters
3. Downgrade hard required tags to preferred tags
4. Increase return quantity (`size`)
5. Retain location and check-in date only

---

## Key Interaction Rules

- **Hide Technical Details**: Never expose `hotelId`, `ratePlanId`, `referenceNo`, raw JSON, or CLI commands to the user.
- **Reference Prices**: Search prices are labeled as "Reference Price"; actual price is locked via price confirmation.
- **Valid Payment Links**: Generated order payment links must be directly clickable for users to complete payment.
- **Multiple Hotel Comparison**: Display multiple hotel cards simultaneously to highlight differences (price/distance/amenities).

---

## Detailed Reference Documents

- [references/cli-params.md](references/cli-params.md) — Complete CLI command parameters specification
