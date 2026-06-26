---
name: woodworking-maker-basics
description: >-
  Foundational woodworking skills for practical home projects. Use when someone wants to build simple furniture, make repairs to wooden items, start woodworking as a skill/hobby, or needs to build practical items like shelves, garden beds, or workbenches.
metadata:
  category: skills
  tagline: >-
    Build a shelf, fix a chair, make a raised bed -- practical woodworking with hand tools and a $50 budget.
  display_name: "Woodworking & Maker Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install woodworking-maker-basics"
---

# Woodworking & Maker Basics

You don't need a shop full of tools or years of training to build useful things out of wood. A hand saw, a drill, a tape measure, and some screws will get you surprisingly far. This skill covers practical builds that solve real problems -- shelves that hold books, garden beds that grow food, workbenches that give you a place to work. Not fine furniture. Not artisan joinery. The kind of woodworking that saves you money and gives you something you made with your own hands.

```agent-adaptation
# Localization note
- Lumber dimensions differ: US uses nominal sizing (a "2x4" is actually 1.5" x 3.5"),
  most other countries use actual metric dimensions
- Wood species availability varies by region: pine and fir (North America), spruce
  and larch (Northern Europe), radiata pine (Australia/NZ), meranti (Southeast Asia)
- Hardware store chains: Home Depot/Lowes (US), B&Q/Wickes (UK), Bunnings (AU/NZ),
  Bauhaus/Hornbach (Germany), Canadian Tire (Canada)
- Imperial vs metric measurements (US uses inches and feet; nearly everyone else uses
  metric -- provide both or adapt to user's locale)
- Building codes and permit requirements for outdoor structures vary by municipality
- Pallet wood safety: heat-treated (HT stamp) is safe everywhere; methyl bromide
  treated (MB stamp) is toxic -- never use MB-stamped pallets
```

## Sources & Verification

- **Fine Woodworking basics series** -- foundational techniques from the leading woodworking publication. https://www.finewoodworking.com
- **This Old House project plans** -- tested beginner-friendly home project plans. https://www.thisoldhouse.com
- **Ana White free furniture plans** -- extensive library of free, beginner-friendly furniture plans with cut lists and materials. https://www.ana-white.com
- **Woodworkers Guild of America** -- video instruction and project guides. https://www.wwgoa.com
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User wants to build a specific item (shelf, garden bed, workbench, storage)
- Someone wants to learn basic woodworking but doesn't know where to start
- User needs to repair a wooden item (loose chair, broken shelf, damaged furniture)
- Someone wants to start a hobby that produces useful things
- User wants to build instead of buy to save money
- Someone has access to free wood (pallets, construction scraps) and wants to use it

## Instructions

### Step 1: Starter Tool Kit

**Agent action**: Help the user assemble the minimum tool kit needed for practical woodworking. Separate into "must have" and "nice to have."

```
STARTER TOOL KIT -- MINIMUM VIABLE WORKSHOP

MUST HAVE (~$50-80 total if buying new):
[ ] Tape measure, 16 or 25 ft ($5-10)
[ ] Combination square ($8-12) -- for marking right angles and
    checking squareness. This is the tool that makes your cuts straight.
[ ] Hand saw ($10-15) -- Japanese pull saw recommended (cuts on the pull
    stroke, easier to control, makes thinner cuts). Or a standard
    crosscut hand saw.
[ ] Cordless drill/driver ($30-60 for a basic model) -- the most
    versatile power tool you'll own. Drill holes and drive screws.
    Get a set of drill bits and a #2 Phillips bit.
[ ] Pencil (carpenter's pencil or any pencil -- you'll be marking a lot)
[ ] Safety glasses ($3-5) -- not optional. Wood splinters and sawdust
    in your eyes is a fast way to ruin a project and your vision.
[ ] Sandpaper assortment ($5-8) -- 80 grit (rough), 120 grit (medium),
    220 grit (fine). That covers everything.

NICE TO HAVE (add as budget allows):
[ ] Clamps, 2-4 bar clamps ($5-10 each) -- "you can never have enough
    clamps" is the oldest woodworking truth. Start with two 12" clamps.
[ ] Miter box + backsaw ($12-20) -- a cheap guide that gives you
    perfectly straight 90-degree and 45-degree cuts every time.
    The single best upgrade from a freehand hand saw.
[ ] Chisel set ($10-15 for a basic 3-piece) -- for cleaning up joints,
    mortises, and trimming
[ ] Level, 24" ($8-12) -- confirms things are actually level and plumb
[ ] Speed square ($5-8) -- triangular marking tool for quick angles

POWER TOOL UPGRADE (when you're ready, ~$50-100):
[ ] Circular saw -- the gateway power saw. Rip cuts, crosscuts,
    plywood breakdown. More versatile than a miter saw for a beginner.
    Get a guide rail or make a straightedge guide from plywood.
[ ] Random orbital sander ($30-50) -- saves hours of hand sanding.
    Get one when you're doing projects with large flat surfaces.

WHERE TO GET TOOLS CHEAP:
- Estate sales and garage sales (often 50-80% off retail)
- Facebook Marketplace / Craigslist (look for "shop cleanout" listings)
- Harbor Freight for basics (quality is fine for occasional use)
- Habitat for Humanity ReStore (donated tools at steep discounts)
- Borrow from neighbors (see the mutual-aid skill)
```

### Step 2: Wood Selection

**Agent action**: Teach the user about common wood types, where to get them, and what to use for what purpose.

```
WOOD SELECTION -- WHAT TO USE FOR WHAT

SOFTWOODS (cheaper, easier to work, good for most projects):
- PINE: Cheapest, most available. Great for shelves, garden beds,
  workbenches. Dents easily. Fine for painted projects.
  A standard 2x4x8' stud costs $3-6.
- CEDAR: Naturally rot-resistant. Best for outdoor projects
  (garden beds, outdoor furniture). More expensive (~$8-15 for 2x4x8').
  Smells fantastic.
- FIR/DOUGLAS FIR: Stronger than pine, takes stain well.
  Good for structural projects.

HARDWOODS (more expensive, harder to work, nicer finish):
- OAK: Strong, takes stain beautifully. Good for furniture.
  ~$5-8 per board foot.
- POPLAR: Cheapest hardwood. Easy to work. Great for painted
  furniture. ~$3-5 per board foot.
- MAPLE: Very hard, very strong. Cutting boards, workbench tops.

PLYWOOD:
- Use for large flat surfaces (tabletops, shelving, cabinet backs)
- 3/4" for structural (shelves, cabinets): $30-60 per 4x8' sheet
- 1/4" for backing and thin panels: $10-20 per sheet
- "Sanded" plywood for visible surfaces, "CDX" for hidden/structural

WHERE TO GET CHEAP/FREE WOOD:
- PALLETS: Free from warehouses, stores, and loading docks. Ask first.
  Only use pallets stamped "HT" (heat treated). Avoid "MB" (toxic).
  Pallet wood is rough but free. Good for rustic projects.
- CONSTRUCTION SITE OFFCUTS: Ask the foreman. Most are happy to have
  you haul off cutoffs rather than pay for dumpster disposal.
- HABITAT FOR HUMANITY RESTORE: Donated lumber, often cheap.
- CRAIGSLIST/MARKETPLACE "FREE" section: People giving away old
  decks, fences, furniture that can be deconstructed.
- TREE SERVICES: Fresh-cut logs can be milled into lumber if you
  know someone with a sawmill or chainsaw mill.

LUMBER SIZING (US nominal vs. actual):
  Nominal  ->  Actual
  1x4      ->  3/4" x 3-1/2"
  1x6      ->  3/4" x 5-1/2"
  2x4      ->  1-1/2" x 3-1/2"
  2x6      ->  1-1/2" x 5-1/2"
  2x8      ->  1-1/2" x 7-1/4"
  4x4      ->  3-1/2" x 3-1/2"
This matters for cut lists. Always measure the actual board.
```

### Step 3: Measuring, Marking, and Cutting

**Agent action**: Cover the fundamental techniques that determine whether a project comes out square and tight or crooked and gapped.

```
THE THREE RULES THAT DETERMINE QUALITY:

RULE 1: MEASURE TWICE, CUT ONCE.
Not a cliche. A mantra. Miscuts waste wood and money.

RULE 2: MARK WITH A KNIFE OR SHARP PENCIL.
A dull pencil line is 1/16" wide -- that adds up fast.
Use the inside edge of the line, not the center.

RULE 3: SQUARE IS EVERYTHING.
If your cuts aren't square (90 degrees), nothing fits together right.
Check with a combination square before every cut.

HOW TO MAKE A STRAIGHT CUT WITH A HAND SAW:
1. Mark your cut line all the way around the board using a
   combination square
2. Position the board so the waste side hangs off the edge of your
   work surface
3. Start the cut with a few gentle backward strokes to create a groove
4. Let the weight of the saw do the work -- don't push hard
5. Support the waste end with your free hand as you finish the cut
   (prevents the wood from splintering as the cut completes)
6. Use long, smooth strokes using the full length of the blade

HOW TO MAKE A STRAIGHT CUT WITH A MITER BOX:
1. Mark your cut line
2. Place the board in the miter box, align mark with the saw slot
3. Hold the board firmly against the far wall of the miter box
4. Cut. The box guides the saw. Result: a perfectly straight cut.
   This is the easiest way to get good cuts as a beginner.

CROSSCUTS VS RIP CUTS:
- Crosscut: cutting ACROSS the grain (shortening a board) -- most common
- Rip cut: cutting ALONG the grain (making a board narrower) -- harder
  with a hand saw, much easier with a circular saw and guide
```

### Step 4: Joining Methods

**Agent action**: Cover the practical joining methods that work for beginner projects. Skip the fancy joinery.

```
JOINING METHODS -- PRACTICAL, NOT FANCY

SCREWS (your primary joining method):
- Pre-drill holes to prevent splitting (especially near edges)
- Drill bit should be slightly thinner than the screw shaft
- For 2x4 framing: #8 or #9 screws, 2.5" to 3" long
- For 1x boards: #6 or #8 screws, 1.25" to 1.5" long
- Deck screws (coated) for outdoor projects -- resist rust
- Drive screws flush with the surface or just below

POCKET HOLES (strongest beginner joint):
- Kreg pocket hole jig (~$25-50) drills angled holes
- Insert pocket screws at an angle to create strong, hidden joints
- Perfect for: face frames, table legs, shelf supports, right-angle joints
- This single tool dramatically expands what you can build

BUTT JOINTS + SCREWS:
- Simplest joint: one board butted against another, screwed together
- Not the strongest, but fine for shelves, garden beds, basic boxes
- Add wood glue for extra strength (Titebond III for outdoor use)

WOOD GLUE:
- Titebond II (water-resistant) for indoor projects
- Titebond III (waterproof) for outdoor projects
- Apply to both surfaces, clamp for 30-60 minutes
- A properly glued joint is stronger than the wood itself
- Wipe excess glue with a damp cloth IMMEDIATELY (dried glue
  won't accept stain and looks terrible)

BRACKETS AND HARDWARE:
- L-brackets and corner braces are not cheating. They're practical.
- Use them for: shelf supports, right-angle reinforcement, table legs
- Simpson Strong-Tie makes structural brackets for serious loads

NAILS:
- Fine for trim, temporary holds, and tacking things in place
- Not as strong as screws for structural joints
- A brad nailer ($30-50) makes trim work 10x faster
```

### Step 5: Sanding and Finishing

**Agent action**: Cover the basics of making a project look finished and protected.

```
SANDING

THE GOAL: Smooth surface that's ready for finish.
THE METHOD: Start rough, end fine.

SANDING SEQUENCE:
1. 80 grit -- removes saw marks, smooths rough spots, shapes edges
   (skip if wood is already relatively smooth)
2. 120 grit -- general smoothing, prepares for finish
3. 220 grit -- final smooth before stain or finish
   (this is fine enough for almost everything)

RULES:
- ALWAYS sand with the grain (in the direction of the wood fibers).
  Sanding across the grain leaves scratches that show up under stain.
- Don't skip grits. Going from 80 to 220 skips the middle step
  and takes longer than doing all three.
- Wipe with a tack cloth or damp rag between grits to remove dust.

FINISHING OPTIONS:

PAINT (easiest, best for pine):
- Sand to 120 grit
- Prime first (one coat, let dry)
- Two coats of paint (let first coat dry completely)
- Works great on pine, plywood, poplar
- Hides imperfections and cheaper wood

POLYURETHANE (clear protection, shows wood grain):
- Oil-based: deeper color, longer dry time (4-6 hours between coats),
  strong fumes (ventilate), very durable
- Water-based: clearer, dries fast (2 hours), low odor, slightly
  less durable but easier to apply
- Apply with a brush or wipe-on (wipe-on is more forgiving)
- 2-3 coats, light sand with 220 between coats

OIL FINISH (natural look, easiest to apply):
- Danish oil, tung oil, or boiled linseed oil
- Wipe on, wait 15 min, wipe off excess
- 2-3 coats, 24 hours between coats
- Brings out wood grain beautifully
- Less protective than poly, but easy to touch up

WHEN EACH MATTERS:
- Outdoor projects: exterior paint or spar urethane (UV resistant)
- Kitchen/food contact: mineral oil or food-safe finish (butcher block oil)
- High-traffic (tabletop, workbench): polyurethane
- Garden beds: leave unfinished, or use raw linseed oil (not boiled)
- Quick and easy: spray-on polyurethane (Minwax clear satin)
```

### Step 6: Five Starter Projects

**Agent action**: Provide cut lists and brief instructions for five practical builds, ordered by difficulty.

```
PROJECT 1: FLOATING SHELF (beginner, 1 hour, ~$15-25)

Materials: 1x8 pine board (length to fit your wall), 2 shelf brackets
           (rated for your expected load), wall anchors if no stud, screws

Cut list:
- 1x8 x [your desired length] -- that's it, one board

Steps:
1. Sand board (120, then 220 grit)
2. Finish (paint, poly, or oil -- your choice)
3. Find studs in wall (stud finder or knock test)
4. Mount brackets level (use a level), screwed into studs
5. Set shelf on brackets, screw from underneath
Total cost: $15-25 depending on finish and brackets.

---

PROJECT 2: RAISED GARDEN BED (beginner, 2 hours, ~$30-60)

Materials: 4x 2x6x8' boards (cedar if budget allows, pine if not),
           16x 3" deck screws

Cut list for a 4' x 8' bed:
- 4 boards at 8' (long sides -- no cuts needed)
- 4 boards at 45" (short sides -- cut from additional 2 boards)
  Wait -- simpler version: just buy 6 boards total.
  4 at full 8' length, cut 2 boards into 4 pieces at 45" each.

Steps:
1. Stack two boards for each long side (12" tall total)
2. Stack two boards for each short side
3. Pre-drill and screw corners with 3" deck screws (3 screws per joint)
4. Place on level ground where you want it
5. Fill with garden soil mix (about 1 cubic yard for a 4x8x1' bed)
No finish needed -- cedar lasts 10-15 years, pine lasts 5-7 in ground contact.
Total cost: $30-60 for lumber + $30-50 for soil.

---

PROJECT 3: SIMPLE BOOKSHELF (intermediate, 3-4 hours, ~$40-70)

Materials: 1x10 or 1x12 boards (pine or poplar), screws, wood glue,
           optional: shelf pins or pocket hole jig

Cut list (for a 3-shelf unit, 36" wide x 48" tall x 10" deep):
- 2 sides: 1x10 x 48"
- 3 shelves: 1x10 x 34.5" (subtract 2x board thickness for inside fit)
- 1 back panel: 1/4" plywood, 36" x 48" (optional but adds rigidity)

Steps:
1. Cut all pieces to length
2. Mark shelf positions on side boards (evenly spaced or to preference)
3. Pre-drill and screw through side boards into shelf ends
   (or use pocket holes on underside of shelves for cleaner look)
4. Add wood glue to every joint before screwing
5. Attach back panel with small nails or screws (this squares the unit)
6. Sand and finish
7. Attach to wall with an L-bracket at the top (prevents tipping)

---

PROJECT 4: WORKBENCH (intermediate, 4-6 hours, ~$50-100)

Materials: 2x4s (8 boards), 3/4" plywood (1 sheet for top), screws

Cut list (for a 2' x 5' bench, 34" tall):
- 4 legs: 2x4 x 34"
- 2 long stretchers (top): 2x4 x 57" (60" minus 2x leg width)
- 2 short stretchers (top): 2x4 x 21" (24" minus 2x leg width)
- 2 long stretchers (bottom, 6" up): same as top
- 2 short stretchers (bottom): same as top
- Top: 3/4" plywood, 24" x 60"

Steps:
1. Build two end frames (2 legs + 2 short stretchers, top and bottom)
2. Connect end frames with long stretchers
3. Screw plywood top down to frame
4. Add a bottom shelf (another piece of plywood) on the lower stretchers
5. No finish needed for a workbench -- let it get beat up

---

PROJECT 5: STORAGE BOX WITH LID (intermediate, 3 hours, ~$20-35)

Materials: 1x8 or 1x10 boards, 1/4" plywood for bottom, small hinges,
           wood glue, screws or nails

Cut list (for a 12" x 18" x 10" box):
- 2 long sides: 1x10 x 18"
- 2 short sides: 1x10 x 10.5" (inside dimension)
- Bottom: 1/4" plywood, 18" x 12"
- Lid: 1x10 or similar, 18" x 12" (or glue up two boards)

Steps:
1. Cut all pieces
2. Assemble sides with glue and screws (butt joints at corners)
3. Attach bottom with small nails and glue
4. Sand all surfaces
5. Attach lid with two small hinges on the back edge
6. Finish as desired (paint, poly, or oil)
7. Optional: add a handle or clasp
```

## If This Fails

- If a cut goes wrong, don't panic. If it's slightly long, trim it. If it's short, cut a new piece. Budget 10-20% extra lumber for mistakes.
- If your project isn't square, you probably didn't check squareness before screwing. Disassemble, re-square, re-attach. This is normal.
- If screws split the wood, you didn't pre-drill or you're too close to the edge. Pre-drill, and keep screws at least 1" from any board edge.
- If you're stuck on a project, search YouTube for the specific build. Video makes woodworking 10x easier to learn than text.
- If your first project looks rough, good. It's supposed to. The second one will be better. The fifth one will surprise you.

## Rules

- Always wear safety glasses when cutting, drilling, or sanding. Always.
- Measure twice, cut once. This is not negotiable.
- Pre-drill screw holes near edges and ends of boards. Wood splits without pilot holes.
- Sand with the grain, never against it.
- Don't skip pre-drilling just because it's one more step. Split boards mean starting over.
- For outdoor projects, use exterior-rated screws and outdoor-rated finish. Indoor hardware rusts.
- Secure your workpiece before cutting. A board that moves mid-cut is dangerous and wastes wood.

## Tips

- The miter box is the best $15 you'll spend in woodworking. Perfect straight cuts without any skill development needed.
- Pocket hole joinery (Kreg jig) is the biggest force multiplier for a beginner. It turns "I can build a box" into "I can build furniture."
- Free lumber sources (pallets, construction scraps, Habitat ReStore) can reduce project costs by 50-80%. Check every time before buying new.
- Label your cut pieces with pencil as you go (left side, right shelf, etc.). Keeps assembly organized.
- Clamps are more important than most people realize. Clamped joints while glue dries are dramatically stronger than unclamped ones.
- When in doubt about wood for a project, use pine. It's cheap, available everywhere, works easily, and paints well. You can always upgrade wood choice on your next build.
- Build things you actually need. A shelf you use every day teaches more than a decorative project that sits in a closet.

## Agent State

```yaml
woodworking:
  skill_level: null
  tools_owned: []
  tools_needed: []
  current_project: null
  project_status: null
  wood_sourced: false
  cut_list_created: false
  cuts_completed: false
  assembly_started: false
  finishing_method: null
  budget: null
  workspace_type: null
  completed_projects: []
```

## Automation Triggers

```yaml
triggers:
  - name: tool_check
    condition: "current_project IS SET AND tools_needed IS NOT EMPTY"
    action: "Before you start cutting, let's verify you have all the tools you need for this project. Missing anything on the list? Consider borrowing from neighbors or checking your local tool lending library."

  - name: cut_list_review
    condition: "cut_list_created IS true AND cuts_completed IS false"
    action: "You have a cut list ready. Before you start cutting, double-check every measurement against your plan. Mark all pieces first, then cut. And remember: measure twice, cut once."

  - name: project_completion
    condition: "current_project IS SET AND assembly_started IS true"
    schedule: "7 days after assembly_started"
    action: "How's the build going? If you're stuck on any step, let's troubleshoot. If it's done, what do you want to build next? Each project builds on skills from the last one."

  - name: next_project_suggestion
    condition: "completed_projects LENGTH >= 1"
    action: "You've completed a project. Your skills are growing. Based on what you've built so far, here are good next projects that'll push your abilities slightly further without being overwhelming."
```
