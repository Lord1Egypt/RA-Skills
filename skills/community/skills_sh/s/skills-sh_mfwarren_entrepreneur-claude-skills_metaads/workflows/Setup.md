# Meta Ads API Setup Guide

**Purpose:** Walk a user through the complete Meta Ads API setup from scratch — Business Manager, Developer App, access tokens, ad account ID, and verification. This guide contains everything an agent needs to help without external research.

**When to Use:**
- User says "set up meta ads", "connect meta ads", "configure facebook ads API"
- `--check` fails with credential errors
- User is setting up this skill for the first time
- Token has expired and needs refreshing

---

## Prerequisites Check

Before starting, confirm the user has:
- [ ] A Facebook account with admin access to their business's Facebook Page
- [ ] An active Meta Ad Account (they've run ads before, or are ready to create one)
- [ ] `uv` installed (Python package runner) — if not: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## Part 0: Verify Scripts

The Python scripts run directly from the skill's `tools/` directory — no copy or install step needed. They load `.env` from the current working directory.

**Verify scripts are accessible:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --setup
```

If this prints the setup guide, proceed to Part 1.

**Expected project structure after setup:**
```
project-root/
├── .env                          # Credentials go here
└── Analytics/meta-ads/           # Created automatically by --sync
```

---

## Part 1: Meta Business Manager

**What it is:** Business Manager (business.facebook.com) is Meta's hub for managing ad accounts, pages, and users. Most businesses running ads already have one.

### If they already have Business Manager:
1. Go to business.facebook.com
2. Confirm they can see their ad account under Accounts > Ad Accounts
3. Note the **Ad Account ID** (numeric, e.g., `739416136921369`)
4. Skip to Part 2

### If they need to create one:
1. Go to business.facebook.com/overview
2. Click "Create Account"
3. Enter business name, their name, and business email
4. Once created, go to Accounts > Ad Accounts
5. Either "Add" an existing ad account or "Create a new ad account"
6. Note the **Ad Account ID**

**The Ad Account ID** is the number shown in Business Manager. When used in the API, it needs the `act_` prefix: if the ID is `739416136921369`, the API format is `act_739416136921369`.

---

## Part 2: Create a Meta Developer App

**What it is:** A Developer App gives you API access. It doesn't need to be published or reviewed — it's just a container for your API credentials.

### Step-by-step:
1. Go to **developers.facebook.com**
2. Click "My Apps" in the top right
3. Click "Create App"
4. Select app type: **"Business"**
5. Enter app name (e.g., "My Ads Manager API")
6. Select the Business Manager account to associate with
7. Click "Create App"

### Add Marketing API product:
1. In the app dashboard, find "Add Products to Your App"
2. Find **"Marketing API"** and click "Set Up"
3. That's it — no further configuration needed for this product

### Get App ID and App Secret:
1. In the left sidebar, go to **Settings > Basic**
2. Copy the **App ID** (numeric, e.g., `167270972883623`)
3. Click "Show" next to App Secret and copy the **App Secret**
4. Save both — you'll need them for token exchange

---

## Part 3: Generate an Access Token

There are two paths: **System User tokens** (recommended, never expire) or **User tokens** (easier, expire in 60 days).

### Option A: System User Token (Recommended — Never Expires)

**What it is:** A System User is a non-human account in Business Manager specifically for API access. Its tokens don't expire.

1. Go to **business.facebook.com/settings**
2. Navigate to **Users > System Users**
3. Click **"Add"**
   - Name: "Ads API" (or whatever you want)
   - Role: **Admin**
4. Click "Create System User"
5. **Assign the ad account:**
   - Click on the System User
   - Click "Add Assets"
   - Select "Ad Accounts"
   - Find and select your ad account
   - Toggle **"Manage campaigns"** permission ON
   - Click "Save Changes"
6. **Generate token:**
   - Click on the System User
   - Click **"Generate New Token"**
   - Select your app (the one from Part 2)
   - Check these permissions:
     - `ads_management`
     - `ads_read`
     - `pages_read_engagement` (optional, for page-linked ads)
   - Click "Generate Token"
   - **Copy and save immediately** — you won't see it again

**Troubleshooting System Users:**
- "Add" button grayed out? You've hit your System User limit. Use Option B instead, or delete an unused System User.
- Can't find your ad account when assigning assets? Make sure the ad account is added to Business Manager first (Accounts > Ad Accounts > Add).
- Permission denied? You need to be a Business Manager admin.

### Option B: User Token (Easier — Expires in 60 Days)

**What it is:** A token tied to your personal Facebook account. Easier to set up but needs refreshing every 60 days.

**Step 1: Get a short-lived token**
1. Go to **developers.facebook.com/tools/explorer**
2. Select your app from the "Meta App" dropdown
3. Click **"Generate Access Token"**
4. When prompted, grant these permissions:
   - `ads_management`
   - `ads_read`
   - `pages_read_engagement`
   - `read_insights`
5. Click "Generate Access Token"
6. Copy the token

**Step 2: Exchange for a long-lived token (60 days)**

The short-lived token expires in ~1 hour. Exchange it immediately:

```bash
curl "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
```

Replace:
- `YOUR_APP_ID` — from Part 2
- `YOUR_APP_SECRET` — from Part 2
- `YOUR_SHORT_LIVED_TOKEN` — from Step 1

The response will contain your long-lived token:
```json
{"access_token": "EAAxxxxxxxxxx...", "token_type": "bearer"}
```

**The agent can run this curl command** for the user if they provide the app ID, app secret, and short-lived token.

**When the token expires (every 60 days):**
Repeat Step 1 and Step 2. The user will need to generate a new short-lived token in Graph API Explorer and exchange it again. The agent can automate the exchange step.

---

## Part 4: Configure .env

Create or update the `.env` file in the project root:

```
META_ADS_ACCESS_TOKEN=EAAxxxxxxxxxx...your_token_here
META_ADS_ACCOUNT_ID=act_XXXXXXXXX
```

Also save the app credentials for future token refreshes:
```
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
```

**Common mistakes:**
- Missing the `act_` prefix on the account ID
- Extra spaces or quotes around the token
- Using an expired token (error code 190, subcode 463)
- Using a token without `ads_management` scope

---

## Part 5: Verify

Run the check command:
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --check
```

**Expected successful output:**
```
Checking Meta Ads API access...

  Account:  Your Business Name
  ID:       act_XXXXXXXXX
  Status:   ACTIVE
  Currency: USD
  Timezone: America/New_York
  Spent:    $X,XXX.XX

  API access verified successfully.
```

**If it fails, diagnose by error:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Error validating access token: Session has expired` | Token expired | Generate new token (Part 3) |
| `Invalid OAuth access token` | Token is malformed | Check for copy-paste errors, no extra spaces |
| `(#100) Missing permissions` | Token lacks required scopes | Regenerate with `ads_management` and `ads_read` |
| `User does not have permission to manage ad account` | System User not assigned to account | Assign in Business Manager (Part 3, Option A, Step 5) |
| `Ad account is disabled` | Account suspended by Meta | User needs to resolve in Business Manager |
| `Error: Missing Meta Ads credentials` | `.env` not configured | Add variables to `.env` (Part 4) |

---

## Part 6: Token Refresh Process

**For System User tokens:** No action needed — they never expire.

**For User tokens (every ~60 days):**

Check if the agent has the app credentials stored:
```bash
# Check .env for app credentials
grep "FACEBOOK_APP" .env
```

If `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET` are present, the refresh process is:

1. Tell the user: "Your Meta Ads token has expired. Please go to developers.facebook.com/tools/explorer, select your app, and click Generate Access Token. Grant the same permissions (ads_management, ads_read). Paste the new token here."

2. Once the user provides the short-lived token, exchange it:
```bash
curl -s "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN"
```

3. Update `META_ADS_ACCESS_TOKEN` in `.env` with the long-lived token from the response.

4. Verify with `--check`.

---

## Meta Pixel Setup (For Conversion Tracking)

**What it is:** The Meta Pixel tracks purchases, add-to-carts, and other actions on your website. Without it, Meta can't optimize for conversions and ROAS won't appear in analytics.

**If using Shopify:**
1. In Shopify admin, go to Settings > Customer Events (or Online Store > Preferences)
2. Look for "Facebook & Instagram" or "Meta" section
3. Enter your Pixel ID (found in Meta Events Manager)
4. Shopify handles all event tracking automatically

**If using a custom site:**
1. Go to business.facebook.com > Events Manager
2. Click "Connect Data Sources" > "Web"
3. Name your pixel and enter your website URL
4. Choose installation method:
   - **Partner integration** (Shopify, WordPress, etc.) — easiest
   - **Manual install** — add the pixel base code to your site's `<head>`
5. Set up standard events: `Purchase`, `AddToCart`, `ViewContent`, `InitiateCheckout`

**Finding your Pixel ID:**
1. Go to Events Manager (business.facebook.com/events_manager)
2. Select your pixel
3. The Pixel ID is the numeric ID shown (e.g., `123456789012345`)

**The Pixel ID is needed in campaign configs** when using `OUTCOME_SALES` objective with `OFFSITE_CONVERSIONS` optimization. Add it to ad set config:
```json
{
  "pixel_id": "123456789012345",
  "optimization_goal": "OFFSITE_CONVERSIONS"
}
```

---

## Quick Reference: Common API Scopes

| Scope | What It Allows | Required For |
|-------|---------------|--------------|
| `ads_management` | Create, edit, delete campaigns/ads | Publishing campaigns |
| `ads_read` | Read campaign metrics and insights | Analytics |
| `pages_read_engagement` | Read page post engagement | Page-linked ad creative |
| `read_insights` | Read page-level insights | Facebook page analytics |
| `business_management` | Manage Business Manager assets | System User setup |

---

## Quick Reference: Meta API Limits

| Limit | Value | Notes |
|-------|-------|-------|
| API rate limit | ~200 calls/hour per ad account | Automatic backoff in scripts |
| Image upload size | 30MB max per image | PNG/JPG/JPEG/WEBP |
| Images per creative | 10 max in asset_feed_spec | Advantage+ flexible format |
| Primary texts per creative | 5 max | Advantage+ testing |
| Headlines per creative | 5 max | Advantage+ testing |
| Min daily budget | $1.00 (100 cents) | Per ad set |
| Campaign name length | 400 chars max | Keep short for readability |
| Token exchange window | Short-lived token must be < 1 hour old | Exchange immediately |
| Long-lived token duration | 60 days | Set a reminder to refresh |

---

**Last Updated:** 2026-02-07
