---
name: "Voice Care Speaking Day Plan"
description: "Builds a general, non-medical speaking-day routine for hydration, pacing, warmups, breaks, and recovery, with clear escalation for pain, voice loss, breathing issues, or persistent symptoms."
version: "1.0.0"
type: prompt-flow
tags: ["voice care", "public speaking", "teaching", "routine", "wellness", "presentation"]
---

# Voice Care Speaking Day Plan

## Overview

Use this prompt-only skill when a user has a heavy speaking day and wants a practical, general routine to protect vocal comfort and stamina.

The skill creates a simple plan for before, during, and after speaking. It covers hydration, gentle warmups, pacing, room setup, breaks, recovery, and warning signs. It is not medical care, diagnosis, or treatment.

## When to Use

Use this skill when the user says things like:

- "I have to speak all day tomorrow. How do I take care of my voice?"
- "Build me a voice care plan for a workshop."
- "I am teaching several classes today."
- "I need a speaking-day routine for a keynote, training, stream, or podcast."
- "How do I pace my voice through back-to-back calls?"
- "Make a checklist so I do not strain my voice."

## Required Inputs

Ask for only the details needed to tailor a general routine:

- Type of speaking day, such as teaching, meetings, stage talk, webinar, stream, podcast, or performance
- Total speaking time and schedule blocks
- Break length and frequency
- Room or setup, such as microphone, classroom, conference room, stage, headset, or noisy space
- Current voice status, such as normal, tired, hoarse, dry, or recovering
- Hydration, food, caffeine, alcohol, smoke, dust, allergies, or dry-air factors if the user wants to share them
- Whether the user has a microphone or amplification
- Any hard constraints, such as no breaks, travel, outdoor work, or back-to-back sessions

If the user reports pain, voice loss, breathing difficulty, coughing blood, severe illness, or symptoms that persist, stop routine-building and recommend qualified professional help.

## Workflow

1. **Screen for red flags.** Ask about or respond to pain, sudden voice loss, breathing issues, severe symptoms, or persistent symptoms before giving a routine.
2. **Map the speaking load.** Turn the schedule into blocks with speaking intensity, breaks, and recovery windows.
3. **Set the voice strategy.** Choose a simple goal, such as conserve, steady, recover, or high-demand day.
4. **Plan before speaking.** Include hydration, gentle body and breath preparation, easy voice onset, room setup, microphone check, and avoidable irritants.
5. **Plan during speaking.** Include pacing, volume management, microphone use, posture, water breaks, pauses, audience activities, and signs to back off.
6. **Plan between sessions.** Add quiet breaks, gentle reset, hydration, and note-taking instead of unnecessary talking.
7. **Plan after speaking.** Add cooldown, quiet recovery, sleep-supporting habits, and next-day check-in.
8. **Add scriptable reminders.** Provide short reminders the user can place on slides, notes, phone alarms, or meeting agendas.
9. **Add escalation guidance.** State when to pause and seek help from a clinician, voice-specialized professional, urgent care, or emergency care.

## Output Format

Produce the plan with these sections:

1. **Speaking Day Snapshot**
   - Event type
   - Total speaking time
   - Voice status
   - Main constraints
2. **Red Flag Check**
   - Any reported warning signs
   - Recommended action if warning signs are present
3. **Before Speaking**
   - Hydration and environment
   - Gentle warmup
   - Microphone or room setup
   - Pacing intention
4. **During Speaking**
   - Volume and pacing
   - Break cues
   - Audience or meeting tactics to reduce continuous talking
   - What to do if the voice feels strained
5. **Between Sessions**
   - Quiet reset
   - Hydration or comfort steps
   - What to avoid
6. **After Speaking**
   - Cooldown
   - Recovery habits
   - Next-day check
7. **Mini Reminders**
   - Three to seven short prompts the user can copy into notes or alarms
8. **Get Help If**
   - Clear escalation list for pain, voice loss, breathing issues, severe symptoms, or persistent symptoms

## Example Prompts

Copy and paste one of these into your AI assistant with your specific details filled in:

1. **Heavy teaching day:** "I'm teaching 5 classes back-to-back tomorrow (8 AM to 3 PM, 45 min each with 5 min breaks). My voice already feels a little tired from yesterday. Build me a speaking-day plan."

2. **Stage keynote:** "I have a 2-hour keynote at 10 AM with a Q&A after. I'll have a handheld mic on stage. I want a plan that keeps my voice strong through the whole thing, including recovery after."

3. **All-day workshop:** "I'm hosting a full-day workshop (9 AM to 4 PM) with mostly me talking and some group activities. It's in a dry conference room and I tend to lose my voice by 3 PM. What should my routine be?"

## Safety Boundary

- This skill provides a general routine only. It does not diagnose, treat, or replace medical, speech-language pathology, or voice-specialist advice.
- Recommend professional help for throat or voice pain, sudden or repeated voice loss, breathing difficulty, trouble swallowing, coughing blood, fever with severe symptoms, injury, or symptoms that persist or keep returning.
- For breathing difficulty, signs of airway trouble, severe allergic reaction, chest pain, or emergency symptoms, recommend urgent or emergency care.
- Do not prescribe medication, supplements, steroid use, antibiotics, reflux treatment, or medical devices.
- Do not tell the user to push through pain or force the voice.
- Avoid extreme vocal exercises, yelling, whispering as a cure, or techniques that require clinical coaching.
- Keep warmups gentle, optional, and comfort-based.
- If the user is a professional singer, actor, broadcaster, teacher, or call worker with recurrent issues, suggest a qualified voice professional or clinician.

## Quality Checklist

A strong result should:

- Start with red flag screening or red flag response
- Tailor the plan to the user's schedule and setup
- Keep advice practical, general, and non-medical
- Include before, during, between-session, and after-speaking steps
- Encourage amplification, pacing, breaks, hydration, and quiet recovery
- Include concise reminders the user can reuse during the day
- Escalate clearly for pain, voice loss, breathing issues, or persistent symptoms
