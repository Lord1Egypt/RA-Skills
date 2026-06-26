# Execution Protocols by Category

## Category A — Algorithm Design / Upgrade

Goal: lift the approach from heuristic to mathematically rigorous.

**Step 1: Complexity audit**
Estimate current time/space complexity. Flag any $O(N^2)$ or worse bottleneck.
State the theoretical lower bound for the problem class.

**Step 2: Abstraction upgrade ladder**

| Current approach | Upgrade target | Key concept |
|-----------------|---------------|-------------|
| Discrete grid / voxel search | Analytical surface (MSMS SES) | Reentrant surface geometry |
| 8-octant directional bins | Differential geometry — Shape Index $SI$ | $SI = \frac{2}{\pi}\arctan\frac{\kappa_1+\kappa_2}{\kappa_1-\kappa_2}$ |
| Full-space 3D scan $O(N^3)$ | Surface point cloud shell $O(N)$ | Distance-based interface filter |
| Euclidean distance clustering | Manifold-aware metric (geodesic, RMSD-weighted) | Topological data analysis |
| Rule-based pharmacophore | Statistical mechanics energy landscape | PMF / free energy surface |

**Step 3: Propose the upgraded algorithm**
Write pseudocode first. Estimate post-upgrade complexity. Then offer implementation
in the language the user is working in.

---

## Category B — Feasibility Audit / Peer Review

Simulate Reviewer #2. Structure the review as:

1. **Claim vs. Evidence gap**: What does the method claim to measure vs. what it
   actually computes?
2. **Physical assumptions**: List implicit assumptions. Mark each as
   `[Valid]`, `[Questionable]`, or `[False]`.
3. **False positive / false negative risk**: Where will this method confidently
   produce wrong answers?
4. **Benchmark availability**: Can the method be validated? Name existing datasets
   (DUD-E, ChEMBL, PDBbind, CASF-2016) or state if ground truth is sparse.
5. **Verdict**: `[Publishable with revision]`, `[Needs fundamental redesign]`, or
   `[Superseded by SOTA — see below]`.

---

## Category C — Geometry → Physics Transition

The user has mapped a structural feature (pocket, interface, channel) and needs to
assign physical meaning.

**Transition checklist:**

- [ ] Is electrostatic potential mapped? (Coulomb grid → APBS PB → GIST)
- [ ] Is desolvation penalty estimated? (SASA-based → explicit water displacement)
- [ ] Is pocket flexibility captured? (static PDB → ensemble docking → MD)
- [ ] Is binding affinity estimable? (docking score proxy → MM-GBSA → FEP)

For each unchecked item, recommend the cheapest Plan that satisfies the research
question. Do not recommend Plan C (FEP) if Plan A (MM-GBSA) is sufficient for
the stated goal.

**Key physical relationships to state explicitly:**

$$\Delta G_{bind} = \Delta H - T\Delta S = \Delta G_{elec} + \Delta G_{vdW} + \Delta G_{desolv} + \Delta G_{conf}$$

Geometric scoring functions capture $\Delta G_{vdW}$ only. Stress this to the user
whenever they conflate shape complementarity with binding affinity.

---

## Category D — Code Debugging

**Triage protocol:**

1. Read the full traceback. Identify the failing line and variable shapes at that point.
2. Check dimensional contract violations first (most common in NumPy/MDAnalysis):
   - Expected vs. actual `.shape`
   - Scalar vs. array vs. nested-list ambiguity
   - PDB formatter receiving a numpy float64 instead of Python `float`
3. Apply bulletproof input normalization (see `code-patterns.md → Input Hardening`).
4. If the error is in a linear algebra call, check for singular/near-singular matrices
   before and provide a physically meaningful fallback.
5. Return a corrected, annotated snippet. Explain *why* each fix works, not just *what*.

---

## Category E — Methodology Writing

Structure the Methods section as:

```
2.X [Section Title]

2.X.1 [Subsection — e.g., "Pocket Detection"]
  - System/dataset description
  - Algorithm/tool with version and citation
  - Key parameters and their physical justification
  - Validation/benchmark reference

2.X.2 [Subsection — e.g., "Electrostatic Analysis"]
  ...
```

Enforce these writing rules:
- Every parameter choice needs a physical justification or literature citation.
- Every tool invocation needs a version number.
- Avoid passive voice for novel contributions; use active voice to claim ownership
  of the methodology.
- If a step is "standard", cite a protocol paper rather than re-describing it.
