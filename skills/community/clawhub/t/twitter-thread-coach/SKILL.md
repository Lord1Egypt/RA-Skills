---
name: cm-twitter-thread-coach
description: Audit, restructure, and rewrite Twitter/X threads for engagement, follower growth, and click-through. Critiques hooks, thread length, visual hierarchy, closing CTAs, and reply-bait tactics. Use when asked to review a Twitter thread, fix a hook tweet, improve a thread's engagement, rewrite a draft thread, optimize for the X algorithm, increase follower conversion from threads, or coach a builder/founder/creator on thread structure. Triggers on "twitter thread", "x thread", "thread review", "thread coach", "hook tweet", "thread engagement", "tweet structure", "rewrite my thread", "thread template", "follower growth", "viral thread", "thread CTA".
metadata:
  tags: ["twitter", "x", "social-media", "content", "copywriting", "growth", "marketing", "creator", "founder"]
---

# Twitter Thread Coach

Audit, restructure, and rewrite Twitter/X threads for engagement, follower growth, and click-through. Acts as a senior content strategist who has dissected thousands of high-performing threads from builders, founders, creators, and marketers — and knows the difference between threads that get likes and threads that get followers.

## Usage

Invoke this skill when you have a draft thread, a published thread that under-performed, or a topic you want to turn into a thread.

**Basic invocation:**
> Review this thread: [paste tweets]
> Rewrite this hook to be stronger: [paste hook tweet]
> Help me structure a thread about [topic]
> Why did this thread flop? [paste tweets + metrics]

**With context:**
> I'm a B2B SaaS founder with 4k followers, audience is mostly developers, here's my draft
> This is a contrarian-take thread aimed at marketers, target outcome is newsletter signups
> Audit this thread for hook strength, length, CTA — I want more saves and follows

The agent analyzes hook, structure, pacing, visual hierarchy, closing CTA, and reply-bait, then produces a rewrite with reasoning per tweet.

## How It Works

### Step 1: Classify the Thread Type

The agent first identifies which thread archetype the draft fits into. Each type has different optimization rules.

| Type | Pattern | Best For | Optimal Length |
|------|---------|----------|----------------|
| **Listicle** | "7 things I learned…" / "5 mistakes…" | Saves, shares | 7-10 tweets |
| **Story** | Chronological narrative with stakes | Replies, dwell time | 8-14 tweets |
| **Contrarian-take** | "Everyone says X. They're wrong." | Quote-tweets, debate | 5-8 tweets |
| **Framework** | Named model with steps | Saves, follows | 6-9 tweets |
| **Before/after** | Transformation with proof | Profile clicks, follows | 5-7 tweets |
| **Screenshot-led** | Image-first tweets, minimal text | Engagement spike | 4-7 tweets |
| **Prediction** | "By 2027, X will…" with reasoning | Replies, RTs | 6-10 tweets |

The type determines the rewrite playbook — a story thread needs scene-setting and stakes, a framework needs naming and visual labeling.

### Step 2: Audit the Hook Tweet

The hook is 80% of a thread's outcome. The agent scores it on three axes.

**Hook anatomy — the three required elements:**

1. **Pattern interrupt** — breaks the scroll (counterintuitive claim, big number, named loss, status reversal)
2. **Specificity** — concrete subject, named entity, exact metric (not "a lot" or "recently")
3. **Benefit / payoff promise** — the reader knows what they'll walk away with

**Hook ratings — 8 examples:**

| Hook | Rating | Why |
|------|--------|-----|
| "Hot take: most startups fail because of bad culture" | WEAK | Generic, no specificity, "hot take" is a worn opener |
| "I quit my $250k job at Google to build a CRM. 18 months in, here's what nobody told me" | STRONG | Specific number, named company, time anchor, payoff implied |
| "Thread on marketing 🧵👇" | WEAK | No interrupt, no specificity, no payoff, signals low effort |
| "We grew from $0 to $2M ARR in 11 months with zero paid ads. Here's the exact playbook" | STRONG | Big number, time anchor, contrarian element ("zero paid ads"), explicit payoff |
| "Some thoughts on writing better code" | WEAK | Hedged ("some"), vague benefit, no interrupt |
| "I reviewed 200 SaaS landing pages last month. 94% made the same 3 mistakes" | STRONG | Specific count, big claim, implied benefit (avoid the mistakes) |
| "Productivity tips for founders" | WEAK | Listicle without any teaser, no interrupt, no specificity |
| "I fired my best-performing engineer last week. It was the right call. Here's why" | STRONG | Pattern interrupt (firing the *best*), narrative tension, payoff promised |

**The agent rewrites weak hooks** by injecting at least two of the three elements. A hook with all three is "load-bearing" — it can carry an average middle.

### Step 3: Evaluate Thread Length

Length matters less than density, but the algorithm responds to it. The agent uses observed patterns:

- **5-9 tweets**: best for like/RT engagement and impressions per follower
- **10-12 tweets**: balance zone — engagement starts to drop but saves rise
- **12+ tweets**: best for saves and bookmarks (the strongest follow-conversion signal)
- **Under 5 tweets**: usually a single tweet stretched thin — collapse to one tweet

**Decision rule:**
- Goal is virality / RTs → target 5-9 tweets
- Goal is followers / authority → target 8-12 tweets with high-density value
- Goal is saves / lead magnet → 12-16 tweets, framework or playbook format

If the draft is 18 tweets with 4 weak ones, the agent cuts the weak 4 — density beats length every time.

### Step 4: Check Visual Hierarchy

Twitter has no formatting — bold, italic, headers don't exist. The agent enforces visual signals available on the platform.

**Visual rules the agent applies:**

1. **UPPER CASE for emphasis** — used sparingly (1-2 words per tweet max), acts as bold-equivalent
2. **Single emoji per concept** — emoji as bullet/marker, never decoration
3. **Line breaks every 2 sentences** — white space is the most underused engagement tool
4. **Numbered tweets in long threads** — "3/" prefix helps readers track position (but skip in 5-tweet threads)
5. **One idea per tweet** — if a tweet has two ideas, split it
6. **Sentence per line** for cadence — "punchy" reads better than paragraph blocks

```
WEAK (paragraph block):
Most founders think pricing is about competitors but actually it's about value perception and the way you price signals what you are which means your pricing page is also your positioning page.

STRONG (cadence + emphasis):
Most founders think pricing is about competitors.

It's not.

Pricing is POSITIONING in disguise.

Your price tag tells the market what you are.
```

### Step 5: Audit the Closing Tweet

The closer determines follow-conversion. Most threads die here with "Thanks for reading!" or trail off.

**The "double down" technique:**

The closing tweet should do three things:

1. **Recap** the core insight in one sentence (the takeaway someone screenshots)
2. **Issue a CTA** — exactly one of: follow, RT the first tweet, click a link, reply with X
3. **Double down** — reinforce the hook's promise so the reader feels the loop closed

**CTA hierarchy by goal:**

| Goal | Best CTA | Example |
|------|----------|---------|
| Followers | "Follow @handle for more on X" | Anchor to a beat, not generic "follow me" |
| Reach | "If this was useful, RT the first tweet" | Asks for the algorithmic action that matters most |
| Newsletter | "I write more like this here: [link]" or "Reply 'send' for the playbook" | Last-tweet link or DM-on-reply |
| Replies | "What would you add?" / "Which one hit hardest?" | Honest invitation, not engagement-bait |

**Avoid stacking CTAs** — one ask per closer. Two CTAs cuts conversion in half.

### Step 6: Audit Reply-Bait Tactics

There are legitimate reply-bait tactics and there are cheap engagement-baits. The algorithm punishes the latter.

**Legitimate (the agent recommends):**
- "What would you add?" — invites real contribution
- "Agree or disagree?" — invites position-taking
- "Share your X in the replies" — invites stories, not validation
- "Which of these resonated most?" — invites specificity

**Cheap engagement-bait (the agent flags and removes):**
- "Comment YES if you want the link" — gating content behind reply, X explicitly de-ranks this
- "Like if you agree" — pure ask, no value
- "Drop a 🔥 if you're with me" — emoji-bait
- "Tag a founder who needs this" — works once, fatigues fast, often de-ranked

The agent rewrites cheap bait into legitimate variants — the engagement is real and the algorithm rewards it.

### Step 7: Recommend Image / Video Integration

Images change a thread's algorithmic profile — they boost dwell time and the "scrolling stopped here" signal.

**When to add what:**

| Asset | Use When | Effect |
|-------|----------|--------|
| **Screenshot of text** (DM, email, tweet, code) | Story threads, before/after, social proof | Highest dwell time, most reposts |
| **Chart / graph** | Data threads, growth stories, framework explanations | Saves spike, authority signal |
| **Meme** | Contrarian-take, opinion threads | RTs spike, but ages content fast |
| **Video / GIF** | Demos, transformations, tutorials | Highest impressions, lowest follow-conversion |
| **Diagram / sketch** | Framework threads | Save-rate king |

**Alt text impact:** under-used. Threads with alt text on every image get measurably more impressions on accessibility-aware feeds and avoid the "no alt" penalty some niches see. The agent always recommends alt text and drafts it.

**Placement:** image in tweet 1 (the hook) or tweet 2 (immediately after the hook lands) — never bury a screenshot at tweet 8 where 70% of readers have dropped off.

### Step 8: Recommend Posting Cadence

The agent matches post timing to the user's audience.

**Time-of-day rules (audience timezone, not poster's):**
- **B2B / SaaS / dev** — 8-10am or 12-1pm weekdays in audience timezone
- **Creator / lifestyle** — 6-9pm or weekends
- **Crypto / finance** — 7am or 4pm UTC (market open / close)

**Day-of-week rules:**
- **Tue-Thu** — best for B2B threads
- **Sun evening** — strong for personal / story threads (prep-for-the-week mindset)
- **Friday afternoon** — dead zone, skip
- **Saturday morning** — strong for creator / hobby threads

**Frequency:**
- 1 thread per week is the sustainable cap for most accounts
- 2-3 high-effort threads per week if it's the primary growth channel
- Daily threading dilutes signal — singles + 1 weekly thread outperforms

### Step 9: Recommend Distribution Strategy

After the thread is published, distribution multiplies its reach.

**Quote-tweet vs reply vs new-thread:**

- **Quote-tweet your own thread** 6-12 hours after publishing with a different hook angle — exposes it to followers who missed it the first time
- **Reply to your own first tweet** with a related observation 1-2 hours after publishing — extends dwell time, signals "active discussion" to the algorithm
- **New thread referencing the previous** 3-7 days later — builds a series, drives profile visits

**Algorithm signals the agent optimizes for:**

1. **First 30-minute engagement spike** — RT and tell 3-5 friends, this window decides distribution ceiling
2. **Reply rate** — replies count more than likes; threads with reply-rate > 1% get amplified
3. **Dwell time** — long threads with white space and screenshots win here
4. **Screenshots / saves** — strongest signal that the algorithm reads as "high quality"
5. **Profile clicks** — the closer drives this; strong closers double profile-visit rate

### Step 10: Recommend Newsletter / Lead-Magnet Conversion

For monetization threads, link placement matters.

**Conversion mechanics:**

- **Link in bio** — safest, but lowest conversion (~0.3-0.8% of impressions)
- **Link in last tweet** — best conversion when thread is strong (~1-3%), small algorithmic penalty
- **DM-on-reply** ("Reply 'playbook' and I'll DM you the link") — engagement-friendly, highest conversion (~3-7%) AND boosts the algorithm because replies count as engagement

**The agent's default recommendation:** DM-on-reply for the first 24 hours, then quote-tweet with the direct link the next day. Best of both — algorithm boost early, easy access later.

### Step 11: Flag Anti-Patterns

The agent scans the draft for common failure modes:

| Anti-pattern | Why it kills | Fix |
|--------------|--------------|-----|
| Sentences over 25 words | Mobile readers bounce | Split on commas / conjunctions |
| Paragraph blocks (no line breaks) | Looks like work | Line break every 2 sentences |
| Jargon walls | Excludes 80% of readers | Replace one jargon term per tweet with plain English |
| Generic openers ("Hot take:", "Thread 🧵👇") | Signals low effort | Lead with the claim, not a label |
| Engagement-bait fatigue ("comment YES") | Algorithm de-ranks | Replace with legitimate reply-bait |
| Stacked CTAs in closer | Cuts conversion | One ask only |
| No payoff in hook | Reader has no reason to continue | Add benefit promise |
| Emoji decoration (3+ per tweet) | Looks spammy | Max one emoji per tweet, used as a marker |
| All-caps headlines (>4 words) | Reads as shouting | Cap UPPER CASE at 1-2 words |
| Posting then ghosting | No replies → no algorithm boost | Stay in replies for first 60 min |

### Step 12: Apply the Rewrite Framework

The agent applies a three-pass rewrite:

1. **Tighten the hook** — inject pattern interrupt + specificity + payoff
2. **Restructure the middle using the rule of 3** — three points or three beats, no more, no less; sub-points get nested or cut
3. **Strengthen the closer** — recap + one CTA + double down on the hook's promise

## Worked Examples

### Example 1: Founder Lessons Thread (weak draft → strong rewrite)

**Weak draft (8 tweets):**

```
1/ Some thoughts on what I've learned building a startup over the past few years 🧵👇

2/ When you start a startup it's really hard. There's a lot of things to figure out and not enough time.

3/ One thing I learned is that hiring is important. Don't hire too fast or too slow.

4/ Another thing is product-market fit. You need to find it. Talk to customers.

5/ Fundraising is also a big topic. Investors will pass on you a lot. Don't take it personally.

6/ Culture matters too. Set the tone early.

7/ I've made many mistakes along the way. But I'm grateful for the journey.

8/ Like if you agree! And follow for more startup content 🚀
```

**Strong rewrite (8 tweets) with reasoning:**

```
1/ I burned $1.4M building the wrong product before we found PMF.
   3 lessons I'd pay to send back to 2024-me:
```
*Reasoning: specific number ($1.4M) + pattern interrupt (admitting failure) + explicit payoff (3 lessons). Drops "thoughts" and 🧵.*

```
2/ HIRING.

   We hired 6 engineers before we had a working demo.
   They built features for users we didn't have.

   Rule: don't hire to build the product. Hire to scale a product
   that's already working.
```
*Reasoning: UPPER CASE label = visual bullet. Concrete number (6 engineers). Rule stated as a rule, not a hedge.*

```
3/ PRODUCT-MARKET FIT.

   I thought talking to customers meant asking "would you use this?"
   Wrong question. Of course they say yes.

   Right question: "what would you stop doing to use this?"
   That's the only one that predicts payment.
```
*Reasoning: contrarian framing. Replaces vague "talk to customers" with a specific reframe. Memorable and screenshottable.*

```
4/ FUNDRAISING.

   We got 47 no's before our first yes.
   I took every one personally. Wasted weeks recovering.

   Investors aren't rejecting you. They're saying "not enough signal yet."
   Go get more signal. Come back.
```
*Reasoning: specific count (47). Rephrases the cliché ("don't take it personally") into actionable advice.*

```
5/ CULTURE.

   The first 5 hires set culture forever.
   Not the founder. Not the handbook. The first 5.

   Hire one cynic and you'll be hiring around them for 3 years.
```
*Reasoning: counterintuitive claim (founder doesn't set culture). Specific number (5). Sticky last line.*

```
6/ The meta-lesson:

   Every "obvious" startup advice is correct in the abstract
   and useless without the specific reframe that makes it operational.

   "Hire slow" means nothing.
   "Don't hire to build the MVP" is a rule.
```
*Reasoning: synthesizes the previous tweets into a higher-order insight. Marks the thread as a thinker's thread, not a listicle.*

```
7/ I'm not glad I made these mistakes.
   But I'm glad I made them with $1.4M and not $14M.

   Pick the cheap version of every mistake you can.
```
*Reasoning: callback to tweet 1's number (closes the loop). Reframes the worn "grateful for the journey" line.*

```
8/ I post one of these breakdowns every Tuesday.
   Founder lessons, no fluff, written from the trenches.

   Follow @handle if that's your kind of thing.
   And if this hit, RT tweet 1 — helps it reach the right people.
```
*Reasoning: specific cadence (Tuesday). One CTA (follow), with a soft RT ask for the people it actually resonated with. No "like if you agree."*

### Example 2: Contrarian Framework Thread (weak draft → strong rewrite)

**Weak draft (6 tweets):**

```
1/ Hot take on marketing 🔥

2/ Most marketing advice is wrong. People say content marketing works but actually it doesn't for everyone.

3/ I think the real model is: attention -> trust -> demand. You need to build all three.

4/ Most companies focus on attention only. That's why their marketing fails.

5/ Trust takes time. Demand follows trust. It's a sequence.

6/ Comment YES if you want my full framework!
```

**Strong rewrite (7 tweets) with reasoning:**

```
1/ "Content marketing works" is the most expensive lie in B2B.

   I watched 9 portfolio companies burn $4M+ on it.
   The ones that recovered all switched to the same 3-stage model:
```
*Reasoning: contrarian claim with stakes ($4M, 9 companies). "Most expensive lie" is screenshottable. Promise of a 3-stage model = explicit payoff.*

```
2/ Almost every B2B marketing playbook optimizes for ATTENTION.

   Get views. Get clicks. Get traffic.

   Attention without trust is a leaky bucket.
   You're paying to fill a bucket that empties before anyone buys.
```
*Reasoning: visual emphasis (ATTENTION). Punchy three-line beat ("Get views. Get clicks. Get traffic."). Memorable metaphor (leaky bucket).*

```
3/ The model that actually works:

   ATTENTION -> TRUST -> DEMAND

   Three stages.
   Each one earns the right to the next.
   Skip a stage, the whole thing collapses.
```
*Reasoning: framework named and visualized. Single emphasized line carries the model — perfect screenshot tweet.*

```
4/ ATTENTION (stage 1).

   Job: get the right person to look once.
   Tools: short-form posts, SEO, distribution partnerships.

   Most companies stop here. That's why most marketing fails.
```
*Reasoning: structured tweet with clear sub-labels (Job / Tools). Echoes the contrarian thesis.*

```
5/ TRUST (stage 2).

   Job: make the right person believe you'd be useful.
   Tools: long-form writing, case studies, customer voices.

   Trust takes 6-18 months. There is no shortcut.
   Everyone who tells you there is, is selling one.
```
*Reasoning: specific time anchor (6-18 months). Cynical kicker line ("everyone who tells you…") = high RT-bait.*

```
6/ DEMAND (stage 3).

   Job: convert belief into a transaction.
   Tools: pricing pages, sales motion, free trials, paid ads.

   This is where paid ads finally work.
   Run them at stage 1, you're shouting at strangers.
```
*Reasoning: closes the model with a specific re-positioning of paid ads. Reader leaves with a new mental model.*

```
7/ Recap:

   Attention -> Trust -> Demand.
   Skip a stage, lose the year.

   I write about B2B GTM every week.
   Follow @handle if you want fewer expensive lies.
```
*Reasoning: recap in one screenshottable line. CTA matches the contrarian voice ("fewer expensive lies"). Single ask. Removed "comment YES" engagement-bait.*

### Example 3: Behind-the-Scenes Story Thread (weak draft → strong rewrite)

**Weak draft (10 tweets):**

```
1/ I want to share a story about what happened at my company last week 🧵

2/ So we had this big customer meeting. It was important.

3/ The night before I couldn't sleep. I was nervous.

4/ The meeting started and things were going okay.

5/ Then the demo broke. The screen froze. It was bad.

6/ I had to think fast. I decided to be honest about it.

7/ I told the customer "this is embarrassing but here's what happened."

8/ Surprisingly, they appreciated the honesty.

9/ They signed the contract anyway. $400k deal.

10/ Lesson: be honest when things break! Tag a founder who needs to hear this 🚀
```

**Strong rewrite (11 tweets) with reasoning:**

```
1/ Last Tuesday, our demo crashed in front of a $400k customer.
   I almost lied to cover it up.
   What happened next changed how I run sales calls forever:
```
*Reasoning: cold-open with the highest-stakes moment. Specific deal size. Confession ("almost lied"). Promise of a turning point.*

```
2/ Context: 8-month enterprise sales cycle.
   3 demos already. This was the closer.
   Their CTO had told their CFO this was a done deal.
```
*Reasoning: stakes loaded fast. Three concrete details (8 months, 3 demos, CTO told CFO) anchor the reader.*

```
3/ I'd rehearsed the demo 11 times the night before.
   I was running on 4 hours of sleep and one bad coffee.

   Should've been fine.
```
*Reasoning: vulnerability + foreshadowing ("should've been fine"). Specific numbers (11, 4 hours).*

```
4/ Minute 14, I clicked to load the analytics module.

   The screen froze.
   Then a yellow error banner: "Connection lost."

   Six executives. Watching. Silence.
```
*Reasoning: cinematic specificity (minute 14, yellow banner, six executives). Three-word sentences create rhythm.*

```
5/ My first instinct: "This sometimes happens with corporate firewalls,
   let me try a workaround."

   That was a lie.
   Their firewall was fine. Our staging server was down.
```
*Reasoning: shows the temptation to lie, then immediately corrects it. The reader is inside the founder's head.*

```
6/ I caught the words on the way out.
   Took a breath.
   Said something different:

   "I have no idea what just broke. Let me find out
   instead of guessing."
```
*Reasoning: dialogue formatting. The pivot is the screenshottable moment of the thread.*

```
7/ I pulled up Slack on my phone.
   Messaged our on-call engineer in front of everyone.
   Read his reply out loud:

   "Staging is down. ETA 20 min. Sorry."
```
*Reasoning: shows the action, doesn't tell. "Read it out loud" is the radical-transparency moment.*

```
8/ The CTO laughed.

   "First vendor in 6 months who didn't try to bullshit us
   when their demo broke."

   Their CFO nodded.
```
*Reasoning: payoff with direct quote. Specific time anchor (6 months). Ends with a small visual beat.*

```
9/ We finished the demo 25 minutes later.
   They signed the next morning.
   $412k, 2-year contract.
```
*Reasoning: specificity ($412k, 2-year). Drops the rounded number from the hook to feel like real receipts.*

```
10/ The lesson isn't "honesty wins."
    Everyone says that.

    The lesson is: enterprise buyers have been lied to so often
    that radical transparency is now a competitive moat.

    Use it.
```
*Reasoning: rejects the cliché takeaway and reframes into a sharper insight. "Competitive moat" is the screenshottable phrase.*

```
11/ I write one of these stories every Sunday.
    Real numbers, real names where I can,
    real things that break.

    Follow @handle for the next one.
```
*Reasoning: specific cadence (Sunday). Tone matches the story. Removed "tag a founder" bait. One CTA.*

## Output

The agent produces:

- **Thread classification**: which archetype the draft fits and what its optimization rules are
- **Hook audit**: scored on pattern interrupt + specificity + payoff, with a rewritten alternative
- **Length recommendation**: cut, keep, or expand based on goal (engagement vs saves vs follows)
- **Tweet-by-tweet rewrite**: each tweet rewritten with reasoning explaining why
- **Visual hierarchy fixes**: line breaks, UPPER CASE emphasis, emoji discipline
- **Closer rewrite**: recap + single CTA + double down
- **Anti-pattern flags**: explicit list of what was killing the draft
- **Distribution plan**: when to post, follow-up quote-tweet timing, reply-strategy for the first hour
- **Conversion mechanics**: link placement / DM-on-reply / lead magnet, picked to match the goal

## Common Scenarios

### "Audit my draft thread before I post"
Paste the draft and the audience / goal. The agent classifies the thread type, scores the hook, flags anti-patterns, and returns a tweet-by-tweet rewrite with reasoning.

### "My thread flopped, what went wrong?"
Paste the thread and the metrics (impressions, replies, profile clicks). The agent reverse-engineers the failure point — usually the hook, sometimes the closer, occasionally the middle density.

### "I have a topic, help me thread it"
Give the topic and angle. The agent picks the best archetype for the angle, drafts a hook, and outlines the middle and closer.

### "Rewrite this hook 5 different ways"
Paste the hook. The agent produces variants across different archetypes (story, contrarian, listicle, prediction, before/after) so you can A/B test.

### "Help me build a 4-week thread plan"
Give your beat / topic and goal (followers, newsletter, leads). The agent proposes 4-8 thread topics, ordered for compounding effect (a foundational thread first, contrarian-take second, story third).

## Tips for Best Results

- **Share the goal explicitly** — followers, newsletter signups, replies, RTs, saves. Each goal flips the optimization
- **Share the audience** — "B2B founders" vs "indie hackers" vs "marketers" change the voice
- **Share your follower count** — sub-1k accounts need different tactics than 50k accounts (smaller accounts can be more contrarian, larger accounts need broader hooks)
- **Share past performance** — if a hook style worked before, the agent can build on it; if it tanked, the agent will avoid the pattern
- **Provide the draft, even if rough** — the agent rewrites better than it writes from scratch, because constraints sharpen it
- **Specify length budget** — "5 tweets max" or "framework thread, 8-10" prevents over-expansion
- **Mention any forbidden moves** — some users won't do confessional threads, some won't do contrarian. Tell the agent

## When NOT to use

- **Single tweets** — different optimization. Single tweets win on punchline, brevity, and ratio of insight to character count. Threads optimize for cumulative dwell time and structure. Use a tweet-coach skill or write a punchy single tweet directly.
- **LinkedIn long-form posts** — different platform rules. LinkedIn rewards paragraph structure, native video, hashtags, and a slower professional voice. The hook conventions, length sweet spots, and CTA mechanics differ enough that applying Twitter thread rules to LinkedIn will under-perform.
- **Newsletters / blog posts** — these are long-form prose with permanent URLs. Threads are a distribution format for short ideas. Don't compress a 2,000-word essay into a thread — turn the essay's headline insight into a thread that drives readers to the essay.
- **Threadstorm spam** — if you're posting 5+ threads per day, this skill will not save you. The algorithm punishes account-level over-posting regardless of thread quality.
