# Bio-chat: Professional RT-qPCR Assay Designer

> **Precision primer design, optimized for real-world lab challenges.**

Bio-chat is a robust RT-qPCR primer and probe design tool tailored for molecular biology laboratories. Developed by a **Bioinformatics PhD from Zhejiang University (ZJU)**, it addresses common pain points in primer design for complex species and high-GC templates.

## 🌟 Key Features

- **Cross-Species Mastery**: Native support for Human, Monkey (Vero/African Green Monkey), and various model organisms.
- **High-GC Virus Optimization**: Specialized algorithms for templates with >70% GC content (e.g., Pseudorabies virus/PRV), automatically adjusting primer length and Tm weight for peak specificity.
- **Full Assay Support**:
  - **SYBR Green**: Strict dimer screening and 3' quality control.
  - **TaqMan Probe**: Automated generation of high-sensitivity probes with precise Tm matching.
- **gDNA Defense**: Integrated exon-junction spanning logic to prevent genomic DNA contamination.
- **Hardcore Homology Mapping**: A unique feature for predicted transcripts (XM_ Accessions) lacking exon annotations; uses Human/Monkey ortholog alignment to accurately locate splicing points.

## 🛠️ Technical Specifications

- **Algorithm Core**: Full Nearest-Neighbor (NN) thermodynamic model (SantaLucia, 1998) for industry-standard Tm accuracy.
- **Quality Control**: Expert-level parameterization for 3' anchor stability and off-target mismatch defense.
- **Output**: Instant, standardized primer ordering sheets.

## 🚀 Developer's Note

In the Bio-chat community, we believe experimental success starts with a "perfect strike" in primer design. Bio-chat distills years of wet-lab and dry-lab iteration into a reliable, automated tool for the OpenClaw ecosystem.

---
*Powered by OpenClaw | Designed by ZJU PhD @ Bio-chat Community*
