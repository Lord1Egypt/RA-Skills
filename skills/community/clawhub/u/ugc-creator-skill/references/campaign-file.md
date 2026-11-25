# campaign.json: the brief as data

Save the brief as the user pasted it in `brief.txt` (and any linked document they paste). Then write
`campaign.json` from it, run `python3 <skill>/scripts/campaign.py campaign.json`, and show the
verdict and `checklist.md`. Write `null` for anything the brief doesn't say; never guess a number.
`examples/orbit-ugc/campaign.json` is a complete one.

| Field | What to write |
|---|---|
| `id` | short id, lowercase letters, digits and dashes (`orbit-app-nov`). The ledger files every post under it |
| `name`, `brand` | the campaign's name and the brand, as on the campaign page |
| `marketplace` | where the campaign is listed (Content Rewards, Whop, a brand's own program), or null |
| `brief_file`, `brief_date` | `brief.txt` and the day it was read. `campaign.py` reads the brief text for what it refuses |
| `mode` | `"post"` (you post on your own accounts, paid per view) or `"deliver_files"` (paid per video, the brand posts) |
| `accounts_owned_by` | `"creator"`. `"brand"` (accounts the brand owns or creates for you) is refused |
| `currency` | `"USD"` unless the brief pays in another |
| `platforms` | the platforms that pay, each with `rate_per_1k`, and its own `min_payout`, `cap_per_video`, `min_views` when the brief sets them per platform: `{"TIKTOK": {"rate_per_1k": 2.0}, "INSTAGRAM": {...}, "YOUTUBE": {...}}`. A cap under the minimum is an error: that platform could never pay |
| `min_payout`, `cap_per_video`, `fee_pct` | the minimum payout per video, the cap per video, the marketplace fee in percent (10 when null) |
| `pay_per_video` | in deliver_files mode: the flat fee per accepted video |
| `budget_total`, `budget_remaining`, `budget_checked_at` | the campaign's budget and what is left, read on the campaign page, with when |
| `geo` | `{"countries": ["US", "UK"], "min_share": 0.4}` when the brief says where viewers must be |
| `language` | the language of the video (`"en"`) |
| `formats` | the layouts the brief accepts: `talking_head`, `split_screen`, `face_screen`, `broll_voiceover` (references/formats.md) |
| `face` | `"required"`, `"either"` or `"none"` (faceless) |
| `supplied_footage` | `{"files": ["orbit-footage.mp4"], "position": "top"}`: the footage the brand supplies for a split screen, and which half it goes in |
| `talking_points` | `[{"id": "tp1", "text": "...", "required": true}]`, the brief's own words. Every brand claim in the script points to one; `required` ones must be in every script |
| `product_on_screen_by_s` | when the brief says "show the product in the first N seconds" |
| `eligibility` | `{"min_followers": 1000, "min_account_age_days": 30, "countries": ["US"], "account_type": "creator", "public": true}`: who may take part. Each account then needs `"eligible": true` in job.json |
| `usage_rights` | what the brief says the brand may do with your video (ads, how long, where), word for word; null when it says nothing (the checklist then says what is usual) |
| `ad_code` | when the brief wants a TikTok Spark Ads code or an Instagram partnership ad permission, and by when |
| `reference_videos` | links to example videos the brief points at |
| `doc_only_rules` | rules that only appear in a linked document, not on the campaign page: listed so the user knows a rejection on them can be appealed |
| `creator` | `{"hourly_floor": 15, "hours_per_video": 1.5}`: the user's own floor; the checklist shows the views each video needs to reach it |
| `campaign_stats` | `{"approved_videos": 120, "total_views": 900000}` from the campaign page, when it shows them: the average views per approved video |
| `do_not_say` | words and phrases the brief bans |
| `cta`, `cta_in` | the call to action word for word, and where it goes: `"spoken"`, `"caption"` or `"both"` |
| `caption` | `{"disclosure": "#ad", "hashtags": [...], "mentions": [...], "links": [...]}` |
| `links_where` | `"caption"`, `"bio"` or `"either"` |
| `disclosure` | `{"spoken_within_s": 10, "on_screen": "Ad", "on_screen_seconds": 3, "caption_position": "first"}`. Add `"not_in_hook": true` when the brief says not to say it's an ad in the hook, or `"not_before_s": 2` when it says not in the first seconds: the script and the video checks follow them |
| `burned_text` | `"any"` (the default: captions, hook text and the "Ad" label), `"disclosure_only"` (the label alone) or `"none"` (clean footage: nothing burned in; the disclosure is said, first in the caption and the platform's paid-partnership setting). For briefs that ask for no text on the video |
| `disclosure_ok_in_writing` | only when the brief asks to hide the ad and the brand then confirmed in writing that a disclosed video is accepted: who, where, when |
| `pre_approval` | true when the brand approves each draft before posting |
| `max_submissions` | how many videos the brief takes from one creator |
| `dedicated_account` | true when the brief wants an account used only for this kind of content |
| `deadline`, `deadline_tz` | the last day to post or submit (`2026-12-15`), and the time zone the brief means (`America/New_York`); a date alone ends at midnight at the end of that day there (UTC when no zone) |
| `length` | `{"min_s": 15, "max_s": 60}` |
| `music` | `"none"`, `"licensed_only"`, `"brief_supplied"` or `"any_licensed"` |
| `make_money`, `typical_earnings` | true for a campaign about earning money; `{"line": "...", "source": "..."}` from the brand, needed only when a video makes an earnings claim (references/claims.md) |
| `topic_reviewed` | `{"<topic>": "why the flagged word doesn't apply"}` when a topic flag is a false alarm |
| `window_days`, `window_from`, `days_live` | how long views count (30), from the post or from crossing the payout threshold (`"threshold"`, the default), how long the post stays up |
| `submit_within_minutes` | the submission window after a post goes live (30) |
| `proof` | what the brief wants as proof (`"analytics screenshot with audience countries at 72 hours"`) |

## The verdict

- **REFUSED**: the brief wants you to pose as an ordinary customer or post from a brand-owned
  account, a testimonial about use or results that didn't happen, or an AI presenter or cloned
  voice. Say why in one sentence and stop.
- **NO-GO**: something to fix or settle first: an error in campaign.json, a missing or too short
  `brief_file` (nothing can be checked without the brief), a brief that asks to hide the ad (until
  the brand confirms in writing that a disclosed video is accepted), a passed deadline, an empty
  budget.
- **GO**, with conditions: the rules to keep in mind (tone notes followed as style with the
  disclosure kept, no TikTok for a banned topic or get-rich-quick framing, earnings claims only
  with the typical result, the brand's approval first, at most N submissions, a dedicated account,
  claims checks in English only).

Exit code 0 only on GO. The checklist is what every later script checks against.
