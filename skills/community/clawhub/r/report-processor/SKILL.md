# Report Processor (研报处理器)

Automatically collect, parse, and extract key information from research reports. Supports PDF, TXT, and other formats.

## Features

- Parse research reports (PDF/TXT)
- Extract key information (core观点、数据、投资建议、风险)
- Auto summary generation
- Knowledge base storage

## Requirements

- Ollama with qwen2.5:14b model installed
- poppler-utils (for PDF parsing)

## Installation

```bash
# Install Ollama and pull model
ollama pull qwen2.5:14b

# Install poppler (for PDF support)
# macOS
brew install poppler
# Linux
sudo apt install poppler-utils
```

## Usage

```bash
# Process single file
python3 scripts/report_processor.py /path/to/report.pdf

# Batch process directory
python3 scripts/report_processor.py /path/to/reports/
```

## Output

Results are saved to `~/.openclaw/workspace/data/reports/` in JSON format.

## Configuration

Edit `scripts/report_processor.py` to customize:
- `OLLAMA_MODEL`: Model to use (default: qwen2.5:14b)
- `OUTPUT_DIR`: Output directory
