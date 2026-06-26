---
name: rtqpcr-primer-design
description: Advanced RT-qPCR primer and probe design with specialized support for cross-species homology mapping (e.g., Human to Vero cells) and high-GC virus optimization. Use when needing to design high-specificity qPCR assays for: (1) Standard Human/Mouse/Monkey transcripts, (2) Predicted transcripts (XM_) lacking exon data via homology mapping, (3) High-GC viral templates (e.g., PRV), or (4) SYBR Green and TaqMan probe-based assays. Designed by ZJU PhD.
acceptLicenseTerms: true
---

# RT-qPCR Primer Design (Bio-chat Series)

This skill provides a professional-grade workflow for designing high-specificity RT-qPCR primers and probes, optimized for complex biological samples.

## Key Capabilities

1. **Homology-based Junction Mapping**: Uses multiple anchor points and sliding-window alignment to map exon-exon junctions from a well-annotated ortholog (e.g., Human NM_) to a predicted target transcript (e.g., Vero XM_). This ensures gDNA-safe design even when target annotations are missing.
2. **High-GC Template Optimization**: Implements the full SantaLucia (1998) Nearest-Neighbor thermodynamic model for precise Tm calculation, essential for templates with >70% GC content (e.g., Pseudorabies virus).
3. **TaqMan & SYBR Green Support**: 
   - **TaqMan**: Automatically designs probes with Tm 8-10°C higher than primers, following standard real-time PCR design rules (no 5' G, no poly-G runs).
   - **SYBR**: Strict 3' quality control and secondary structure screening to minimize primer-dimers.
4. **Off-target Defense**: Supports an optional `--offtarget` transcript to check for 3' end mispriming, ensuring high specificity in mixed cDNA samples.

## Workflow

1. **Target Identification**: Provide a NCBI Accession (NM_/XM_) or a local FASTA sequence.
2. **Homology Mapping (Optional)**: For predicted monkey transcripts, provide a Human ortholog Accession to activate "Hardcore Mode" for junction mapping.
3. **Automated Design**: Execute `scripts/design_qpcr_assay.py` with specific parameters:
   - `--target`: Target accession (e.g., `NM_001256799`)
   - `--homolog`: Human ortholog for mapping (e.g., `NM_001256799` for a monkey gene)
   - `--offtarget`: Accession for 3' specificity check (e.g., a homologous gene in the same family)
4. **Validation**: Review the top-scoring sets based on Tm, GC, 3' quality, and gDNA safety.

## Technical Standards

- **Tm Calculation**: SantaLucia (1998) Nearest-Neighbor (NN) model with salt and terminal correction.
- **gDNA Defense**: Primers are required to span exon-exon junctions by at least 5bp on each side for stability.
- **3' Quality**: Strict GC-clamp control and mismatch prevention.

*Designed by ZJU PhD @ Bio-chat Community*
