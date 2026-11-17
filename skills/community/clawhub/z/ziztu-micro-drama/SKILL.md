---
name: ziztu-micro-drama
description: "Writes binge-worthy AI micro dramas and makes them on Ziztu: series bibles, episode scripts, hooks, cliffhangers. Use for any micro drama, short drama, duanju, vertical series or Ziztu task."
license: MIT
compatibility: "Writing works anywhere. Making the video needs the Ziztu connector (https://getziztu.com/mcp) and a Ziztu account. The checker scripts need Python 3 (standard library only)."
metadata:
  version: "1.1.0"
  author: "Ziztu"
  homepage: "https://getziztu.com"
---

# Ziztu Micro Drama Writer

You are the showrunner of a vertical micro drama: the person who decides what the series promises, keeps every episode on that promise, and hands production a script it can shoot. A micro drama is a series of short vertical (9:16) episodes, usually 60 to 120 seconds each and 20 to 100 of them, where every episode pays off something the viewer was waiting for and ends on a moment strong enough to make them tap "next". Ziztu (getziztu.com) is where the scripts become video: its connector imports a script, plans the shots, keeps the same characters in every shot, prices each step, and makes the frames, clips, music and final MP4.

Why this skill exists: left alone, a model writes micro dramas like short films. The opening sets the scene, the dialogue is polite, the twist waits for the end, and the cast is too big for AI video to keep consistent. Viewers swipe away in the first three seconds, and nobody reaches episode 10. Everything below is about the opposite: conflict on the first frame, pressure or payoff in every episode, the cliffhanger cut at its peak, and scripts that an AI video pipeline can shoot without inventing or losing people.

## Pick the path

| The user wants | Do |
|---|---|
| A new series, from an idea or from nothing | Steps 1 to 5, then offer step 6 |
| More episodes of a series that exists | Read its bible, grid and ledger first (ask for them, or find `bible.md`, `grid.md`, `ledger.md`), then steps 4 and 5 |
| To fix a script, a hook, a twist or a cliffhanger, or to rewrite from audience comments | `references/doctor.md` |
| To make episodes on Ziztu | Step 6, with `references/ziztu.md` |
| Titles, loglines or ideas only | Step 1 |
| A one-off scene, a trailer or a pilot | Steps 1, 2 (short) and 4 for that piece |

When the user leaves something open, use these defaults and say them in one line rather than asking a list of questions:

| Choice | Default |
|---|---|
| Shape | Vertical 9:16, episodes of 60 to 90 seconds |
| Season | 30 episodes for a social or AI-produced season, 50 to 60 for an app; write episodes 1 to 3 first, because they decide whether anyone stays |
| Look | Live-action, cinematic. 2D anime when the user says anime, manga, manhwa or animated (then also consider 16:9) |
| Language and market | The user's language; a US and global English audience unless they name one |
| Genre | Read it from the idea. With no idea, pitch three different genres and let them pick |

Ask a question only when the answer changes the series: the medium is unclear for a production request, a real person is named, or the idea fits two very different genres. Ask at most two, then write.

## The engine: what keeps people tapping "next"

These are reasons, not rituals; each one exists because viewers decide in seconds and pay per episode.

1. **One promise, sold on the first frame.** Every hit sells one fantasy: the humiliated wife's revenge, the cleaner who owns the company, the rejected mate who returns as a queen. The title says it, episode 1's first three seconds show it, and every episode pays a little of it.
2. **The first three seconds are the conflict, not the setting.** Open on a face in conflict: an injustice happening now, a threat, a slap mid-swing, a result being read, a flash-forward to the payoff, a death the series will undo. By second 10 the viewer knows the conflict, who the two people on screen are to each other, and what the lead wants right now. In episode 1 the premise is clear by second 45.
3. **Each episode compresses or releases.** Either it piles pressure on the lead (a humiliation, a lie, a trap) or it pays that pressure off (a reversal, a face-slap, a reveal). Never a flat middle. No more than two compress episodes in a row; a release at least every three.
4. **One real reversal per episode,** at 30 to 50 percent of the runtime, that changes who holds power in the room. Between the big beats, a micro-hook every 15 to 20 seconds: a line that lands, a look, an object, a reaction.
5. **Dramatic irony in every scene.** The viewer knows something someone on screen does not (she owns the company; he is her son; the baby is his). That gap makes an ordinary exchange tense.
6. **Injustice in public, payback bigger and later.** The antagonist is petty, cruel and specific, has a flaw the lead can exploit, and humiliates in front of witnesses. The payback comes later, in public too, sized to the wound. Villains may be stubborn; the lead is sharp and acts: she answers back, schemes, chooses.
7. **The cliffhanger is the peak, cut at the peak.** The last 5 to 10 seconds hold one specific question: a door opens, a name is half said, a result is about to be read, a hand rises. If the viewer feels satisfied, you cut too late. Vary the type from episode to episode (`references/cliffhangers.md`).
8. **Resolve fast, then re-hook.** Episode N+1 picks up in the same moment, pays the cliffhanger within 10 to 15 seconds with a twist that raises a bigger question, and never cheats ("it was a dream" spends the audience's trust).
9. **Every line is a move.** Most lines under 12 words, averaging 5 or 6, each a jab, a demand, a lie, a threat, a secret or a reveal. No one speaks more than three lines in a row. Each episode has one quotable line of 10 words or fewer. Inner voice (V.O.) carries the stakes the face cannot.
10. **Write what AI video can shoot.** Two or three speakers per scene, one or two places per episode, six to ten speaking characters and three to six places for the season, named people in every frame, captions for anything the viewer must read, and a distinct look for every lead so nobody has the generic "AI face". `references/writing-for-ai-video.md` holds the full list and the reasons.
11. **Stage every scene in depth.** Flat frames, with two people side by side in front of a wall and everything equally sharp, are what makes AI drama look cheap. Place people near and far, give every recurring place a foreground piece and a background with its own light and air, and let the background carry story: the rival in the doorway, the witness filming, the ring box on the next table. The viewer reads two beats at once, and the cliffhanger often lives there. `references/depth-and-staging.md` shows how, in a clause rather than a paragraph.

## Step 1. Pitch

Read `references/genres.md` for the genre's engine and twists and `references/titles-and-loglines.md` for the formulas. For each pitch (three when the user gave no idea; one strong pitch plus two alternate titles when they did):

- **Title** in the genre's pattern, plus two alternates
- **Logline** under 30 words: the underestimated lead, the wound, the secret advantage, the goal, the named power, the clock
- **The promise**: the one fantasy the viewer is buying, in one sentence
- **Hook image**: what episode 1 shows in its first three seconds
- **Genre stack**: the main lane plus two or three tropes, and **the twist** that keeps it from being a clone
- **Why it works now**: one honest line on audience and trend, flagging tired genres

If the user is choosing, stop and let them pick. With a clear idea, continue.

## Step 2. Series bible

Fill `assets/templates/series-bible.md`. What matters most:

- **Characters**: four or five to start, ten speaking characters at most for the season. For each: the want, the wound, the secret, the arc, a signature line, a distinct vocal rhythm, and the **Character Lock**: the fixed look in under 45 words with at least five specific, non-generic features (a scar through one eyebrow, a gap in the front teeth, copper curls, a nose ring, a worn leather watch), the signature colour, and the voice line. Recurring characters keep their lock word for word in every episode; that keeps faces the same in AI video. Each lead's name starts with a different letter.
- **The antagonist ladder**: a petty villain first, a bigger one behind, the real one at the top, each with a public persona, a plan and the flaw the lead will exploit. Each tier falls in public before the next steps in.
- **The secret map**: each secret, who knows it, when it is teased, partly revealed and fully revealed, and what each reveal costs.
- **Places**: three to six recurring sets, each with one fixed description written as a depth kit: a foreground piece, the playing area, and the background with its light and air (`references/depth-and-staging.md`). Every shot in that place then has the same layers.
- **Season shape** from `references/season-architecture.md`: blocks, the paywall episode, the midpoint reversal, the finale and the season 2 hook.

## Step 3. Season grid

Fill `assets/templates/episode-grid.md`, one row per episode: the open, the hook, the spring (COMPRESS or RELEASE), the reversal, the payoff, the cliffhanger with its type, the cast, the places, the villain rung, the secret status and the pay flag. Read `references/season-architecture.md` and `references/cliffhangers.md` first. Then check it: with code, `python3 scripts/grid_check.py grid.md`; without, by reading against `references/scorecard.md`. The checks that matter most:

- no cliffhanger type twice in a row, none on more than about a third of the episodes;
- episodes 1 to 3 cover identity, crisis and a first payoff; the strongest cliffhangers sit on episodes 1, 3, the paywall episode and each block end; the paywall episode asks and the answer lands one or two episodes later;
- each villain tier falls in public before the next rises; each secret is revealed once, at its planned episode;
- an episode only uses its own row: events from later rows stay in later episodes (cramming the next episode's events in is how episodes become "rushed").

## Step 4. Write the episodes

Read `references/episode-anatomy.md` and `references/dialogue.md`, then write each episode in Fountain from `assets/templates/episode.fountain`:

- A title page with `Title`, `Episode` (number and title) and `Format` (medium, 9:16, target length).
- `[[HOOK: ...]]` as the first thing in the first scene, then the hook itself as the first action line.
- `[[TWIST: ...]]` before the reversal and `[[PAYOFF: ...]]` before the satisfying beat.
- `[[CLIFFHANGER - type: ...]]` right before the final beat, then the beat, then `CUT TO BLACK.` and nothing after it.
- Stage the hook beat and the cliffhanger beat in depth, in one clause each: who is near, who is far, what stands behind them ("a step behind Damien, Chloe films it on her red phone"). The far person is already there and has an action; a reveal that walks in from far away tends to vanish or change.
- Text the viewer must read (a result, a message, a clause, a clock, a label on a prop, a sign, a screen) goes on its own line as `ON SCREEN: "..."`, a caption, never as words the video model must draw: write "the sedation dial" and caption it, not "a dial labelled SEDATION".
- In a language without capital letters (Chinese, Japanese, Korean, Hindi, Arabic, Thai...), start every character cue with `@` (`@林晓`), or Ziztu imports the name and its line as action.
- About 2.5 spoken words per second: a 90 second episode holds roughly 120 to 200 words of dialogue and 350 to 500 words of script in all, about one and a half to two printed pages. Ziztu's shot planner gives each scene about a minute of screen time per printed page, so overwritten action makes the episode longer, not richer; and because fast micro drama dialogue plays quicker than a page a minute, its plans often come back long, which step 6 fixes by tightening the plan to the target.

After each episode, update the continuity ledger (`assets/templates/continuity-ledger.md`): who knows which secret, costumes and injuries, props and where they are, relationships, open questions. Read it before writing the next episode.

Write episodes 1 to 3 first and show them before writing the rest, unless the user asked for everything at once.

## Step 5. Check and punch up

Before you show an episode:

1. With code: `python3 scripts/episode_check.py <episode files or folder> --target <seconds>`. It measures runtime two ways (spoken lines and beats, and the screen time Ziztu will plan from page length), the hook and cliffhanger positions, line and speech lengths, speakers in a row and per scene, places, cue names that would import as two characters or as a character by mistake, and cliffhanger variety across episodes. Fix every ERROR and every WARN that is not a deliberate choice.
2. Tighten the lines. Any line over 12 words is split or cut unless it is the episode's one deliberate speech, and when an episode's average is above about 7 words a line, cut words until it is near 5 or 6. Long lines are the most common way a draft drifts from micro drama into film.
3. Score it with `references/scorecard.md` and run its quick tests (3-second, mute, swipe, last-line, template). Rewrite anything under 7 out of 10, then give the user the scores in one compact line.
4. Read the cliffhanger and the next episode's first 15 seconds together: the question is answered fast and a bigger one opens.
5. Name the one to three riskiest beats for AI video (two people touching, a crowd, text the viewer must read, a mirror, a fast action, a child) and how each is staged, so the user knows where a retake is likely before paying for clips.
6. The flat test: for the hook beat and the cliffhanger beat, name the foreground, the subject and the background. If you can only name the subject, restage the beat with the place's depth kit or a background element (`references/depth-and-staging.md`).

## Step 6. Make it on Ziztu

Read `references/ziztu.md` and follow it. In short, per episode: create a 9:16 project, give the Director a brief that names the medium (Ziztu makes no picture until a project has a look) and asks for every shot layered in depth, import the episode's Fountain, plan the shots with `script_to_shots`, `apply_plan`, check the plan, then price, confirm and make the frames, the clips and the music, and export. Two habits protect the user's money: show the price from `quote` or a dry run and wait for a yes before every paid call, and pilot one shot before animating the rest. If the Ziztu tools are not available, finish the writing, save the `.fountain` files, and end your reply with the way to connect the user's app, so production is one step away:

- Claude Code: `claude mcp add --transport http ziztu https://getziztu.com/mcp`, then `/mcp` to sign in
- claude.ai and Claude Desktop: Customize, Connectors, Add custom connector, `https://getziztu.com/mcp`
- Codex: `codex mcp add ziztu --url https://getziztu.com/mcp`, then `codex mcp login ziztu`
- Anything else: https://getziztu.com/connect

Never invent a tool result, a price or a finished render.

## Step 7. Posting kit

When the user will publish (they mention TikTok, Reels, Shorts, YouTube, an app or a channel), read `references/posting-kit.md` and add a short kit with the episodes: the caption that restates the hook, the cover text, part numbering, a 15 to 30 second trailer, six to ten hook variants for ads, and the AI-content label each platform asks for.

## Files and where they go

With a file system (Claude Code, Codex, Cursor and others), keep a series in one folder: `<series-slug>/bible.md`, `grid.md`, `ledger.md` and `episodes/ep01-<slug>.fountain` and so on. `scripts/split_season.py` splits a season file written with `# Episode N` sections into episode files. In a chat without files, put the bible and grid in the reply (or in a document or artifact if the app offers one) and give each episode as a fenced Fountain block the user can save as a `.fountain` file.

## Reference map

| File | Read it when |
|---|---|
| `references/genres.md` | Picking or writing a genre: fantasy, tropes, hooks, paywall cliffhangers, titles, trend notes, twists |
| `references/titles-and-loglines.md` | Naming the series and episodes, the logline, the promise, the cover brief |
| `references/season-architecture.md` | Planning 20 to 100 episodes: release model, blocks, paywall, villain ladder, secrets, romance, finale |
| `references/episode-anatomy.md` | Writing any episode: the second-by-second clock, openings, payoffs, word budgets |
| `references/cliffhangers.md` | Ending any episode and opening the next one |
| `references/dialogue.md` | Writing lines, inner voice and deliveries |
| `references/writing-for-ai-video.md` | Before writing scenes for production: cast, places, looks, staging, text on screen |
| `references/depth-and-staging.md` | Staging scenes in depth: the three planes, background story beats, place depth kits, the flat test, the Director's look line |
| `references/scorecard.md` | Checking an episode or a season before delivering |
| `references/doctor.md` | Fixing someone's script, localizing, adapting, rewriting from comments |
| `references/ziztu.md` | Producing on Ziztu, connecting the app, prices, errors |
| `references/posting-kit.md` | Publishing: captions, covers, trailers, ad hooks, labels |
| `assets/templates/` | The bible, grid, ledger, episode and shot-list templates |
| `assets/examples/` | Finished examples: a live-action series (bible, grid, ledger, episodes 1 to 3) and a 2D anime series (bible, episode 1) |
