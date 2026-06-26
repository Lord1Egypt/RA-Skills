---
name: values-clarification
description: >-
  Structured process for identifying personal values and life purpose. Use when someone feels directionless, is making a major life decision, suspects their life is misaligned with what they actually want, or is rebuilding after a crisis.
metadata:
  category: mind
  tagline: >-
    Figure out what you actually care about when you strip away what you're supposed to care about — then align your life to match.
  display_name: "Values Clarification & Purpose"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install values-clarification"
---

# Values Clarification & Purpose

"Find your passion" is garbage advice. Passion doesn't precede action — it follows it. And most of the time, when people feel directionless, the problem isn't missing passion. It's misalignment: their life is structured around values they inherited, absorbed, or defaulted into instead of values they actually hold. This skill is a structured process for figuring out what you actually care about when you strip away what you're supposed to care about, then looking at whether your life matches. The gap between those two things is the source of most chronic dissatisfaction.

```agent-adaptation
# Localization note — values are universal but their relative cultural weight differs.
- The values list and exercises in this skill are drawn from ACT (Acceptance and
  Commitment Therapy), which has been validated across cultures.
- HOWEVER: the relative importance of values is deeply cultural.
  In individualist cultures (US, UK, Australia): autonomy, achievement, and
  independence tend to rank higher.
  In collectivist cultures (Japan, China, many Latin American and African countries):
  family, community, loyalty, and tradition tend to rank higher.
  NEITHER is wrong. The agent must not impose a cultural frame on what the
  "right" values are.
- The "ideal Tuesday" exercise works globally but the specifics differ.
  A good regular day in Lagos looks different from one in Stockholm. Adapt
  the exercise to the user's actual context.
- Family/cultural expectation conflicts are universal but manifest differently.
  In some cultures, choosing personal values over family expectations carries
  more social cost. Acknowledge this reality rather than treating it as
  a problem to be solved.
- If the user's values include faith, tradition, or community obligation,
  respect these as genuine values — not as constraints to overcome.
```

## Sources & Verification

- **ACT Values Work** -- Acceptance and Commitment Therapy. Core therapeutic framework for values clarification. Developed by Steven Hayes.
- **Russ Harris** -- "The Happiness Trap" (2008) and "The Confidence Gap" (2011). Practical ACT-based values exercises.
- **Martin Seligman** -- VIA Character Strengths. [viacharacter.org](https://www.viacharacter.org/). Research-based strengths and values assessment.
- **William Miller** -- Motivational Interviewing values card sort and values exploration exercises.
- **Shalom Schwartz** -- Theory of Basic Human Values. Cross-cultural values research across 82 countries.

## When to Use

- User feels directionless, stuck, or chronically dissatisfied without a clear reason
- Someone is making a major life decision (career change, move, relationship, having kids) and doesn't know what to optimize for
- User suspects they're living according to someone else's values (parents, culture, employer, social media)
- Someone is rebuilding after a crisis (job loss, divorce, health scare, identity disruption)
- User says things like "I don't know what I want" or "I should be happy but I'm not"
- Someone wants a foundation before using career-reinvention or identity-rebuild skills
- User wants to do an annual values review and life audit

## Instructions

### Step 1: The values card sort — find your actual top 5

**Agent action**: Present the full values list. Guide the user through sorting from 50 down to their top 5. This is not a quiz — it's a process of elimination that forces tradeoffs.

```
VALUES CARD SORT:

Read through this list. Your job is to get from 50 to 5.

ROUND 1: Remove any that genuinely don't matter to you.
Be honest — drop the ones you think SHOULD matter but don't.
(If "achievement" makes you exhausted rather than motivated,
drop it. If "spirituality" is something you do out of obligation,
drop it.)

ROUND 2: From what's left, pick your top 15.

ROUND 3: From those 15, pick your top 10.

ROUND 4: From those 10, pick your top 5.

THE LIST:
Achievement    Adventure     Authenticity   Autonomy      Balance
Beauty         Challenge     Community      Compassion    Competence
Contribution   Courage       Creativity     Curiosity     Fairness
Faith          Family        Freedom        Friendship    Fun
Growth         Health        Honesty        Humor         Independence
Influence      Integrity     Justice        Kindness      Knowledge
Leadership     Love          Loyalty        Mastery       Nature
Openness       Order         Peace          Pleasure      Power
Purpose        Recognition   Reliability    Resilience    Respect
Responsibility Security      Service        Simplicity    Spirituality
Stability      Tradition     Truth          Wisdom

IMPORTANT NOTES:
-> There are no wrong answers. "Pleasure" is not a lesser value
   than "service." "Power" is not a shameful value if it's honest.
-> If a value isn't on this list, add it. This list is a starting
   point, not a constraint.
-> The hard part is Round 3 to Round 4. That's where the real
   tradeoffs happen. "I value both security AND freedom" — yes,
   but which one wins when they conflict? That's your answer.
-> Your values are yours, not your parents', your partner's,
   your employer's, or your culture's. If your honest top 5
   surprises you, that's information, not a problem.
```

### Step 2: The "ideal Tuesday" exercise

**Agent action**: Guide the user through this exercise. Not their ideal vacation — their ideal regular day.

```
THE IDEAL TUESDAY:

Not your ideal vacation. Not your dream life in a movie montage.
Your ideal REGULAR day. A good, sustainable Tuesday.

Walk through the day:

MORNING:
-> What time do you wake up?
-> Where are you? (City, home type, surroundings)
-> Who else is there?
-> What's the first thing you do?
-> How do you feel?

MIDDAY:
-> What work are you doing? (Or are you not working?)
-> Who are you working with?
-> Where are you working?
-> What kind of problems are you solving?
-> How much autonomy do you have?

AFTERNOON:
-> How do you spend the hours between work and evening?
-> What are you doing with your body?
-> Who are you with?

EVENING:
-> Who are you eating with?
-> What are you doing after dinner?
-> What's your state of mind going to bed?

NOW EXTRACT THE VALUES:
-> If your ideal Tuesday involves waking up slowly with no
   alarm, that's probably freedom or peace.
-> If it involves solving hard problems with smart people,
   that's probably challenge or competence or community.
-> If it involves being outdoors, that's nature or health.
-> If it involves time alone, that's independence or simplicity.
-> If it involves a house full of people, that's family or
   community or love.

THE IDEAL TUESDAY REVEALS YOUR VALUES MORE HONESTLY THAN ANY
ABSTRACT RANKING EXERCISE. Because you're not thinking about
what's impressive — you're thinking about what feels right.

Compare your ideal Tuesday values with your card sort top 5.
If they match: your values are clear.
If they don't: dig into the discrepancy. The card sort might
reflect what you think you should value. The Tuesday exercise
reveals what you actually value.
```

### Step 3: The eulogy test

**Agent action**: This is uncomfortable. That's the point.

```
THE EULOGY TEST:

Imagine your funeral. Someone who knows you well stands up to speak.

What do you want them to say?

Not your resume. Not your accomplishments. Not your job title
or net worth or social media following.

What do you want them to say about WHO YOU WERE?

Write 3-5 sentences. Be specific.

EXAMPLES:
-> "She was the person who showed up. Every time. Even when
   it was inconvenient."
-> "He told you the truth even when it was hard to hear,
   and you trusted him because of it."
-> "She made everyone around her feel like they mattered."
-> "He built things that worked and taught other people how."
-> "She never let fear make her decisions."

WHAT THIS REVEALS:
Your eulogy sentences are your deepest values in action.
If your eulogy is about honesty but your daily life involves
constant people-pleasing, there's a gap.
If your eulogy is about presence and connection but you work
80 hours a week, there's a gap.
If your eulogy is about courage but you've been avoiding a
hard conversation for six months, there's a gap.

THE GAP IS THE WORK.

Now: do your eulogy values match your card sort and your
ideal Tuesday? If all three exercises point the same direction,
you know your values. If they diverge, look at where and why.
```

### Step 4: Identify misalignment

**Agent action**: This is where insight becomes actionable. Help the user see where their values and their life don't match.

```
MISALIGNMENT AUDIT:

Take your top 5 values. For each one, ask:

1. HOW MUCH TIME do I spend on this per week?
   (Actual hours, not "I think about it a lot")

2. HOW MUCH MONEY do I spend on this per month?
   (Budget is a values document — what you spend on is
   what you actually prioritize)

3. WHAT DECISIONS have I made in the last year that
   ALIGN with this value?

4. WHAT DECISIONS have I made in the last year that
   CONTRADICT this value?

5. On a scale of 1-10, how well does my current life
   reflect this value?

COMMON MISALIGNMENT PATTERNS:

"I value family but I work 60 hours a week."
-> Your schedule says you value career. Your heart says
   family. Something has to change or the dissonance
   will eat you alive.

"I value creativity but my job is pure administration."
-> You're trading your core value for security.
   That's a valid tradeoff — but is it conscious?

"I value health but I haven't exercised in months."
-> Aspiration is not the same as value. A value you
   don't act on is a wish.

"I value independence but I've never said no to my parents."
-> This might be a genuine values conflict (independence
   vs family loyalty) rather than a misalignment.
   See Step 5.

THE QUESTION THAT MATTERS:
For each misalignment, ask: "Is this a tradeoff I'm consciously
making, or is it a default I've never examined?"

Conscious tradeoffs are fine. Unexamined defaults are where
chronic dissatisfaction lives.
```

### Step 5: Navigate competing values

**Agent action**: Help the user handle the reality that values conflict with each other.

```
WHEN VALUES COMPETE:

Your values will conflict with each other. This is normal.
There is no right answer — only your answer.

COMMON VALUE CONFLICTS:
-> Security vs Freedom (stable job vs entrepreneurship)
-> Family vs Achievement (being present vs career ambition)
-> Honesty vs Kindness (telling the truth vs sparing feelings)
-> Independence vs Community (doing it your way vs belonging)
-> Stability vs Adventure (staying put vs taking the leap)

HOW TO NAVIGATE:

1. ACKNOWLEDGE THE CONFLICT
   Don't pretend you can have both at maximum intensity.
   "I want both security and freedom" is a starting position,
   not a solution.

2. IDENTIFY YOUR CURRENT ALLOCATION
   Right now, which side are you serving? If your life is
   95% security and 5% freedom, is that the ratio you'd choose?

3. DETERMINE WHAT "ENOUGH" LOOKS LIKE
   You don't need maximum security OR maximum freedom.
   What's the minimum security that lets you sleep at night?
   What's the minimum freedom that keeps you from feeling trapped?

4. MAKE SEASONAL ADJUSTMENTS
   Your 20s might optimize for adventure. Your 30s might
   shift toward family. Your 50s might return to growth.
   Values have stable cores but shifting priorities.

5. ACCEPT THE LOSS
   Choosing one value over another means losing something real.
   Grief over the unchosen path is not a sign you chose wrong.
   It's a sign you valued something you couldn't fully have.

WHEN VALUES CONFLICT WITH FAMILY/CULTURE/EMPLOYER:
-> This is the hardest version. Your honest values may put you
   at odds with people you love or systems you depend on.
-> You have three options: (a) change the external situation,
   (b) find creative integration, (c) accept the misalignment
   as a conscious tradeoff.
-> There is no option (d) where the conflict disappears.
   Pretending it doesn't exist is what makes people sick.
```

### Step 6: Build alignment — concrete actions

**Agent action**: Move from insight to action. Values without behavior change are just a nice journaling exercise.

```
ALIGNMENT PROTOCOL:

For each of your top 5 values, define:

1. ONE DAILY ACTION (takes <15 minutes)
   Small, consistent, non-negotiable.
   Value: creativity -> Write for 10 minutes every morning.
   Value: health -> Walk for 15 minutes after lunch.
   Value: connection -> One genuine conversation per day (not text).

2. ONE WEEKLY ACTION (takes 1-2 hours)
   Meaningful investment in the value.
   Value: family -> Sunday dinner, phones off, every week.
   Value: growth -> One hour of deliberate learning.
   Value: nature -> One outdoor activity regardless of weather.

3. ONE QUARTERLY DECISION
   A larger choice that moves your life toward the value.
   Value: freedom -> Negotiate remote work or reduce expenses by 10%.
   Value: contribution -> Commit to a volunteer role.
   Value: courage -> Have the conversation you've been avoiding.

4. ONE ANNUAL REVIEW
   Check your values against your life. Have they shifted?
   Has your alignment improved? Where are the remaining gaps?

THE FIRST WEEK:
-> Pick ONE value.
-> Define the daily action.
-> Do it for 7 days.
-> Then add the second value.
-> Stacking slowly works. Overhauling everything at once doesn't.

THE ALIGNMENT METRIC:
You're not trying to get to 10/10 on every value.
You're trying to close the gap between what you care about
and how you actually spend your time, money, and energy.
Progress from 3/10 to 6/10 changes your life more than
moving from 7/10 to 8/10.
```

### Step 7: Annual values review

**Agent action**: Establish the review practice. Values shift over time — checking them yearly prevents drift.

```
ANNUAL VALUES REVIEW:

Your values shift. Not dramatically, but they shift. The person
you are at 25 does not hold the same hierarchy as the person
you are at 40 or 55. Checking annually prevents you from living
by outdated values.

THE REVIEW:
1. Pull out last year's top 5. Do they still feel right?
   If something has shifted, that's not failure — it's growth.

2. Redo the card sort (or at least the top 10 -> top 5 round).
   See what's different.

3. Run the alignment audit again (Step 4).
   Where are the gaps now?

4. Look at your major decisions this year.
   Which values drove them? Were those the right values for
   those decisions?

5. Set your alignment actions for the next year (Step 6).

WHEN VALUES SHIFT:
-> After major life events (birth, death, illness, divorce,
   job change) — re-assess immediately, don't wait for annual
-> When chronic dissatisfaction persists despite "everything
   being fine" — your values may have shifted without your
   conscious awareness
-> When you notice you're excited about things that used
   to bore you, or bored by things that used to excite you

VALUES REVIEW PAIRS WELL WITH:
-> identity-rebuild skill (for major identity transitions)
-> career-reinvention skill (for professional alignment)
-> stoicism-daily-practice skill (for the dichotomy of control
   applied to values conflicts)
-> death-preparation skill (memento mori clarifies values fast)
```

## If This Fails

- **"I can't narrow down to 5 values"?** You're trying to keep everything because choosing feels like loss. It is. Choose anyway. You can revisit in a year. Five values you act on beats twenty you admire from a distance.
- **Card sort results feel "wrong" or surprising?** That surprise is the point. You may have been living by assumed values rather than actual values. Sit with the discomfort for a week before overriding your honest results.
- **Values conflict with family expectations feels impossible?** This is real and hard. See the competing-values section (Step 5). You may not be able to fully resolve it, only manage it consciously. Family therapy can help if the conflict is severe.
- **Did the exercises but nothing changed?** Values clarification without behavior change is just self-knowledge. Go back to Step 6 and commit to ONE daily action for ONE value. Start there.
- **Stuck in analysis paralysis?** Stop sorting and start acting. Pick the value that made you feel the most emotion during the exercises (positive or negative). That's your starting point. Act on it for a month. Clarity comes from action, not from thinking harder.

## Rules

- Never tell the user what their values should be. Not even subtly. "Power" and "pleasure" are as valid as "service" and "compassion."
- Do not assume Western individualist framing. Values of family, tradition, loyalty, and community obligation are not less evolved — they're different.
- Push back on "should" values. If the user says "I should value X," ask whether they actually do or whether they're performing a value they inherited.
- Distinguish between values and goals. "Make a million dollars" is a goal. The value underneath might be security, achievement, freedom, or recognition. Find the value.
- This skill is a foundation for other skills (career-reinvention, identity-rebuild). Reference those connections when relevant.

## Tips

- Your budget is a values document. Look at where your money goes, and you'll see what you actually prioritize — regardless of what you say you value.
- Your calendar is a values document too. Where your time goes is where your values are, not where your intentions are.
- If your top 5 values are identical to what your parents would pick for you, do the exercises again more honestly.
- The ideal Tuesday exercise often reveals more than the card sort because it bypasses your ego. You can't perform values in a daydream.
- Values work is not a one-time event. The review matters as much as the initial discovery. Revisit annually.
- Chronic dissatisfaction without an obvious cause is almost always a misalignment between values and life structure. The cause is not mysterious — it's just invisible until you do this work.

## Agent State

```yaml
state:
  process:
    card_sort_completed: false
    top_5_values: []
    ideal_tuesday_completed: false
    eulogy_test_completed: false
    alignment_audit_completed: false
    alignment_scores: {}  # value: score (1-10)
    misalignments_identified: []
    competing_values_identified: []
  actions:
    daily_actions_defined: []
    weekly_actions_defined: []
    quarterly_decisions_defined: []
    actions_started: false
    actions_start_date: null
  context:
    trigger: null  # directionless, major_decision, crisis_rebuild, annual_review
    previous_values: []  # from prior assessment if any
    values_shifted: null
  follow_up:
    next_review_date: null
    check_in_frequency: null
```

## Automation Triggers

```yaml
triggers:
  - name: start_with_card_sort
    condition: "process.card_sort_completed IS false AND user_seeking_values_work"
    action: "Let's start with the values card sort. I'll give you a list of 50 values. Your job is to get down to your top 5. The hard part isn't picking your favorites — it's dropping the ones you think you should keep but don't actually care about."

  - name: alignment_gap_detected
    condition: "process.alignment_audit_completed IS true AND ANY alignment_scores < 4"
    action: "You've got some significant gaps between what you value and how you're living. That's not unusual — it's why you're here. Let's pick the biggest gap and build a concrete plan to close it, starting with one daily action."

  - name: action_check_in
    condition: "actions.actions_started IS true AND days_since(actions_start_date) == 7"
    action: "It's been a week since you started your values-aligned actions. How's it going? Which ones stuck? Which ones fell off? Adjusting the actions is fine — abandoning the value is what we want to avoid."

  - name: annual_review_prompt
    condition: "process.card_sort_completed IS true"
    schedule: "annually from card_sort_date"
    action: "It's been a year since your last values assessment. Time for an annual review. Values shift over time — what felt essential a year ago might have moved. Want to redo the card sort and see what's different?"

  - name: crisis_trigger
    condition: "context.trigger == 'crisis_rebuild'"
    action: "Rebuilding after a crisis is one of the best times to do values work, because the old structure is already gone. You're not disrupting anything — you're building from scratch. Let's find out what you actually want to build toward."
```
