# Publish Meta Ads Campaign

**Purpose:** Create and publish a full Meta ad campaign (campaign -> ad sets -> creative -> ads) from local assets and copy.

**When to Use:**
- User wants to publish, create, or launch a Meta/Facebook/Instagram ad campaign
- User has ad images and copy ready to push to Meta Ads Manager
- User wants to upload images and get image hashes

**Prerequisites:**
- `META_ADS_ACCESS_TOKEN` and `META_ADS_ACCOUNT_ID` in `.env`
- If not configured, route to **Setup.md** first
- Ad images (PNG/JPG) in a local directory
- Ad copy (primary texts, headlines, descriptions)
- Landing page URL

---

## Workflow Steps

### Step 1: Check Credentials

**Description:** Verify Meta Ads API access before attempting publish.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --check
```

**Expected Outcomes:**
- **Success:** Account name and status displayed -> Proceed to Step 2
- **Failure: Token expired (error 190)** -> Route to Setup.md Part 6 (Token Refresh)
- **Failure: Missing credentials** -> Route to Setup.md for full setup

---

### Step 2: Upload Images

**Description:** Upload ad images from local directory to Meta and get image hashes.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --upload-images ./path/to/images/
```

**Notes:**
- Supported formats: PNG, JPG, JPEG, WEBP
- Max file size: 30MB per image
- Max 10 images per Advantage+ creative
- Returns `{filename: image_hash}` map
- Image hashes are used in the creative config

**Expected Outcomes:**
- **Success:** Image hashes returned -> Use in config JSON
- **Failure:** Upload errors -> Check image format/size, retry

---

### Step 3: Create Campaign Config

**Description:** Build the JSON config file for the campaign. Ask the user for the details, or gather from context in the conversation.

**Information needed from user:**
1. **Campaign name** — short descriptive slug (e.g., "summer-sale-june")
2. **Objective** — what are they optimizing for? (see objective table below)
3. **Daily budget** — how much per day? (converted to cents in config)
4. **Target audience** — age range, gender, countries, interests
5. **Ad images** — directory path to images
6. **Primary texts** — 2-5 variants of the main ad copy
7. **Headlines** — 2-5 short headlines (40 chars or less ideal)
8. **Descriptions** — 1-2 supporting descriptions
9. **Landing page URL** — where clicks go
10. **CTA button** — SHOP_NOW, LEARN_MORE, SIGN_UP, etc.

**Objective selection guide:**
| User Goal | Objective | Optimization Goal |
|-----------|-----------|-------------------|
| "I want sales/purchases" | `OUTCOME_SALES` | `OFFSITE_CONVERSIONS` |
| "I want leads/signups" | `OUTCOME_LEADS` | `LEAD_GENERATION` |
| "I want website traffic" | `OUTCOME_TRAFFIC` | `LINK_CLICKS` |
| "I want brand awareness" | `OUTCOME_AWARENESS` | `REACH` |

**Template:**
```json
{
  "campaign": {
    "name": "campaign-name-month-year",
    "objective": "OUTCOME_SALES"
  },
  "adsets": [
    {
      "name": "Broad-25-54-US",
      "daily_budget": 5000,
      "targeting": {
        "age_min": 25,
        "age_max": 54,
        "genders": [0],
        "geo_locations": {
          "countries": ["US"]
        },
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "video_feeds", "story", "reels"],
        "instagram_positions": ["stream", "story", "reels", "explore"]
      },
      "optimization_goal": "OFFSITE_CONVERSIONS",
      "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
    }
  ],
  "creative": {
    "images_directory": "./path/to/images/",
    "primary_texts": [
      "Hook with the pain point or desire",
      "Lead with social proof or a stat",
      "Comparison or price-anchoring angle"
    ],
    "headlines": [
      "Short Punchy Headline",
      "Benefit-Driven Headline"
    ],
    "descriptions": [
      "Supporting description with key differentiator"
    ],
    "link_url": "https://yoursite.com/landing-page",
    "url_parameters": "utm_source=meta&utm_medium=paid-social&utm_campaign=campaign-name&utm_content={{ad.name}}",
    "call_to_action_type": "SHOP_NOW"
  }
}
```

**Config rules:**
- `daily_budget` is in **cents** (5000 = $50.00/day)
- `genders`: 0 = all, 1 = male, 2 = female
- `{{ad.name}}` is a Meta dynamic parameter — auto-fills with the ad name in UTMs
- Advantage+ creative tests all image/text/headline combinations automatically
- Save config as JSON file for reproducibility

**Targeting options reference:**

Geo locations:
```json
{"countries": ["US"]}
{"countries": ["US", "CA"]}
{"regions": [{"key": "4081"}]}
{"cities": [{"key": "2421836", "radius": 25, "distance_unit": "mile"}]}
```

Interest targeting (optional — broad often outperforms):
```json
{
  "flexible_spec": [
    {
      "interests": [
        {"id": "6003139266461", "name": "Yoga"},
        {"id": "6003384145981", "name": "Meditation"}
      ]
    }
  ]
}
```

---

### Step 4: Publish Campaign

**Description:** Run the full publish flow.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --publish path/to/config.json
```

**What happens:**
1. Config is validated (budget, targeting, required fields)
2. Images are uploaded from `images_directory`
3. Campaign is created (PAUSED)
4. Advantage+ creative is created with all text/image variants
5. Ad set is created with targeting and budget
6. Ad is created linking creative to ad set
7. Campaign ID is returned

**All objects are created PAUSED.** Nothing spends money until explicitly activated.

---

### Step 5: Review in Ads Manager

**Description:** Verify everything looks right before activating.

**Checklist:**
- [ ] Campaign name and objective correct
- [ ] Ad set targeting matches intended audience
- [ ] Budget is correct (daily vs lifetime)
- [ ] Creative images display correctly
- [ ] All text variants are present
- [ ] Landing page URL and UTM parameters correct
- [ ] Pixel/conversion tracking is configured (for OUTCOME_SALES)
- [ ] Page identity is correct

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --status CAMPAIGN_ID
```

---

### Step 6: Activate Campaign

**Description:** Once reviewed, activate the campaign.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Publish.py --resume CAMPAIGN_ID
```

**Post-activation guidance for the user:**
- Don't touch it for 24-48 hours — let Meta's algorithm learn
- Check metrics with `~/.claude/skills/MetaAds/tools/Analytics.py --campaign CAMPAIGN_ID` after day 2
- Meta's learning phase needs ~50 conversions in 7 days to optimize fully
- Don't increase budget more than 20-30% at a time (resets learning)
- If no spend after 48 hours: try switching optimization to Link Clicks temporarily

---

## Outputs

**Primary Output:**
- Campaign ID (for tracking and management)
- Full hierarchy: campaign -> ad sets -> creatives -> ads

**Where outputs are stored:**
- Campaign exists in Meta Ads Manager
- Config JSON saved locally for reference and reproducibility
- Image hashes printed to console

---

## Error Handling

**Invalid config:**
- Validation runs before any API calls
- Lists all config errors at once
- Fix and re-run

**Image upload failure:**
- Check file format (PNG/JPG/JPEG/WEBP only)
- Check file size (Meta max: 30MB per image)
- Retry individual images

**API permission error:**
- Verify token has `ads_management` permission
- Verify token owner/System User is assigned to the ad account
- Run `--check` to diagnose
- Route to Setup.md if needed

**Rate limiting:**
- Automatic exponential backoff (up to 5 retries)
- If persistent, wait 15 minutes and retry

**Token expired:**
- Error code 190, subcode 463
- Route to Setup.md Part 6 for token refresh

---

**Last Updated:** 2026-02-07
