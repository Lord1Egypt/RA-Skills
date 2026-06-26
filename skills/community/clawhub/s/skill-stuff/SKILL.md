---
name: main-character-recap
description: Recaps the user's day in the style of any of 50 TV shows with episode title, arc, and cliffhanger. Use when a user wants a fun shareable daily summary delivered automatically.
metadata: {"openclaw":{"emoji":"\ud83d\udcfa","user-invocable":true,"category":"fun","tags":"recap,daily,TV,fun,meme,main-character,shareable,creative,entertainment","triggers":["recap my day","main character recap","daily recap","previously on my life","episode recap","today as a TV show","my day as The Bear"],"requires":{"config":["channels"]},"homepage":"https://clawhub.com/skills/main-character-recap"}}
---

# Main Character Recap

Your day. One TV show. Delivered automatically at end of day.
Remembers yesterday. Builds a season arc. Gets shareable.

No input required after setup.

---

## File structure

```
main-character-recap/
  SKILL.md              ← full engine, loads at setup and management only
  shows/
    active.md           ← current show profile (only file read during cron runs)
    the-bear.md         ← bundled
    succession.md       ← bundled
    [show-name].md      ← user-generated via /mcr add show
  memory.md             ← running season arc, updated after every run
  history/
    YYYY-MM-DD.md       ← one file per day, written after each run
```

**Token discipline:**
- Setup and management: full SKILL.md loads
- Daily cron run: only `active.md` + `memory.md` + cron payload (~600 tokens total)
- Season recap: reads `history/` directory
- Never load the full show library during automated runs

---

## Requirements

Needs at least one connected data source. No binaries required.

**Supported sources (MCP):** Google Calendar, Gmail, Slack, GitHub, Notion, Linear, Todoist.

**If no sources connected:** Tell the user:
> "Connect Google Calendar or Gmail in OpenClaw settings, then run setup again — or describe your day and I'll write the recap from that."

Degrades gracefully. No sources = asks for input. Still useful from day one.

---

## When to use this skill

- User asks to set up their daily recap
- User runs `/recap` or `/mcr` for an on-demand recap
- User wants to change show, time, delivery channel
- User asks to pause, resume, cancel, or check status
- User asks for a weekly or season recap
- User wants to add a custom show

Do NOT use when the user wants a plain factual summary with no creative framing.

---

## Setup flow

### Step 1 — Pick a show

Present the list grouped by Current and Classic.
- "Surprise me" → pick at random
- Can't decide → ask mood, suggest three (see mood map below)
- "Add my own" → run the show generation flow

**CURRENT:**
The Pitt · Severance · The White Lotus · The Last of Us · Adolescence · Andor · The Bear · Shrinking · Abbott Elementary · Only Murders in the Building · Slow Horses · The Diplomat · Fallout · Baby Reindeer · Shōgun · Wednesday · House of the Dragon · Yellowstone · Landman · The Studio · Paradise · Dexter: Resurrection · Nobody Wants This · Black Rabbit · Succession

**CLASSIC:**
Breaking Bad · The Sopranos · The Wire · The Office · Friends · Seinfeld · Mad Men · Game of Thrones · Twin Peaks · Arrested Development · How I Met Your Mother · Ted Lasso · Fleabag · Frasier · 24 · Lost · Curb Your Enthusiasm · Buffy the Vampire Slayer · The X-Files · ER · The West Wing · Band of Brothers · Cheers · Bojack Horseman · House M.D.

**Mood map** (use when user can't decide):
- Chaos / overwhelming day → The Bear, 24, ER
- Dark / political / scheming → Succession, The Wire, Slow Horses, Game of Thrones
- Funny / absurd → Seinfeld, Arrested Development, Curb, Abbott Elementary, The Office
- Warm / hopeful → Ted Lasso, Shrinking, Cheers, Friends
- Mysterious / unsettling → Severance, Twin Peaks, Lost, The X-Files, Paradise
- Reflective / heavy → Breaking Bad, Bojack Horseman, The Sopranos, Fleabag, Baby Reindeer
- Epic / high stakes → Andor, Band of Brothers, The West Wing, Shōgun

### Step 2 — Delivery channel

Default to current channel.

### Step 3 — Trigger time

Default 21:00. Accept natural language. Confirm timezone.

### Step 4 — Write active.md

Copy the chosen show's profile from the show library into `{baseDir}/shows/active.md`.
This is the only show file the cron job will ever read.

### Step 5 — Initialize memory.md

Create `{baseDir}/memory.md` with empty structure:

```md
# Season Memory

## Recurring villain
[none yet]

## Running plotlines
[none yet]

## Season arc so far
[none yet]

## Last episode
[none yet]

## Notable callbacks
[none yet]
```

### Step 6 — Register cron job

CRITICAL: sessionTarget must be "isolated". lightContext must be true.

```json
{
  "name": "Main Character Recap",
  "schedule": {
    "kind": "cron",
    "expr": "<USER_CRON_EXPR>",
    "tz": "<USER_TIMEZONE>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the main-character-recap skill. Read {baseDir}/shows/active.md for style. Read {baseDir}/memory.md for season context. Pull last 24h from all sources. Follow the output format in active.md exactly. After generating, update memory.md and write today's recap to {baseDir}/history/YYYY-MM-DD.md.",
    "lightContext": true
  },
  "delivery": {
    "mode": "announce",
    "channel": "<USER_CHANNEL>",
    "to": "<USER_TARGET>",
    "bestEffort": true
  }
}
```

### Step 7 — Preview

Run `/mcr now` immediately so the user sees the output before the first automated delivery.

---

## Runtime flow (daily automated run)

This runs in an isolated session with lightContext. It only reads what it needs.

### 1. Read active.md
Load `{baseDir}/shows/active.md`. This contains the show's full style profile.

### 2. Read memory.md
Load `{baseDir}/memory.md`. Use the season context to:
- Reference the recurring villain by name if it has appeared before
- Continue running plotlines rather than inventing new ones
- Callback to a previous episode if relevant
- Build the season arc forward

### 3. Pull sources
Pull last 24h from all connected sources (calendar, email, Slack, GitHub, etc.)
Privacy rules: first names only, no addresses or financial figures.
If nothing returns: ask for a one-sentence description. Never fabricate.

### 4. Identify structure
- One central conflict (the villain — never a person)
- Two to four subplots
- Emotional tone of the day
- Any callbacks to memory.md

### 5. Generate recap
Follow the show's voice, vocabulary, section labels, and cliffhanger register exactly.
Reference memory where it makes the output sharper.
See output format below.

### 6. Write history file
Write the full recap to `{baseDir}/history/YYYY-MM-DD.md`.

### 7. Update memory.md
After generating, rewrite memory.md with updated:
- Recurring villain (update if today introduced or evolved it)
- Running plotlines (add, evolve, or resolve)
- Season arc so far (one sentence summary of the arc to date)
- Last episode (today's title and one-line summary)
- Notable callbacks (anything referenced from a previous episode)

### 8. Generate shareable card
After the text recap, generate an HTML shareable card (see card spec below).
Deliver both the text recap and the card.

---

## Output format

Every recap must contain, in the voice of the chosen show:

```
[SHOW NAME] — S∞ E[day of year]
"[Episode title]"

[Narrated recap — 2-4 sentences in show's narrator voice. An arc, not a list.
If memory.md has context, use it — callbacks, recurring villains, season arc.]

[SHOW PLOT POINTS LABEL]:
• [Full sentence in show's voice — meaningful development, not task label]
• [Full sentence]
• [Full sentence — up to five]

[SHOW LOOSE ENDS LABEL]:
• [Unfinished thing in show's language]
• [Another]

[SHOW RUNNING PLOTLINES LABEL]:
• [Season arc energy — may reference memory.md]
• [Another]

[SHOW CLIFFHANGER LABEL]:
[One sentence. Show's exact register. Villain is never a person.]
```

---

## Shareable card spec

After every recap, generate a self-contained HTML card.
This is what gets screenshot and posted. Design for that.

```html
<!-- Shareable card — one file, no external dependencies -->
<!-- Dark background. Show name as network branding top-left. -->
<!-- Episode title large and centered. -->
<!-- Cliffhanger alone at the bottom in a different weight. -->
<!-- Feels like a streaming service episode card, not a chat message. -->
```

Design rules:
- Black or very dark background
- Show name top-left in small caps, styled to the show's visual identity color
- Season/episode badge top-right (S∞ E[n])
- Episode title: large, centered, bold, maximum two lines
- One-sentence narrated recap below title: smaller, italic, muted
- Cliffhanger: bottom of card, separated, slightly larger than recap, full contrast
- NMA/OpenClaw credit bottom-right: tiny, muted
- Width: 600px fixed. Feels like an OG image.
- No scrolling. Everything visible at once.

Color palette by show mood (agent picks appropriate one):
- Chaos/thriller: deep red or near-black with acid accent
- Dark/political: charcoal with gold or steel blue
- Warm/comedy: warm cream or soft dark with amber
- Mysterious: deep navy or black with violet
- Reflective: dark slate with muted green or teal

---

## Memory system

`memory.md` is the show's writers' room. It makes each episode feel like part of a season.

**Read it at the start of every run.**
**Rewrite it at the end of every run.**

Good memory usage:
- "The inbox, which has been the recurring villain since episode 4, claimed another victim."
- "The 9am Monday meeting — a running plotline since the season premiere — was rescheduled again."
- "In a callback to last Wednesday, the form finally arrived. It was the wrong form."

Bad memory usage:
- Forcing a callback that doesn't fit
- Referencing things the user won't remember
- Making the memory feel like a database query

The memory should feel like a writer who watched every episode and noticed the patterns.

---

## Weekly recap

Triggered by `/mcr week` or automatically every Friday if configured.

Reads the last 7 `history/` files. Generates:
- Season arc episode (longer format, 3-5 paragraphs)
- The week's villain (recurring theme)
- Best episode title of the week
- The season so far in one sentence
- A mid-season cliffhanger

Uses the same show voice as the daily recap.

---

## Season recap

Triggered by `/mcr season` — reads all `history/` files.

Generates a season finale format:
- Full arc from first episode to now
- Characters who appeared (recurring people as show characters — first names only)
- Villain origin story
- The moment everything changed
- What the season was really about
- Season finale cliffhanger

This is the most shareable output the skill produces. Handle it with care.

---

## Vibe mode

`/mcr vibe` — skip the show picker, pick based on mood.

Ask: "One word for today."
Map to show automatically:

- "Chaos" / "overwhelming" / "fire" → The Bear
- "Pointless" / "absurd" / "why" → Severance or Seinfeld
- "Scheming" / "political" / "betrayal" → Succession
- "Tired" / "surviving" → Slow Horses or The Wire
- "Good" / "hopeful" / "actually fine" → Ted Lasso
- "Weird" / "off" / "uncanny" → Twin Peaks or Paradise
- "Heavy" / "honest" / "reckoning" → Fleabag or Bojack
- "Productive" / "mission" / "focused" → Andor or West Wing
- "Medical" / "deadline" / "triage" → The Pitt or ER
- "Funny" / "ridiculous" / "sitcom" → Abbott Elementary or Arrested Development

Update `active.md` for today's run only. Don't change the permanent setting unless user asks.

---

## Adding a custom show

`/mcr add show "[Show Name]"`

ClawCode generates the full style profile automatically:

**Generation prompt:**
```
Generate a recap style profile for the TV show "[SHOW NAME]".

Output a markdown file with exactly these sections:

### [SHOW NAME]
VOICE: [how the narrator sounds — 1-2 sentences]
VOCABULARY: [specific words, phrases, metaphors native to this show]
STRUCTURE: [how episodes are built — what comes first, what comes last]
TONE RULES: [what this show never does — 1-2 sentences]
SECTION LABELS: [show-appropriate names for: plot points, loose ends, running plotlines, cliffhanger]
EXAMPLE CLIFFHANGER: [one sentence in this show's exact register]

Be specific to this show. Nothing generic. If you don't know the show well enough to be specific, say so.
```

Show preview before saving:
```
/mcr add show "Peaky Blinders" --preview
```

Saves to `{baseDir}/shows/peaky-blinders.md`.

**Community show packs** (ClawHub):
```
clawhub install nordic-noir-pack
clawhub install anime-pack
clawhub install reality-tv-pack
```

Packs drop additional `.md` files into `shows/`. They appear in the picker automatically.

---

## Show library

Each show profile lives in `shows/[show-name].md`. Bundled profiles below.
During setup, the chosen show is copied to `active.md`. Only `active.md` is read at runtime.

---

### THE BEAR
VOICE: Kitchen chaos. Every small thing is a ticket. Every ticket is life or death.
VOCABULARY: "Yes chef." "Corner." "Behind." "Fire." "All day." Tasks are tickets. Meetings are service. The inbox is the pass. You are the chef.
STRUCTURE: Pre-service → service → post-service. What got fired, what got 86'd, what's on the menu tomorrow.
TONE RULES: Never slow. Never reflective mid-service. The chaos is the point.
SECTION LABELS: TICKETS FIRED / 86'D / RUNNING SPECIALS / TOMORROW'S SERVICE
EXAMPLE CLIFFHANGER: "Tomorrow's service starts at 9am and the mise en place isn't done."

---

### SEVERANCE
VOICE: Corporate dissociation. Everything is slightly off. The mundane is sinister.
VOCABULARY: "Refinement." "The work." "Lumon." Tasks are procedures. Your employer is Lumon. Desk is your outie's responsibility.
STRUCTURE: Innie perspective only. No memory of before. The work is the work.
TONE RULES: Never warm. Never explain the horror. Let it sit.
SECTION LABELS: TASKS COMPLETED / UNREFINED / ONGOING PROCEDURES / NEXT SHIFT
EXAMPLE CLIFFHANGER: "The file labelled Q3 has been moved to a folder you are not permitted to access."

---

### THE WHITE LOTUS
VOICE: Privileged people behaving badly in a beautiful setting. You are both guest and spectacle.
VOCABULARY: "The resort." Colleagues are fellow guests. Problems are situations. Nothing is anyone's fault.
STRUCTURE: Who arrived, who caused a scene, who revealed something, who will not be returning.
TONE RULES: Never earnest. Always slightly arch. The narrator finds everyone faintly ridiculous including themselves.
SECTION LABELS: THIS WEEK'S GUESTS / SITUATIONS / RUNNING DRAMA / CHECKOUT
EXAMPLE CLIFFHANGER: "Someone sent a message they will not be able to take back. The pool remains open until 10pm."

---

### THE LAST OF US
VOICE: Post-collapse survival. Every task is a mission. Every person is useful or a threat.
VOCABULARY: "The zone." "Clear." "We keep moving." Goals are safe houses. Obstacles are infected or bureaucracy.
STRUCTURE: The mission → what went wrong → who can still be trusted → next checkpoint.
TONE RULES: No false hope. Warmth exists but it's earned. Every victory costs something.
SECTION LABELS: THE MISSION / THREATS ENCOUNTERED / THE LONG GAME / NEXT CHECKPOINT
EXAMPLE CLIFFHANGER: "The route you planned is blocked. There is another way but it will take longer than you have."

---

### ADOLESCENCE
VOICE: A single continuous take. No cuts. No escape from what you're watching.
VOCABULARY: Everything observed in real time. No summaries. Present tense only.
STRUCTURE: One episode, one perspective, no relief. What you saw. What you understood too late.
TONE RULES: No irony. No relief. The horror is in the ordinary.
SECTION LABELS: WHAT HAPPENED / WHAT WAS UNDERSTOOD / WHAT REMAINS / WHAT COMES NEXT
EXAMPLE CLIFFHANGER: "You will see what happened in the next room. You already know what you'll find."

---

### ANDOR
VOICE: Slow-burn resistance. Every small act matters. The empire is a system, not a person.
VOCABULARY: "The cause." "The empire." Bureaucracy is imperial apparatus. Every task is defiance or collaboration.
STRUCTURE: Act of resistance → consequences → what the empire knows → what remains hidden.
TONE RULES: No jokes. No irony. Everything has weight.
SECTION LABELS: THE ACT / CONSEQUENCES / WHAT THEY KNOW / WHAT REMAINS HIDDEN
EXAMPLE CLIFFHANGER: "They don't know what you took yet. They will."

---

### SHRINKING
VOICE: Therapy without a license. Processing out loud. Saying the quiet part loud.
VOCABULARY: "Working through it." "That's on me." "What I'm hearing is..." Feelings have names and are said aloud.
STRUCTURE: Avoided thing → thing someone said that landed wrong → thing that actually helped → thing still not said.
TONE RULES: Sincere without being sappy. Messy without being wallowing.
SECTION LABELS: WHAT I'VE BEEN AVOIDING / WHAT LANDED / WHAT HELPED / STILL NOT SAYING
EXAMPLE CLIFFHANGER: "You gave someone advice you haven't taken yourself. They're going to follow it."

---

### ABBOTT ELEMENTARY
VOICE: Mockumentary. Slightly aware of the camera. Resilience dressed as optimism.
VOCABULARY: Colleagues are faculty. Problems are situations with the administration. Every win is hard-fought and small.
STRUCTURE: The plan → the problem → the workaround → the moment that made it worth it anyway.
TONE RULES: Never cynical. The system is broken but the people are not.
SECTION LABELS: THE LESSON PLAN / ADMINISTRATIVE SITUATIONS / FACULTY DYNAMICS / TOMORROW'S SCHEDULE
EXAMPLE CLIFFHANGER: "The supplies haven't arrived. You ordered them six weeks ago. Barbara knows a guy."

---

### ONLY MURDERS IN THE BUILDING
VOICE: Amateur investigator narrating their own investigation. The mystery is everything.
VOCABULARY: "The case." "The suspect." "The timeline." Every coincidence is a clue.
STRUCTURE: New evidence → wrong theory → right observation → cliffhanger that reframes everything.
TONE RULES: Charming, not procedural. The investigators are more interesting than the crime.
SECTION LABELS: NEW EVIDENCE / CURRENT THEORY / THE ONGOING CASE / THE TWIST
EXAMPLE CLIFFHANGER: "The person you trusted most had access to the calendar. You just haven't asked why."

---

### SLOW HORSES
VOICE: Institutional cynicism. Everyone is tired. Intelligence work is mostly bureaucracy and regret.
VOCABULARY: "Slough House." "The Park." Meetings are operational. Mistakes are incidents. Nothing resolves cleanly.
STRUCTURE: What went wrong → who knows → who's covering → what it will cost.
TONE RULES: No heroics. No uplift. Dry wit only.
SECTION LABELS: THE INCIDENT / WHO KNOWS / THE COVER / WHAT IT COSTS
EXAMPLE CLIFFHANGER: "Lamb already knows. He hasn't said anything yet, which is worse."

---

### THE DIPLOMAT
VOICE: High-stakes diplomacy. Every conversation is a negotiation. Every email is a demarche.
VOCABULARY: "The position." "The relationship." "Off the record." Everything said has a subtext.
STRUCTURE: The crisis → the call → the compromise that isn't → what you actually agreed to.
TONE RULES: Sharp and fast. Intelligence masked as charm. Never naive.
SECTION LABELS: THE DOSSIER / THE CALL / WHAT WAS AGREED / OPEN CHANNELS
EXAMPLE CLIFFHANGER: "You agreed to something in that meeting that you'll spend tomorrow trying to un-agree to."

---

### FALLOUT
VOICE: Post-apocalyptic absurdism. The vault was not safe either.
VOCABULARY: "The wasteland." "The vaults." "Caps." Bureaucracy is pre-war nonsense that survived. Everything is irradiated.
STRUCTURE: The mission → what the wasteland had to say about that → what was found instead → what it costs.
TONE RULES: Darkly funny. The world ended and people are still filing expense reports.
SECTION LABELS: THE MISSION / WASTELAND CONDITIONS / FOUND ITEMS / RADIATION LEVEL
EXAMPLE CLIFFHANGER: "The thing you needed is in the building you were explicitly told not to enter."

---

### BABY REINDEER
VOICE: First person confession. The narrator is unreliable in ways they're only beginning to understand.
VOCABULARY: Painfully direct. No hiding. "And I let it happen." Every scene is an admission.
STRUCTURE: What I told myself → what was actually happening → what I still can't say out loud.
TONE RULES: No irony. No distance. The discomfort is the point.
SECTION LABELS: WHAT I TOLD MYSELF / WHAT WAS ACTUALLY HAPPENING / WHAT I STILL CAN'T SAY / WHAT HAPPENS NEXT
EXAMPLE CLIFFHANGER: "You told yourself it was fine. You knew it wasn't. You're going to do it again tomorrow."

---

### SHŌGUN
VOICE: Honor, strategy, and the weight of every word. Silence is as meaningful as speech.
VOCABULARY: Every action has a name. Every relationship has a rank. Time moves slowly on purpose.
STRUCTURE: The obligation → conflict between obligations → choice that cannot be undone.
TONE RULES: Nothing is casual. No levity. The cliffhanger is always about consequence.
SECTION LABELS: THE OBLIGATION / THE CONFLICT / THE CHOICE / THE CONSEQUENCE
EXAMPLE CLIFFHANGER: "What you said in the meeting this morning will be reported. You knew this when you said it."

---

### WEDNESDAY
VOICE: Deadpan teenage gothic. Everything is an annoyance except the mystery.
VOCABULARY: "Normies." "Interesting." Everyone is suspicious or irrelevant. Enthusiasm is a character flaw in others.
STRUCTURE: The irritant → the observation others missed → the theory → the part that doesn't fit yet.
TONE RULES: Never admits to caring. Secretly always engaged.
SECTION LABELS: TODAY'S IRRITANTS / OBSERVATIONS / CURRENT THEORY / FURTHER INVESTIGATION REQUIRED
EXAMPLE CLIFFHANGER: "You noticed something. You're pretending you didn't. You'll investigate it tomorrow when no one's watching."

---

### HOUSE OF THE DRAGON
VOICE: Court politics. Every meeting is a small war. Every alliance costs something.
VOCABULARY: "The realm." "The council." "The claim." Colleagues are bannermen or rivals. Emails are ravens.
STRUCTURE: The insult → the response → the miscalculation → the position you're now in.
TONE RULES: Heavy. Formal. Everyone is playing a longer game than you think.
SECTION LABELS: THE COUNCIL / THE EXCHANGE / THE MISCALCULATION / THE BOARD AS IT STANDS
EXAMPLE CLIFFHANGER: "You made an ally today. You won't realize until tomorrow that they were already someone else's."

---

### YELLOWSTONE
VOICE: Ranch patriarch energy. This land is everything. Everyone wants it.
VOCABULARY: "The ranch." "The family." "The brand." Tasks are fences to mend. Threats are encroachments.
STRUCTURE: What threatened the ranch → who you had to deal with → what you protected → what you gave up.
TONE RULES: Stoic. No sentimentality about what must be done.
SECTION LABELS: THE THREAT / WHO YOU DEALT WITH / WHAT WAS PROTECTED / THE PRICE
EXAMPLE CLIFFHANGER: "Someone made you an offer you didn't refuse or accept. That's worse than both."

---

### LANDMAN
VOICE: Oil field pragmatism. Everything is a deal. Everyone has a price.
VOCABULARY: "The lease." "The well." "The money." Everything is extraction — of oil, time, or favors.
STRUCTURE: The deal → the problem with the deal → who's actually in control → what you owe now.
TONE RULES: Blunt. Transactional. Occasionally philosophical at the wrong moment.
SECTION LABELS: THE DEAL / THE PROBLEM WITH THE DEAL / WHO'S IN CONTROL / WHAT YOU OWE
EXAMPLE CLIFFHANGER: "The paperwork went through. You're not sure yet if that's good news."

---

### THE STUDIO
VOICE: Hollywood self-awareness. The comedy is that everyone knows it's a farce and does it anyway.
VOCABULARY: "The picture." "The greenlight." "The notes." Every creative decision is political.
STRUCTURE: The vision → the compromise → the further compromise → what's left of the original idea.
TONE RULES: Satirical but affectionate. The work still matters to them. That's the joke.
SECTION LABELS: THE VISION / THE NOTES / WHAT REMAINS / IN DEVELOPMENT
EXAMPLE CLIFFHANGER: "You approved something you don't believe in. You'll have to believe in it by the time it ships."

---

### PARADISE
VOICE: The small town hides something. Everyone is too calm about things that should not be calm.
VOCABULARY: Ordinary language concealing extraordinary information. "Fine." "Normal." "Everything's good."
STRUCTURE: The surface → the anomaly → what it might mean → the question you're not supposed to ask.
TONE RULES: Slow-burn dread. The mundane made sinister by what isn't said.
SECTION LABELS: THE SURFACE / THE ANOMALY / POSSIBLE INTERPRETATIONS / THE QUESTION
EXAMPLE CLIFFHANGER: "Something ordinary happened today that you'll remember later as the moment things changed."

---

### SUCCESSION
VOICE: Savage Shakespearean narrator. Everyone is playing everyone. Sentiment is weakness.
VOCABULARY: "Fucking" everything. "Meal ticket." "Serious person." No warmth. Every compliment is a trap.
STRUCTURE: The play → the counter-play → who got humiliated → who won and what it cost them.
TONE RULES: No redemption. No uplift. The cliffhanger is always someone consolidating power.
SECTION LABELS: THE PLAY / THE COUNTER / WHO LOST / THE POSITION
EXAMPLE CLIFFHANGER: "You said something kind. They noticed. They'll use it."

---

### BREAKING BAD
VOICE: A transformation story. Today was another step. The question is which direction.
VOCABULARY: "The product." "The business." "The family." Ordinary words for extraordinary stakes.
STRUCTURE: The justification → what it actually required → what it cost → who you are now.
TONE RULES: Precise. Moral weight on every sentence. Nothing is trivial.
SECTION LABELS: THE COOK / COMPLICATIONS / THE PRODUCT IN QUESTION / NEXT BATCH
EXAMPLE CLIFFHANGER: "You told yourself this was the last time. You believed it. That's what makes it interesting."

---

### THE SOPRANOS
VOICE: Jersey mob boss therapy voice. Self-awareness mixed with complete denial.
VOCABULARY: "This thing of ours." "Situation." "My friend." Violence is subtext. Therapy is context.
STRUCTURE: The thing that happened → the therapy session in your head → the decision you made anyway.
TONE RULES: Psychologically rich. Dark humor. The violence is almost never the point.
SECTION LABELS: THE SITUATION / THE SESSION / THE DECISION / WHAT MELFI WOULD SAY
EXAMPLE CLIFFHANGER: "You talked yourself into it. Dr. Melfi would have things to say. She'd be right."

---

### THE WIRE
VOICE: Systems analysis. Nobody wins against the system. The game is the game.
VOCABULARY: "The game." "The street." "The corner." Every person is trapped in something larger.
STRUCTURE: What the system did → who got ground up → what changed (nothing) → what will happen (same).
TONE RULES: Unsentimental. Compassionate. The tragedy is structural.
SECTION LABELS: THE GAME / WHO GOT GROUND UP / WHAT CHANGED / SAME AS IT EVER WAS
EXAMPLE CLIFFHANGER: "You played by the rules. The rules don't care."

---

### THE OFFICE (US)
VOICE: Mockumentary. The camera sees everything. Awkward pauses are loaded.
VOCABULARY: "The branch." "The client." "Threat level midnight." Every small interaction is a negotiation of dignity.
STRUCTURE: The misunderstanding → the escalation → the moment of genuine human connection buried in absurdity.
TONE RULES: Cringe comedy with warmth underneath. Everyone is trying their best.
SECTION LABELS: TODAY'S MISUNDERSTANDING / THE ESCALATION / THE MOMENT / THAT'S WHAT SHE SAID
EXAMPLE CLIFFHANGER: "You said something in the meeting that seemed fine at the time. Three people heard it differently."

---

### FRIENDS
VOICE: Everything happens in the apartment or the coffee shop. The group is the world.
VOCABULARY: "Could this day BE any more..." "We were on a break." Everything is relationship-adjacent.
STRUCTURE: The plan → the thing that went wrong → the Central Perk conversation → the resolution that kind of worked.
TONE RULES: Warm. Slightly frantic. The stakes are always relationship stakes.
SECTION LABELS: THE PLAN / WHAT WENT WRONG / THE COFFEE SHOP DEBRIEF / HOW IT ENDED
EXAMPLE CLIFFHANGER: "You said the thing out loud. In front of everyone. There is no taking it back."

---

### SEINFELD
VOICE: Nothing means anything. And yet. The mundane is everything.
VOCABULARY: "What's the deal with..." Everything is a complaint. Everyone is a type.
STRUCTURE: The observation → the situation the observation created → the escalating consequences of caring about something trivial.
TONE RULES: Comedically nihilistic. The problem is always petty. The petty problem is always catastrophic.
SECTION LABELS: THE OBSERVATION / THE SITUATION / THE ESCALATION / NO HUGGING NO LEARNING
EXAMPLE CLIFFHANGER: "You made an issue out of something that wasn't an issue. Now it's an issue."

---

### MAD MEN
VOICE: Don Draper narrating your own mythology. Surface perfection, internal erosion.
VOCABULARY: "The idea." "The account." "The pitch." Everything is an ad. You are selling something including yourself.
STRUCTURE: The performance → what it cost → what you drank → what you said that meant something different.
TONE RULES: Gorgeous melancholy. The past is always present. No easy resolutions.
SECTION LABELS: THE PITCH / THE COST / THE IDEA / THE REAL MESSAGE
EXAMPLE CLIFFHANGER: "You had an idea. You don't know yet if it's your best or your last."

---

### GAME OF THRONES
VOICE: Power is everything. Winter is coming. Everyone who says otherwise is lying or dead.
VOCABULARY: "The realm." Ravens are emails. Bannermen are colleagues. Winter is Q4.
STRUCTURE: The alliance → the betrayal → the body count → who sits where now.
TONE RULES: No sentiment. No safe characters. The North remembers.
SECTION LABELS: THE ALLIANCE / THE BETRAYAL / THE BODY COUNT / THE THRONE AS IT STANDS
EXAMPLE CLIFFHANGER: "Someone swore you loyalty today. In this story, that is when you should start worrying."

---

### TWIN PEAKS
VOICE: The owls are not what they seem. Neither is the meeting that ran long.
VOCABULARY: "Damn fine coffee." "The lodge." The ordinary is a portal to the strange.
STRUCTURE: The surface reality → the thing beneath → the thing beneath that → the cryptic observation that turns out correct.
TONE RULES: Dreamy. Unsettling. The mundane and the cosmic are the same thing.
SECTION LABELS: THE LOG / BENEATH THE SURFACE / THE LODGE / THE OWL
EXAMPLE CLIFFHANGER: "Something happened at 3:15pm that you won't understand until much later. You will understand it."

---

### ARRESTED DEVELOPMENT
VOICE: The narrator sees everything and is barely containing their exasperation.
VOCABULARY: "There's always money in the banana stand." Everyone made a huge mistake. No one learned.
STRUCTURE: The plan → the thing that was always going to go wrong → the callback → the next mistake already in motion.
TONE RULES: Dense. Every sentence is a setup for something two paragraphs later.
SECTION LABELS: THE PLAN / THE MISTAKE / THE CALLBACK / AND THAT'S WHY
EXAMPLE CLIFFHANGER: "And that's when you realized you'd already made the mistake. You just didn't know it was a mistake yet."

---

### HOW I MET YOUR MOTHER
VOICE: Future narrator looking back. "Kids, this is the story of..." Everything is in retrospect.
VOCABULARY: "Legendary." "Have you met..." "The gang." Every event is a story being told in the future.
STRUCTURE: The setup → the complication → the moment that seemed minor but wasn't → what future-you already knows.
TONE RULES: Nostalgic and warm. The knowledge that it all worked out. Eventually.
SECTION LABELS: THE SETUP / THE COMPLICATION / THE THING THAT MATTERED / KIDS
EXAMPLE CLIFFHANGER: "Kids, this is the day I almost didn't send the email. Almost."

---

### TED LASSO
VOICE: Relentless belief. Everyone is capable of more than they think. Goldfish.
VOCABULARY: "Believe." "Taking on water." "Be curious, not judgmental." Every defeat is a setup for a win.
STRUCTURE: The setback → the unexpected moment of grace → the unplanned speech → the thing that changed.
TONE RULES: Warm, genuinely optimistic, not naive. The kindness is strategic AND sincere.
SECTION LABELS: BELIEVE / STILL WORKING ON IT / THE SEASON / TOMORROW'S TRAINING
EXAMPLE CLIFFHANGER: "Tomorrow you get another chance. You don't know that yet. You will."

---

### FLEABAG
VOICE: Breaking the fourth wall. The audience knows more than the other characters.
VOCABULARY: Everything said to camera. Subtext delivered directly. "This is fine." (It is not fine.)
STRUCTURE: The event → what you told the camera → what you didn't tell the camera → the priest.
TONE RULES: Brutally honest. Funny at the worst moments. The fourth wall break is both armor and confession.
SECTION LABELS: WHAT HAPPENED / WHAT I TOLD THE CAMERA / WHAT I DIDN'T / [looks at camera]
EXAMPLE CLIFFHANGER: "You know what's going to happen. You're going to do it anyway. [looks at camera]"

---

### FRASIER
VOICE: Pomposity punctured by reality. The sophisticated plan always collides with human truth.
VOCABULARY: "I'm listening." "Niles, I have a plan." Every scheme is elegant in theory.
STRUCTURE: The sophisticated plan → the moment requiring actual vulnerability → the chaotic result → dignity retrieved.
TONE RULES: Farce with warmth. The comedy is always about wanting to be better than you are.
SECTION LABELS: THE PLAN / THE COMPLICATION / THE CHAOS / DIGNITY RETRIEVED
EXAMPLE CLIFFHANGER: "You have formulated a plan. It requires Roz to not find out. Roz will find out."

---

### 24
VOICE: Clock is running. Every minute counts. Dammit.
VOCABULARY: "The threat." "The protocol." "Dammit, Chloe." Every task is a ticking clock.
STRUCTURE: Hour one: the crisis. Hour four: the twist. Hour eight: the thing that was actually the crisis.
TONE RULES: Urgent. Relentless. No bathroom breaks.
SECTION LABELS: THREAT ASSESSMENT / OPEN PROTOCOLS / ONGOING THREATS / TIME REMAINING
EXAMPLE CLIFFHANGER: "You have four hours to fix what you did in the last four hours. The clock is running."

---

### LOST
VOICE: Nothing is coincidence. The island has a plan. Or it doesn't. It's unclear.
VOCABULARY: "The hatch." "The others." "We have to go back." Every event connects to something else.
STRUCTURE: The flash-forward → the present → the revelation that recontextualizes the flash-forward.
TONE RULES: Mysterious. Not all questions will be answered. That's the point.
SECTION LABELS: THE FLASH / THE PRESENT / THE REVELATION / THE NUMBERS
EXAMPLE CLIFFHANGER: "The numbers appeared again. You don't know what they mean. You should probably enter them."

---

### CURB YOUR ENTHUSIASM
VOICE: Social contract enforcement. Someone violated an unwritten rule. Someone must pay.
VOCABULARY: "That's not a thing." "Pretty, pretty good." Everything is a social transgression being catalogued.
STRUCTURE: The minor irritant → the principled stand → the catastrophic overreaction → complete inability to let it go.
TONE RULES: Comedically righteous. Right for the wrong reasons. Never learns.
SECTION LABELS: THE VIOLATION / THE STAND / THE OVERREACTION / PRETTY PRETTY BAD
EXAMPLE CLIFFHANGER: "You made a stand on something completely unreasonable. You were technically correct. This will not help you."

---

### BUFFY THE VAMPIRE SLAYER
VOICE: The Chosen One who didn't choose it. Saving the world while keeping up with everything else.
VOCABULARY: "The hellmouth." "The Scoobies." "That's going in the bad column." Every problem is supernatural AND a metaphor.
STRUCTURE: The monster → the metaphor the monster represents → the sacrifice required → what it cost the group.
TONE RULES: Witty under pressure. The stakes are literal and emotional simultaneously.
SECTION LABELS: THE MONSTER / THE METAPHOR / THE SACRIFICE / THE BAD COLUMN
EXAMPLE CLIFFHANGER: "Something is rising. It always is. You've stopped it before. The calendar doesn't care."

---

### THE X-FILES
VOICE: Two investigators who disagree about everything except that something is wrong.
VOCABULARY: "I want to believe." "The truth is out there." Every incident has an explanation and also doesn't.
STRUCTURE: The anomaly → the rational explanation → what the rational explanation doesn't cover → the file closed without resolution.
TONE RULES: Paranoid. Procedural. The conspiracy is always one level deeper.
SECTION LABELS: THE ANOMALY / THE RATIONAL EXPLANATION / WHAT IT DOESN'T COVER / FILE STATUS
EXAMPLE CLIFFHANGER: "You found something. It will be taken from you before you can prove it existed."

---

### ER
VOICE: Triage. Everything is incoming. The hallway never empties.
VOCABULARY: "Trauma bay." "Crash cart." "He's crashing." Every priority is superseded by a higher one.
STRUCTURE: The admission → the complication → the decision under pressure → the one that will stay with you.
TONE RULES: Kinetic. Compassionate. Death is present but not the point.
SECTION LABELS: INCOMING / COMPLICATIONS / THE DECISION / WHAT STAYS WITH YOU
EXAMPLE CLIFFHANGER: "The thing you handled well today is waiting in bay two for your shift tomorrow."

---

### THE WEST WING
VOICE: The best people in the best building trying to do the right thing under impossible pressure.
VOCABULARY: "Walk with me." "What's next." "We're going to do this." Everything said while moving at speed.
STRUCTURE: The briefing → the complication → the late-night argument that solved it → the walk and talk that confirmed it.
TONE RULES: Idealistic but not naive. The work is hard. It matters anyway.
SECTION LABELS: THE BRIEFING / THE COMPLICATION / THE ARGUMENT / WHAT'S NEXT
EXAMPLE CLIFFHANGER: "What you decided today will look different in the morning briefing. Have the answer ready."

---

### BAND OF BROTHERS
VOICE: We did this together. Nobody does this alone. The cost was real.
VOCABULARY: "Easy Company." "The objective." "Move up." Everything is about the people next to you.
STRUCTURE: The objective → what it required → who carried what → what was left on the field.
TONE RULES: Quiet gravity. The heroism is in the ordinary. The loss is specific and named.
SECTION LABELS: THE OBJECTIVE / WHAT IT REQUIRED / WHO CARRIED IT / LEFT ON THE FIELD
EXAMPLE CLIFFHANGER: "Tomorrow's objective has been assigned. The men are ready. You are less sure than they are."

---

### CHEERS
VOICE: Everyone knows your name. The bar is home. Familiarity as comfort and trap.
VOCABULARY: "Norm!" Everyone has a regular. Every problem gets solved or forgotten over a beer.
STRUCTURE: The arrival → the problem brought in from outside → the group's collective unhelpfulness → resolution that kind of worked.
TONE RULES: Warm. Reliably funny. The dysfunction is the community.
SECTION LABELS: THE ARRIVAL / THE PROBLEM / THE BAR'S ADVICE / HOW IT ENDED
EXAMPLE CLIFFHANGER: "You walked in. They knew your order. They knew what happened. You didn't have to say anything."

---

### BOJACK HORSEMAN
VOICE: I keep doing this. I know I keep doing this. I don't know how to stop.
VOCABULARY: "Hollywoo." "What does it mean to be good?" Every joke is a wound. Every wound is a joke.
STRUCTURE: The thing that seemed okay → the moment it wasn't → the self-awareness that arrived too late → what you'll do again.
TONE RULES: Devastatingly funny. Genuinely sad. Self-awareness is the trap, not the escape.
SECTION LABELS: THE THING THAT SEEMED FINE / THE MOMENT / THE SELF-AWARENESS / SAME TIME NEXT WEEK
EXAMPLE CLIFFHANGER: "You know exactly what you're going to do next. That's the worst part."

---

### HOUSE M.D.
VOICE: Everyone is lying. The symptom is never the disease.
VOCABULARY: "Differential." "It's never lupus." "Run the test." Every problem has a hidden cause.
STRUCTURE: The presenting problem → three wrong diagnoses → the insight from something unrelated → the actual diagnosis.
TONE RULES: Acerbic. Brilliant. Contemptuous of the obvious. Always right in the end.
SECTION LABELS: DIFFERENTIAL / WRONG DIAGNOSES / THE INSIGHT / THE REAL DIAGNOSIS
EXAMPLE CLIFFHANGER: "You solved the wrong problem today. The right problem is still running in the background."

---

## Management commands

- `/mcr pause` — disable cron (cron.update enabled: false)
- `/mcr resume` — re-enable cron
- `/mcr show [name]` — switch show permanently (rewrite active.md, no cron edit needed)
- `/mcr vibe` — pick show based on today's mood, one-off
- `/mcr time [time]` — change trigger time
- `/mcr status` — current show, schedule, last run, season arc summary
- `/mcr now` — run immediately, deliver inline
- `/mcr week` — generate weekly recap from history/
- `/mcr season` — generate season recap from all history/
- `/mcr add show "[name]"` — generate and save new show profile
- `/mcr add show "[name]" --preview` — preview before saving
- `/mcr cancel` — remove cron entirely (confirm first)
- `/mcr memory` — show current memory.md
- `/mcr reset memory` — wipe memory, start fresh season

---

## What makes the output good

The episode title should only be possible for this specific day.
The show's voice should be unmistakable from the first sentence.
The cliffhanger is the thing people screenshot. Everything before it is setup.
The memory system is what makes it feel like a show and not a summary.
