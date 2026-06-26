---
name: welding-basics
description: >-
  Use when you need to repair broken metal tools, equipment, or structures; fabricate custom parts for home, farm, vehicle, or gig-work setups; or build from scrap in resource-scarce or post-AI unstable conditions. The agent will assess your workspace, budget, and project needs; research equipment and materials; generate step-by-step plans, safety checklists, and practice trackers; schedule daily/weekly sessions; log progress; and draft sourcing emails or supplier queries. This skill turns your hands and a basic welder into a full fabrication capability — agent handles all planning, research, and tracking so you focus purely on the physical welding and craft.
metadata:
  category: skills
  tagline: >-
    Agent-planned metal fabrication: repair anything, build what you need, and improvise solutions with your own hands in an unstable world.
  display_name: "Welding Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-30"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install welding-basics"
---
# Welding Basics

Master entry-level arc and MIG welding so you can permanently repair farm equipment, vehicles, gates, tools, and custom fabrications without waiting for shops or supply chains. This is not theory — it is a complete, agent-executed training and project protocol that gets you welding safely and productively within 14 days.

`npx clawhub install welding-basics`

## When to Use This Skill

Activate this skill when:
- A critical tool, trailer hitch, gate hinge, or equipment bracket breaks and shop repair costs exceed your budget or timeline.
- You need custom brackets, brackets, jigs, or reinforcements for your trade, small business, or off-grid setup.
- Scrap metal or used equipment is available and you want to convert it into functional assets.
- You are preparing for longer-term self-reliance in gig-economy or crisis scenarios where professional fabrication services may disappear.
- You already own or can acquire a basic welder and want structured, measurable skill progression instead of dangerous trial-and-error YouTube attempts.

The agent begins with a 2-minute intake questionnaire to tailor everything to your exact space, power supply, budget, and first project.

## Agent Role vs Human Role

**Agent responsibilities** (all planning, research, bureaucracy, tracking):
- Run intake and generate personalized equipment list, material shopping plan, and 30-day practice calendar.
- Research current local/used welder prices, safety gear, and consumables; draft emails or marketplace queries.
- Create daily practice plans, safety checklists, and project blueprints with cut lists and sequences.
- Maintain filesystem-based progress log (`welding-log.md`) with photos descriptions, bead quality notes, and hours tracked.
- Send timed reminders for practice sessions and equipment maintenance.
- Analyze logs and adjust difficulty or recommend technique corrections.
- Draft supplier communications, permit checklists (if required locally), or escalation notes to mentors.
- Research updates from AWS (American Welding Society) or OSHA only when explicitly commanded.

**Human responsibilities** (all physical, embodied work):
- Acquire or borrow the recommended welder and safety gear.
- Perform every weld, grind, and practice bead with full attention to feel, sound, and puddle control.
- Provide honest post-session feedback (photos described verbally, what felt off, heat control issues).
- Execute the actual project fabrication once the agent has sequenced the steps.
- Store and maintain equipment safely.

The symbiosis is explicit: agent removes every non-physical barrier; you supply the hands-on craft that no AI can replicate.

## Step-by-Step Protocol

### Phase 1: Setup & Safety (Days 1–3)
Goal: Safe workspace and gear ready in under 72 hours.

1. **Agent runs intake** — asks about available power (110V/220V), workspace ventilation, budget ceiling, and first target project.
2. **Agent generates and ranks 3 equipment packages** (entry-level MIG vs stick welder, helmet, gloves, jacket, grinder, clamps, safety glasses, fire extinguisher). Includes used-market search terms and exact model recommendations based on real 2026 pricing.
3. **Human acquires gear** while agent prepares safety checklist.
4. **Day 3 safety walkthrough** — agent walks you through a 10-point pre-weld checklist (ground clamp placement, ventilation, no flammable materials within 10 ft, leather apron, closed-toe boots). Human performs dry-run setup.

Agent creates `welding-safety-checklist.md` and requires a “checked” confirmation before any arc is struck.

### Phase 2: Foundational Beads & Machine Familiarity (Days 4–10)
Goal: Consistent, defect-free beads on scrap metal.

- Daily 20–40 minute sessions (agent reminds at your chosen time).
- Technique progression:
  - Stringer beads (flat position) → weave beads → vertical up/down → overhead (only after flat mastery).
  - Machine settings: agent provides exact voltage/wire-speed charts tailored to your welder model and metal thickness.
- Human welds 10–15 beads per session on 1/8"–1/4" mild steel scrap; describes puddle behavior and any undercut or porosity.
- Agent logs each session (date, position, settings, self-rated quality 1–10, notes) and suggests micro-adjustments (“increase travel speed 10% next session”).

By day 10 you will produce beads that pass a visual and bend test (agent describes exact test procedure).

### Phase 3: Simple Projects & Joints (Days 11–21)
Agent selects your first real project from your intake (e.g., trailer hitch reinforcement, gate latch, workbench bracket) and breaks it into sequenced steps.

- **Project blueprint generation**: cut list, fit-up order, tack-weld plan, final weld sequence, post-weld cleanup.
- Daily practice + project time split (agent tracks total arc time).
- Technique focus: fillet welds, lap joints, butt joints, corner joints. Agent supplies AWS-recommended travel angles and work angles with verbal cues you repeat aloud.
- Human performs every tack and final pass; agent prompts for inter-pass cleaning and temperature checks (using color or temp sticks if you have them).

Agent maintains a running project status in the log file.

### Phase 4: Maintenance, Advanced Repairs & Iteration (Day 22+)
- Weekly preventive maintenance schedule for welder (agent generates).
- New project intake loop: whenever you need something fabricated, agent repeats the blueprint process.
- Skill maintenance: one 20-minute bead session per week to prevent regression.
- Agent archives successful project files for reuse (“template: heavy-duty bracket v1”).

## Decision Trees

**Welder type selection (agent runs once at intake)**  
- Thin sheet metal (<1/8") or auto body → MIG  
- Thick structural steel, field repairs, or no gas available → Stick (SMAW)  
- Budget under $300 and occasional use → Used 110V MIG  
- Frequent heavy use → 220V MIG or multi-process

**During practice**  
- Porosity or spatter? → Check gas flow / clean metal / adjust voltage down 1–2 points  
- Undercut? → Slow travel speed or reduce amperage  
- Electrode sticking (stick welder)? → Increase amperage or shorten arc length  
- If burn-through on thin metal? → Switch to smaller wire / lower settings or back-step technique

**Project troubleshooting**  
- Warpage occurring? → Clamp heavily, weld in short segments, alternate sides  
- Cannot achieve 100% penetration? → Grind root pass and back-gouge before capping  
- If safety red flag (e.g., frayed cables, no ventilation) → Agent halts protocol and drafts “Do not weld until resolved” message

## Ready-to-Use Templates & Scripts

**Agent Intake Questionnaire**  
1. What is your first project and why?  
2. Available power outlet type and amperage?  
3. Workspace size and ventilation (indoor garage, outdoor, etc.)?  
4. Budget for starter gear?  
5. Any prior welding experience (even if zero)?

**Shopping List Template (agent populates)**  
- Welder: [model] – current used price on marketplace  
- Safety: auto-darkening helmet (shade 9–13), leather gloves, jacket  
- Consumables: 0.030" wire, 75/25 gas or flux-core, 1/8" 7018 rods  
- Tools: angle grinder, C-clamps, wire brush, slag hammer

**Sourcing Email Draft**  
Subject: Looking for used MIG welder in [your city]  
Body: Hi, I’m a tradesperson building self-reliance skills. Seeking a working 110V or 220V MIG welder under $[budget]. Happy to pick up today. Thanks!

**Daily Practice Reminder Script**  
“Session 3 of 30. Today: 15 vertical-up beads on 3/16" scrap. Safety checklist complete? Set welder to [exact settings]. Begin when ready.”

**Progress Log Entry Format (agent maintains)**  
Date | Session | Position | Settings | Quality (1-10) | Notes | Arc Time

**Project Completion Sign-Off**  
Agent asks: “Photo description of finished weld? Any distortion? Functional test result?” Then archives as template.

## Success Metrics

- **Week 1**: Workspace set up and first 50 defect-free beads logged.
- **Week 3**: Completed one functional project that replaces a purchased part (verified by user).
- **Week 8**: Able to diagnose and repair a broken piece of equipment in under 2 hours with agent guidance.
- **Ongoing**: Average bead quality rating ≥8/10; total arc time >20 hours; at least 3 independent projects completed without external help.

Agent generates weekly summary report with metrics and next-project recommendations.

## Maintenance / Iteration

- Monthly equipment maintenance checklist (agent generates).
- Quarterly skill refresh: return to bead practice for one week if projects slow down.
- Agent can re-run full protocol for new processes (TIG if you upgrade welder) or advanced certifications if you request research.

## Rules / Safety Notes

- Never weld without full PPE and proper ventilation — fumes can be lethal.
- Keep a charged fire extinguisher rated ABC within arm’s reach.
- Ground clamp must be clean and within 12" of weld zone.
- Do not weld on pressurized containers, painted surfaces (lead fumes), or galvanized steel without proper prep and respirator.
- If you feel dizzy, nauseous, or see arc flash symptoms, stop immediately and seek fresh air.
- Children and pets must be kept out of the work area.
- Comply with all local fire codes and burn permits if outdoors.

This protocol follows OSHA 1910.252 and AWS D1.1 entry-level guidelines. Agent will flag any deviation.

## Disclaimer

Welding involves high heat, electricity, UV radiation, and toxic fumes. Improper use can cause severe burns, eye damage, respiratory illness, or fire. This skill provides structured guidance based on publicly available industry standards and should supplement, not replace, hands-on training from a qualified instructor or apprenticeship program. Always follow manufacturer safety instructions for your specific equipment. Consult local regulations and a licensed professional for any structural or code-compliant work. The agent assists with planning and tracking but cannot physically weld or guarantee outcomes. Use at your own risk and prioritize safety above all else.

Start the intake now. In two weeks you will be turning scrap into solutions — the ultimate post-AI self-reliance upgrade.