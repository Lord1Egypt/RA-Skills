# Disclosure: every campaign video says it's paid

A video made for a paid UGC campaign is an ad, also when it is paid per view. The creator has a
material connection to the brand, so advertising law in the US (FTC Endorsement Guides), the UK
(CMA, which can fine directly since the DMCC Act) and the EU (consumer protection law) asks for a
clear disclosure. Content Rewards treats all content posted for one of its campaigns as a material
connection and requires the platform's paid-partnership setting where it exists and "#Ad" at the
top of the caption.

The skill makes disclosure part of the video, not an option.

## Four places, every time

1. **Said out loud, early.** The script has a line with `"kind": "disclosure"` that plainly says
   it is paid and ends inside the brief's window (`disclosure.spoken_within_s`, 10 s by default),
   counted with the longest hook first. It can sit anywhere in that window and be short:
   - "<brand> is paying me to show you this, and..."
   - "#ad with <brand>, but look at this"
   - "Paid partnership with <brand>:"
   - "This is an ad for <brand>."
   Common words in other languages count too (publicidad, publicidade, patrocinado, Werbung,
   Anzeige, sponsorisé, publicité, pubblicità, reclame, gesponsord). A hook that discloses counts
   too ("Ad, but this could be your lock screen"): that is how a 3-second window is met.
   What never counts: a negation ("no ads", "this is not an ad", "ad-free"), a bare "paid" or
   "promotion", or a word that only happens to be there ("I saw an ad", "the pub", "my sponsor at
   the gym"). In the video, only the script's own disclosure line (or a close match, or a hook that
   discloses) counts, found in the transcript of what was said, on every route: make_video edits,
   `"assemble": false`, hook takes and your own edits. `check_videos.py` reads it again every time
   and refuses a video where it comes late, too early for the brief, or not at all.
   Timing notes in the brief are followed: `"not_in_hook": true` keeps it out of the hook,
   `"not_before_s"` keeps it out of the first seconds; it still ends inside the window.
2. **On screen from the first frame** (unless the brief wants no text on the video: then
   `"burned_text": "none"` and the other three carry it; confirm that with the brand). `make_video.py` draws `disclosure.on_screen` ("Ad", or the
   brief's wording) as a compact label in the top-left corner for `on_screen_seconds` (3 by
   default), below the apps' top tabs and clear of the hook.
3. **First in the caption.** The caption starts with `#ad` (or the brief's stronger wording), so it
   shows before "more". Not acceptable: `#sp`, `#spon`, `#collab`, a brand tag alone, a disclosure
   buried among hashtags or only in a comment.
4. **The platform's setting.** TikTok's paid partnership label is sent with the post
   (`isBrandedContent: true`). WoopSocial can't set Instagram's paid partnership label or YouTube's
   paid promotion box, so the plan page and the submission sheet list them as steps in the app,
   inside the 30-minute window.

## What is refused

- A campaign without an on-screen or caption disclosure, or one that doesn't say it is paid.
- A video without the spoken line, said too late, or without the on-screen line from the first
  frame.
- Anything that denies the ad, in the script, what is said, the captions or the titles: "not
  paid", "nobody is paying me", "not even an ad", "even if they didn't pay me", `#notanad`. No
  `--confirm` clears it.
- A TikTok campaign post set to "only you" (TikTok doesn't allow branded content there, and it
  earns nothing).

## Tone notes are not hiding

"Keep it natural", "it shouldn't feel like an ad", "a regular post, not an ad", "make it feel
native, not salesy" next to a required `#ad` ask for a style, not for hiding the ad. `campaign.py`
lists them under "Tone notes", the verdict stays GO, and the script reads relaxed with every
disclosure in place. The same for timing ("don't say ad in the hook, disclose within 10 s", "not in
the first 2 seconds"): GO, with `not_in_hook` or `not_before_s` set.

Briefs that call the disclosure optional ("disclosure optional", "no disclaimers") or put it only
in a comment or the caption are GO with a warning: every video discloses anyway, as the law asks.

## Brief text that asks to hide it

`campaign.py` flags sentences like "no #ad", "don't disclose", "don't say it's sponsored", "don't
use the paid partnership label", "use #partner instead of #ad", "put the #ad at the end",
"posts with #ad will not be approved", "keep the label off" or "nobody should know it's sponsored". The verdict is NO-GO until the brand confirms in writing that a disclosed video is
accepted; record who and where in `disclosure_ok_in_writing`. Even then the sentences are shown
under "Never followed" on the checklist and the plan page, and every video keeps all four
disclosures. If the user insists on removing it, decline: the skill doesn't make undisclosed
campaign posts.

Sentences that ask for a different wording of the disclosure are fine; only hiding it is refused.
"Posts without #ad will be rejected" asks for the disclosure and isn't flagged. Sentences the
patterns can't place are listed under "Read these sentences yourself". The patterns can't catch
every phrasing, so read the brief yourself as well.

## Not legal advice

These are the marketplaces' and regulators' published rules as of November 2026. A user with a
specific legal question should ask a lawyer where they live.
