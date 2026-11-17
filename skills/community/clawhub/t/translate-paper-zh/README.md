# Translate Paper ZH

Translate full academic papers into searchable Chinese PDFs, preserving scholarly layout as closely as practical: two-column text, equations, figures, tables, citations and appendices.

- Source-led LaTeX composition preferred; explicit PDF regions or reconstruction when source is unavailable.
- Four local Python helpers for source inventory, planned region overlays, audit and font optimization.
- Every output page and translation unit needs actual visual/semantic review.
- Python 3.10+, `requirements.txt` dependencies and an embeddable Chinese font required. The TeX route also needs an appropriate TeX installation.
- The helpers do not upload manuscripts or use an external translation API.

Example prompt: Use $translate-paper-zh to translate this entire paper into Simplified Chinese as a searchable PDF. Preserve its two-column layout, equations, figures, citations and appendices. Translate figure labels and inspect every page.

Canonical repository, bilingual docs and attributed PDF example: https://github.com/vittta/translate-paper-zh

ClawHub edition is released under MIT-0 by explicit author authorization. The GitHub edition remains MIT licensed. Third-party paper examples are not included in this bundle.
