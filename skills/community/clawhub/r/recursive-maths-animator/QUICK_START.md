# 🎬 Pattern Library Quick Start Guide

## ✅ What's Available

You have **9 working Manim animation patterns** ready to use!

### 📁 File Locations

```
# Main pattern library (source of truth)
references/pattern_library/
├── __init__.py                    # Import all patterns from here
├── table_transforms.py            # 3 table → graph patterns
├── statistical_viz.py             # 3 statistical patterns
└── pie_chart_animations.py      # 3 pie chart patterns

# Stacked copies (for easy access)
.training/stacked_animations/
├── 01_table_transforms.py
├── 02_statistical_viz.py
└── 03_pie_charts.py

# Example customization
EXAMPLE_CUSTOM_ANIMATION.py      # Template for your own animations
```

## 🚀 Quick Start Commands

### 1. Test that patterns work (no rendering)
```bash
source .training/.venv-3.12/bin/activate
cd /Users/ashishdogra/repos/growth/manim-video-skill/recursive-maths-animator

python -c "
from references.pattern_library import TableToBarChartPattern
scene = TableToBarChartPattern()
print('✓ Pattern loaded successfully!')
print(f'Data: {scene.data}')
"
```

### 2. Render a quick GIF preview (fast)
```bash
source .training/.venv-3.12/bin/activate
python references/pattern_library/table_transforms.py -ql --format gif --disable_caching
```

### 3. Render medium quality MP4
```bash
source .training/.venv-3.12/bin/activate
python references/pattern_library/table_transforms.py -qm --format mp4 --disable_caching
```

### 4. Render example animation
```bash
source .training/.venv-3.12/bin/activate
python EXAMPLE_CUSTOM_ANIMATION.py -ql --format gif
```

## 📺 Output Location

After rendering, videos appear in:
```
media/videos/1080p60/MyQuarterlyReport.mp4
media/videos/1080p60/TableToBarChartPattern.mp4
media/videos/1080p60/BasicPieChart.mp4
...
```

## 🎨 The 9 Patterns

### Table → Graph (3 patterns)
1. **TableToBarChartPattern** - Morph table to animated bars
2. **TableToLineGraphPattern** - Table to line graph with points
3. **TableToScatterPlotPattern** - Table to scatter + trend line

### Statistical Viz (3 patterns)
4. **DistributionAnimation** - Normal/Gaussian bell curve
5. **FormulaDerivation** - Step-by-step formula walkthrough
6. **SamplingVisualization** - Central Limit Theorem demo

### Pie Charts (3 patterns)
7. **BasicPieChart** - Simple animated pie segments
8. **StaggeredPieChart** - Sequential entry + explode effect
9. **PieToBarTransition** - Morph between pie and bar chart

## ✏️ How to Customize

### Step 1: Copy a pattern
```bash
cp references/pattern_library/table_transforms.py my_report.py
```

### Step 2: Edit the data
```python
# In my_report.py, find:
data = [
    ("Q1", 2500),
    ("Q2", 3200),
    ...
]

# Change to your data:
data = [
    ("Jan", 45000),
    ("Feb", 52000),
    ...
]
```

### Step 3: Edit colors
```python
# Find:
bar_colors = [BLUE, GREEN, YELLOW, RED]

# Change to hex colors:
bar_colors = ["#3498db", "#2ecc71", "#f1c40f", "#e74c3c"]
```

### Step 4: Edit voiceover text
```python
# Find:
with self.voiceover(text="Let's look at..."):

# Change to:
with self.voiceover(text="Your custom narration here."):
```

### Step 5: Render
```bash
source .training/.venv-3.12/bin/activate
python my_report.py -qm --format mp4
```

## 🔧 Quality Options

| Flag | Quality | Time | Use For |
|------|---------|------|---------|
| `-ql` | Low (480p) | Fast | Testing |
| `-qm` | Medium (720p) | Medium | Drafts |
| `-qh` | High (1080p) | Slow | Final output |
| `-qp` | Production (4K) | Very slow | Presentations |

## 🎯 Next Steps

1. **Try the example**: Run `EXAMPLE_CUSTOM_ANIMATION.py` with your data
2. **Pick a pattern**: Choose from the 9 patterns for your needs
3. **Customize**: Edit data, colors, text for your content
4. **Render**: Generate MP4 or GIF
5. **Use**: Drop into presentations, social media, documentation

## 📚 Documentation

- `.training/LEARNING_REPORT_01.md` - What we learned from AutoAgent
- `.training/COMPREHENSIVE_ANALYSIS.md` - Full technical analysis
- `.training/HYBRID_APPROACH_REPORT.md` - How the system was built

## ❓ Common Issues

**"manim: command not found"**
→ Run: `source .training/.venv-3.12/bin/activate`

**"Syntax error"**
→ Check that you copied the full file, not partial

**"LaTeX not found"**
→ These patterns don't use LaTeX, should work without it

**"Video not playing"**
→ Check `media/videos/1080p60/` directory

## 💡 Pro Tips

- Start with `-ql` (low quality) for quick testing
- Use `--disable_caching` for cleaner renders
- GIFs are smaller but lower quality than MP4
- The example file shows all customization points
- All patterns work with voiceover automatically

---

**You're all set! Pick a pattern and start creating! 🎨**
