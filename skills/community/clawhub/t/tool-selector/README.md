# Tool Selector

## The Problem

Starting a DIY project without the right tools leads to frustration, wasted money, and abandoned projects:

- **The average household makes 2.3 extra trips to the hardware store** per DIY project because they forgot something (Home Improvement Research Institute)
- **Overbuying tools** costs the average DIYer $200-500/year on tools used fewer than 3 times
- **Using the wrong tool** for a material causes damage and injury — masonry bits on regular drills burn out, using a flathead on a Phillips screw strips it
- **Material miscalculation** — buying too little means mid-project store runs, too much means wasted money

The core issue: there's no easy way to go from "I want to do X" to "here's exactly what you need and how to do it."

## Who Needs This

- **Homeowners** — 76% of US homeowners do at least one DIY project per year
- **First-time DIYers** who don't know what tools exist or which to buy
- **Apartment dwellers** with limited tool storage who need minimal kits
- **Weekend makers** who want to plan shopping trips efficiently
- **Budget-conscious people** who need to know costs before committing

## How It Works

### Project Planner (`scripts/project_planner.py`)
Contains a database of 50+ common DIY projects, each with:
- Required and recommended tools
- Material lists with quantities and common sizes
- Step-by-step instructions
- Time and difficulty estimates
- Cost ranges (budget / mid-range / quality)

```bash
# Plan a project
python scripts/project_planner.py plan "raised garden bed"

# Filter by available tools
python scripts/project_planner.py plan "shelf" --have "drill,screwdriver,hammer"

# List all projects
python scripts/project_planner.py list

# Cost estimate only
python scripts/project_planner.py cost "picture frame"
```

### Tool Substitution (`scripts/tool_substitution.py`)
```bash
# Find alternatives
python scripts/tool_substitution.py "miter saw"

# What can I use instead of a pipe wrench?
python scripts/tool_substitution.py "pipe wrench"
```

### Sample Output

```
$ python scripts/project_planner.py plan "raised garden bed" --have "drill,circular saw,tape measure"
═══════════════════════════════════════════════════════
  📊 PROJECT: Raised Garden Bed
  ⏱️ Time: 2-3 hours | 🎯 Difficulty: Beginner
═══════════════════════════════════════════════════════

TOOLS:
  ✅ Cordless drill (have)
  ✅ Circular saw (have)
  ✅ Measuring tape (have)
  ⬜ Speed square         ~$8    (for square cuts)
  ⬜ Phillips bit set     ~$12   (for driving screws)

MATERIALS:
  Cedar lumber (naturally rot-resistant):
    • 4× 2×6 board, 8ft     ~$12 ea = $48
    • 2× 2×4 board, 8ft     ~$7 ea  = $14
  Hardware:
    • 1 box 3" deck screws  ~$8
  Consumables:
    • Landscape fabric 4×8  ~$5
    • 12 cu ft potting soil ~$30

💰 TOTAL COST: ~$125 (materials only)

📋 STEPS:
  1. Measure and mark cut lines on all boards
  2. Cut 4× side boards to 4ft and 2× end boards to 8ft
  3. Cut 4× corner posts from 2×4 at 12" lengths
  4. Pre-drill holes (prevents cedar from splitting)
  5. Screw side boards to corner posts, staggering joints
  6. Place bed in location, line with landscape fabric
  7. Fill with soil, plant!

⚠️ NOTE: Use cedar or redwood, not pressure-treated,
   for edible gardens (chemicals can leach into soil).
```

## Real-World Example

Maria just moved into her first apartment and wants to hang floating shelves. She doesn't own any tools. She uses the planner:

```bash
$ python scripts/project_planner.py plan "floating shelf" --have ""
```

The planner tells her she needs: a stud finder ($15), a drill ($40-80), a level ($10), wall anchors ($5), and screws ($3). Total: $73-113. 

She then checks substitutions and learns she can rent a drill from Home Depot for $30/day instead of buying one, reducing her cost to $63. The step-by-step guides her through finding studs, drilling pilot holes, and installing anchors.

## License

MIT — see [LICENSE](LICENSE)
