# Solution Templates — Hierarchical Decision Matrix

Use these as starting scaffolds. Adapt prerequisites and payoffs to the user's
specific system and research question.

---

## Domain: Electrostatics / Desolvation

| | Plan A | Plan B | Plan C |
|-|--------|--------|--------|
| **Method** | Coulomb + VdW grid probe | APBS Poisson-Boltzmann | GIST explicit water thermodynamics |
| **Implementation** | Pure Python / NumPy | External APBS binary | MD trajectory (GROMACS/AMBER) + `gisttools` |
| **Runtime** | Seconds | Minutes | Days (requires ns-scale MD) |
| **Prerequisites** | PDB + partial charges | PDB + APBS install | Full MD setup, water model |
| **Output** | Qualitative interaction hotspots | Continuous electrostatic potential (kT/e) | $\Delta G_{water}$ per voxel (kcal/mol) |
| **Academic payoff** | Hypothesis generation | Publication-ready for non-FEP papers | Required for explicit desolvation claims |

**When to recommend Plan C:** only when the user is explicitly publishing on
water-mediated binding or allosteric mechanisms. For most druggability papers, Plan B is sufficient.

---

## Domain: Pocket Detection / Druggability

| | Plan A | Plan B | Plan C |
|-|--------|--------|--------|
| **Method** | fpocket / DoGSiteScorer (geometry-based) | SiteMap (Schrödinger) or CryptoSite | MD ensemble + volmap clustering |
| **Runtime** | Seconds | Minutes | Days |
| **Prerequisites** | PDB only | Licensed software | MD trajectory |
| **Blind spot** | Misses cryptic pockets; no dynamics | Partially addresses flexibility | Full cryptic pocket sampling |
| **Academic payoff** | Rapid screening; standard benchmark (DUD-E) | Industry-standard; publishable | Required for cryptic pocket papers |

---

## Domain: Binding Affinity Estimation

| | Plan A | Plan B | Plan C |
|-|--------|--------|--------|
| **Method** | Docking score (Glide SP / AutoDock Vina) | MM-GBSA / MM-PBSA rescoring | FEP+ or thermodynamic integration |
| **Typical error** | ~2–3 kcal/mol (rank order only) | ~1–2 kcal/mol | ~0.5–1 kcal/mol (congeneric series) |
| **Runtime** | Seconds per pose | Minutes per complex | Days per perturbation |
| **Prerequisites** | Receptor structure + ligand 3D | Docked poses + force field | FEP setup expertise; GPU cluster |
| **Academic payoff** | Virtual screening hit enrichment | Lead optimization support | Required for quantitative $\Delta\Delta G$ claims |

**Key caveat to always state:** docking scores are *not* $\Delta G_{bind}$. They are
empirical scoring functions trained on PDBbind. Conflating them is a common and
peer-reviewer-detected error.

---

## Domain: Structural Flexibility / Conformational Sampling

| | Plan A | Plan B | Plan C |
|-|--------|--------|--------|
| **Method** | Ensemble from PDB homologs / NMR models | Short MD (10–100 ns) + clustering | Enhanced sampling (metadynamics, REST2) |
| **Runtime** | Minutes | Hours–days | Days–weeks |
| **Prerequisites** | Multiple PDB structures available | MD setup | Sampling expertise + GPU cluster |
| **Captures** | Pre-existing conformers only | Local fluctuations, induced fit | Rare events, cryptic pocket opening |
| **Academic payoff** | Rapid ensemble docking | Standard flexibility for most papers | Required for cryptic pocket / allostery claims |

---

## Domain: SASA / Surface Geometry

| | Plan A | Plan B | Plan C |
|-|--------|--------|--------|
| **Method** | Shrake-Rupley rolling sphere (BioPython) | MSMS analytical reentrant surface (SES) | MD-averaged SASA with probe-size sensitivity |
| **Runtime** | Milliseconds | Seconds | Hours (per trajectory) |
| **Error vs. analytical** | ~3–5% | Reference (analytical) | Trajectory-averaged; converges with sampling |
| **Use when** | Rapid screening; relative comparisons OK | Accurate SES/SAV for publication | Flexibility-dependent desolvation papers |
