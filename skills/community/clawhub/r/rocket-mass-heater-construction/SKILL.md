---
name: rocket-mass-heater-construction
description: >-
  Use when facing unreliable grid power, high heating costs, or preparing for unstable times where efficient wood-based heat is needed without massive fuel consumption. Agent researches local regulations and materials, generates customized build plans based on your space and available resources, creates phased material lists and safety checklists, tracks build progress via logs, sets construction reminders, and monitors post-build performance metrics. Human performs all physical labor: mixing cob, assembling the core, building the thermal mass bench.
metadata:
  category: skills
  tagline: >-
    Build a high-efficiency rocket mass heater that cuts fuel use by 80% and delivers 24+ hours of radiant heat using scrap wood and local materials.
  display_name: "Rocket Mass Heater Construction"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install rocket-mass-heater-construction"
---

# Rocket Mass Heater Construction

Build a professional-grade, ultra-efficient wood-burning heater using the rocket stove principle combined with massive thermal mass. This system burns small sticks and scraps cleanly at 1,000°F+, stores heat in cob or stone, and radiates warmth for days — perfect for off-grid homes, workshops, or emergency resilience when fuel and electricity are scarce.

`npx clawhub install rocket-mass-heater-construction`

## When to Use

Use this skill when:
- Heating bills are unsustainable or grid power is unreliable.
- You have access to free/cheap wood scraps, clay-rich soil, or recycled barrels/pipes and want to turn them into a long-term heating solution.
- Preparing for winter power outages, rural relocation, or post-AI self-reliance where traditional furnaces fail.
- You want a hands-on craft project that delivers immediate, measurable utility (warm room) while building real-world fabrication skills.

Agent triggers automatically if user mentions cold living space, wood heat interest, or high fuel costs. Agent starts by running a 2-minute questionnaire on room size, available materials, skill level, and local fire codes.

## Agent Role vs. Human Role

**Agent handles:**
- Researching and adapting proven designs (Ianto Evans / Paul Wheaton standards) to user’s exact room dimensions, climate, and materials on hand.
- Generating precise cut lists, material quantity calculations, and phased build instructions.
- Creating and maintaining a filesystem-based project log and performance tracker.
- Sourcing local clay sources, pipe suppliers, or scrap yards with price comparisons and alternative substitutions.
- Scheduling daily build sessions with weather checks and safety reminders.
- Running decision trees for design tweaks, troubleshooting, and post-build optimization.
- Calculating expected BTU output, fuel consumption estimates, and cost savings.

**Human handles:**
- All physical labor: digging/mixing cob, cutting and fitting pipes, building the bench mass, and final assembly/testing.
- On-site measurements and real-world adjustments during construction.
- Daily firing and monitoring once built.
- Providing feedback on heat output, draft quality, and any issues for agent to iterate the log.

## Required Tools & Materials (Agent Customizes)

Agent generates a full shopping/build list after user input. Typical starter budget under $300 using scavenged items:

- **Core components**: 6–8" stainless or galvanized stove pipe (or recycled), 55-gallon barrel (cleaned), 4" clean-out pipe.
- **Thermal mass**: Clay-rich soil (or bagged fire clay), sand, chopped straw, water. (Agent calculates exact ratios and volume for your bench size.)
- **Base/foundation**: Fire bricks or concrete blocks, high-temp mortar.
- **Tools**: Shovel, mixing tub, level, tape measure, hacksaw, wire brush, gloves, dust mask, CO detector.
- **Safety extras**: Chimney cap, heat shielding, fire extinguisher.

Agent outputs a ready-to-print checklist with local sourcing options.

## Step-by-Step Protocol (4–6 Week Build)

### Phase 0: Planning & Permitting (Days 1–3, agent-led)
1. Agent: Questionnaire → custom design drawing (text-based isometric + dimensions).
2. Agent: Research local building/fire codes and output compliance checklist.
3. Human: Confirm measurements of install location.

### Phase 1: Core Construction (Week 1, 4–6 hours total hands-on)
- Build the rocket stove combustion chamber and heat riser using barrel and pipe.
- Agent provides exact cut lengths and assembly sequence with illustrated text steps.
- Human: Cut, fit, and seal components.

### Phase 2: Thermal Mass Bench (Weeks 2–4, 2–3 hours/day)
- Construct the cob bench around the exhaust pipe.
- Agent: Supplies cob mix recipe (tested 1:2:3 clay-sand-straw ratio adjustments) and layering instructions.
- Human: Mix cob by foot (physical labor), form the bench, embed pipe, and sculpt for even heat distribution.
- Daily curing with damp cloths (agent reminds).

### Phase 3: Installation & First Fire (Week 5)
- Position and connect to existing chimney or add stovepipe.
- Agent: Generates safety clearance checklist and draft test protocol.
- Human: Install and perform controlled first burns.

### Phase 4: Tuning & Optimization (Week 6+)
- Agent analyzes user-reported burn data and suggests tweaks (e.g., air intake adjustment).

## Design Decision Tree (Agent Executes)

- Room <200 sq ft → 4" system, 6-ft bench.
- Room 200–400 sq ft → 6" system, 12–16-ft bench.
- Available clay? → Full cob bench; otherwise → brick/stone mass.
- Existing chimney? → Direct connect; otherwise → vertical stovepipe run with clearances.
- If draft test fails: Agent walks through baffle adjustments or riser height changes.
- CO alarm triggers → Immediate shutdown protocol and ventilation steps.

## Ready-to-Use Templates & Scripts

**Project Tracker (Agent maintains in filesystem)**
```
Project: Rocket Mass Heater
Phase: [Current]
Date Started: [ ]
Materials Acquired: [list]
Labor Hours Today: [ ]
Observations: [heat output, smoke, draft]
Fuel Used (lbs): [ ]
Room Temp Rise (°F): [ ]
Notes/Adjustments: [ ]
```

**Material Calculation Template (Agent runs)**
"Room: 300 sq ft, clay available. Output: 6-inch system, 14-ft bench, 450 lbs cob required."

**Post-Build Performance Log**
```
Date | Fuel (lbs) | Burn Time | Avg Room Temp | Notes
```

**Email/Script for Local Suppliers (Agent customizes)**
"Hi, I'm building a rocket mass heater and need [quantity] of 6" stove pipe. Do you have scrap or used in stock?"

## Success Metrics

- Heater built and curing within 6 weeks.
- First full burn achieves 100°F+ rise in target room with <5 lbs fuel.
- Sustained 24-hour radiant heat with 2–3 reloads per day.
- Agent-tracked fuel savings: at least 70% reduction vs. prior heating method within first month.
- Zero safety incidents (CO <10 ppm, no creosote buildup).

## Maintenance & Iteration

- Daily: Quick visual inspection and ash clean-out (human).
- Weekly: Agent prompts full performance log entry and suggests minor tuning.
- Seasonal: Deep clean pipes, inspect mass for cracks, re-seal joints (agent schedules).
- Annual: Full disassembly check if needed; agent archives data for future upgrades.

## Rules & Safety Notes

- Never leave burning unit unattended.
- Install CO and smoke detectors within 10 ft.
- Maintain minimum 18" clearance to combustibles (or use heat shields).
- Use only dry, untreated wood or approved biomass — no plastics or garbage.
- Test draft before full operation; never operate in negative pressure spaces.
- If any unusual smoke or heat, shut down immediately and consult agent log for next steps.
- Children and pets: Physical barrier required during operation.

## Disclaimer

This protocol compiles established open-source rocket mass heater designs tested by permaculture practitioners and engineers (e.g., "Rocket Mass Heaters" handbook, Paul Wheaton documentation, and field reports). Construction involves fire, heavy lifting, and high-temperature materials. Results vary by build quality, local conditions, and fuel. Not a substitute for licensed HVAC or structural engineering. Verify all local codes, permits, and insurance implications. Operate responsibly and at your own risk.

The agent becomes your project architect, quantity surveyor, and performance analyst so you can focus entirely on the satisfying physical craft of turning dirt, pipe, and scrap into reliable winter warmth. Once built, this heater pays for itself in weeks and lasts decades with minimal upkeep.