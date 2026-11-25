# job.json: the posts, one per account

```json
{
  "campaign": "campaign.json",
  "script": "script.json",
  "manifest": "videos/manifest.json",
  "timezone": "America/New_York",
  "ai_generated": false,
  "stagger": false,
  "accounts": [
    {"name": "TikTok", "platform": "TIKTOK", "handle": "@you", "socialAccountId": "<from social_accounts_list>",
     "privacyOptions": ["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"],
     "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false,
     "marketplace_verified": true, "audience": {"US": 0.46, "UK": 0.08}},
    {"name": "Reels", "platform": "INSTAGRAM", "handle": "@you", "socialAccountId": "<id>", "marketplace_verified": true},
    {"name": "Shorts", "platform": "YOUTUBE", "handle": "@you", "privacy": "public", "madeForKids": false,
     "marketplace_verified": true, "by_hand": true}
  ],
  "posts": [
    {"id": "orbit-tiktok", "account": "TikTok", "file": "videos/tiktok.mp4", "caption": "#ad ... @brand #tag"},
    {"id": "orbit-reels", "account": "Reels", "file": "videos/reels.mp4", "caption": "#ad ..."},
    {"id": "orbit-shorts", "account": "Shorts", "file": "videos/shorts.mp4", "title": "...", "caption": "#ad ...",
     "tags": ["space"]}
  ]
}
```

Accounts:

- `socialAccountId` comes from this session's `social_accounts_list`, never typed by the user; or
  `"by_hand": true` for an account the user posts in the app (it gets a `by-hand/<post>.md` page).
- TikTok: `privacyOptions` from `social_accounts_get_platform_inputs`; `privacyLevel`,
  `allowComment`, `allowDuet`, `allowStitch` are the user's answers. Nothing is defaulted.
- YouTube: `privacy` and `madeForKids` are the user's answers.
- `marketplace_verified`: the account is connected and verified in the marketplace (posts from
  other accounts are rejected). Ask every campaign; left out, it is an error. `eligible`: true once
  the user says the account meets every eligibility point the brief sets (followers, age, country,
  account type, public); required when the brief has an `eligibility` block. Two accounts with the
  same `socialAccountId` are an error. `dedicated`: true for an account used only for this kind of content,
  when the brief asks. `audience`: shares of viewers per country from the app, for the geo rule.
- `ai_generated` (here or per post): realistic AI-made scenes or voices anywhere in the video. The
  person on camera is always the creator.

Posts: one per account, the caption starting with the disclosure, every required hashtag, mention
and link, the call to action when the brief wants it in the caption. Captions and titles get the
same claims check as the script: no use or result that isn't confirmed, no absolute claims, no
quick-money framing, nothing banned. One file can go to one account per platform (TikTok, Reels and
Shorts is normal cross-posting); the same file or the same take on two accounts of one platform, or
in another campaign, is an error. With `pre_approval`, `"approved": {"by": ..., "at": ...,
"sha256": "<first 12 of the approved file>", "evidence": "<the brand's message or a link to it>",
"account": "<the account it was approved for>"}`.

`"stagger": true` writes one request per post instead of one post with a child per account, so the
user can post one, do its in-app step and submit it before the next.

`python3 <skill>/scripts/check_videos.py job.json` checks it all (`--report lint-report.md` saves the
result); `plan.py job.json` makes the plan page from it.

## A finished edit of your own

A creator who edits in their own app hands in the finished file. Transcribe it, show the first
frames, and add `own_edit` to its post:

```bash
python3 <skill>/scripts/transcribe.py my-edit.mp4 --out work-own
python3 <skill>/scripts/make_video.py --frames my-edit.mp4        # writes my-edit-frames.jpg
```

```json
{"id": "orbit-shorts", "account": "Shorts", "file": "my-edit.mp4", "caption": "#ad ...",
 "own_edit": {"transcript": "work-own/transcript.json", "layout": "talking_head",
              "on_screen": {"disclosure": "Ad", "seconds": 3, "from": 0},
              "music": {"source": "none"}, "hook": "Watch me find today's space photo",
              "take": "takes/creator.mp4", "product_on_screen_s": 1.5, "confirmed_by_user": true}}
```

The transcript must be of this exact file (its fingerprint is in it). `hook` is one of the script's
hooks and gets the same claim checks. `take` names the clip (or a list of clips) the edit was cut
from, so a take is never used for two campaigns or twice on one platform; a re-export or a copy in
another format is caught by its sound and frames too. `on_screen` and
`confirmed_by_user` are what the creator saw on the frames: never set them without asking. Then the
same checks as a make_video edit (what is said, the disclosure in time, length, 9:16, captions, the
ledger), the plan, the yes, posting and the ledger.

## deliver_files mode

When the brand posts the videos (`"mode": "deliver_files"` in campaign.json), `accounts` can be
empty and each post names its `platform` instead. `plan.py` writes `deliver/compliance.md` and
`deliver/manifest.json` (every file's SHA-256, its disclosure on screen and said, a suggested
caption) to hand over with the files, and no requests.
