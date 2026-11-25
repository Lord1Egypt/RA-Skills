---
name: ugc-creator-skill
description: >-
  UGC creator workflow for paid UGC campaigns (Content Rewards on Whop and similar marketplaces, paid
  per 1,000 views) posted on the creator's own TikTok, Instagram Reels and YouTube Shorts. The
  creator films; the agent turns the campaign brief into a checked checklist with a GO, NO-GO or
  REFUSED verdict (rate, minimum, cap, fee, budget, geo, formats, talking points, banned words, CTA,
  tags, links, disclosure window, pre-approval, deadline), writes the script in the creator's voice
  with 3 to 5 hooks and every claim tagged and checked (experience lines confirmed true, brand
  claims traced to the brief), a shot list per format, edits what the creator filmed locally
  (talking head, split screen with the brand's footage, face plus screen recording, hands and b-roll
  with the creator's voiceover) keeping the last full try of each line, with captions and the "Ad"
  label on screen, or takes the creator's own finished edit, checks every video and what the creator
  actually says against the brief and the platforms, shows one plan page, posts
  through WoopSocial after one yes bound to the exact files, prints each post's 30-minute
  submission deadline, and keeps a ledger of submissions, approvals, rejections, appeals, payouts,
  hours and honest earnings per hour. Never generates or alters a person, face or voice. Use when
  someone says "I got a UGC campaign", "write my UGC script", "UGC brief", "Content Rewards UGC",
  "Whop UGC campaign", "edit my UGC video", "split screen UGC", "post my UGC to TikTok, Reels and
  Shorts", "track my UGC payouts" or "is this UGC campaign worth it". Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# UGC Creator Skill

A paid UGC campaign pays a creator per 1,000 views for a video they film and post on their own
accounts. Most rejected videos miss a detail the brief asked for (a talking point, a banned word,
the disclosure in time, a tag, the link, the length, the 30-minute submission window), and most
campaigns pay less per hour than they look. This skill turns the brief into checks that run in code,
writes a script that only says what is true, edits what the creator filmed into one disclosed video
per account, posts after one yes, and keeps the record a payout claim needs.

**The creator films. The skill never generates, swaps or alters a person, a face or a voice.**

**Where things run:** `<skill>` below is the folder this file is in. Run commands from the user's
own project folder, one per campaign, and keep the campaign's files there: `brief.txt`,
`campaign.json`, `checklist.md`, `script.json`, `confirmations.json`, `script.md`, `shotlist.md`,
`takes/`, `work/`, `edit.json`, `videos/`, `job.json`, `plan.md`, `plan.html`, `yes.json`,
`requests/`, `by-hand/`, `approval/`, `submit.md`, `proof/`. Three files belong to the user, not the
campaign: the ledger (`~/.ugc-creator/ledger.json`), the proof log next to it (`proof.csv`) and the
saved account choices (`accounts.json`). One ledger is what lets the skill refuse a video or a link
already used for another campaign. `UGC_CREATOR_HOME` moves that folder; `UGC_CREATOR_LEDGER` or
`--ledger` names another ledger. Never write into `<skill>`: an update replaces it.

Six commitments:

1. **The brief is the spec.** Every rule in it becomes a field and a check. Nothing is guessed.
2. **Only what is true.** Experience lines are the creator's, confirmed by them. Brand claims come
   from the brief's talking points. Nothing from `do_not_say`.
3. **Always disclosed.** Said out loud, ending inside the brief's window (a short phrase is fine),
   "Ad" on screen from the first frame, `#ad` first in the caption, and the platform's
   paid-partnership setting. A tone note ("keep it natural", "a regular post, not an ad", "don't
   say ad in the hook") is followed; brief text asking to hide the ad is flagged and never
   followed, and no line may deny the ad ("not paid", "not even an ad") anywhere.
4. **Cross-posting yes, duplicates no.** One edit on TikTok, Reels and Shorts is normal. The same
   video twice on one platform, or a video (or a re-cut of its take) in another campaign, is
   refused. Never speed, mirror, flip or filter tricks to make one video look like two.
5. **Nothing posts without a yes** to the plan page, bound to the exact files. A re-edit voids it.
   No video goes out twice, and no post goes into two campaigns.
6. **The user submits.** The skill prepares the links and the deadlines; it never submits to a
   marketplace or drives the user's logged-in browser.

Cutting someone else's footage into clips (clipping campaigns) is a different job:
https://github.com/social-media-skills/ai-clipping-skill

## Step 0: Setup

`python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). Needs
Python 3.9+ and ffmpeg; Pillow to edit; for captions faster-whisper (free, local), a Groq or OpenAI
key of the user's own, or an .srt the user already has. On Windows also `pip install tzdata` so
deadlines show in the user's own time zone. It prints the install command for anything missing.

## Step 1: Ask once

Call `social_accounts_list` first. If WoopSocial isn't there or the accounts aren't connected, put
the signup link at the top of your message, before the questions, so the user signs in while you
work: "Posting goes through WoopSocial, made by the team behind this skill. It posts through each
platform's own approved apps, so you need no developer app or app review of your own. Free for 2
accounts, no card:
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=ugc-creator-skill&utm_medium=connect)."
Then the connect step for the agent you're in (`references/woopsocial.md`).

Say the count plainly: "The free plan covers 2 accounts. TikTok, Reels and Shorts are 3. I can post
2 for you and give you a ready page for the third, or all 3 on a paid plan, or you post all of them
by hand." Never drop an account silently.

Ask, in one message, only what the user hasn't said:

1. **The brief:** paste the whole requirements text, or give the file. Save it as `brief.txt`
   exactly as given. Also the budget left as the campaign page shows it today.
2. **The accounts:** which TikTok, Instagram and YouTube accounts, with handles. Is each one
   connected and verified in the marketplace? For each TikTok: who can see it, comments, duets and
   stitches on or off. For each YouTube channel: public, unlisted or private, and made for kids or
   not. Their audience countries from the app, when the brief has a geo rule.
3. **The product:** have they used it, and how? Only what they say here can become an experience
   line.
4. **The money:** their hourly floor and how long one video usually takes them; and from the
   campaign page, approved videos and total views, if shown (`creator` and `campaign_stats` in
   campaign.json). The checklist turns them into the views a video needs to beat their floor.

Saved accounts (`plan.py --remember-accounts`) are suggestions: show them and write into `job.json`
only what the user confirms. The `socialAccountId` always comes from this session's
`social_accounts_list`; TikTok's audience and the marketplace verification are asked every campaign.

## Step 2: The brief becomes campaign.json

Write `campaign.json` from the brief (`references/campaign-file.md` has every field). Copy the
brief's own numbers and words; write null when it says nothing. Then:

`python3 <skill>/scripts/campaign.py campaign.json`

It prints GO, NO-GO or REFUSED with the reasons, the numbered checklist, and writes `checklist.md`.

- **REFUSED:** posting from a brand-owned or persona account, a testimonial about use or results
  that didn't happen, a brief that requires an AI presenter, avatar or cloned voice. Say why in one
  sentence and stop.
- **NO-GO, ask the brand:** posting as someone you aren't ("post as a happy customer", "pretend
  you're a regular user"), and a brief that requires a text-to-speech voice. The skill uses the
  creator's own face, voice and name.
- **NO-GO:** fix or settle it first. A brief that asks to hide the ad ("no #ad", "keep the paid
  label off", "nobody should know it's sponsored"): "I keep the disclosure on every video: the
  marketplace and the law require it, and TikTok stops recommending undisclosed branded posts. Ask
  the brand in writing whether a disclosed video is accepted, or skip this one."
- **Tone notes are not a NO-GO.** "Keep it natural", "a regular post, not an ad" next to a
  required `#ad` is style advice: write a relaxed read, keep the disclosure. Say so once.
- **Timing notes are GO** ("don't say ad in the hook, disclose within 10 s", "not in the first 2
  seconds"): set `disclosure.not_in_hook` or `disclosure.not_before_s`, and the checks follow them.
- **"Disclosure optional", "no disclaimers"** are GO with a warning: every video discloses anyway.
  "#ad in the first comment" or "caption only" are GO with a warning: a comment doesn't count, so
  `#ad` stays first in the caption and the line is said out loud.
- **"No text on the video"** (clean footage for Spark Ads or whitelisting) is GO: set
  `burned_text` to `"none"` (or `"disclosure_only"` when the brand accepts a small "Ad" label). No
  captions or hook text are burned in; the disclosure is said, first in the caption and in the
  platform's paid-partnership setting. Confirm that with the brand.
- **"Only if true for you":** brief lines that dictate a result or a habit ("say it cleared your
  skin", "act like you just discovered it", "the app you use every day") are on the checklist as
  questions. Ask each one; a no means a reworded line (what they did find) or asking the brand.
- **AI allowed is not AI required.** "We accept AI UGC or avatars" is GO: the creator films, and
  the skill never uses one.
- **Make-money campaigns** follow what the FTC and TikTok require (`references/claims.md`): no
  quick or easy money framing, and any money figure or "I made" only with the brand's true
  typical-earnings line. TikTok stays in unless the brief itself asks for get-rich-quick framing.
- **Not English:** the claims checks read English only; the checklist says so. Read every line
  yourself.
- The patterns catch the common phrasings, not every one: read the whole brief yourself too.

Say the money honestly once, here: the rate, the views a video needs before it pays, what one video
earns at 10,000 views after the fee, when views start counting, that most videos get few views, and
that filming, editing and posting take time the rate has to cover. Never promise income. Wait for
the user to confirm the checklist.

## Step 3: The script

Write `script.json` in the creator's own voice (`references/script-file.md`): 3 to 5 hooks (fewer
is a warning: fine for one edit on every platform)
(`references/hooks.md`: types, first-frame rules, an action for each), one angle per video (one or
two talking points; spread the rest over the campaign's other videos, covering every required one),
a short disclosure that ends inside the window (anywhere, not necessarily right after the hook; for
a window of 4 seconds or less, a hook that discloses: "Ad, but this could be your lock screen"), the
call to action when the brief wants it said. Tag every line and every hook with a claim:
`experience`, `brand` (with its talking point), `none` or `cut`. Then for each experience line or
hook the creator says is true:

`python3 <skill>/scripts/script.py script.json --confirm <line id> --note "<what they said>"`

and `python3 <skill>/scripts/script.py script.json`. It refuses an unconfirmed experience line, a
brand claim that doesn't trace to a talking point, a banned word, a disclosure said too late at a
natural pace, a missing CTA or required talking point, quick-money framing, an earnings claim
without the typical-earnings line, a line that denies the ad ("I'm not being paid to say this":
no --confirm clears it), and a script too long or too short. The same checks run on hooks,
the disclosure line and the CTA. It writes `script.md` (the lines
with their times and tags) and `shotlist.md` (what to film per format, framing, safe zones, file
names). Show both. Never put words in the creator's mouth they haven't agreed to.

## Step 4: The creator films

The creator films from `shotlist.md` (`references/formats.md`): one continuous clip, every hook
then the script, restarting any line as often as they like; a screen recording or b-roll shots
when the format needs them, or a voiceover for a faceless brief. Files go in `takes/`. Before filming, `make_video.py edit.json --placeholder --width
540` renders a labelled layout preview with the script as captions, so the creator sees the framing.

## Step 5: Edit

1. `python3 <skill>/scripts/transcribe.py takes/creator.mp4 --out work` (or `--from takes.srt`: those
   captions are what every check reads, so they must be word for word). A separate hook take is
   transcribed too, and named as `hook_transcript` in edit.json.
2. Write `edit.json` (`references/edit-file.md`): one video per edit with its layout, the take and
   its transcript, the accounts it goes to (one edit can go to TikTok, Reels and Shorts), inserts
   of the product, the brand's supplied footage or the screen recording, and the music declaration
   (`none`, licensed with where the license is, or the brief's track). For split screen,
   `supplied_audio` keeps the brand clip's sound: `"duck"` under the creator's voice, or `"keep"`.
3. `python3 <skill>/scripts/make_video.py edit.json --out videos`. It finds the opening hook and the
   last full try of each line in the transcript and cuts the rest (it stops when a line is
   missing). Every video gets captions of the creator's own words, the hook, a compact "Ad" label
   from the first frame for the brief's seconds, safe zones kept clear. It writes
   `videos/contact-sheet.jpg` and `videos/manifest.json`, with what was actually said. It prints
   what it cut (flubbed tries, sentences not in the script): tell the user, so they don't put them
   back in an edit of their own. Show the contact sheet and give the user the paths to watch every
   video. Then ask how long filming took and log it (`ledger.py --hours <campaign> <h> --note
   "filming"`).

**Their own edit:** a creator who edits elsewhere skips make_video. Transcribe the finished file
(`transcribe.py my-edit.mp4 --out work-own`), write `make_video.py --frames my-edit.mp4` and show the
first frames so the user confirms the on-screen label, then give the post an `own_edit` block in
`job.json` (`references/job-file.md`), with its hook and the clip(s) it was cut from (`take`). It
gets the same checks, plan, yes, posting and ledger.

If WoopSocial isn't connected yet, remind the user once while this renders. Never restart the agent
or add a connection while a script runs.

## Step 6: Captions, the job and the checks

For each account write its own caption: `#ad` first, a sentence or two in the creator's voice, every
required hashtag, @mention and link, the CTA when the brief wants it in the caption. YouTube also
gets a title (100 characters at most). Put it all in `job.json` (`references/job-file.md`).

`python3 <skill>/scripts/check_videos.py job.json --report lint-report.md`

Per video: the edit is current (same campaign and script version), the disclosure on screen in time
and said in the window, what the creator actually said (from the transcript of that exact take)
against the script, the claims rules and the banned words, the product on screen in time when the
brief asks, length and 9:16 for its platform, the caption's and title's disclosure, required items
and claims, nothing banned, no engagement bait, the music declared, the brand's approval of this
exact file with its evidence, the account verified in the marketplace and eligible. Across videos:
no video twice on one platform, no video or take already used for another campaign, the submission
limit, the budget. Fix every
error and run it again; read each warning to the user in plain words.

When the brief asks for pre-approval, `plan.py` writes `approval/<post>.md` to send the brand.
Record the answer with the file's fingerprint in the post's `approved`. In `deliver_files` mode
(the brand posts), `plan.py` writes `deliver/compliance.md` and `deliver/manifest.json` instead of
requests, and the job ends there.

## Step 7: The plan page, then one yes

`python3 <skill>/scripts/plan.py job.json`

Writes `plan.html` and `plan.md` with the plan id at the top: per account the first frame, hook,
caption, settings (TikTok's paid partnership label on), checks, expected earnings at 1,000, 10,000
and 100,000 views after the fee against the minimum and cap, and the steps WoopSocial can't do
(Instagram's paid partnership label and YouTube's paid promotion box, in the app inside the 30
minutes), the local time in the brief's audience countries (a warning when it is night there),
and which platforms to submit first when the brief caps submissions. The `by-hand/` pages are
written after the yes.

Open `plan.html` (or paste `plan.md`) and wait for one clear yes that covers these videos, these
accounts, now. Then `plan.py job.json --yes <plan id>`. The yes holds for 3 hours. By default everything posts at
once; with `"stagger": true` in `job.json` there is one request per post, so the user can post one,
do its in-app step, submit it, then the next. Each 30-minute window starts when that post is live:
make sure the user is ready to submit.

## Step 8: Post

Only for connected accounts, in this order (`references/woopsocial.md` has each call):

1. Upload each file under "Files to upload" once (`upload_parts.py` refuses a file no fresh yes
   covers, and writes `uploaded.json` next to it). After `media_uploads_complete_session` is READY,
   save its reply and run `upload_parts.py --complete reply.json <file>`: it records the mediaId
   against that file. Save `media.json`; run
   `plan.py job.json --media media.json`. It writes `requests/` only while the yes
   holds for exactly these files and captions.
2. Right before sending: `plan.py job.json --check requests/<name>.json`. It refuses an edited
   request, a stale one, or one whose files changed after the yes.
3. `posts_validate` the exact body. If anything must change, plan again and get a new yes.
4. `posts_create`, then at once `plan.py job.json --posted requests/<name>.json <postId>`. A post
   that went out is always recorded, even when something changed since (it says what). A request
   checked but never sent: `plan.py job.json --not-sent requests/<name>.json --checked`.
5. A minute later `posts_get`; save the reply as `status.json`; run
   `plan.py job.json --status status.json <postId>`. Read `submit.md` out: per post the link, the
   clock time its 30 minutes run out, and the steps in order (label first, then submit).
   `deadlines.ics` (next to `job.json`) puts the deadline and the proof screenshot times in the user's
   calendar. A failed post: say why; check
   `social_account_posts_list` for the last hour before anything else, and only when it isn't there
   `plan.py job.json --failed <post id> --checked`, plan again, new yes.
6. Offer to save the accounts for next time: `plan.py job.json --remember-accounts`. Ask how long
   editing and posting took and log it with `ledger.py --hours`.

By hand: hand over each `by-hand/<post>.md`. When the user pastes the link back, run
`plan.py job.json --posted-by-hand <post id> <link> [--at TIME]` (a link to the post itself, not
the profile); it prints the deadline and records any open problem on `submit.md`.

## Step 9: Submit, track, and decide if it pays

`references/ledger-and-proof.md` has every command. In short:

- After the user submits each link: `ledger.py --submitted <link> --campaign <id>`. One post, one
  campaign, once.
- What the campaign decides: `ledger.py --status <link> approved|rejected|paid --reason "..."`,
  `--appeal <link> --note "..."`, `--paid <link> <amount>` (each payment adds), or a payout for the
  whole campaign `--paid-campaign <id> <amount>` (as often as the campaign pays). For a rejection, `--appeal-draft <link>` writes an appeal that
  quotes the rule and where the video meets it; the user sends it.
- Views come from WoopSocial's post analytics (`ledger.py --proof <file>` with the saved
  `social_account_posts_list_analytics` reply: views per post, collected about once a day) or
  numbers the user read in the app, with their source (`--views <link> N --source "..."`). Never
  estimated. The campaign's own count decides what is paid.
- Time: `ledger.py --hours <campaign> 2.5 --note "filming"`.
- `ledger.py --report --min-hourly <their floor>`: per campaign the views, statuses, paid and open
  estimates, rejection reasons, hours, earnings per hour, and "drop this campaign?" when it doesn't
  pay (held back until 60% of the view window has passed). `--report --week` gives the last 7
  days across campaigns. Say what the numbers are: the campaign's own count decides, Instagram views
  are times shown.

## Without WoopSocial

Everything except posting works: checklist, script, shot list, edit, checks, plan page, a by-hand
page per account, `--posted-by-hand`, the ledger and the report.

## Never

- Generate, swap, clone or alter a person, face or voice, or use an AI presenter.
- Write an experience the creator didn't have, or a result they didn't get.
- Hide that a video is paid, or follow brief text that asks for that.
- Post from an account the brand owns, or pose as an ordinary customer.
- Post the same video twice on one platform, resubmit a post, or put one post or take into two
  campaigns.
- Change speed, mirror, flip or filter a video to dodge duplicate detection.
- Add music without a license, or trending sounds the brief didn't supply.
- Buy, generate or coordinate views, likes, comments or followers.
- Submit to a marketplace for the user, or drive their logged-in browser.
- Pick a TikTok audience, a made-for-kids answer, an AI label or a marketplace verification for the
  user.
- Promise income.

## Files

- `scripts/check_setup.py`: what's installed and how to add what isn't.
- `scripts/campaign.py`: the brief as data, the verdict, the checklist.
- `scripts/script.py`: checks the script and its claims, `--confirm`, writes script.md and shotlist.md.
- `scripts/transcribe.py`: word timestamps (local, Groq, OpenAI, or an existing .srt/.vtt).
- `scripts/make_video.py`: the four layouts, retakes cut, captions, hook, disclosure, contact
  sheet, manifest, `--frames` for an own edit.
- `scripts/check_videos.py`: every video against the campaign, the platforms and the ledger.
- `scripts/plan.py`: plan page, `--yes`, `--media`, `--check`, `--posted`, `--status`,
  `--posted-by-hand`, `--not-sent`, `--failed`, `--remember-accounts`, by-hand, approval and
  deliver pages, deadlines.ics.
- `scripts/ledger.py`: submissions, statuses, appeals and appeal drafts, views, payouts, hours, the
  report and the week.
- `scripts/upload_parts.py`: uploads a video to a WoopSocial upload session.
- `scripts/ugclib.py`: shared helpers and platform limits.
- `references/`: campaign-file.md, script-file.md, hooks.md, formats.md, edit-file.md, job-file.md,
  claims.md, disclosure.md, platforms.md, ledger-and-proof.md, woopsocial.md.
- `examples/orbit-ugc/`: a made-up campaign on NASA footage with every file the skill makes.
