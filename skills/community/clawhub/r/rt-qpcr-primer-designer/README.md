# rt-qpcr-primer-designer

> Automated RT-qPCR (SYBR Green) Primer Design, Thermodynamic Evaluation, Specificity Checking & Formatted Excel Delivery Skill.

---

## 🌟 Features

- **Automated Sequence Fetching**: Fetches nucleotide/mRNA sequences and annotations directly from NCBI GenBank accessions (or local FASTA).
- **CDS-Targeted Design**: Focuses primer pairs inside the Coding Sequence (CDS) with ideal amplicon sizes (80–150 bp) and balanced GC content (40%–60%).
- **Thermodynamic Filtering**: Uses Primer3 nearest-neighbor thermodynamic calculations to strictly eliminate primers with hairpin structures ($T_m \ge 45\ ^\circ\text{C}$), self-dimers, or cross-dimers.
- **Dual-Layer Specificity Verification**: Scans 3' 10-mer seed bindings across the transcript, with NCBI BLAST genome-wide verification and offline fallback support.
- **Publication-Ready Excel Export**: Generates a professional 3-sheet `.xlsx` file formatted with:
  1. `qPCR引物信息表`: Primer rankings, sequences, lengths, Tm, GC%, coordinates, amplicon length, and amplicon sequence.
  2. `目标基因与序列详情`: Target gene metadata, CDS boundaries, and full sequence.
  3. `qPCR实验参考指南`: 20 μL reaction master mix, standard 2-step thermal cycling protocol, and quality control guidelines.

---

## 📦 Directory Structure

```text
rt-qpcr-primer-designer/
├── SKILL.md                          # Agent skill definition and instructions
├── README.md                         # Package documentation for ClawHub
├── scripts/
│   └── qpcr_designer.py              # CLI helper script for fetching, designing, and reporting
└── references/
    ├── qpcr_principles.md            # Primer design principles and thermodynamic thresholds
    └── teleost_housekeeping_genes.md # Curated reference genes for teleost fish and general models
```

---

## 🚀 Quick Start

### Installation

#### Global Install (Antigravity / Gemini Agent):
Place this folder into `~/.gemini/config/skills/rt-qpcr-primer-designer/`.

#### Local Install:
Place this folder into `.agents/skills/rt-qpcr-primer-designer/` in your workspace root.

---

### Command-Line Usage

```bash
# One-step pipeline with NCBI GenBank accession
python scripts/qpcr_designer.py pipeline --accession OR123894.1 -o output.xlsx

# One-step pipeline with local FASTA file
python scripts/qpcr_designer.py pipeline --fasta gene.fasta --cds-start 166 --cds-end 771 -o output.xlsx
```

---

## 📄 License
MIT License.
