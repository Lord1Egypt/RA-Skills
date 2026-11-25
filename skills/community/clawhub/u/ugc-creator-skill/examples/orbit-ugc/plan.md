<!-- written by plan.py; it replaces this file on every run -->
# UGC plan: Example Orbit: split-screen UGC

Campaign `example-orbit-app` for Example Orbit. Checklist version `eae2ccd694`, script version `e81c093343e5`. Planned Wed 18 Nov 09:00 America/New_York (EST).

**Plan id `2df01d14d86f`.** To post exactly this, say yes to plan `2df01d14d86f`. If any video, caption or setting changes after that, the yes no longer holds and you get a new page.

3 videos for 3 accounts (2 posts through WoopSocial, 1 by hand). Everything goes out now, when you say yes, so you can submit each link within 30 minutes.

**EXAMPLE ONLY: a made-up demo campaign. The brand, the app, the accounts and the links are invented, nothing here is a real ad, the creator's half is a placeholder, and NASA endorses nothing.**

## Before you post

- Post only from accounts connected and verified in an example marketplace (made up); posts from any other account are rejected.
- At least 40% of each video's viewers must be in the US, the UK, Canada, Australia. Post from the accounts whose viewers are already there, when they are awake. Never a VPN or location trick.
- Deadline: 2026-12-15 (America/New_York).
- This brief takes 3 submissions. Per video, the platforms rank: TikTok ($18.00 at 10,000 views, pays from 2,500), Instagram Reels ($18.00 at 10,000 views, pays from 2,500), YouTube Shorts ($9.00 at 10,000 views, pays from 5,000). A second video on the best platform can earn more than one on the weakest. Your call.
- Posting all at once means every in-app step and submission inside the same 30 minutes. Add "stagger": true to job.json to send one post at a time, each with its own clock.

### TikTok @example.creator (TikTok), post `orbit-tiktok`

- Video: `videos/tiktok.mp4`, 22.3 s, 540x960, 0.6 MB, fingerprint 8175e9d2b69b, split screen
- Opens with (h1): "This launch could be your lock screen"
- Disclosure on screen: "Ad" from the first frame for 3 s; said out loud at 6.3 s (estimated: placeholder, no audio)
- Caption (148 of 2200):

  > #ad This launch could be your lock screen: a new space photo every day. Example Orbit, made-up app for this demo @example.orbit #exampleorbit #space

- Settings: seen by everyone; comments on; duets off; stitches off; branded content on ("Paid partnership" label); by posting, you agree to TikTok's Branded Content Policy and Music Usage Confirmation; no auto music
- Expected earnings: $2.00 per 1,000 views, 10% fee (the $5.00 minimum applies to the amount before the fee). Pays nothing under 2,500 views. 1,000 views: $0.00; 10,000 views: $18.00; 100,000 views: $180.00. Cap $200.00 per video, reached at 100,000 views.
- Checks: all passed (see below)
  - note: placeholder take: the skill's example has no person in it. A real video is your own recording

### Reels @example.creator (Instagram Reels), post `orbit-reels`

- Video: `videos/reels.mp4`, 22.3 s, 540x960, 0.6 MB, fingerprint d3ff1d44edaf, split screen
- Opens with (h2): "A new space photo every single day?"
- Disclosure on screen: "Ad" from the first frame for 3 s; said out loud at 6.3 s (estimated: placeholder, no audio)
- Caption (104 of 2200):

  > #ad A new space photo every day, two taps to make it your wallpaper. @example.orbit #exampleorbit #space

- Settings: Reel; paid partnership label: you turn it on in the app
- Expected earnings: $2.00 per 1,000 views, 10% fee (the $5.00 minimum applies to the amount before the fee). Pays nothing under 2,500 views. 1,000 views: $0.00; 10,000 views: $18.00; 100,000 views: $180.00. Cap $200.00 per video, reached at 100,000 views.
- Checks: all passed (see below)
  - note: placeholder take: the skill's example has no person in it. A real video is your own recording
- Inside the 30 minutes after it is live:
  - Instagram: edit the Reel in the app and turn on the paid partnership label (add Example Orbit as partner if the brief asks). WoopSocial can't set it.

### Shorts @examplecreator (YouTube Shorts), post `orbit-shorts`

**By hand**: see `by-hand/orbit-shorts.md`.

- Video: `videos/shorts.mp4`, 21.9 s, 540x960, 0.4 MB, fingerprint 6d7b8f3e9a8a, face screen
- Opens with (h3): "Watch me find today's space photo"
- Disclosure on screen: "Ad" from the first frame for 3 s; said out loud at 5.9 s (estimated: placeholder, no audio)
- Title: Finding today's space photo
- Caption (127 of 5000):

  > #ad Watch me find today's space photo and save it as a wallpaper in Example Orbit (a made-up app). @example.orbit #exampleorbit

- Tags: space, wallpaper, example
- Settings: public; not made for kids; "includes paid promotion": you tick it in YouTube Studio
- Expected earnings: $1.00 per 1,000 views, 10% fee (the $5.00 minimum applies to the amount before the fee). Pays nothing under 5,000 views. 1,000 views: $0.00; 10,000 views: $9.00; 100,000 views: $90.00. Cap $200.00 per video, reached at 200,000 views.
- Checks: all passed (see below)
  - note: placeholder take: the skill's example has no person in it. A real video is your own recording
- Inside the 30 minutes after it is live:
  - YouTube: in YouTube Studio open the Short's details and tick that it includes paid promotion. WoopSocial can't set it.

## Files to upload

Only after the yes, once each:

- `videos/reels.mp4` (0.6 MB, fingerprint `d3ff1d44edaf61a2`)
- `videos/tiktok.mp4` (0.6 MB, fingerprint `8175e9d2b69bcf34`)

Save each upload in media.json as {"<file>": {"mediaId": ..., "sha256": "<fingerprint>"}}.

## Requests

- `requests/example-orbit-app.json`

## By hand

- `by-hand/orbit-shorts.md`

## After it's live

- Submit every link within 30 minutes, into this campaign only, once. `submit.md` gives the clock time per post and when to take the proof screenshots.
- Leave every post public and unchanged for 30 days. Views count for 30 days from the day a video crosses the payout threshold.
- Earnings are estimates: the campaign's own count decides what is paid, and many videos earn little. Never buy views or join engagement groups: it is a permanent ban on the marketplaces.
