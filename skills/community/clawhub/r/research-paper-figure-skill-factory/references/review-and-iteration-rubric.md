# Review and Iteration Rubric

Use this after image generation or when critiquing existing figures.

## Review dimensions

| Dimension | Check |
|---|---|
| Claim fit | Does the figure support the paper's actual thesis? |
| Reader effect | Is the 10-second message visible? Is the 60-second understanding achievable? |
| Paper slot fit | Is the density appropriate for intro/method/results/appendix/rebuttal/slides? |
| Figure type fit | Does the design perform the intended role, or did it drift? |
| Panel choreography | Is the reading order obvious? |
| Hierarchy | Do novelty, problem, mechanism, and evidence have correct visual weight? |
| Label burden | Are labels short, readable, and consistent with paper terminology? |
| Color semantics | Does color mean one thing consistently? |
| Visual style risk | Is it too decorative, too cartoonish, too dry, too 3D/toy-like, or too poster-like? |
| Reviewer safety | Could reviewers misunderstand or distrust it? |
| Generation artifacts | Are there fake labels, malformed diagrams, or irrelevant details? |
| Caption boundary | Is detail assigned to caption instead of figure body? |

## Diagnostic output template

```markdown
### 图稿诊断
| 维度 | 评价 | 修改建议 |
|---|---|---|
| Claim fit | ... | ... |
| Reader effect | ... | ... |
| Panel order | ... | ... |
| Label burden | ... | ... |
| Style risk | ... | ... |

**默认推荐修订路线：**...
```

## Revision prompt types

- Conservative repair: keep layout and style; fix labels, hierarchy, clutter.
- Structural repair: keep figure type; change panel choreography.
- Style repair: keep content; change visual language.
- Thesis repair: change what the figure is trying to prove.
- Slot repair: adapt intro figure to method/appendix or vice versa.

## When to regenerate

Regenerate when:

- visual hierarchy contradicts the paper claim;
- the image invented technical details;
- labels are unreadable or wrong;
- style undermines seriousness;
- panel order is impossible to follow;
- key mechanism is missing.

Do not regenerate when a caption or minor label edit would solve the issue.
