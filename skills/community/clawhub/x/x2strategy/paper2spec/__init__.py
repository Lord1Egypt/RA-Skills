"""paper2spec — Extract structured strategy specifications from quantitative finance research.

Multi-format input: PDF, Markdown, DOCX, plain text.

Multi-layer extraction pipeline:
  Stage 1 (Parser):   Document → PaperContent (methodology, signal_logic, data_description)
  Stage 2 (Extractor): PaperContent → ExtractionResult (List[StrategySpec])

Multi-strategy support:
  Layer 0 detects independent strategies in a paper.
  Layers 1-4 run per strategy with focused context injection.
"""

__version__ = "0.4.0"
