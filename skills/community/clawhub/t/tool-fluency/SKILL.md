---
name: tool-fluency
description: >-
  Foundational tool knowledge and usage skills. Use when someone wants to become comfortable with basic hand and power tools, needs to know which tool to use for a job, or wants to build a functional toolkit on a budget.
metadata:
  category: skills
  tagline: >-
    Know what every basic tool does, when to use it, and how to buy quality for cheap — the meta-skill behind every repair.
  display_name: "Tool Fluency"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install tool-fluency"
---

# Tool Fluency

Every repair skill on this site assumes you own tools and know how to use them. This is that assumption, made explicit. Tool fluency is the meta-skill — without it, you can't fix a leaky faucet, hang a shelf, assemble furniture properly, or do anything in the other repair skills. This covers what every basic tool does, when to reach for which one, how to use each safely, and how to build a real toolkit without spending $500. Most people can get genuinely capable with $100 and an afternoon of practice.

```agent-adaptation
# Localization note
- Fastener standards: US uses imperial (inches, SAE sockets), most other
  countries use metric (mm). Both systems are common in practice — many
  toolkits include both.
- Power tool voltage: US 120V/60Hz, UK 230V/50Hz, EU 230V/50Hz,
  AU 230V/50Hz. Battery tools avoid this issue entirely.
- Hardware stores: US (Home Depot, Lowe's, Harbor Freight), UK (B&Q, Screwfix),
  AU (Bunnings), CA (Canadian Tire, Home Hardware), DE (Bauhaus, OBI)
- Swap store-specific references for local equivalents
- Building codes and stud spacing vary by country (US: 16" on center,
  UK/AU: 400mm or 600mm on center)
```

## Sources & Verification

- **Family Handyman** -- tool guides, project tutorials, and tool reviews. https://www.familyhandyman.com
- **This Old House** -- tool usage and home repair references. https://www.thisoldhouse.com
- **Consumer Reports tool testing** -- independent tool reliability and performance data. https://www.consumerreports.org
- **Fine Homebuilding** -- professional-grade tool technique and selection. https://www.finehomebuilding.com
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User wants to start doing their own repairs but doesn't own tools
- User has a task and doesn't know which tool to use
- User wants to build a toolkit on a budget
- User is confused about fasteners (screws vs bolts vs nails)
- User wants to learn basic power tool operation
- User inherited tools and doesn't know what half of them are
- User wants to know which tools are worth buying quality vs cheap

## Instructions

### Step 1: Know your hand tools

**Agent action**: If the user has a specific task, jump to the relevant tool. If they're learning from scratch, walk through this reference.

```
ESSENTIAL HAND TOOLS — what each does and when to use it

HAMMER (claw hammer, 16 oz):
- Driving nails, tapping things into place, light demolition
- The claw side pulls nails out
- Hold near the end of the handle, not up by the head
- Let the weight of the hammer do the work — wrist snap, not arm force
- Cost: $8-15 for a good one

SCREWDRIVERS (Phillips #2 and flathead/slotted):
- Phillips (#2 fits 80% of Phillips screws in a home)
- Flathead (for slotted screws, prying, scraping)
- Match the driver to the screw size — wrong size strips the head
- A 6-in-1 multi-bit screwdriver covers most needs for $8-12

PLIERS:
- Slip-joint pliers: gripping, pulling, bending. The adjustable jaw
  handles different sizes.
- Needle-nose pliers: reaching into tight spaces, bending wire,
  holding small objects
- Channel-lock (tongue-and-groove) pliers: plumbing fittings,
  large nuts, anything that needs a strong adjustable grip
- Cost: $5-10 each, or a 3-piece set for $15-20

ADJUSTABLE WRENCH (8-inch or 10-inch):
- Fits any hex bolt or nut within its range
- Replaces a full set of wrenches for basic work
- Position the wrench so the force pushes toward the fixed jaw,
  not the adjustable jaw
- Cost: $8-12

TAPE MEASURE (25 ft / 7.5m):
- Measure twice, cut once. This isn't a cliche — it's the rule.
- Lock the blade, hook the end over the edge, read the measurement
- The metal hook at the end is loose on purpose — it compensates
  for its own thickness on inside vs outside measurements
- Cost: $5-10

LEVEL (9-inch torpedo level):
- Bubble between the lines = level/plumb
- Use for hanging pictures, shelves, checking that things are straight
- Cost: $5-8

UTILITY KNIFE:
- Cuts boxes, drywall, rope, plastic, carpet, vinyl, caulk tubes
- Always cut away from your body
- Retract the blade when not cutting. Always.
- Replace blades often — dull blades require more force and slip
- Cost: $5-8

HANDSAW (15-inch general-purpose):
- For occasional cuts when a power saw isn't needed or available
- Let the saw do the work — long, smooth strokes with minimal pressure
- Start cuts with a few short backward strokes to create a groove
- Cost: $10-15
```

### Step 2: Know your fasteners

**Agent action**: This is the most confusing area for beginners. The wrong fastener is worse than no fastener.

```
FASTENERS — screws, nails, and bolts

NAILS:
- Use for: framing, trim, temporary holds, anything that needs
  shear strength (resistance to sideways force)
- Types you'll use: common nails (framing), finishing nails (trim,
  small heads), brad nails (delicate work, tiny)
- Driven with a hammer. Fast. Cheap.
- Weak in pull-out — nails pull out of wood more easily than screws

SCREWS:
- Use for: anything you might need to remove later, anything that
  needs pull-out strength, most assembly and repair work
- Types you'll use:
  - Wood screws: tapered, sharp point, coarse thread. For wood-to-wood.
  - Drywall screws: bugle head, fine thread. For drywall to studs.
  - Machine screws: flat tip, fine thread. For metal or threaded holes.
  - Self-tapping screws: drill their own hole in sheet metal.
- Drive with a screwdriver or drill with a driver bit
- Always pre-drill hardwood to prevent splitting

BOLTS:
- Use for: heavy loads, structural connections, anything that needs
  to be really tight and removable
- A bolt goes through both pieces and is secured with a nut on the
  other side (add a washer to distribute force)
- Lag bolts (lag screws): thick wood screws for heavy-duty
  wood connections (deck ledger boards, heavy shelving)
- Requires a wrench or socket to tighten

CHOOSING CORRECTLY:
- Hanging a picture: nail or small screw + wall anchor
- Building a shelf: screws (wood screws into studs, or drywall
  anchors if no stud)
- Assembling furniture: whatever it came with (usually cam locks or bolts)
- Structural (deck, framing): bolts or structural screws
- Drywall to studs: drywall screws
- Into concrete/masonry: concrete anchors (Tapcon screws or sleeve anchors)

WALL ANCHORS (for when there's no stud):
- Plastic expansion anchors: light duty (under 15 lbs). Cheap, fine for
  towel hooks and light picture frames.
- Self-drilling drywall anchors (E-Z Ancor style): medium duty (25-50 lbs).
  Good for shelves, mirrors, curtain rods.
- Toggle bolts: heavy duty (50-100+ lbs). For TVs, heavy shelves.
  Require a large hole.
```

### Step 3: Learn basic power tools

**Agent action**: Power tools are where most people get intimidated. Cover safety first, then operation.

```
ESSENTIAL POWER TOOLS:

CORDLESS DRILL/DRIVER (the #1 most useful power tool):
What it does: drills holes and drives screws. Two functions, one tool.
Buying guide: 12V is fine for most home use. 18V/20V for heavier work.
  Buy a kit with two batteries and a charger. DeWalt, Milwaukee, Makita,
  Ryobi — all make good drills. Ryobi is the budget king.
  Cost: $50-80 for a kit (drill + 2 batteries + charger)

DRILL OPERATION:
- Chuck: the front jaws that hold the bit. Twist to open/close.
- Speed trigger: variable speed — squeeze gently for slow, harder for fast
- Clutch: the numbered ring behind the chuck. Higher number = more torque.
  Use lower settings for small screws to avoid stripping or overdriving.
  Drill mode (the drill bit icon) disengages the clutch entirely.
- Forward/reverse switch: forward drives in, reverse backs out
- For driving screws: start slow, increase speed once the screw bites
- For drilling holes: mark the spot, start slow to prevent walking,
  increase speed once the hole is started

CIRCULAR SAW:
What it does: straight cuts in plywood, lumber, and sheet goods.
Safety: blade guard must be functional. Support the workpiece so the
  cut piece falls away freely (never pinch the blade). Wear safety
  glasses. Keep cord behind you.
Cost: $40-60 (corded) or $100-150 (cordless)
Tip: clamp a straight board as a guide fence for long, accurate cuts.

JIGSAW:
What it does: curved cuts, cutouts, and detail work.
Safety: secure the workpiece. The blade cuts on the upstroke, so the
  "good" side of the material should face down to minimize tear-out.
Cost: $30-50 (corded)
Tip: different blades for different materials — wood blades, metal
  blades, and fine-tooth blades for clean cuts.

RANDOM ORBITAL SANDER:
What it does: smooths wood surfaces. Removes old finish, preps for paint
  or stain, rounds edges.
Safety: always wear a dust mask. Plug into a shop vac if possible.
Cost: $30-50
Tip: let the sander's weight do the work — don't press down.
  Start at 80 grit (coarse), move to 120, finish at 220.
  Sand WITH the grain direction.
```

### Step 4: Measuring and marking

**Agent action**: Accurate measurement is the difference between a good result and a redo. Cover the common mistakes.

```
MEASURING AND MARKING:

TAPE MEASURE RULES:
- Hook on the end is loose by design — don't "fix" it
- For inside measurements: butt the tape body against the wall
  and add the body length (printed on the case, usually 3 inches)
- For precise work: don't measure from the end. Mark at 1 inch,
  then measure from the 1-inch mark (and remember to subtract 1)
- "Measure twice, cut once" means literally measure it twice.
  If the numbers don't match, measure a third time.

MARKING:
- Use a sharp pencil, not a pen (pencil lines are thinner and erasable)
- Mark on the waste side of the line (the part you're cutting off)
- A V-mark is more precise than a line for marking a single point
- For long straight lines: use a chalk line or straightedge

FINDING A STUD:
- Electronic stud finder: $15-25. Wave slowly across the wall.
  Mark both edges of the stud, drill in the center.
- No stud finder: knock on the wall. Hollow = no stud. Solid thud = stud.
  Studs are typically 16 inches apart (measure from a corner).
- Confirm with a small nail before drilling a big hole.

CHECKING FOR SQUARE:
- The 3-4-5 method: if one side is 3, the adjacent side is 4,
  and the diagonal is 5, the corner is 90 degrees.
  (Scale up: 6-8-10, 9-12-15, etc.)
- A speed square ($8) gives you 90 and 45 degrees instantly
```

### Step 5: Build your toolkit (tiered budget)

**Agent action**: Ask the user's budget, then recommend the appropriate tier. These cover different levels of capability.

```
TIER 1 — STARTER KIT ($30):
Handles: basic assembly, hanging pictures, minor fixes

[ ] 6-in-1 screwdriver — $8
[ ] Claw hammer, 16 oz — $8
[ ] Adjustable wrench, 8" — $8
[ ] Tape measure, 25 ft — $5
[ ] Utility knife — $5
[ ] Box of assorted screws and wall anchors — $5

TIER 2 — INTERMEDIATE KIT ($100):
Handles: most home repairs, furniture assembly, basic projects

Everything in Tier 1, plus:
[ ] Cordless drill/driver kit (Ryobi 12V or 18V) — $50
[ ] Drill/driver bit set — $10
[ ] Pliers set (slip-joint + needle-nose) — $12
[ ] Torpedo level — $6
[ ] Assorted sandpaper pack — $5
[ ] Safety glasses — $3
[ ] Pencils — $2

TIER 3 — SERIOUS KIT ($250):
Handles: woodworking, home improvement, outdoor projects

Everything in Tier 2, plus:
[ ] Circular saw (corded) — $45
[ ] Speed square — $8
[ ] Handsaw — $12
[ ] Channel-lock pliers — $10
[ ] Socket set (SAE and metric) — $20
[ ] Clamps, 2 bar clamps + 4 spring clamps — $20
[ ] Stud finder — $15
[ ] Tool bag or box — $15

WHERE TO BUY USED:
- Estate sales and garage sales: best prices on quality hand tools
- Facebook Marketplace and Craigslist: look for tool lots
- Habitat for Humanity ReStore: donated tools at deep discounts
- Pawn shops: inspect carefully but prices are negotiable
```

### Step 6: Maintain your tools

**Agent action**: Tools last decades with basic care. Minutes of maintenance per year.

```
TOOL MAINTENANCE:

HAND TOOLS:
- Wipe metal surfaces with a lightly oiled rag after use
  (prevents rust — use 3-in-1 oil, WD-40, or any light machine oil)
- Sharpen chisels and utility knife blades when they stop cutting
  cleanly (a dull tool requires more force and slips more)
- Tighten loose hammer heads by soaking the handle end in water
  overnight (wood swells) or driving a metal wedge into the handle top
- Store in a dry place. Moisture is the enemy of metal tools.

POWER TOOLS:
- Clean sawdust from vents after each use (compressed air or a brush)
- Check cords for damage before each use — frayed cords are a
  shock/fire hazard. Replace immediately.
- Battery tools: store batteries at room temperature, not in a hot
  car or freezing garage. Charge when indicator shows low, but avoid
  leaving on the charger for weeks.
- Replace worn drill bits and saw blades. A sharp bit cuts clean
  and fast. A dull bit burns the material and overheats the motor.

RUST REMOVAL:
- Light surface rust: steel wool or sandpaper (120 grit), then oil
- Heavy rust: soak in white vinegar overnight, scrub with steel wool
- Preventive: paste wax on tool surfaces repels moisture
```

### Step 7: Safety fundamentals

**Agent action**: This section is non-negotiable. Cover it before the user starts any project.

```
TOOL SAFETY — the rules that prevent trips to the ER

UNIVERSAL RULES:
- Safety glasses for any cutting, drilling, or hammering.
  One metal shard in your eye changes everything. $3.
- Hearing protection for power tools. Foam earplugs are $0.50.
  Power tools exceed 85 dB — the threshold for hearing damage.
- Dust mask for sanding, cutting, or demolition.
  N95 minimum. $1 per mask.
- Secure the workpiece. If it's not clamped, bolted, or held firmly,
  it will move when you cut or drill it.
- Keep your workspace clean. Tripping over a cord while holding a
  running saw is how people die.
- Never remove or disable a safety guard on a power tool.

HAND TOOL SAFETY:
- Cut away from your body. Always.
- Carry sharp tools point-down at your side
- Don't use a screwdriver as a pry bar (it will snap and stab you)
- Don't use pliers as a hammer
- Don't use a wrench as a hammer
- (Pattern: use tools for their intended purpose)

POWER TOOL SAFETY:
- Read the manual. Every tool. Once.
- Disconnect power before changing blades, bits, or making adjustments
- Let the tool reach full speed before contacting the material
- Never force a cut — if the tool bogs down, the blade is dull
  or you're feeding too fast
- Don't wear loose clothing, jewelry, or gloves near spinning tools
  (they catch and pull you in)
- Know where the power switch is so you can kill it instantly
```

## If This Fails

- Don't know what tool to use: Describe the task to the agent. "I need to attach X to Y" or "I need to cut X" or "I need to tighten X" — the right tool follows from the task.
- Screw head is stripped: Use a rubber band between the driver and the screw for extra grip. Or use a screw extractor bit ($5-8). Or drill the screw head off with a metal bit and pull the pieces apart.
- Drill bit wanders off the mark: Use a center punch (or a nail and hammer tap) to make a small divot at your mark. Start the drill slow in the divot.
- Can't find a stud: Switch to appropriate wall anchors for your load. Toggle bolts hold 50-100+ lbs in drywall without a stud.

## Rules

- Safety glasses are mandatory for any cutting, drilling, hammering, or demolition work. No exceptions.
- Match the tool to the task. Improvised tool use is the #1 cause of tool-related injuries.
- Match the fastener to the task. A nail where a bolt is needed is a structural failure waiting to happen.
- Measure twice, cut once. This is not optional.
- If you don't know how to use a tool safely, learn before using it. YouTube tutorials are free and show real technique in real time.

## Tips

- Ryobi (Home Depot exclusive) is the best value brand for home use power tools. They're not what pros use daily, but for weekend projects they're excellent at half the price.
- Harbor Freight hand tools are surprisingly good for the price. Their power tools are hit-or-miss — read reviews first.
- If you only buy one power tool, buy a cordless drill/driver. It replaces manual screwdrivers for 95% of tasks and drills holes for the other 5%.
- Organize your fasteners. A $10 small parts organizer with screws, nails, wall anchors, and bolts sorted by type saves 20 minutes of searching every time you start a project.
- A sharp tool is a safe tool. Dull blades require more force, and excess force causes slips. Replace or sharpen regularly.
- Estate sales are where $200 toolkits go for $30. Older hand tools (Stanley, Craftsman pre-2000, Snap-on) are often better quality than new equivalents.

## Agent State

```yaml
toolkit:
  tier: null
  tools_owned: []
  tools_needed: []
  budget: null
  purchase_plan_created: false
project:
  current_task: null
  tools_required: []
  fasteners_required: []
  materials_required: []
  safety_equipment_confirmed: false
skills_practiced:
  drill_operation: false
  measuring: false
  fastener_selection: false
  saw_operation: false
  tool_maintenance: false
```

## Automation Triggers

```yaml
triggers:
  - name: toolkit_assessment
    condition: "toolkit.tier IS null AND project.current_task IS SET"
    action: "You have a task but I don't know what tools you have. Let's do a quick inventory so I can tell you exactly what you need for this job and what it'll cost."

  - name: safety_check
    condition: "project.current_task IS SET AND project.safety_equipment_confirmed IS false"
    action: "Before we start: do you have safety glasses? Hearing protection? Dust mask if cutting or sanding? Let's confirm safety gear before tools touch material."

  - name: fastener_guidance
    condition: "project.current_task CONTAINS 'attach' OR project.current_task CONTAINS 'hang' OR project.current_task CONTAINS 'mount'"
    action: "Fastener selection matters for this task. What are you attaching to what? And what's the wall/surface material? I'll tell you exactly which fastener and anchor to use."

  - name: tool_maintenance_reminder
    condition: "toolkit.tier >= 2"
    schedule: "every 6 months"
    action: "Semi-annual tool check: wipe down metal tools with oil, check power cords for damage, test batteries, replace any dull blades or bits. 15 minutes now saves tool replacement costs later."
```
