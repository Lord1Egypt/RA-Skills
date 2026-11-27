# Analysis framework

How to go from a list of outlier videos to patterns worth acting on. The aim is to separate what *causes* performance from what merely *accompanies* it.

## 1. Dissect each shortlisted video

Fill these in for the top 10 to 15 outliers (a compact table in your notes is enough):

| Field | What to capture |
|---|---|
| Title formula | The reusable shape, not the exact words (see formulas below) |
| Hook type | Taxonomy below; from the title, description opening, or transcript if one is available |
| Format | Talking head, screen recording, listicle, story, experiment, reaction, tutorial, versus |
| Length | `duration_sec` bucketed: under 60s, 1 to 3 min, 3 to 10 min, 10+ min |
| Angle | The specific promise or tension (not just the topic) |
| Emotional driver | Curiosity, fear of missing out, status, relief, anger, humor, aspiration |
| Channel size | Small channel outlier means the idea is strong; big channel outlier may be audience, not idea |

If you cannot see something (thumbnail, spoken hook), write "not observed". Do not guess.

## 2. Hook taxonomy

- **Curiosity gap:** a specific unanswered question the viewer needs closed.
- **Contrarian claim:** says the common advice is wrong.
- **Specific result:** a concrete number, timeframe or outcome.
- **Problem agitation:** names a pain the viewer feels right now.
- **Story in medias res:** starts mid-event.
- **Authority or proof:** credentials, receipts, screenshots.
- **Challenge or experiment:** "I tried X for N days".
- **Mistake or warning:** "Stop doing X".
- **Before and after:** visible transformation.
- **Pattern interrupt:** unexpected visual or statement in the first seconds.

## 3. Common title formulas

Specific number plus outcome; "Why X is [unexpected adjective]"; "I [did hard thing] so you don't have to"; "X vs Y: which wins"; "The [N] mistakes behind [bad result]"; "How [specific person/type] [achieved result] without [common requirement]"; plain how-to with a concrete payoff. Note the formula, then judge whether it appears across channels.

## 4. Validate before calling it a pattern

- At least 3 videos from at least 3 channels show it. Report it as "k of n".
- Compare with a **control group**: run the same queries with `--order date` (recent uploads regardless of views) and look at typical performers. If the "winning" trait is just as common among average videos, it is not a differentiator. Without this step you only see survivorship bias.
- Check for a confounder: is the pattern really about format, or about one hot topic that happens to share a format?
- Prefer patterns that hold in both small and large channels.

## 5. Timing: rising, peaking or saturated

- **Rising:** few outliers, mostly small channels, high `views_per_day`, uploads clustered in the last 1 to 2 weeks.
- **Peaking:** many outliers in the last 2 weeks from mixed channel sizes.
- **Saturated:** dozens of near-identical angles, big channels already covered it, newer uploads show falling `outlier_x`.
- **Evergreen:** outliers spread over months with steady velocity.

Say which one applies per pattern, since the advice differs: rising means move fast, saturated means find a sub-angle.

## 6. From pattern to idea

Each idea carries: working title, hook (one sentence, in the audience's language), format and length, the angle that differentiates it, linked evidence (2 to 3 videos), and why it suits this user (their audience, skills, resources). Transform the pattern: change the topic, example or angle so the result is new. Copying a specific video's structure beat for beat is neither original nor durable.
