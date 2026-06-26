# Scholar Research

Academic paper search and analysis tool that queries multiple databases (arXiv, PubMed, OpenAlex, CrossRef), scores papers by relevance/quality, and generates field timelines.

## Features

- 🔍 Search across 4 academic databases
- 📊 Score papers (0-100) based on citations, recency, and credibility
- 📈 Generate field evolution timelines
- 🧪 Comprehensive test coverage

## Installation

```bash
# From GitHub
pip install git+https://github.com/yourusername/scholar-research.git

# Or install locally
pip install -e .
```

## Usage

```bash
# Search for a topic
python -m scholar_research "quantum computing" --top=5

# Search with custom output
python -m scholar_research "machine learning" --top=3 --output json
```

## Supported Topics

- Battery research (sodium ion, zinc ion, lithium, solid state)
- Computing (quantum computing, neural networks, ML)
- Energy (solar cells, fuel cells)
- Health (cancer immunotherapy, CRISPR)

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
python test_runner.py

# Or with pytest
pytest tests/
```

## License

MIT License - see LICENSE file.
