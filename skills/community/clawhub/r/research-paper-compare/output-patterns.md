# Output Patterns

## Default Output Order

1. Paper acquisition summary
2. Comparison table
3. Analytical synthesis
4. Confidence and evidence notes

## 1. Paper Acquisition Summary

Briefly list:
- resolved paper titles
- PDF source for each paper
- whether full text was successfully read
- any retrieval or extraction caveats

## 2. Comparison Table

Use a compact table first.

Recommended columns:

- Paper
- Problem
- Core method
- Key distinguishing feature
- Strengths
- Weaknesses
- Limitations
- Best-fit scenario
- Evidence quality

Add `Experimental setting` or `Comparability caveat` if they materially affect interpretation.

## 3. Analytical Synthesis

After the table, provide a concise analysis with these subsections:

### Shared focus

What common problem or theme connects the papers?

### Main differences

What are the major methodological or experimental differences?

### Comparative advantages

What does each paper do especially well?

### Comparative weaknesses

Where does each paper fall short?

### When to prefer which paper

Explain selection logic based on task setting, constraints, or research goals.

## 4. Confidence and Evidence Notes

Explicitly state:
- whether each paper was compared from full PDF evidence
- whether text extraction quality was high / medium / low
- whether direct metric comparison is safe or unsafe
- which conclusions are robust and which remain tentative

## Optional Variants

### Theme-focused comparison

If the user specifies an axis, reorganize both the table and analysis around that axis.
Examples:
- method design
- evaluation quality
- efficiency
- robustness
- applicability

### Shortlist recommendation

If the user asks which paper is better for a goal, end with a brief recommendation grounded in extracted evidence, not preference language alone.
