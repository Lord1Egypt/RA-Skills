# Publication-Grade R Visualization

## Nature/Science Style

### Theme

```r
theme_classic(base_size = 8, base_family = "sans") +
theme(
    plot.title = element_text(size = 9, face = "bold", hjust = 0),
    axis.line = element_line(linewidth = 0.4),
    axis.ticks = element_line(linewidth = 0.3),
    panel.grid = element_blank(),
    legend.background = element_blank()
)
```

### Rules

- **No plot titles** — titles belong in figure captions
- **Panel labels**: bold lowercase **a**, **b**, **c**, **d**
- **Font**: sans-serif (Arial/Helvetica), 7-9pt
- **Axis labels**: "Frequency (%)" with bare numbers on ticks
- **No gridlines**, white background, axis lines only
- **Dimensions**: single column 89mm, double 183mm, 300 DPI

### Colorblind-Safe Palette

Wong B (2011) *Nat Methods* 8:441:

```r
blue      = "#0072B2"
vermillon = "#D55E00"
green     = "#009E73"
skyblue   = "#56B4E9"
orange    = "#E69F00"
purple    = "#CC79A7"
```

### Paired Data: Dot Plot > Bar Chart

For before/after comparisons, NEVER use bar charts with error bars.
Use **paired dot plots** with connecting lines:

```r
ggplot(df, aes(x = condition, y = value)) +
    geom_line(aes(group = sample), color = "#CCCCCC",
              linewidth = 0.3, alpha = 0.6) +
    geom_point(aes(color = condition), size = 1.5, alpha = 0.7) +
    stat_summary(fun = median, geom = "point",
                 shape = 18, size = 3.5, color = "black") +
    stat_summary(fun = median, geom = "crossbar",
                 width = 0.3, linewidth = 0.4, color = "black")
```

This shows every individual data point + median, not just
mean ± SE hiding the distribution.

### Many Samples (>7)

When too many samples for individual colors:
- Use single color histogram, no legend
- Panel D: histogram of counts per sample, not individual bars
- Annotate with summary stats (n, pass rate)

### Figure Captions (README)

Use blockquote format with numbered panels:

```markdown
> **Figure 1 | Title.** Description. (**a**) Panel A.
> (**b**) Panel B. Data: Author (Year) *Journal*.
```
