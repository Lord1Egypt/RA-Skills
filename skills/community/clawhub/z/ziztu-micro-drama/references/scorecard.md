# The scorecard: check before you deliver

Score every episode before showing it, and every season grid before writing episodes from it. Scores are out of 10. Anything under 7 gets rewritten before delivery; tell the user the scores in one compact line ("Hook 9 · Clarity 8 · Turn 8 · Payoff 7 · Cliffhanger 9 · Dialogue 8 · Lead 8 · Shootable 9 · Depth 8 · Continuity 9").

Contents
1. Episode scorecard
2. The quick tests
3. Season grid checks
4. Automated checks

## 1. Episode scorecard

| Criterion | 9 to 10 looks like | Under 7 looks like |
|---|---|---|
| **Hook** | The first frame is a conflict a stranger understands with the sound off | A place, a wake-up, a greeting, backstory |
| **Clarity** | By second 10 the viewer knows the conflict, who the two people are to each other, and what the lead wants right now | The viewer is still working out who is who at 20 seconds |
| **Turn** | One real reversal, between 30 and 50 percent of the runtime, that changes the power in the room | No turn, or two turns crammed into a minute so neither lands |
| **Payoff** | A satisfying beat sized to the wound: a comeback, a refusal, an exposure, a rescue (big and public on a release episode) | Nothing is won, or the win happens off screen |
| **Cliffhanger** | Cut on the peak with one specific question; a different type from the last episode; new information, not louder volume | Cut after the peak, a vague mood, the same type as last time, or resolved before the cut |
| **Dialogue** | Every line is a move; most lines under 12 words; one quotable line of 10 words or fewer | Speeches, pleasantries, explaining feelings, "as you know" |
| **Lead** | The lead acts: answers back, chooses, schemes | The lead only suffers, or misses something obvious |
| **Shootable** | Two or three speakers per scene, one or two places, everyone in the frame named, captions for text | Crowds talking, five places, readable documents, an unnamed person in the shot |
| **Depth** | The hook and the cliffhanger are staged near and far; places use their depth kits; the background carries a story beat at least once (a witness, an arrival, an object) | Everyone side by side in front of a wall; nothing near the camera or far from it; a reveal that walks in from far away |
| **Continuity** | Names, looks, props, places and who-knows-what match the bible and the ledger | A costume that changed silently, a secret someone should not know yet |

## 2. The quick tests

- **3-second test**: read only the first action line and the first line of dialogue. Is it a conflict?
- **Mute test**: would the episode still make sense with the sound off and captions on?
- **Swipe test**: find the most boring ten seconds. If nothing lands in them (a line, a look, an object, a reaction), rewrite them.
- **Last-line test**: after the final beat, does the viewer need the next answer more than they needed this episode's?
- **Template test**: replace the names with A, B and C. If the beat order matches the previous episode's, change the shape (a different payoff type, a different cliffhanger type, a different place).
- **Flat test**: for the hook beat and the cliffhanger beat, name the foreground, the subject and the background. If you can only name the subject, restage it (`depth-and-staging.md`).
- **Wound-to-payoff test**: is the payoff sized to the wound? A tiny insult with a huge payoff feels cheap; a huge wound with a tiny payoff feels like a cheat.

## 3. Season grid checks

- Every episode has a reversal, a payoff and a cliffhanger, and each is marked COMPRESS (pressure piles on) or RELEASE (pressure pays off). No more than two COMPRESS episodes in a row; a RELEASE at least every three episodes.
- No cliffhanger type twice in a row; no type on more than about a third of the episodes.
- Episodes 1 to 3 cover identity, crisis and a first payoff; episode 3 ends on the strongest cliffhanger so far.
- The paywall episode (or episode 3 and 5 on a free series) asks, does not answer; the answer lands one or two episodes later.
- Each villain tier falls in public before the next rises; humiliation and payback cycles last three to six episodes.
- Every secret has a tease, a partial and a full reveal, at planned episodes. No planted question stays untouched for more than about 15 episodes.
- At least ten real complications (reveals, twists, shifts) across a 40 to 70 episode season.
- Cast and places stay inside the limits: about 6 to 10 named speaking characters and 3 to 6 recurring places for the season; two places per episode (a third only as a short insert), four characters per episode at most.

## 4. Automated checks

- `python3 scripts/episode_check.py <files or folder> --target <seconds>` checks runtime (lines and beats, and Ziztu's page-based plan), hook and cliffhanger notes and positions, line and speech lengths, three-in-a-row speakers, speakers per scene, places per episode, cue names, and cliffhanger variety across episodes.
- `python3 scripts/grid_check.py <grid.md>` checks the season grid: cliffhanger types, COMPRESS and RELEASE rhythm, the paywall row, cast and place counts per episode.

Both need only Python 3. When code cannot run, apply the same checks by reading.
