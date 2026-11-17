# Contributing

Thanks for helping keep this skill accurate and useful. Contributions of all
sizes are welcome.

## The one hard rule

**Every factual claim about the algorithm must cite the specific file or value
it comes from** in X's [open-source algorithm](https://github.com/twitter/the-algorithm).
That citation is the whole point of this skill. A claim without a source does
not get merged, no matter how plausible it sounds. If you cannot point to the
code, it is folklore, and folklore belongs in [references/myths.md](references/myths.md)
(as a myth), not in the guidance.

## Good contributions

- **Refreshed values after an upstream change.** X rewrites the production
  defaults in `home-mixer/params/param.rs` periodically. If a weight or
  threshold has moved, update it and note the new snapshot date.
- **New myths, with citations.** Popular advice the code confirms or refutes,
  each with the mechanism that settles it.
- **Worked examples.** Weak-to-strong post rewrites in
  [references/examples.md](references/examples.md), with the reasoning tied to
  weights.
- **Critic improvements.** Better heuristics, new signal detectors, or
  calibration fixes in `scripts/post_critic.py`. Keep it standard-library only.
- **Clarity edits.** Tightening prose, fixing errors, improving structure.

## Style

- Prefer plain sentences. Avoid overusing em dashes.
- Keep `SKILL.md` lean; push detail into `references/`.
- Use precise numbers from the code, and label them as a dated snapshot.
- ASCII-friendly output in scripts (the critic runs on Windows consoles too).

## Working on the critic

The critic is pure Python standard library, no dependencies.

```bash
python scripts/post_critic.py "a test draft"
python scripts/post_critic.py --compare "draft A" "draft B"
python -c "import py_compile; py_compile.compile('scripts/post_critic.py', doraise=True)"
```

If you change the weight table or calibration, sanity-check that rage-bait
scores negative, a plain like-bait post scores weak, and a genuinely
forward-worthy post scores ok or better.

## Submitting

1. Fork and branch.
2. Make your change, with citations.
3. Open a pull request describing what changed and the source in the algorithm
   repo that backs it.

## Scope

Keep contributions aligned with the skill's ethics: this optimizes genuine,
policy-compliant content. Contributions aimed at spam, inauthentic behavior, or
evading enforcement will be declined.
