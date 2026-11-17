# RT-qPCR Primer Design Principles & Guidelines

## 1. Core Primer Design Parameters (SYBR Green I)

| Parameter | Recommended Range | Optimal Value | Rationale |
| :--- | :--- | :--- | :--- |
| **Primer Length** | 18–24 nt | 20 nt | Balances annealing specificity and binding kinetics. |
| **Melting Temp ($T_m$)** | 58–62 °C | 60.0 °C | Standard two-step qPCR annealing temperature. |
| **$\Delta T_m$ (Fwd - Rev)** | $\le 1.5$ °C | $\le 0.5$ °C | Ensures simultaneous and balanced extension. |
| **Primer GC%** | 40%–60% | 50% | Prevents non-specific binding and secondary structures. |
| **Amplicon Length** | 80–150 bp | 100–120 bp | High amplification efficiency (near 100%) and short extension times. |
| **Amplicon GC%** | 40%–60% | ~50% | Ensures sharp, single melting curve peaks. |
| **3' End GC Clamp** | 1–2 G/C in last 5 nt | 1 G or C at 3' | Stabilizes polymerase binding while avoiding non-specific 3' mispriming. |
| **Avoid Poly-X** | Max 3 identical bases | $\le 3$ (no GGGG/CCCC) | Poly-G/C causes non-specific hybridization and slipped strand mispairing. |

---

## 2. Secondary Structures & Thermodynamics

* **Hairpins**: $\text{Hairpin } T_m < 45\ ^\circ\text{C}$, $\Delta G > -2.0\text{ kcal/mol}$.
* **Homodimers (Self-dimer)**: $\text{Dimer } T_m < 35\ ^\circ\text{C}$, $\Delta G > -5.0\text{ kcal/mol}$ (specifically 3' end $\Delta G > -2.0\text{ kcal/mol}$).
* **Heterodimers (Cross-dimer)**: $\text{Dimer } T_m < 35\ ^\circ\text{C}$, $\Delta G > -5.0\text{ kcal/mol}$.
* **Thermodynamic model**: SantaLucia nearest-neighbor method (`primer3`).

---

## 3. Specificity Strategy

1. **Target Region Selection**:
   * Prioritize the **CDS (Coding Sequence)** for mRNA quantification.
   * If genomic DNA sequence is known, design primers crossing an **exon-exon junction** or spanning a large intron (>500 bp) to eliminate genomic DNA amplification.
2. **Transcript-Level Off-Target Scan**:
   * Check 3' 10-mer seed sequences across the full transcript. Ensure exactly 1 on-target hit and 0 off-target matches.
3. **Genome/Transcriptome BLAST**:
   * Run BLAST against the host species (NCBI `taxid`). Confirm that no off-target transcript has $\ge 80\%$ identity or 3'-end matching within $\le 1000\text{ bp}$.

---

## 4. qPCR Standard Protocol & Quality Control

### 20 μL Reaction Setup
* $2\times$ SYBR Green Master Mix: 10.0 μL
* Forward Primer (10 μM): 0.4–0.8 μL (0.2–0.4 μM final)
* Reverse Primer (10 μM): 0.4–0.8 μL (0.2–0.4 μM final)
* cDNA Template: 2.0 μL (10–100 ng)
* Nuclease-free $\text{ddH}_2\text{O}$: up to 20.0 μL

### Standard 2-Step Cycling Program
1. **Pre-denaturation**: 95 °C for 30 s – 2 min
2. **Amplification (40 cycles)**:
   * Denaturation: 95 °C for 5–10 s
   * Annealing & Extension: 60 °C for 20–30 s (Acquire fluorescence)
3. **Melt Curve Stage**: 65 °C to 95 °C, ramp rate 0.5 °C/step, 5 s dwell time.
