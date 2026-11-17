---
name: rt-qpcr-primer-designer
description: >-
  Automated design, thermodynamic evaluation, specificity checking (BLAST & transcript off-target),
  and experimental Excel reporting for RT-qPCR primers (SYBR Green). Supports NCBI GenBank accession,
  FASTA sequence, or gene name lookup.
---

# RT-qPCR Primer Designer & Delivery Skill

## Overview
This skill provides an end-to-end automated workflow to design high-specificity, thermodynamically verified primers for Reverse Transcription Quantitative PCR (RT-qPCR, SYBR Green I method) and directly outputs publication/lab-ready formatted Excel delivery workbooks (`.xlsx`).

Key capabilities:
- **Sequence Retrieval**: Automatically fetches mRNA sequence, parses CDS coordinates, UTRs, and gene annotations from NCBI GenBank accessions.
- **Thermodynamic Primer Design**: Leverages Primer3 to design primers targeting the CDS region with optimal amplicon sizes (80–150 bp), matching melting temperatures ($T_m \approx 60\ ^\circ\text{C}$), balanced GC content (40%–60%), and 3' GC clamps.
- **Secondary Structure Filtering**: Rigorously eliminates primers with stable hairpins ($T_m \ge 45\ ^\circ\text{C}$), self-dimers, or cross-dimers.
- **Dual Specificity Verification**: Scans 3' 10-mer seed binding sites across the target transcript, with NCBI BLAST genome/transcriptome validation and graceful offline fallback.
- **Formatted Excel Delivery**: Automatically produces a 3-sheet styled workbook containing:
  1. `qPCR引物信息表`: Ranked primer pairs, sequences, positions, amplicon length, GC%, and full amplicon sequences.
  2. `目标基因与序列详情`: Full gene metadata, CDS coordinates, and nucleotide sequences.
  3. `qPCR实验参考指南`: 20 μL reaction master mix table, standard 2-step thermal cycling protocol, and quality control guidelines (DNase I treatment, NTC controls, reference genes).

---

## Dependencies
- **`ncbi-sequence-fetch`**: Used for fetching NCBI sequence records and annotations.
- **Python Libraries**:
  - `primer3-py`: Thermodynamic nearest-neighbor calculations ($T_m$, hairpin, dimers).
  - `openpyxl`: Excel workbook formatting and styling.
  - `biopython`: Sequence parsing and BLAST query handling.

---

## Quick Start

### 1. One-Stop End-to-End Pipeline
Given an NCBI accession number (e.g. `OR123894.1`):
```bash
python scripts/qpcr_designer.py pipeline \
  --accession OR123894.1 \
  --output "IFN_gamma_qPCR_primers.xlsx"
```

### 2. From Local FASTA File with Specified CDS
```bash
python scripts/qpcr_designer.py pipeline \
  --fasta "gene.fasta" \
  --cds-start 166 \
  --cds-end 771 \
  --organism "Nibea albiflora" \
  --product "IFN-gamma" \
  --output "gene_qpcr_primers.xlsx"
```

---

## Utility Scripts (`scripts/qpcr_designer.py`)

The helper CLI supports both individual modular subcommands and the complete `pipeline`:

### 1. `fetch`
Fetches GenBank record by accession and saves structured metadata to JSON:
```bash
python scripts/qpcr_designer.py fetch \
  --accession OR123894.1 \
  -o "gene_meta.json"
```

### 2. `design`
Designs primer pairs within the CDS with specified amplicon length and $T_m$:
```bash
python scripts/qpcr_designer.py design \
  --input "gene_meta.json" \
  --min-prod 80 \
  --max-prod 150 \
  --opt-tm 60.0 \
  -o "candidates.json"
```

### 3. `specificity`
Performs transcript-level off-target scanning and adds specificity annotations:
```bash
python scripts/qpcr_designer.py specificity \
  --input "candidates.json" \
  -o "verified_candidates.json"
```

### 4. `export-excel`
Renders the verified primer data into a styled 3-sheet Excel delivery file:
```bash
python scripts/qpcr_designer.py export-excel \
  --input "verified_candidates.json" \
  -o "qPCR_Primers_Report.xlsx"
```

---

## Workflow Guide

When the user asks to design qPCR primers:
1. **Identify the Input**:
   - GenBank accession / NCBI link $\rightarrow$ Call `fetch` or `pipeline --accession`.
   - FASTA sequence or raw text $\rightarrow$ Save to `.fasta` and specify `--cds-start` and `--cds-end`.
2. **Execute Design & Specificity Verification**:
   - Run `pipeline` with default 80–150 bp amplicon range and 60 °C annealing temperature.
3. **Present Results in Chat**:
   - Highlight the **Top Recommended Pair** and 1–2 **Alternative Pairs** with $T_m$, GC%, amplicon length, and amplicon sequence.
   - Summarize the BLAST/transcript specificity findings.
4. **Deliver the Excel File**:
   - Provide a clickable markdown file link to the generated `.xlsx` report.

---

## Rate Limiting & Error Handling

- **NCBI API Requests**: Standard NCBI rate limit is 3 requests/second (or 10 req/s with `NCBI_API_KEY`).
- **BLAST / Network Fallback**: If NCBI BLAST times out or the target species has incomplete genome assembly in NCBI, the pipeline automatically falls back to transcript-level seed scan + closely related species homologous verification, surfacing a clear notice in the output.

---

## Common Mistakes to Avoid
- **Designing outside the CDS**: Primers in long UTR regions may amplify non-coding splice variants. Always locate primers inside the coding region (CDS) unless specifically targeting UTR.
- **Amplicon too long (>200 bp)**: Standard fast qPCR cycles (20–30 s extension) require short amplicons (80–150 bp). Longer amplicons lead to lower amplification efficiency.
- **Ignoring gDNA Contamination**: Always advise the user to treat RNA with DNase I or use gDNA-removing reverse transcriptase kits.
