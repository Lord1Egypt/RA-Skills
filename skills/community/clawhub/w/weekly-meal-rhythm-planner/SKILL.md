---
name: weekly-meal-rhythm-planner
displayName: "Weekly Meal Rhythm Planner"
version: "1.0.0"
description: "Creates a simple 7-day meal rhythm card for people who want steadier eating without detailed dieting, calorie tracking, or rigid menus. Helps map weekly constraints, choose prep anchors, add fallback meals, make a prep list, and set a light review point."
triggerKeywords: [meal planning, routine, food, weekly planning, fallback meals]
tags: [health, routine, meal planning, home, planning]
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
healthSafety: "This skill provides general routine-planning support only. It is not medical nutrition advice, and users with medical conditions, eating disorders, pregnancy needs, allergies, or special diets should consult a qualified professional."
---
# Weekly Meal Rhythm Planner

## Purpose

Use this skill when the user wants steadier eating but does not want detailed dieting, calorie tracking, macros, weight-loss coaching, or a strict meal plan. The goal is a practical weekly rhythm that lowers friction: predictable meal anchors, flexible fallback meals, and a short prep list.

## Safety Boundary

This skill provides general routine and planning support. It does not diagnose, treat, prescribe, manage medical conditions, or provide individualized nutrition therapy. For diabetes, kidney disease, heart disease, eating disorders, pregnancy, infant or child nutrition, food allergies, medically restricted diets, or other special dietary needs, advise the user to work with a qualified clinician or registered dietitian.

Do not calculate calories, macros, supplement plans, weight-loss targets, medical diets, or therapeutic food rules. If the user describes disordered eating, severe food restriction, fainting, rapid weight change, or urgent symptoms, encourage professional or emergency support as appropriate.

## Intake

Ask only for the details needed to build the rhythm:

- Which meals feel most inconsistent: breakfast, lunch, dinner, snacks, or hydration
- Usual week shape: workdays, commute, school, caregiving, late nights, social meals, travel
- Cooking capacity: realistic prep time, cooking confidence, kitchen access, cleanup tolerance
- Food constraints: preferences, budget, allergies, dietary restrictions, shared household needs
- Existing reliable foods: meals or ingredients the user already eats without much friction
- Hard days: the 1-3 days where fallback meals matter most

If the user gives limited information, make a clearly labeled starter draft and invite edits.

## Workflow

1. Map the week.
   - Identify high-energy, medium-energy, and low-energy days.
   - Mark nights that need leftovers, assembly meals, takeout, or no-cook options.
   - Keep the map simple enough to fit on one page.

2. Choose anchors.
   - Pick 2-4 recurring meal anchors, such as a repeat breakfast, a batch lunch base, a soup night, a leftovers night, or a grocery pickup day.
   - Prefer anchors that match the user's existing habits over new complicated recipes.
   - Avoid moralizing language about "good" and "bad" foods.

3. Add backups.
   - Choose 3-5 fallback meals that are shelf-stable, frozen, assembled, or fast to prepare.
   - Include at least one no-cook fallback and one low-cleanup fallback when possible.
   - Match backups to the user's budget and equipment.

4. Make the prep list.
   - Convert the rhythm into a short grocery and prep list.
   - Separate "buy," "prep once," and "keep on hand."
   - Keep prep tasks specific and realistic.

5. Set review.
   - Add a 10-minute review point after the week.
   - Ask what was easiest, what failed, and what should be repeated or simplified.

## Deliverable Format

Produce a concise 7-day meal rhythm card:

- Week map: one line per day with the intended rhythm
- Anchors: recurring meals, prep points, or household routines
- Fallback meals: fast options for hard days
- Prep list: buy, prep once, keep on hand
- Review prompt: a short end-of-week check
- Safety note: general routine support only, with professional guidance for special diets or health conditions

## Style Rules

- Keep the tone practical, flexible, and nonjudgmental.
- Focus on rhythm, friction reduction, and repeatable defaults.
- Do not turn the output into a diet plan.
- Do not imply a meal is required, forbidden, healthy, unhealthy, clean, or cheating.
- When information is missing, label assumptions instead of presenting them as facts.

## Example Prompts

Copy and run any of these to see what the skill does:

1. "I want steadier meals but I don't want to track calories. Help me build a simple weekly rhythm."
2. "My dinners are chaotic. I work late Tuesday and Thursday and I never know what to cook. Make me a meal rhythm card."
3. "Give me a 7-day meal plan with fallback meals for my busiest days. I have a small budget and only 20 minutes to cook."

## Install-First Success Path

1. **Input:** User installs the skill and says, "I want steadier meals but I don't want to track calories. Help me build a simple weekly rhythm."
2. **Steps:**
   - Skill recognizes the meal-planning trigger and starts intake.
   - Asks about inconsistent meals, week shape, cooking capacity, constraints, reliable foods, and hard days.
   - Maps the week, chooses 2-4 recurring anchors, adds 3-5 fallback meals, builds a prep list, and sets a review point.
3. **Output:** A concise 7-day meal rhythm card with week map, anchors, fallback meals, prep list, review prompt, and safety note.
