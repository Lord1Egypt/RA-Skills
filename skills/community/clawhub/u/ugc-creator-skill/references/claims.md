# Claims: say only what is true for you, or what the brand says

The FTC Endorsement Guides say an endorser must actually use the product, and can't talk about an
experience they didn't have. A paid creator saying "I've used it for months" after one day is a
fake testimonial, and the brand and the creator are both on the hook. So every line of the script
carries a tag, and `script.py` checks each one.

| Tag | What it is | What `script.py` asks for |
|---|---|---|
| `"claim": "experience"` | your own use or result: "I open it every morning", "it saved me an hour" | a recorded confirmation from you that it is true (`script.py --confirm <line> --note "..."`). Change the line, and it needs confirming again |
| `"claim": "brand"` with `"talking_point": "tp1"` | what the brand says about its product | the talking point it comes from, shown next to the line in `script.md`. A line that strays far from its talking point is flagged; an absolute claim ("guaranteed", "100%", "cures") must be in the talking point word for word |
| `"claim": "cut"` | a line you decided not to say | nothing: it is listed under "Cut" in `script.md` and never filmed |
| `"claim": "none"` or no claim | a plain line with no claim in it | nothing. A line that sounds like a claim (numbers, "best", "fastest", "free", "I've used", "my skin", "now my", "doctors recommend") is an error until it is tagged |

Hooks, the disclosure line and the call to action are checked the same way. So are the captions and
YouTube titles: a claim word ("clinically proven", "#1", "dermatologist approved", "best", a number)
needs a talking point or script line that says it, and a sentence about you ("Day 14 of using it",
"we use it every night", "obsessed") needs a line you confirmed. And what the creator actually
said: `check_videos.py` reads each take's transcript and compares every sentence with the closest
script line (or two neighbouring lines). A sentence that isn't in the script is an error until it
is added (and confirmed when it is an experience) or cut, and so is one that adds or drops a "not"
or "never" ("it never shows a new photo every day").

When the brief dictates a result or a habit ("say it cleared your breakouts", "act like you just
discovered it", "the app you use every day"), the checklist asks it as a question first, under
"Only if true for you". A no means a reworded line that is true (what you did find, how you
actually use it) or asking the brand.

Also refused anywhere: the brief's `do_not_say` words (matched without caring about case, curly
apostrophes, hyphens or punctuation), and anything that plays down the ad ("not an ad", "nobody paid
me").

The claims patterns read English. For a script in another language the checklist says so, and every
line needs reading by hand.

## Make-money campaigns

A campaign about earning money (side hustles, cashback, get paid to ...) follows what the FTC and
TikTok require:

- **No earnings claim without the typical result.** A money figure, "I made", "you can make" or
  "earn up to" is an earnings claim. It is allowed only with a true line on what people typically
  earn, from a source the brand gives (`typical_earnings`: `{"line": ..., "source": ...}`), said in
  the video (`"kind": "typical_earnings"`). "Results not typical" alone isn't enough. Without that
  line, earnings claims are refused, and a plain video ("this app pays creators per view") runs.
- **No get-rich-quick framing.** "Easy money", "passive income", "in 20 minutes a day", "quit your
  job", "guaranteed income" are refused in the script, the captions and what is said.
- **TikTok stays in** when the framing is plain and honest. TikTok's branded content policy bans
  get-rich-quick schemes; when the brief itself asks for that framing, the plan leaves TikTok out.

Never your own income claims you can't show, never a promise.

## Refused outright

- Posting from an account the brand owns or runs as a made-up person (`accounts_owned_by:
  "brand"`): viewers can't tell a paid creator is talking.
- A brief asking for a testimonial about use or results that didn't happen.
- A brief that requires an AI presenter, avatar, cloned voice or face swap. (A brief that only
  allows AI UGC is fine: you film, and the skill never uses one.)

NO-GO until the brand answers: posting as someone you aren't ("post as a happy customer", "pretend
you're a regular user"), and a brief that requires a text-to-speech voice.

The skill only edits what a real creator films; it never generates or alters a face or a voice.
