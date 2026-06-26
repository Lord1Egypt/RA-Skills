---
name: teaching-physical-skills
description: >-
  Methods for teaching physical/embodied skills to others. Use when someone needs to teach a child or adult a hands-on physical skill like riding a bike, swimming, cooking, driving, using tools, or any skill that requires physical demonstration.
metadata:
  category: life
  tagline: >-
    Teach someone to ride a bike, swim, use a knife, drive a car — the meta-skill of transferring embodied knowledge from your body to theirs.
  display_name: "Teaching Physical Skills"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install teaching-physical-skills"
---

# Teaching Physical Skills

This is the meta-skill: how to teach someone else a physical skill. Not theory. Not reading about it. The actual transfer of embodied knowledge from your body to theirs — how to ride a bike, swim, use a chef's knife, drive a car, throw a ball, tie a knot. Education workers, coaches, parents, and trades instructors do this every day, and it's one of the skill categories with near-zero AI exposure because it requires physical co-presence, real-time observation, and hands-on adjustment. The principles of motor learning are well-studied and consistent: demonstrate, break it down, let them practice, give specific feedback, manage their frustration, and progress when they're ready. Most people skip half these steps, which is why most people are mediocre teachers of physical skills. This skill makes you better.

```agent-adaptation
# Localization note — physical skill contexts vary by culture and country
- Driving: left-hand vs right-hand traffic. Licensing age varies.
  US: right-hand traffic, 15-16 for learner's permit
  UK/AU/Japan: left-hand traffic
  Adapt all driving instruction to local traffic rules.
- Swimming: cultural attitudes toward water and swimming instruction
  vary significantly. Some cultures have less access to pools or
  swimming education. Adapt to context.
- Tool use: metric vs imperial measurements in workshop contexts.
- Knife skills: European vs Asian knife techniques. Chef's knives
  vs cleavers vs santoku. Adapt to the user's kitchen context.
- Sports: cricket vs baseball, football vs soccer, etc. Substitute
  locally relevant throwing/catching examples.
- Educational frameworks differ (Montessori availability,
  scouting programs, swim programs vary by country).
```

## Sources & Verification

- **Schmidt & Lee, "Motor Control and Learning"** -- The standard academic textbook on motor skill acquisition, practice conditions, and feedback. 6th edition, Human Kinetics. https://us.humankinetics.com/
- **Montessori practical life methods** -- Age-appropriate progression for teaching children physical skills. American Montessori Society. https://amshq.org/
- **American Red Cross Learn-to-Swim program** -- Structured swimming progression from water comfort to stroke development. https://www.redcross.org/take-a-class/swimming
- **National Highway Traffic Safety Administration (NHTSA)** -- Driver education resources and graduated licensing data. https://www.nhtsa.gov/
- **Ericsson, K.A., "Peak: Secrets from the New Science of Expertise"** -- Research on deliberate practice and skill acquisition.
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User needs to teach a child to ride a bike
- User is teaching someone to swim
- User wants to teach knife skills in the kitchen
- User is helping a teenager learn to drive
- User needs to teach a child to tie their shoes
- User is teaching someone to use a hand tool or power tool
- User wants to teach throwing, catching, or a sport skill
- User is frustrated that their learner "just can't get it"
- User wants general guidance on how to be a better physical skills teacher

## Instructions

### Step 1: The demonstration-practice-feedback loop

**Agent action**: Teach the universal framework that underlies all physical skill instruction.

```
THE CORE LOOP (every physical skill follows this):

1. DEMONSTRATE
   - Show the complete skill at normal speed first. Let them see
     what "done" looks like before you break it down.
   - Then demonstrate slowly, narrating what you're doing and WHY.
   - Position yourself so they see the movement from the angle
     that matters. For knife skills: stand next to them, same
     side. For a golf swing: face them, then stand behind them.
   - Demonstrate multiple times. They need to see it more than
     you think. Three times minimum for a new movement.

2. BREAK IT DOWN
   - Identify the 2-4 key movements in the skill.
   - Teach ONE movement at a time until it's consistent.
   - Don't add the next piece until the current one is reliable
     about 70-80% of the time. Not perfect — reliable.
   - Use "part practice" (isolating components) for complex skills,
     then combine components into "whole practice."

3. LET THEM PRACTICE
   - Give them uninterrupted practice time. Resist the urge to
     correct every rep. Let them feel the movement.
   - Early practice should be slow and deliberate. Speed comes
     after the pattern is established.
   - Expect it to look ugly at first. That's normal. Motor
     patterns take 50-100+ repetitions to become consistent and
     thousands to become automatic.

4. GIVE FEEDBACK
   - Specific, not general. "Keep your elbow closer to your body"
     is useful. "Do it better" is useless.
   - One correction at a time. The brain can process one motor
     adjustment per attempt. Multiple corrections = confusion.
   - Positive-specific-positive: "Your grip is good. Try keeping
     your wrist straighter this time. That rotation is getting
     much smoother."
   - Reduce feedback frequency as they improve. Constant feedback
     creates dependency. They need to develop their own sense of
     what "right" feels like (intrinsic feedback).
   - Ask them what they felt: "What was different that time?" This
     builds self-awareness.

5. PROGRESS
   - Add complexity only when the current level is consistent.
   - Vary conditions slightly to build adaptability (practice in
     different locations, at different speeds, with slight
     variations).
   - Revisit fundamentals periodically. Even advanced learners
     benefit from checking the basics.
```

### Step 2: Managing fear and frustration

**Agent action**: Cover the emotional management that makes or breaks physical skill learning.

```
FEAR MANAGEMENT:

Fear is the primary barrier to learning physical skills, not
coordination or talent. A kid afraid of falling off a bike will
tense up, which guarantees they fall. An adult afraid of the
water will hold their breath and stiffen, which guarantees they
sink. Address the fear before the technique.

PRINCIPLES:
- Acknowledge the fear directly. "It's normal to be nervous about
  this. Everyone is the first time." Dismissing fear ("There's
  nothing to be afraid of") makes it worse.
- Reduce the stakes systematically. Can't ride a bike? Start
  without pedals on grass (soft landing). Afraid of water? Start
  sitting on the steps in the shallow end. Afraid of the stove?
  Start with cold ingredients, then warm, then hot.
- Give them control. Let them set the pace. "Tell me when you're
  ready for the next step." Taking away their control increases
  fear.
- Never force a progression. Pushing a terrified child off the
  diving board does not teach them to swim. It teaches them to
  not trust you.
- Model calm. If you're anxious, they will be too. Your body
  language is half the instruction.

FRUSTRATION MANAGEMENT:

Frustration peaks when the learner can see what "right" looks
like but can't make their body do it. This is the most common
point where people quit.

PRINCIPLES:
- Normalize the plateau. "Everyone gets stuck here. It means
  your brain is rewiring. It will click."
- End each session on a success, even if it means stepping back
  to an easier version of the skill. Never end on repeated
  failure. The last thing they feel is what they remember.
- Take breaks. Motor learning actually consolidates during rest.
  A 10-minute break (or a night's sleep) often produces visible
  improvement without any additional practice. Tell them this.
- Shorten sessions when frustration is high. Three focused
  15-minute sessions beat one miserable 45-minute session.
- Avoid comparisons. "Your sister learned this faster" is
  the fastest way to destroy motivation.
- Celebrate specific progress, not just completion. "Your
  balance was solid for 3 seconds that time — that's double what
  you did yesterday."
```

### Step 3: Age-appropriate progression

**Agent action**: Cover how teaching approach differs by learner age.

```
TEACHING BY AGE:

TODDLERS (2-4 years):
- Attention span: 5-10 minutes maximum per session.
- Make it a game, not a lesson. They don't know they're learning.
- Demonstration is everything. Explanation is almost useless.
  Show, don't tell.
- Hand-over-hand guidance (your hands on theirs) works for fine
  motor skills (holding a crayon, using a spoon).
- Expect regression. They'll do it right Tuesday and wrong
  Wednesday. Normal.
- Praise effort, not results. "You tried so hard!" not "Good job!"
  (which is meaningless if repeated constantly).

CHILDREN (5-9 years):
- Attention span: 15-20 minutes for focused practice.
- Can follow 2-3 step verbal instructions.
- Respond well to "challenges" — "Can you do it three times in a
  row?" Turn practice into achievable goals.
- Peer learning is powerful. If a friend is doing it, they want to.
- Correction should be private, not in front of other kids.
- This is the golden age for motor learning. New movement patterns
  are acquired faster between 5-9 than at any other age.

PRETEENS/TEENS (10-17):
- Can understand complex verbal instruction and self-correct.
- Self-consciousness is the primary barrier. They don't want to
  look stupid. Provide a low-audience practice environment.
- Explain the WHY behind the technique. "Bend your knees because
  it lowers your center of gravity" works with teens in a way it
  doesn't with a 6-year-old.
- Give them autonomy. Let them problem-solve before you correct.
- Respect their pace. Pressure to perform accelerates dropout.

ADULTS:
- Come with existing motor patterns (some helpful, some not).
  Unlearning a bad habit is harder than learning from scratch.
- Overthink everything. Adults try to intellectualize physical
  movement. "Stop thinking and feel it" is legitimate instruction
  for adults.
- Fear of looking foolish is huge. Normalize being bad at new
  things. "Everyone looks ridiculous learning to ski."
- Can handle complex feedback and self-direct practice.
- Often need permission to be slow. "You don't have to go fast
  yet. Slow and correct first."
```

### Step 4: The 8 most common physical skills people teach

**Agent action**: Provide specific, step-by-step protocols for the skills people most commonly need to teach.

```
1. BIKE RIDING (balance-first method):

This method works. It's faster and less traumatic than training
wheels, which teach pedaling but not balance.

Equipment: bike sized so the child can place both feet flat on
the ground while seated. Helmet (non-negotiable). Flat, paved
area with no traffic (parking lot, dead-end street, park path).

Step 1: Remove the pedals (15mm wrench, left pedal is reverse-
  threaded). Lower the seat so both feet are flat on the ground.
Step 2: Walk-ride. They walk the bike while seated, getting used
  to the weight and steering. 10-15 minutes.
Step 3: Glide. Gentle downhill slope. They push off and coast
  with feet up. Focus: balance, not speed. Once they can glide
  10-15 feet without putting feet down, they've got it.
Step 4: Reinstall pedals. Start on a slight downhill. Feet on
  pedals, push off, and pedal. They already know how to balance
  so they only need to add the pedaling motion.
Step 5: Starting from a stop. One foot on pedal (at 2 o'clock
  position), push down to start, other foot follows.

Timeline: Most kids get it in 1-3 sessions (30-45 min each).
Don't hold the seat and run alongside. It teaches them to rely
on you, not on their own balance.

2. SWIMMING (water comfort before strokes):

Step 1: Water comfort. Sit on pool steps. Splash. Pour water on
  head. Face in water. Blow bubbles. This phase takes as long as
  it takes. DO NOT RUSH.
Step 2: Floating. Back float first (support their head and lower
  back, slowly reduce support). "Look at the sky. Ears in the
  water. Belly up like a table."
Step 3: Kicking. Hold the wall or a kickboard. Straight legs,
  kick from the hips, not the knees. Toes pointed.
Step 4: Arm movement. Dog paddle first (simple, builds confidence),
  then freestyle arms.
Step 5: Breathing. Turn head to breathe, don't lift it. This is
  the hardest part and takes the most practice.
Step 6: Combine into whole stroke.
Never teach swimming alone. Always have a second adult present.

3. KNIFE SKILLS (curl the fingers, anchor the tip):

Appropriate age to start: 7-8 with a butter knife or kid-safe
knife, 10-12 with a real chef's knife under supervision.

Step 1: The claw grip. Curl the fingertips of the holding hand
  under, with knuckles forward. The flat of the blade rides
  against the knuckles. Fingertips can't be cut if they're behind
  the knuckles.
Step 2: The knife grip. Pinch the blade just above the handle
  between thumb and index finger ("pinch grip"). Other fingers
  wrap the handle. This gives control.
Step 3: The rocking motion. Tip of the knife stays on the board.
  The handle lifts and lowers. The blade rocks through the food.
  "Anchor the tip" is the mantra.
Step 4: Practice on soft foods first (mushrooms, bananas,
  zucchini) before hard foods (carrots, onions).
Step 5: Board management: keep the board stable (damp towel
  underneath), keep cut food organized, clear scraps as you go.

4. DRIVING (parking lot first, progressive complexity):

Session 1 — Parking lot, engine off:
  Mirrors, seat adjustment, seatbelt. Identify every control.
  Practice hand position (9 and 3, not 10 and 2 — airbag safety).
  Start the car. Brake, accelerate gently, brake. Feel the pedals.
Session 2 — Parking lot, moving:
  Forward and backward, slow speed. Turning. Parking between lines.
  Mirror checking. Stopping smoothly (brake early and light, not
  late and hard).
Session 3 — Quiet residential streets:
  Right turns, left turns, stop signs, speed management. Scanning
  intersections. Checking mirrors every 5-8 seconds.
Session 4 — Moderate traffic:
  Lane changes, yielding, merging.
Session 5+ — Progressive complexity:
  Highway, night driving, rain, parking garages, parallel parking.

Key rule: NEVER yell or grab the wheel unless there's an actual
emergency. You'll create a nervous driver. Calm voice, clear
instruction: "Start braking now. A little more. Good."

5. THROWING (step and opposite arm):
  - Stand sideways to the target (not facing it).
  - Step toward the target with the foot OPPOSITE the throwing
    arm.
  - Release at the point where the arm is roughly at ear height,
    fingers pointing at the target.
  - Follow through — arm continues forward and down.
  Common error: throwing flat-footed, facing the target. Fix the
  feet first, the arm follows.

6. CATCHING:
  - Start close (5-6 feet). Use a soft ball (tennis ball, foam).
  - Hands out in front, fingers spread, pinkies together for low
    catches, thumbs together for high catches.
  - Watch the ball all the way into the hands. "Track it with
    your eyes."
  - Give with the catch (pull hands toward body on contact).
  - Gradually increase distance and ball firmness.

7. TYING SHOES:
  - The bunny ears method is easier for kids than the loop-and-
    wrap method. Two loops, cross them, pull one through.
  - Practice with large laces or rope first. Fine motor skills
    at 5-6 years old are still developing.
  - Consistent direction matters — pick one way and stick with it.
  - Expect it to take 2-4 weeks of daily practice.
  - Practice on a shoe that's OFF the foot first (on a table,
    facing them the right way).

8. HANDWRITING:
  - Correct grip first: pinch the pencil between thumb and index
    finger, resting on the middle finger. Not a full-fist grip.
  - Start with large movements (whiteboard, big paper on the
    floor) before small movements (lined paper).
  - Letters: start with straight-line letters (L, T, I, H)
    before curved ones (S, C, O).
  - Don't correct letter formation constantly. Focus on the 2-3
    most problematic letters at a time.
  - Left-handers: angle the paper about 30-45 degrees clockwise.
    Don't try to make them write like right-handers.
```

### Step 5: Teaching readiness checklist

**Agent action**: Help the user determine when the learner is ready for the next step.

```
TEACHING READINESS CHECKLIST:
Is the learner ready for the next progression?

PHYSICAL READINESS:
[ ] Can perform the current step 7-8 times out of 10 consistently
[ ] Can perform it without constant verbal prompting
[ ] Body is relaxed, not tense or stiff during the movement
[ ] Speed is controlled (not rushing or moving in slow motion)

EMOTIONAL READINESS:
[ ] Shows interest or willingness to try the next step
[ ] Not expressing fear about progression
[ ] Not frustrated from the current step (end on success first)
[ ] Has had at least one rest period since last practice

COGNITIVE READINESS:
[ ] Can describe what they're doing in their own words
    ("I'm keeping my elbows in and looking at the target")
[ ] Can identify their own mistakes without your prompting
    ("That one was off because I didn't follow through")
[ ] Understands what the next step involves

IF MORE THAN TWO BOXES ARE UNCHECKED:
Stay at the current step. Add variety to keep it interesting
(different location, different time of day, different music,
a game or challenge format) but don't advance the skill.

IF ALL BOXES ARE CHECKED:
Introduce the next step. Demonstrate it. Expect a temporary
performance dip — this is normal when adding a new component.
Their consistency will drop from 80% to 40-50% at first and
rebuild over the next few sessions.
```

## If This Fails

- If the learner is not progressing despite repeated practice, check fundamentals. Often a skill that seems stuck is actually built on a shaky earlier step. Go back and reinforce the foundation.
- If frustration is destroying the learning process, take a break measured in days, not minutes. Motor consolidation happens during rest. They may come back and do it.
- If you're losing your patience as the teacher, hand off to someone else temporarily. A different voice and approach often unsticks things. You're not failing — you're too close.
- If the skill involves any safety risk (swimming, driving, tools), and you're not confident in your own ability to keep the learner safe, get professional instruction. Swim instructors, driving schools, and shop classes exist for a reason.
- If the learner has a physical or developmental condition affecting motor skills, consult an occupational therapist or physical therapist who can adapt teaching methods to their specific needs.

## Rules

- Never force a progression on a frightened learner — fear-based teaching creates avoidance, not skill
- Give one correction at a time — the brain processes one motor adjustment per attempt
- End every session on a success, even if you have to step back to an easier version to achieve it
- Safety equipment is non-negotiable (helmets, life jackets, goggles, gloves) regardless of the learner's protests
- The teacher's job is to make themselves unnecessary — reduce guidance and feedback as the learner improves
- Never compare learners to each other, especially siblings

## Tips

- Sleep is when motor skills consolidate. The brain literally replays and strengthens movement patterns during sleep. Practicing before bed and reviewing the next day is more effective than marathon sessions.
- Video is an underrated teaching tool. Record the learner, show them what they're doing vs. what you're demonstrating. Seeing it from outside their body accelerates correction.
- The "constraint-led approach" is powerful: change the environment to force the correct movement. Can't stop a kid from looking at their feet while riding? Give them something to read off a sign ahead. Can't get an adult to bend their knees skiing? Put them in a narrow corridor. Remove the wrong option instead of constantly correcting it.
- Teaching a physical skill to someone else is the best way to deepen your own understanding of it. If you want to get better at something, teach it.
- The 10-minute rule: if they haven't shown any improvement in 10 minutes of focused practice, change something — the approach, the environment, or stop and try tomorrow.
- Young children learn better from peer demonstration than adult demonstration. If another kid their age can do it and they can watch, that's more motivating than any adult showing them.

## Agent State

```yaml
teaching:
  user_context:
    skill_being_taught: null
    learner_age: null
    learner_relationship: null
    previous_attempts: null
    current_frustration_level: null
  instruction_phase:
    demonstrated: false
    broken_into_steps: false
    current_step: null
    total_steps: null
    practice_sessions_completed: 0
  learner_status:
    fear_present: false
    frustration_present: false
    physical_readiness: null
    emotional_readiness: null
    current_consistency_percent: null
  skills_covered:
    core_teaching_method: false
    fear_management: false
    frustration_management: false
    age_appropriate_methods: false
    specific_skill_protocol: false
    readiness_assessment: false
  follow_up:
    next_session_date: null
    notes_for_next_session: null
```

## Automation Triggers

```yaml
triggers:
  - name: frustration_intervention
    condition: "teaching.learner_status.frustration_present IS true"
    action: "The learner is frustrated. This is the most common quitting point. Three options: (1) step back to an easier version and end on a success, (2) take a break and try tomorrow — motor skills consolidate during rest, (3) change the practice format (make it a game, change location, add music). Which feels right for this situation?"

  - name: fear_intervention
    condition: "teaching.learner_status.fear_present IS true AND teaching.instruction_phase.current_step IS SET"
    action: "Fear is blocking progress. The fix is to reduce the stakes, not push harder. What's the lowest-risk version of this step? Can you make it softer, slower, shallower, or shorter? Give the learner control over when to progress. Forced progression builds avoidance, not skill."

  - name: plateau_check
    condition: "teaching.instruction_phase.practice_sessions_completed >= 3 AND teaching.learner_status.current_consistency_percent < 50"
    action: "Three sessions in and consistency is still below 50%. This usually means the foundation isn't solid enough, not that the learner can't do it. Go back one step and reinforce. Also check: are they practicing the wrong pattern? Sometimes early reps build bad habits that need correcting before progress can happen."

  - name: progression_ready
    condition: "teaching.learner_status.current_consistency_percent >= 75 AND teaching.learner_status.fear_present IS false AND teaching.learner_status.frustration_present IS false"
    action: "The learner is hitting 75%+ consistency and they're emotionally ready. Time to introduce the next step. Demonstrate it first, then let them try. Expect their consistency to drop temporarily — that's normal when adding a new component."

  - name: session_planning
    condition: "teaching.follow_up.next_session_date IS SET AND days_until(teaching.follow_up.next_session_date) <= 1"
    action: "Your next teaching session is coming up. Review: what step are you on, what worked last time, what's the plan for this session? Remember to start with a quick warm-up of what they already know before progressing."
```
