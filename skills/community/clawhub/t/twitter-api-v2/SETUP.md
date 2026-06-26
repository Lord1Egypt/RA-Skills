# X API Setup Guide

## Prerequisites

- Python 3 (stdlib only, no pip dependencies)
- X Developer account: <https://developer.x.com>
- 5 minutes

---

## Option 1: Bearer Token Only (Recommended)

**For:** User profiles, timelines, search, tweet lookup  
**Setup time:** 2 minutes  
**Cost:** Free tier available, then pay-per-usage

### Steps

1. **Go to Developer Portal**  
   <https://developer.x.com/en/portal/projects-and-apps>

2. **Create or select an app**  
   - Click "Create App" or select existing
   - Fill in required fields (name, description)

3. **Get Bearer Token**  
   - Navigate to: **Keys and tokens**
   - Under "Bearer Token" → Click **Generate** or **Regenerate**
   - Copy the token (starts with `AAAAAAAAAA...`)

4. **Save credentials**

   ```bash
   mkdir -p ~/.openclaw/x
   cat > ~/.openclaw/x/credentials.json <<EOF
   {
     "bearer_token": "YOUR_BEARER_TOKEN_HERE",
     "consumer_key": "OPTIONAL",
     "consumer_secret": "OPTIONAL"
   }
   EOF
   ```

   Replace `YOUR_BEARER_TOKEN_HERE` with the token you copied.

5. **Test**

   ```bash
   python3 scripts/x.py user steipete
   ```

   Should display Peter Steinberger's profile.

### What Works

✅ User info (`user`)  
✅ Timelines (`timeline`)  
✅ Search (`search`)  
✅ Threads (`thread`)  
✅ Tweet lookup (`tweet`, `tweets`)

❌ Bookmarks (need OAuth)  
❌ Likes (need OAuth)  
❌ Posting (need OAuth)

---

## Option 2: OAuth 2.0 (Advanced)

**For:** Bookmarks, likes, posting  
**Setup time:** 10 minutes  
**Requires:** Client ID + Client Secret

### Steps

1. **Go to Developer Portal**  
   <https://developer.x.com/en/portal/projects-and-apps>

2. **Select your app → User authentication settings**

3. **Click "Set up"** and configure:

   | Field | Value |
   |-------|-------|
   | **App permissions** | Read and Write |
   | **Type of App** | Web App |
   | **Callback URI** | `http://localhost:8080/callback` |
   | **Website URL** | Any valid URL (e.g., `https://example.com`) |

4. **Save and copy credentials**  
   After saving, you'll see **Client ID** and **Client Secret**.

5. **Create OAuth credentials file**

   ```bash
   cat > ~/.openclaw/x/oauth2.json <<EOF
   {
     "client_id": "YOUR_CLIENT_ID_HERE",
     "client_secret": "YOUR_CLIENT_SECRET_HERE"
   }
   EOF
   ```

6. **Authenticate**

   ```bash
   python3 scripts/x.py auth
   ```

   This will:
   - Open your browser
   - Ask you to authorize the app
   - Redirect to `localhost:8080/callback`
   - Save tokens to `~/.openclaw/x/tokens.json`

   **Scopes granted:** `tweet.read`, `users.read`, `bookmark.read`, `tweet.write`, `offline.access`

7. **Test**

   ```bash
   python3 scripts/x.py bookmarks --max 10
   python3 scripts/x.py post "Hello from OpenClaw! 🦞"
   ```

### What Works

✅ Everything from bearer token  
✅ Bookmarks (`bookmarks`)  
✅ Likes (`likes`)  
✅ Posting (`post`)

---

## Billing Setup

X API uses **pay-per-usage** pricing (credit-based).

### 1. Buy Credits

1. Go to: <https://developer.x.com/en/portal/billing>
2. Purchase credits (start with $10-25)
3. Credits are deducted per API call

### 2. Set Spending Limit (Recommended)

- In billing settings: Set **Monthly spending limit** (e.g., $50)
- Prevents runaway costs
- API requests blocked when limit hit

### 3. Enable Auto-Recharge (Optional)

- Trigger: When balance < $5
- Recharge: Add $25
- Prevents downtime

### 4. Monitor Usage

```bash
# Via API
curl "https://api.x.com/2/usage/tweets" \
  -H "Authorization: Bearer $BEARER_TOKEN"

# Via console
https://developer.x.com/en/portal/dashboard
```

**Cost example (pay-per-usage):**
- Fetching 100 tweets: ~$0.10-0.50 (varies by endpoint)
- Deduplication: Same tweet twice in 24h UTC window = charged once
- Failed requests: Free (4xx/5xx errors not billed)

See [references/pricing.md](references/pricing.md) for detailed pricing.

---

## File Structure

After setup, you'll have:

```
~/.openclaw/x/
├── credentials.json    # Bearer token (required)
├── oauth2.json         # OAuth client creds (optional)
└── tokens.json         # OAuth user tokens (auto-generated)
```

**Security:** These files contain secrets. Keep them private.

---

## Troubleshooting

### Bearer Token Not Working

**Error:** `401 Unauthorized`

**Fix:**
- Verify bearer token is correct (copy-paste from Developer Portal)
- Check credentials.json syntax (valid JSON)
- Ensure token starts with `AAAAAAAAAA...`

### OAuth Callback Fails

**Error:** `Invalid redirect URI`

**Fix:**
- Callback URI must exactly match: `http://localhost:8080/callback`
- Check for typos (http not https, no trailing slash)
- Ensure port 8080 is free

### Rate Limit Hit

**Error:** `429 Too Many Requests`

**Fix:**
- Wait 15 minutes (rate limits reset every 15 min)
- Check `x-rate-limit-reset` header for exact reset time
- Reduce `--max` values in commands
- Add delays between requests

### No OAuth Credentials

**Error:** `OAuth 2.0 credentials not found`

**Fix:**
- Create `~/.openclaw/x/oauth2.json` with client_id and client_secret
- Follow "Option 2: OAuth 2.0" steps above

---

## Next Steps

1. ✅ **Set up bearer token** (2 min) — enables most features
2. ⚙️ **Buy credits** ($10 to start) — enables API usage
3. 🔒 **Set spending limit** — prevents surprises
4. 🔐 **OAuth setup** (optional) — for bookmarks/posting

Then explore: [SKILL.md](SKILL.md) or [references/quickstart.md](references/quickstart.md)
