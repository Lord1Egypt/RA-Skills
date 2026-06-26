---
name: sedentary-reminder
description: Designs practical sedentary-break reminder systems with strong timing logic. Use when users want help deciding when to remind, how often to remind, when to defer, how to adapt to focus/meeting/presence context, and how to generate natural reminder copy or recurring reminder plans.
---

# Sedentary Reminder

Sedentary Reminder is a reusable skill for designing sit-break reminder systems that feel timely instead of annoying. Its main job is not just writing reminder copy, but helping decide **when a reminder should fire, when it should wait, and when it should stay quiet**.

Use it to generate:
- sit-break reminder timing rules
- work-state-aware and presence-aware reminder behavior
- reminder escalation logic for long uninterrupted sitting
- rotating reminder copy sets
- single-language reminder output based on context
- cron-friendly or workflow-friendly reminder plans
- user control logic for pause, resume, quiet windows, and profile switching
- automatic break detection logic for away, idle, lock, sleep, or manual break signals
- direct state-editing rules that map user chat commands into heartbeat-state updates

This skill is best when the user cares about realism: fewer bad reminders, better timing, less interruption, and messages that still feel human.

## Purpose
Use this skill to help people break up long sitting periods during work or study with reminders that are practical, context-aware, and easy to follow.

This skill is useful when someone wants:
- short sit-break reminders
- a smarter answer to when reminders should happen
- reminder timing rules for work, study, or coding
- rotating reminder copy for recurring prompts
- reminder systems that defer during focus or meetings
- cron-friendly recurring break-reminder plans
- simple user commands like pause, resume, today off, or switch to focus mode
- automatic recognition that the user already got up and should not be treated as continuously sitting
- chat commands that directly modify the reminder state file

## Core principle
A good sedentary reminder system should optimize for **helpful timing**, not maximum frequency.

The goal is:
- remind after meaningful sitting time, not constantly
- avoid interrupting the user at obviously bad moments
- catch long uninterrupted sessions before they become excessive
- resume gracefully after meetings, focus blocks, or away periods
- keep reminders actionable and low-friction

## What this skill does not do
Do not treat this skill as a medical, sensor, or posture-tracking system.

It does not:
- diagnose medical conditions
- detect real body posture with certainty
- know whether the user can safely stand up right now
- replace medical advice
- execute recurring reminders by itself without being paired with scheduling or automation tools

If the user asks about pain, injury, rehabilitation, or treatment, keep guidance general and recommend professional advice when appropriate.

## Good use cases
Use this skill when the user wants help with:
- office or desk-work break reminders
- coding-session reminder timing
- study-session sit-break prompts
- adaptive reminder systems for bots, cron jobs, or productivity tools
- wellness-oriented microcopy about reducing sedentary time
- designing reminder logic that avoids bad interruption timing

## Avoid or limit use when
Be careful in these situations:
- the user explicitly does not want reminders
- the user is in a situation where interruption may be unsafe
- the request is actually about diagnosis or treatment
- the system has no useful context and would end up spamming generic reminders

## Output goals
Prefer outputs that are:
- short and easy to act on
- natural rather than robotic
- encouraging rather than scolding
- timing-aware rather than mechanically repetitive
- varied enough for recurring use
- conservative when interruption cost is high

For recurring reminders, prefer rotation instead of repeating the same sentence every time.

## Language decision rules
Choose language using this order:
1. If the user explicitly asks for a language, use that language.
2. Otherwise, default to the language of the current conversation.
3. Only generate bilingual output when the user explicitly asks for bilingual output.
4. For public or reusable reminder sets, keep language-specific copy separated by language.

## Tone decision rules
Choose tone based on context:
- Default to neutral-friendly tone.
- Use cute or playful tone only when the user asks for it or the context clearly fits.
- Use shorter and lighter reminders for focus-heavy contexts.
- Use slightly more informative reminders for educational or public-facing copy.
- When reminders are frequent, make copy calmer and less emotionally loud.

## Timing-first reminder rules
When the user asks when reminders should trigger, reason in this order:
1. continuous sitting duration
2. current work state
3. presence confidence
4. interruption cost
5. time since last reminder
6. time since last acknowledged break

Never base timing only on a fixed interval if context clearly suggests waiting.

## Recommended baseline timing
Use these as practical defaults unless the user asks otherwise:

### Standard work or desk use
- first reminder after **45 to 60 minutes** of likely continuous sitting
- if ignored, next reminder after **20 to 30 minutes**, not immediately
- encourage a short stand, stretch, water, or brief walk

### Study sessions
- first reminder after **40 to 50 minutes**
- use lighter reminders during active concentration
- after 90 to 120 minutes of sustained sitting, increase urgency slightly

### Coding or deep-focus work
- first reminder after **60 to 75 minutes**
- avoid hard interruptions in the middle of an obvious focus run
- if focus appears ongoing, defer to a softer reminder at a natural boundary

### Casual browsing or low-pressure computer use
- first reminder after **30 to 45 minutes**
- tone can be lighter and slightly more playful

### Long uninterrupted sitting safeguard
Regardless of state, if likely sitting extends past **90 to 120 minutes**, send some form of reminder unless the user explicitly disabled it. Long uninterrupted sitting is where the system should become more confident.

## Best moments to remind
Prefer reminders at natural breakpoints instead of arbitrary timestamps.

Good moments include:
- finishing a task or subtask
- after sending a message or email
- after a build, run, export, or upload completes
- when the user switches windows or apps
- after a meeting ends
- after a focus timer ends
- when activity resumes after an idle period, if the user sits back down and keeps working

If no breakpoint signals are available, use elapsed time conservatively.

## Bad moments to remind
Avoid or defer reminders during:
- active meetings or calls
- live demos or presentations
- obvious deep-focus stretches
- intense back-and-forth chat during urgent work
- full-screen presentation or screen sharing contexts
- moments right after another reminder fired

A reminder that lands at the wrong moment is worse than a slightly late reminder.

## Work-state reminder rules
Adjust reminder behavior based on the user's current work state.

### Supported states
- normal
- focus
- meeting
- study
- casual

### Behavior by state
- **normal**: standard reminder cadence, usually 45 to 60 minutes
- **focus**: lower frequency, shorter copy, prefer natural boundaries, usually 60 to 75 minutes
- **meeting**: defer reminders until the meeting ends or a likely gap appears
- **study**: moderate cadence, usually 40 to 50 minutes, supportive tone
- **casual**: shorter cadence, usually 30 to 45 minutes, can be lighter in tone

If the user explicitly describes their state, prefer that over inference.

Examples:
- "I'm in deep focus right now." -> focus
- "I'm in a meeting." -> meeting
- "I'm studying." -> study
- "I'm just browsing casually." -> casual
- "I'm working normally." -> normal

If the user gives no explicit state, infer conservatively from the current conversation and task context.

## State priority rules
Use this order when deciding reminder behavior:
1. explicit user-selected state
2. recent conversation context
3. current task or schedule context
4. conservative inference

When signals conflict, prefer the user's explicit state.

## Presence detection rules
Use conservative presence states when deciding whether to send a reminder.

Presence states:
- present
- uncertain
- away

Suggested signals:
- recent keyboard or mouse activity
- system idle time
- screen lock state
- screen sleep state
- foreground app activity

Behavior:
- If present, reminders may be sent normally.
- If uncertain, reduce frequency or defer.
- If away, suppress reminders until the user returns.
- When the user returns after being away, do not instantly fire a stale reminder unless sitting continues for a bit.

Goal:
Avoid sending reminders when the user is likely not at the computer.

## Deferral and escalation rules
Use deferral before repetition.

### Deferral
Defer a reminder when:
- the user is in a meeting
- the user is likely screen sharing or presenting
- a focus block is clearly active
- the last reminder was recent
- presence is uncertain

When deferring, retry at the next likely natural boundary or after a modest delay.

### Escalation
Escalate only when uninterrupted sitting is getting long.

Suggested escalation ladder:
1. **soft**: gentle stand-up cue after baseline sitting duration
2. **standard**: clearer action prompt after continued sitting
3. **firm but calm**: stronger nudge after 90 to 120 minutes of likely uninterrupted sitting

Do not escalate tone aggressively. More urgency should come from clarity, not guilt.

## Cooldown rules
To prevent nagging:
- avoid back-to-back reminders inside a short window
- after a reminder, wait at least **15 to 20 minutes** before another unless the user asked for high frequency
- after an acknowledged break, reset the sitting timer or reduce urgency substantially
- if several reminders were ignored, space them wider instead of tighter unless safety or explicit preference says otherwise

## Rotation rules
When generating recurring reminders:
- avoid repeating the exact same line back-to-back
- rotate by category instead of random repetition when possible
- prefer this sequence for long-running reminders:
  1. minimal
  2. friendly
  3. action-oriented
  4. cute
  5. informative
- for professional contexts, reduce cute reminders unless requested
- reserve firmer lines for long uninterrupted sitting, not ordinary cadence

## Workflow
When the user asks for help, follow this sequence:

1. Identify the request type:
   - one reminder
   - multiple reminder variants
   - rotating reminder set
   - public-facing wellness copy
   - cron/reminder schedule design
   - state-aware reminder design
   - timing-strategy design

2. Gather key context when needed:
   - work, study, reading, coding, or general desk use
   - current work state
   - current presence state when available
   - preferred tone
   - preferred language
   - preferred reminder frequency or maximum interruption tolerance
   - whether reminders should minimize interruption
   - whether timing should be elapsed-time-based, breakpoint-based, or hybrid

3. Produce the result:
   - start with timing logic first when timing is the main question
   - keep it concise
   - keep it actionable
   - keep it natural
   - keep it varied for recurring use
   - adapt timing and tone to current state when available
   - suppress or defer reminders when the user is likely away or busy

4. Suggest the next useful step when relevant:
   - alternate timing profiles
   - reminder rotation groups
   - language variants
   - cron-friendly schedules
   - pseudo-code or rule logic for automation

## Recommended default profiles
Use these preset profiles when the user wants a ready-made configuration.

### Balanced default
- first reminder: 50 minutes
- follow-up: 25 minutes later if still continuously sitting
- defer during meetings
- soften during focus
- suppress while away

### Focus-friendly
- first reminder: 70 minutes
- follow-up: 30 minutes later
- prefer natural boundaries over strict timers
- keep copy minimal

### Study-friendly
- first reminder: 45 minutes
- follow-up: 20 to 25 minutes later
- supportive tone
- stronger nudge after 100 minutes

### Gentle high-frequency
- first reminder: 35 to 40 minutes
- follow-up: 20 minutes later
- very light tone
- suitable for casual desk use

## References
- Chinese reminder library: read `references/reminder-copy-zh.md`
- English reminder library: read `references/reminder-copy-en.md`
- Chinese integration guide: read `references/integration-guide-zh.md`
- Heartbeat template: read `references/heartbeat-template-zh.md`
- Heartbeat state rules: read `references/heartbeat-state-rules-zh.md`
- User controls guide: read `references/user-controls-zh.md`
- Break detection guide: read `references/break-detection-zh.md`
- Direct state editing guide: read `references/direct-state-editing-zh.md`

Use the reference files when the user wants batches of reminders, rotation sets, language-specific outputs, a practical reminder deployment design, a heartbeat-ready reminder workflow, self-updating state logic, user-facing control commands, automatic break detection, or direct chat-to-state control.

## Examples
### Example requests
- Write 10 Chinese sit-break reminders for office workers.
- Design a reminder strategy that knows when to wait during meetings.
- Generate a focus-friendly rotating reminder set for coding.
- Draft a neutral reminder system for a productivity app.
- Design a cron-friendly sit-break reminder plan for work hours only.

### Example outputs
**Neutral**
- 你已经坐一阵了，起来站两分钟，顺手活动下肩颈。

**Friendly**
- 先起来走两步，接杯水，再回来继续也不迟。

**Minimal focus-safe**
- 到点了，起身两分钟。

**Long-sit stronger nudge**
- 这轮坐得有点久了，先站起来活动一下，再继续。

## Cron integration example
If the user wants a recurring reminder design, suggest a practical schedule plus timing logic.

Example guidance:
- baseline frequency check: every 10 to 15 minutes
- actual reminder decision: based on sitting duration plus state checks, not every scheduler tick
- output: single-language reminders unless bilingual output is explicitly requested
- strategy: rotate multiple reminders instead of repeating one line
- timing: defer in meetings, soften in focus, suppress while away

Example reminder text:
- 你已经坐挺久了，起来两分钟，伸展一下，顺手喝口水。

## Safety and quality notes
- Do not overstate health claims.
- Do not frame reminders as medical advice.
- Do not assume the user can always stop immediately.
- Prefer gentle encouragement over guilt or fear.
- Prefer clear action over vague slogans.
- Prefer fewer better-timed reminders over frequent generic ones.
