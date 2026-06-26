---
name: trades-longevity-training
description: >-
  Use when you work (or plan to work) a physically demanding job like construction, delivery, caregiving, farming, warehousing, or any manual trade/gig work and want to build a resilient body that lasts decades. Agent personalizes a minimal-equipment strength, mobility, and recovery program based on your specific job demands, tracks progress, schedules around shifts, and adjusts for pain or fatigue so you can focus on doing the work.
metadata:
  category: skills
  tagline: >-
    Train your body to thrive in demanding physical work for 20+ years without chronic pain or forced early retirement.
  display_name: "Trades Longevity Training"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-30"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install trades-longevity-training"
---

# Trades Longevity Training

You depend on your body to earn a living through physical labor. This skill equips your AI agent to act as your dedicated occupational strength and conditioning coach, creating and managing a customized, evidence-based program of strength, mobility, and recovery practices tailored to your exact job stresses. The goal is simple: work hard today and still be able to work hard in 2035.

`npx clawhub install trades-longevity-training`

## When to Use This Skill

Use this protocol when:
- You are new to or transitioning into a physically demanding role and want to build a foundation that prevents early breakdown.
- You are experiencing accumulating aches, stiffness, or reduced work capacity after shifts.
- You want to extend your career in trades by 10-20 years and avoid the common "body gave out" exit.
- Seasonal peaks are coming (construction season, harvest, busy delivery periods) and you need to peak your capacity.
- You have access to minimal or no gym equipment but have your body, perhaps basic tools or household items.

This is not general fitness. It is occupational resilience training.

## Agent Role vs. Human Role

**Agent Responsibilities:**
- Conduct initial and ongoing assessments via structured questions.
- Generate and update personalized weekly training plans based on job demands (e.g., overhead work for electricians, lifting for movers, repetitive motions for assembly).
- Maintain filesystem logs: user_profile.md, workout_log.md, pain_tracker.md.
- Schedule sessions around your work shifts and energy levels with automated reminders.
- Research specific exercise variations or modifications if new issues arise.
- Provide ready-to-use checklists, progression schemes, and decision trees.
- Analyze logged data and recommend adjustments (deload, focus areas).
- Draft summaries for sharing with doctors or physical therapists if needed.

**Human Responsibilities:**
- Perform all physical exercises with proper form and full attention (the embodied part).
- Provide honest feedback on energy, pain (1-10 scale, location), and how the body feels post-work.
- Make the time for 3-5 short sessions per week (15-45 minutes).
- Apply the mobility and activation drills during work breaks when possible.
- Listen to your body and stop if something feels sharply wrong.

The agent plans, tracks, and optimizes. You do the physical work that builds the resilience.

## Initial Assessment Protocol (Agent Executes This)

1. Ask for job details: "Describe a typical shift. What are the most demanding movements? How much lifting (frequency, weights, heights)? Overhead work? Repetitive motions? Standing/walking duration? Tools used?"
2. Current status: Age, any injuries or chronic pain locations, current activity level, available equipment/time (home workouts? gym access? 20 min/day?).
3. Baseline tests (human performs, agent records): 
   - Overhead squat hold (mobility screen)
   - Plank hold time (core)
   - Farmer's carry simulation (grip/shoulders)
   - Single leg balance
   - Shoulder flexion range
Agent saves to user_profile.md and generates Phase 1 plan.

## Step-by-Step Training Protocol

### Phase 1: Foundation (Weeks 1-4) — Mobility, Stability, Work Capacity

Focus: Address common deficits in trades workers (tight hips/shoulders, weak core/glutes, poor thoracic mobility).

**Daily (or 5x/week) 15-20 minute Mobility Flow (do before/after shifts or as active recovery):**
- Cat-Cow to Thoracic Rotations: 10 reps/side
- World's Greatest Stretch: 30s/side, 3 rounds
- Hip 90/90 Transitions: 8/side
- Ankle Rocks: 10/side
- Wrist and Forearm Mobilizations: 30s each direction (critical for tool use)
- Neck and Shoulder CARs (Controlled Articular Rotations)

**3x/week Strength & Stability (20-30 min):**
1. Glute Bridge Variations (single leg progressions) - 3 sets of 10-15
2. Bird-Dog - 3 sets of 8/side
3. Dead Bug variations - 3 sets of 10/side (anti-extension core)
4. Side Planks with hip dips - 3 sets of 20-40s/side
5. Goblet Squat or Bodyweight Squat to Box - 3 sets of 8-12 (use bucket if no weight)
6. Push-up variations or Wall Push (depending on level) - 3 sets
7. Farmer's Carry or Loaded Carry simulation (heavy buckets, tool bag) - 3 sets of 20-40m

Progression: Add holds, slow tempos, or light weight (water jugs, sandbags).

Agent provides exact weekly template in markdown table format and reminds.

### Phase 2: Strength Development (Weeks 5-12)

Introduce progressive overload with job-specific patterns.

**Key Lifts (3-4x/week full body or upper/lower split based on recovery):**
- Hinge: Romanian Deadlift or Single Leg RDL variations
- Squat: Goblet or Zercher style (simulates carrying loads)
- Push: Overhead Press (dumbbell or improvised) or Push-up progressions
- Pull: Inverted Rows or Doorway Rows if no equipment; focus on scapular strength
- Core: Pallof Press simulation or Anti-rotation cable mimics with bands/rope
- Grip: Dead hangs, plate pinches, or towel hangs

Sets/reps: 3-5 sets of 5-12 reps. Use RPE 7-8 (room in tank).

Include conditioning: 1-2x/week short metabolic circuits (e.g., 4 rounds of squat, carry, push) mimicking work bursts.

### Phase 3: Maintenance & Peaking (Ongoing)

- 2-3 strength sessions
- 2-3 mobility/active recovery
- 1 deload week every 8-10 weeks
- Periodic re-assessment every 8 weeks
- Job-specific add-ons: e.g., rucking for delivery workers, overhead endurance for painters.

Agent handles periodization and auto-adjusts volume based on reported fatigue (e.g., "On a scale of 1-10, how recovered do you feel today?").

## Decision Trees (Agent Uses These)

**If new or worsening pain reported:**
- Sharp pain during movement: Stop that exercise, switch to mobility only, recommend professional eval.
- Dull ache post-work: Increase mobility time in that area, add foam roll/self-massage proxy (tennis ball), reduce load 20%.
- Back pain: Prioritize core bracing drills, hip mobility, consult body-mechanics-injury-prevention skill.
- Shoulder pain: Emphasize thoracic mobility, external rotation strength, reduce overhead volume.

**If time crunched:**
- Shorten to 15 min "work break circuits": 5 min mobility + 3 key strength moves.

## Ready-to-Use Templates & Scripts

**Agent Check-in Script:**
"Hi, how was the shift today? Rate your energy 1-10. Any new pain (location and 1-10 intensity)? Did you complete today's session? What felt good/hard?"

**Weekly Log Template (Agent maintains):**

| Date | Session | Exercises Completed | Notes/Pain | Energy Post-Work |
|------|---------|---------------------|------------|------------------|
| ...  | ...     | ...                 | ...        | ...              |

**Progression Rules:**
- When you hit upper rep range easily for 2 sessions, increase weight/reps/time.
- Deload: 50-60% volume if fatigue >7/10 for 3 days.

**Doctor Communication Template:**
"Hi Dr., I am following a structured strength and mobility program for my [job]. I have been experiencing [symptom]. Here is my current routine [paste summary]. Any recommendations?"

## Success Metrics

- Can perform daily work tasks with less post-shift fatigue/pain after 8 weeks.
- Improved baseline test scores (e.g., plank time +30s, better squat depth).
- No missed work days due to preventable musculoskeletal issues over 6 months.
- Subjective: Feeling stronger and more capable at end of shifts.

Track in agent-managed log. Celebrate milestones.

## Maintenance & Iteration

- Every 3 months: Full re-assessment and program overhaul.
- Integrate with existing skills: Use sleep-hygiene-overhaul, nutrition-physical-labor, body-mechanics-injury-prevention for synergistic results.
- Agent flags if progress stalls and suggests variations or external resources (local PT, etc.).

## Rules & Safety Notes

- Always warm up with 5 min light movement or the mobility flow.
- Prioritize form and controlled movement over heavy loads. Bad form in training + bad form at work = injury.
- Stop immediately for sharp, shooting, or neurological pain (numbness, tingling).
- Hydrate, breathe properly (nasal breathing where possible), recover with good sleep.
- If you have pre-existing conditions, get medical clearance before starting.
- This is training to support work, not replace proper work technique.

## Evidence Base

Drawn from:
- National Strength and Conditioning Association (NSCA) guidelines for tactical and occupational athletes.
- Physical therapy principles (mobility from Functional Range Conditioning, stability from McGill's spine research for laborers).
- Studies on construction and manual workers showing reduced injury rates with targeted strength/mobility interventions (e.g., OSHA-aligned ergonomics plus training).
- Progressive overload and periodization from exercise physiology (ACSM).

## Disclaimer

This skill provides practical, agent-managed protocols based on general expert practices but is not a substitute for personalized medical advice, physical therapy, or professional training. Listen to your body. Consult a physician or qualified professional for any health concerns, injuries, or before beginning any new exercise program. Results vary based on individual factors, consistency, and work conditions.

The agent will help you stay consistent. The human does the hard physical work that makes the difference. Stay strong. Keep building.