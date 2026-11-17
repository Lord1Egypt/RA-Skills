# Common Reference & Housekeeping Genes in Teleost Fish

When quantifying gene expression via RT-qPCR in fish (*Nibea albiflora*, *Larimichthys crocea*, *Danio rerio*, *Salmo salar*, etc.), accurate normalization requires stably expressed internal reference genes.

## Recommended Housekeeping Genes

| Gene Symbol | Full Name | Typical Function | Recommended Usage |
| :--- | :--- | :--- | :--- |
| **ACTB / $\beta$-actin** | $\beta$-actin | Cytoskeleton structural protein | Broadly used across tissue and infection models. |
| **EF1A / EEF1A1** | Elongation factor 1-alpha | Protein translation elongation | High stability in embryonic development, gills, spleen. |
| **GAPDH** | Glyceraldehyde-3-phosphate dehydrogenase | Glycolysis metabolic enzyme | Highly expressed; suitable for high-abundance target genes. |
| **18S rRNA** | 18S ribosomal RNA | Ribosomal subunit | Extremely stable; requires cDNA dilution due to high abundance. |
| **B2M** | $\beta$-2-microglobulin | MHC class I component | Commonly used in immune/viral challenge studies. |
| **RPL13A / RPL17** | Ribosomal protein L13A / L17 | Ribosomal structural protein | Excellent stability across temperature stress challenges. |

## Best Practices
1. **Geometric Averaging**: Combine at least two reference genes (e.g. $\text{ACTB} + \text{EF1A}$) to reduce experimental bias.
2. **Stability Evaluation**: Use geNorm, NormFinder, or BestKeeper to validate reference stability in your specific tissue and treatment conditions.
