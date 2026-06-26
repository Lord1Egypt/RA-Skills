# Recursive Maths Animator

> 🎬 **Production-ready Manim animations with zero LaTeX dependencies**

[![Patterns](https://img.shields.io/badge/Patterns-9%20Verified-success)](./references/pattern_library/)
[![Success Rate](https://img.shields.io/badge/Success%20Rate-100%25-brightgreen)](./.training/learnings/)
[![LaTeX Free](https://img.shields.io/badge/LaTeX-Free-blue)](./SKILL.md)

Create beautiful, narrated mathematical animations in minutes—not hours.

---

## 🚀 Quick Start (30 Seconds)

```bash
# 1. Activate environment
source .training/.venv-3.12/bin/activate

# 2. Render a pattern
python references/pattern_library/table_transforms_tested.py TableToBarChartPattern -ql --format mp4

# 3. Get your video
# Output: media/videos/1080p60/TableToBarChartPattern.mp4
```

**That's it.** No LaTeX installation. No complex setup. Just working animations.

---

## 🎨 What You Can Create

### 1. Table-to-Graph Transformations
Transform boring data tables into engaging animated visualizations.

| Pattern | Output | Use Case |
|---------|--------|----------|
| **TableToBarChartPattern** | [📹 Video](media/videos/1080p60/TableToBarChartPattern.mp4) | Quarterly reports, category comparisons |
| **TableToLineGraphPattern** | [📹 Video](media/videos/1080p60/TableToLineGraphPattern.mp4) | Time series, trends over months |
| **TableToScatterPlotPattern** | [📹 Video](media/videos/1080p60/TableToScatterPlotPattern.mp4) | Correlation analysis, relationships |

**Example:**
```python
from references.pattern_library import TableToBarChartPattern

scene = TableToBarChartPattern()
scene.data = [("Q1", 2500), ("Q2", 3200), ("Q3", 2800), ("Q4", 4100)]
scene.bar_colors = [BLUE, GREEN, YELLOW, RED]
scene.render()
```

**Result:** 19.3s animated video with synchronized voiceover

---

### 2. Statistical Visualizations
Make statistics intuitive with animated distributions and derivations.

| Pattern | Output | Use Case |
|---------|--------|----------|
| **DistributionAnimation** | [📹 Video](media/videos/1080p60/DistributionAnimation.mp4) | Normal/Gaussian curves, statistics education |
| **FormulaDerivation** | [📹 Video](media/videos/1080p60/FormulaDerivation.mp4) | Step-by-step math proofs, theorem explanations |
| **SamplingVisualization** | [📹 Video](media/videos/1080p60/SamplingVisualization.mp4) | Central Limit Theorem, sampling demos |

**Example:**
```python
from references.pattern_library import FormulaDerivation

scene = FormulaDerivation()
scene.formula_steps = [
    "a² + b² = c²",
    "c = √(a² + b²)"
]
scene.render()
```

**Result:** 17.2s video showing formula derivation with narration

---

### 3. Pie Chart Animations
Animated pie charts that engage and explain.

| Pattern | Output | Use Case |
|---------|--------|----------|
| **BasicPieChart** | [📹 Video](media/videos/1080p60/BasicPieChart.mp4) | Market share, percentage breakdowns |
| **StaggeredPieChart** | [📹 Video](media/videos/1080p60/StaggeredPieChart.mp4) | Exploded segments, emphasis |
| **PieToBarTransition** | [📹 Video](media/videos/1080p60/PieToBarTransition.mp4) | Same data, two perspectives |

**Example:**
```python
from references.pattern_library import StaggeredPieChart

scene = StaggeredPieChart()
scene.data = [("Product A", 40), ("Product B", 30), ("Product C", 30)]
scene.explode_index = 0  # Highlight first segment
scene.render()
```

**Result:** 21.8s video with sequential reveals and explode effect

---

## 📚 Video Gallery

All 9 patterns rendered and ready:

| # | Pattern | Video | Duration | Size |
|---|---------|-------|----------|------|
| 1 | TableToBarChartPattern | [▶️](media/videos/1080p60/TableToBarChartPattern.mp4) | 19.3s | 845KB |
| 2 | TableToLineGraphPattern | [▶️](media/videos/1080p60/TableToLineGraphPattern.mp4) | 19.5s | 872KB |
| 3 | TableToScatterPlotPattern | [▶️](media/videos/1080p60/TableToScatterPlotPattern.mp4) | 20.1s | 1.0MB |
| 4 | DistributionAnimation | [▶️](media/videos/1080p60/DistributionAnimation.mp4) | 18.8s | 1.1MB |
| 5 | FormulaDerivation | [▶️](media/videos/1080p60/FormulaDerivation.mp4) | 17.2s | 910KB |
| 6 | SamplingVisualization | [▶️](media/videos/1080p60/SamplingVisualization.mp4) | 22.4s | 1.6MB |
| 7 | BasicPieChart | [▶️](media/videos/1080p60/BasicPieChart.mp4) | 19.4s | 874KB |
| 8 | StaggeredPieChart | [▶️](media/videos/1080p60/StaggeredPieChart.mp4) | 21.8s | 1.4MB |
| 9 | PieToBarTransition | [▶️](media/videos/1080p60/PieToBarTransition.mp4) | 23.1s | 1.7MB |

**Total:** 9.4MB of production-ready animations

---

## 🎯 Key Features

### ✅ Zero LaTeX Dependencies
Unlike standard Manim, our patterns work without texlive:

| Instead of | We Use | Benefit |
|------------|--------|---------|
| `Axes()` | `Line()` + `Text()` | -2GB dependency |
| `MathTex()` | `Text()` | No compilation |
| `FunctionGraph()` | `VMobject()` | Full control |
| `PieChart()` | `AnnularSector()` | No internal deps |

### ✅ Auto-Generated Voiceover
Every pattern includes synchronized narration:
- GTTSService generates audio automatically
- 5-7 sync points per video
- SRT captions auto-generated
- No manual audio editing

### ✅ Evidence-Based Timing
All animations use verified timing:
- 0.5s per staggered element
- 2.0s for transitions
- 2.0s final pause
- Total: 17-23 seconds (ideal for explainers)

### ✅ Customizable
Change anything in 3 lines:
```python
scene = TableToBarChartPattern()
scene.data = [("Your", 100), ("Data", 200)]
scene.bar_colors = ["#3498db", "#2ecc71"]
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- ffmpeg
- No LaTeX required! 🎉

### Setup
```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install manim manim-voiceover[gtts]
```

### Skill Installation (Optional)
For system-wide access:
```bash
# Copy to Claude Code skills
cp -r references/pattern_library ~/.claude/skills/recursive-maths-animator/references/
```

---

## 📖 Usage Patterns

### Pattern 1: Quick Render
```python
from references.pattern_library import BasicPieChart

scene = BasicPieChart()
scene.data = [("A", 30), ("B", 70)]
scene.render()
```

### Pattern 2: Customize and Render
```python
from references.pattern_library import TableToBarChartPattern
from manim import RED, BLUE, GREEN

scene = TableToBarChartPattern()
scene.data = [("Jan", 100), ("Feb", 150), ("Mar", 120)]
scene.bar_colors = [RED, BLUE, GREEN]
scene.bar_width = 0.9
scene.render()
```

### Pattern 3: Production Quality
```bash
# Development (fast)
python pattern.py -ql --format mp4  # 30s render

# Production (high quality)
python pattern.py -qh --format mp4  # 3min render
```

---

## 🎓 Learning Resources

### For Beginners
- [QUICK_REFERENCE.md](references/pattern_library/QUICK_REFERENCE.md) - Pattern usage guide
- [SKILL.md](SKILL.md) - Complete skill documentation

### For Advanced Users
- [COMPREHENSIVE_PATTERN_LEARNINGS.json](.training/learnings/COMPREHENSIVE_PATTERN_LEARNINGS.json) - Evidence from all 9 patterns
- [FINAL_RELENTLESS_REPORT.md](.training/FINAL_RELENTLESS_REPORT.md) - Testing methodology

### Understanding the System
- [LEARNING_SYSTEM_EXPLAINED.md](.training/learnings/LEARNING_SYSTEM_EXPLAINED.md) - Why we captured learnings this way
- [DIRECTORY_GUIDE.md](.training/DIRECTORY_GUIDE.md) - What's in `.training/`

---

## 🔬 The Relentless Testing Process

Every pattern was:
1. ✅ Rendered successfully
2. ✅ Verified as valid H.264 MP4
3. ✅ Checked for LaTeX dependencies (none found)
4. ✅ Timed and documented
5. ✅ Added to skill

**Result:** 9/9 patterns (100% success rate)

See [.training/FINAL_RELENTLESS_REPORT.md](.training/FINAL_RELENTLESS_REPORT.md) for complete evidence.

---

## 🚀 What You Can Build

### Educational Content
- Math tutorial videos
- Statistics explanations
- Data visualization lessons

### Business Presentations
- Quarterly reports
- Market share breakdowns
- Trend analysis

### Social Media
- Short-form explainers (17-23s perfect for TikTok/Reels)
- Animated infographics
- Data stories

### Documentation
- API visualization
- Process flows
- Feature explanations

---

## 📦 Project Structure

```
.
├── references/
│   └── pattern_library/          # ⭐ 9 verified patterns
│       ├── __init__.py
│       ├── table_transforms_tested.py    # 3 patterns
│       ├── statistical_viz_tested.py       # 3 patterns
│       ├── pie_charts_tested.py          # 3 patterns
│       └── QUICK_REFERENCE.md     # Usage guide
├── media/
│   └── videos/
│       └── 1080p60/               # 📹 Rendered videos
│           ├── TableToBarChartPattern.mp4
│           ├── DistributionAnimation.mp4
│           └── ... (9 videos total)
├── .training/
│   └── learnings/                 # 📚 Evidence & learnings
│       ├── COMPREHENSIVE_PATTERN_LEARNINGS.json
│       ├── FINAL_RELENTLESS_REPORT.md
│       └── ...
└── SKILL.md                       # 📖 Skill documentation
```

---

## 🤝 Contributing

### Adding New Patterns
1. Create pattern in `references/pattern_library/`
2. Use LaTeX-free techniques (see existing patterns)
3. Render and verify
4. Add to `__init__.py`
5. Update documentation

### Improving Learnings
1. Test patterns with different data
2. Document what works
3. Add to `COMPREHENSIVE_PATTERN_LEARNINGS.json`

---

## 📝 License

MIT License - Use for personal, educational, or commercial projects.

---

## 🙏 Acknowledgments

- Built with [Manim](https://github.com/3b1b/manim) (community edition)
- Voiceover via [manim-voiceover](https://github.com/MathBlocks/manim-voiceover)
- Relentlessly tested to ensure quality

---

## 💡 Quick Commands Cheat Sheet

```bash
# Render specific pattern
python references/pattern_library/table_transforms_tested.py TableToBarChartPattern -ql --format mp4

# List all patterns
python -c "from references.pattern_library import __all__; print('\n'.join(__all__))"

# Check video outputs
ls -lh media/videos/1080p60/*.mp4

# Render all patterns
for p in TableToBarChartPattern TableToLineGraphPattern TableToScatterPlotPattern DistributionAnimation FormulaDerivation SamplingVisualization BasicPieChart StaggeredPieChart PieToBarTransition; do
  python references/pattern_library/table_transforms_tested.py $p -ql --format mp4
done
```

---

**Ready to create?** Pick a pattern, customize your data, and render. Your animated video is 30 seconds away. 🎬

[Get Started →](references/pattern_library/QUICK_REFERENCE.md)
