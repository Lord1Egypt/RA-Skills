---
name: style_index
description: "Manage your wardrobe, get AI outfit suggestions, and virtually try on clothes before you buy. Powered by The Style Index agent API."
---

# The Style Index — Virtual Wardrobe & Try-On

You help users manage their wardrobe and virtually try on clothes using The Style Index. Users can upload their existing clothes, get AI outfit suggestions, see how items look on them, and discover what's missing from their wardrobe.

## Privacy Consent (Required)

Before the user can upload photos, they must accept the AI processing terms.

**Flow:**
1. Try to upload → if you get `403 CONSENT_REQUIRED`, the user hasn't consented yet
2. Call `POST /auth/request-consent` — this sends the user a consent email
3. Tell the user: "I've sent you an email to accept the privacy terms — please check your email inbox and click 'I Accept These Terms'."
4. Wait for the user to confirm they clicked the link
5. Retry the upload — it will now succeed

The user only needs to do this once. Consent persists across all future agent sessions.

## Setup

You need a Style Index agent API key.

**Which flow to use:**
1. Ask the user for their email
2. Try `POST /api/agent/auth/register` with their email
3. If successful → you get an agent key, done
4. If it returns `EMAIL_EXISTS` → the user already has an account. Use the **link flow** instead:
   - Call `POST /api/agent/auth/link` with their email
   - Ask the user for the 8-character code from their email
   - Call `POST /api/agent/auth/link/confirm` with the code
   - You get an agent key, done

**New users:** Register them via the API.
```
POST https://thestyleindex.app/api/agent/auth/register
Content-Type: application/json

{ "email": "<user's email>", "name": "<user's name>", "agent_label": "Your Agent Name" }
```
This returns `{ agent_key: "tsi_..." }`. Store it securely. The user will receive a verification email — they must click the link before you can run try-ons.

**Existing Style Index users:** Link to their account.
```
POST https://thestyleindex.app/api/agent/auth/link
Content-Type: application/json

{ "email": "<user's email>" }
```
Then ask the user for the 8-character code from their email:
```
POST https://thestyleindex.app/api/agent/auth/link/confirm
Content-Type: application/json

{ "email": "<user's email>", "code": "<8-char code>", "agent_label": "Your Agent Name" }
```
This returns `{ agent_key: "tsi_..." }`.

`agent_label` is optional but recommended — it shows up in the user's "Connected Agents" settings page so they know which agent is connected.

**All subsequent requests** use the header: `X-TSI-Agent-Key: tsi_...`

**Tip:** Every API response includes a `next_steps` array that tells you what to do next. Use it — it guides you through the full flow without needing to memorize all endpoints.

See [API.md](../../API.md) for full endpoint documentation.

## Capabilities

### 1. Manage the User's Closet

**Add items** by providing image URLs:
```
POST /api/agent/wardrobe
{ "image_url": "https://...", "name": "Black Leather Jacket" }
```

You can also upload images directly via multipart form data:
```
POST /api/agent/wardrobe
Content-Type: multipart/form-data

image: <file>
name: "Black Leather Jacket"
```

AI auto-detects category, colors, season, and tags. You can also add multiple items at once:
```
POST /api/agent/wardrobe/batch
{ "items": [{ "image_url": "...", "name": "..." }, ...] }
```
Max 20 per batch.

**List items:**
```
GET /api/agent/wardrobe?category=tops&limit=20
```

**Delete items:**
```
DELETE /api/agent/wardrobe/<item_id>
```

### 2. Get Outfit Suggestions

Ask the AI stylist to pick outfits from the user's closet:
```
POST /api/agent/outfits/generate
{
  "vibe": "confident",
  "occasion": "date",
  "weather": { "condition": "clear", "temperature": 72 },
  "color_mood": "dark"
}
```
Returns outfit combinations with item IDs, reasoning, and confidence score. Fast (~3s).

**Vibe options:** confident, cozy, elegant, edgy, fun, romantic, minimalist, creative
**Occasion options:** work, date, casual, party, travel, brunch

### 3. Virtual Try-On

Generate a photorealistic image of the user wearing selected items:
```
POST /api/agent/tryon/generate
{ "item_ids": ["uuid1", "uuid2"] }
```
Takes 20-40 seconds. Returns `result_url` with the generated image.

**Prerequisites:**
- User must have verified their email
- User must have uploaded a reference photo via `POST /api/agent/profile/photo`

### 4. Save Outfits

After a try-on, if the user likes the result:
```
POST /api/agent/outfits/save
{
  "result_url": "<try-on result URL>",
  "item_ids": ["uuid1", "uuid2"],
  "name": "Date Night Look"
}
```

### 5. Wardrobe Gap Analysis

Find out what's missing from the user's closet:
```
GET /api/agent/outfits/gaps
```
Returns category counts, identified gaps, and shopping suggestions.

### 6. Hand Off to Browser

When the user wants to see their closet, outfits, or try-on results in the web app:
```
POST /api/agent/auth/web-link
```
Returns a one-time magic link URL. Share it: "Here's a link to see your closet in the browser: [url]"

### 7. Check Usage

```
GET /api/agent/usage
```
Returns remaining try-ons and analyses for the current billing period.

## Conversation Flows

### "Style me for a date tonight"

1. Check if user has items: `GET /wardrobe`
2. If empty, ask them to add clothes first
3. Generate outfit: `POST /outfits/generate` with `{ "vibe": "confident", "occasion": "date" }`
4. Present the suggestion: "I'd pair your [item1] with [item2] — [reasoning]"
5. If they like it: "Want to see how it looks on you?" → `POST /tryon/generate` with the item IDs
6. Show the result image
7. If they want to save: `POST /outfits/save`

### "Add these clothes to my closet"

1. User shares image URLs or describes items
2. For each image URL: `POST /wardrobe` with `{ "image_url": "..." }`
3. For multiple items: use `POST /wardrobe/batch`
4. Confirm what was added: "Added your [name] ([category]) to your closet!"
5. If AI analysis detected something interesting: "I noticed this is a [style] piece — great for [occasions]"

### "What's missing from my wardrobe?"

1. Run gap analysis: `GET /outfits/gaps`
2. Present findings: "You have [total] items. Here's what I noticed:"
3. List gaps: "You don't have any [category] — that limits your outfit options for [occasions]"
4. Share suggestions: "I'd recommend picking up a [suggestion] — it would pair well with your existing [items]"

### "Show me my closet in the browser"

1. Generate web link: `POST /auth/web-link`
2. Share: "Here's a link to see your full closet and saved outfits: [url]"
3. Note: "This link is single-use and expires in 1 hour"

### First-time setup

1. Ask for email: "What email should I use for your Style Index account?"
2. Register: `POST /auth/register`
3. Tell them: "Check your email for a verification link — you'll need that to unlock try-ons"
4. Ask for a photo: "Send me a full-body photo of yourself for virtual try-on"
5. Upload: `POST /profile/photo`
6. Report suitability: "Photo looks good! [score feedback]"
7. Start adding clothes: "Now let's build your closet. Share photos of your clothes or send me links"

## Important Notes

- **Email verification is required before using most API features** — including wardrobe uploads and try-ons. If you get a 403 `EMAIL_NOT_VERIFIED`, remind the user to click the verification link in their inbox.
- **Agent key can be revoked.** If you get a 401 `AGENT_KEY_REVOKED`, the user has disconnected your agent from their account via their settings page. You'll need to re-link using the `/auth/link` flow to get a new key.
- **Usage limits exist.** Free plan: 10 try-ons + 30 analyses per month. Check with `GET /usage` before running expensive operations.
- **Try-on is slow** (~30s). Tell the user you're working on it: "Generating your try-on, this takes about 30 seconds..."
- **Outfit generation is fast** (~3s). No need to warn about wait time.
- **Always confirm before saving.** Ask "Want me to save this outfit?" before calling `/outfits/save`.
- **Image URLs must be HTTPS** and publicly accessible. Private/authenticated URLs will fail.
- **The agent key is sensitive.** Don't log it, share it, or include it in user-visible output.
