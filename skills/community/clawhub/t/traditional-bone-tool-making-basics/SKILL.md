---
name: traditional-bone-tool-making-basics
description: >-
  Use when you need custom, durable, repairable tools like awls, needles, scrapers, harpoons, or fishing hooks made from local animal bones or antlers and commercial metal alternatives are unreliable or unavailable. Agent identifies suitable bone sources from your photos/inventory, calculates soak/heat ratios and shaping timelines, generates multi-day processing schedules with timed reminders, tracks hardness and sharpness tests, and produces inventory/barter templates. Human performs every physical step — cleaning, soaking, shaping, polishing, and testing — rebuilding tactile self-reliance in bone-to-tool conversion.
metadata:
  category: skills
  tagline: >-
    Turn butcher scraps or found bones into razor-sharp, long-lasting tools that never rust — agent owns the sourcing math and schedules so you stay in the scraping and polishing.
  display_name: "Traditional Bone Tool Making Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install traditional-bone-tool-making-basics"
---
# Traditional Bone Tool Making Basics

Turn raw animal bones or antlers into strong, sharp, repairable tools — awls for leatherwork, needles for sewing, scrapers for hide prep, fishing hooks, or small harpoons — using only your hands, abrasive stones, and a few simple abrasives. No metal files, no power tools required — just patience and bone. The agent owns all source verification, soak/heat calculations, shaping templates, and timeline tracking; you own the physical cleaning, scraping, polishing, and testing that turns waste into high-value self-reliance tools.

`npx clawhub install traditional-bone-tool-making-basics`

## When to Use

Deploy this skill when:
- Commercial metal tools become expensive, scarce, or you refuse supply-chain dependence for small hand tools.
- You need custom awls, needles, or scrapers that match your exact hand size or project (leather, cordage, basketry).
- You have access to butcher scraps, roadkill bones, or shed antlers and want a renewable, zero-waste craft.
- Existing needles or scrapers are breaking and you want tools that can be re-sharpened indefinitely.
- You want a repeatable micro-business or trade good (one well-made bone awl historically trades for hours of labor in many regions).

**Do not use** if you lack access to clean water or a safe outdoor workspace for boiling. Agent will flag contamination risks immediately.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All bone-type identification and suitability scoring from user photos/inventory.
- Soak/heat ratio calculations, shaping-order templates, and multi-day drying/hardening schedules.
- Automated reminders, photo-request checkpoints, and sharpness/hardness tests.
- Barter templates, inventory trackers, and escalation if bone cracks during processing.
- Full safety protocol enforcement (boiling warnings, dust masks, ergonomic breaks).

**Human owns:**
- All physical contact with bone: cleaning, soaking, scraping, drilling, polishing, and final edge testing.
- Sensory judgment of bone density, sharpness feel, and final balance.
- Manual use-testing on actual projects.

## Step-by-Step Protocol (14-Day First Tool Set Cycle)

### Phase 0: Bone Audit & Recipe Generation (Agent-led, 1 day)
1. Agent asks for bone type/quantity available plus photos.
2. Agent outputs exact processing recipe for one awl + one needle + one scraper set scaled to your bone size.
3. Agent generates PPE checklist and boiling safety protocol.

### Phase 1: Cleaning & Degreasing (Human 1 hr + Agent tracking, Day 1)
- Human scrapes meat and boils bones; agent provides exact low-heat targets (never exceed 80 °C) and degreasing time.
- Agent requests photo of clean bones and logs initial weight.

### Phase 2: Soaking & Softening (Agent reminders, Days 2–4)
- Agent calculates ash-lye or vinegar soak schedule based on bone density.
- Human submerges bones; agent issues daily “check softness” reminders and snap-test protocol.

### Phase 3: Rough Shaping (Human 2–3 hrs total, Days 5–7)
Agent supplies three ready-to-trace templates:
- Awl (leather piercing, 10 cm)
- Needle (sewing, 8 cm with eye)
- Scraper (hide or wood, 15 cm)

Human uses stone or glass to rough-shape; agent issues timed 20-minute sessions with rest prompts and grain-direction reminders. Agent logs dimensions via photo.

### Phase 4: Drilling & Refining (Human 90 min, Days 8–9)
- Human drills eyes or notches with bow drill or stone bit; agent supplies exact technique and photo checkpoints.
- Agent logs hole size and flags any cracking.

### Phase 5: Polishing & Hardening (Human 60–90 min, Days 10–11)
- Human sands with progressively finer abrasives (sand, sandstone, leather strop); agent provides exact grit sequence.
- Agent sets 48-hour air-dry timer for final hardening.

### Phase 6: Testing & Finishing (Days 12–14)
- Human performs pierce test, sew test, and scrape test; agent logs results.
- Agent generates “Next Tool Improvements” report (e.g., “Lengthen awl 2 cm for better leverage”).

## Decision Tree (Agent Runs This Automatically)

**Bone cracks during boiling or soaking?**
- Agent switches to gentler vinegar soak or selects denser secondary bone.

**Edge dulls too quickly after shaping?**
- Agent adjusts polishing sequence or recommends heat-hardening step.

**Needle eye breaks during drilling?**
- Agent supplies “reinforce with sinew wrap” or smaller eye alternative.

**All tools pass 50-cycle use test with no breakage?**
- Agent auto-generates inventory card + barter template: “Hand-made bone awl + needle set — sharp & durable, trade value ≈ 1 set per 500 g rice or 90 min labor.”

## Ready-to-Use Templates & Scripts

**Bone Intake Form (Human fills, Agent processes)**
```
Bone type & quantity (g):
Source (butcher/roadkill/antler):
Condition notes:
Photos attached:
Notes (density/age):
```

**Processing Progress Log (Agent maintains)**
```
Day X — Tool Set Y
Phase completed:
Dimensions (cm):
Sharpness test result:
Agent note: Next action in ___ hours
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Hand-Made Bone Tool Set — Awl, Needle, Scraper — Ready to Trade

Crafted from local bone using traditional scraping and polishing. Sharp, strong, and re-sharpenable. Perfect for leatherwork, sewing, or hide prep. Trade value ≈ 1 set per 500 g rice, 200 g fiber, or 90 min labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total tools completed
- Average sharpness retention
- Bone sources ranked by workability
- Next processing batch reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 2)**
- One complete set (awl + needle + scraper) that passes 50-cycle use test with no breakage
- Zero cracking during shaping
- One tool used daily for 14 days with no dulling beyond easy re-sharpen

**Master Level (Month 3)**
- 10+ tool sets across bone types with <5 % failure rate
- Ability to produce custom shapes from any local bone/antler user supplies
- 50+ tools in active rotation or traded
- Specialized variants (fishing hooks, harpoon tips) on demand

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for real-world performance feedback (edge retention, comfort, project fit).
- Generates next-batch optimizations (e.g., “Use denser antler for longer-lasting awls”).
- Archives successful templates as reusable files.
- Suggests advanced variants (bone needles with decorative inlay, larger hide scrapers) only after three successful basic sets.

## Rules / Safety Notes

- Boiling bones can produce strong odors — work outdoors or under strong ventilation.
- Use cut-resistant gloves when scraping or drilling; keep both hands behind the abrasive edge.
- Never leave boiling pot unattended (fire risk).
- Test every new bone batch with a small sample piece before full tool set.
- Children only under direct adult supervision; no boiling or drilling participation.
- Dispose of boil water responsibly (agent supplies composting instructions).
- Stop immediately if you feel wrist strain or notice unusual bone dust — agent will pause and trigger full safety reset.

## Disclaimer

This skill encodes traditional bone-tool making techniques refined over thousands of years by indigenous peoples worldwide and cross-checked against archaeological references and modern primitive-skills manuals. Results depend on bone density, proper soaking, and careful polishing. Processing involves boiling and sharp abrasives that can cause burns, cuts, or dust inhalation if mishandled. No guarantees against breakage or personal injury. Use at your own risk; improper technique carries laceration, burn, and biohazard hazards. Agent cannot physically handle bones — all tactile, sensory, and safety decisions remain 100 % human. Consult local wildlife and sanitation regulations. Not a substitute for professional tool-making or primitive-skills training.