# script.json: hooks, lines and claim tags

The agent writes the script in the creator's own voice from the talking points, then runs
`python3 <skill>/scripts/script.py script.json`. It checks the script and writes `script.md` (what
to say, with times and tags) and `shotlist.md` (what to film per format).

```json
{
  "campaign": "campaign.json",
  "format": ["split_screen", "face_screen"],
  "language": "en",
  "hooks": [
    {"id": "h1", "text": "This launch could be your lock screen", "claim": "none",
     "action": "hold the phone up to the camera with the launch photo on screen"},
    {"id": "h2", "text": "A new space photo every single day?", "claim": "brand", "talking_point": "tp1",
     "action": "point at the launch on screen, then look at the camera"},
    {"id": "h3", "text": "Watch me find today's space photo", "action": "open the app on camera as you say it"}
  ],
  "lines": [
    {"id": "d1", "kind": "disclosure", "say": "Example Orbit is paying me to show you this."},
    {"id": "l1", "claim": "brand", "talking_point": "tp1", "say": "It shows a new space photo every day."},
    {"id": "l2", "claim": "experience", "say": "I've opened it every morning this week to see the new one."},
    {"id": "l5", "claim": "cut", "say": "Honestly it's the best space app out there."},
    {"id": "c1", "kind": "cta", "say": "Download Example Orbit, link in bio."}
  ],
  "openings": {"TikTok": "h1", "Reels": "h2", "Shorts": "h3"}
}
```

Checked:

- 3 to 5 hooks, all different (`references/hooks.md`). `openings` says which hook opens each
  account's video; one hook can open the same edit on TikTok, Reels and Shorts. `action` is what
  the creator does while saying it; it goes into the shot list.
- Hooks get the same claim check as lines: a hook with a brand claim is tagged `brand` with its
  `talking_point`, one about the creator's own use is `experience` and confirmed, anything
  absolute ("the best", "guaranteed") is refused.
- Every line has an `id` and `say`. `kind` is `disclosure`, `cta`, `typical_earnings` or a plain
  line; `claim` is `experience`, `brand` (with `talking_point`), `none` (no claim at all: a
  transition) or `cut` (references/claims.md). The disclosure line and the call to action are
  checked for claims too.
- `experience` lines and hooks need the creator's confirmation:
  `script.py script.json --confirm l2 --note "yes, every morning since Monday"` (saved in
  `confirmations.json`, tied to the exact words; change the line and it needs confirming again).
- The disclosure can be short and sit anywhere: it must plainly say it is paid ("Example Orbit is
  paying me to show you this", "#ad with Example Orbit", "Paid partnership with Example Orbit") and
  the end of the sentence that says it must fall inside the brief's window, counted with the
  longest hook first at a natural pace (2.6 words a second; `"words_per_second"` from 1.5 to 4.5
  for a faster or slower speaker). "No ads" or "this is not an ad" never counts.
- One angle per video: more than 2 talking points is a warning. A talking point marked `required`
  in campaign.json must be in every script.
- The call to action is said when the brief wants it spoken; nothing from `do_not_say`; no quick or
  easy money framing; a money figure or "I made" only with a `typical_earnings` line; the length
  inside the brief's.

The script version (a fingerprint of hooks, lines and openings) goes into every edit. If the script
changes after filming or editing, `check_videos.py` asks for the edit again, so a video never goes
out with lines that weren't checked. What the creator actually said is checked too: the transcript
of each take goes through the same claims, `do_not_say` and disclosure checks, and a sentence that
isn't in the script is an error until it is added to the script (and confirmed) or cut.
