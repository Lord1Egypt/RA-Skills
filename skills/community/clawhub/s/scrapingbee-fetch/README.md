# ScrapingBee Fetch

A Python script to fetch and render JavaScript-heavy websites using the [ScrapingBee API](https://www.scrapingbee.com/). It extracts the main content and returns it as clean Markdown, making it perfect for LLM reading and data extraction.

## Features

- Automatically renders JavaScript
- Extracts relevant text content and title
- Fixes common encoding issues
- Supports custom proxies, wait times, and ad blocking

## Requirements

- Python 3.10+
- `uv` (recommended) or `pip` for dependency management
- A ScrapingBee API key (you can get one at [dashboard.scrapingbee.com/dashboard](https://dashboard.scrapingbee.com/dashboard))

## Installation

Clone the repository:

```bash
git clone https://github.com/flobo3/skill-scrapingbee.git
cd skill-scrapingbee
```

Set your ScrapingBee API key as an environment variable:

```bash
export SCRAPINGBEE_API_KEY="your_api_key_here"
```

Alternatively, you can create a `.env` file in the project directory:

```env
SCRAPINGBEE_API_KEY=your_api_key_here
```

## Usage

You can run the script directly using `uv`:

```bash
uv run fetch.py --url "https://example.com"
```

### Optional Arguments

- `--no-render-js`: Disable JavaScript rendering (faster, but might miss dynamic content).
- `--country-code <code>`: Use a proxy from a specific country (e.g., `us`, `uk`, `ru`).
- `--wait <milliseconds>`: Wait time in milliseconds before extracting content (default: 3000).
- `--no-block-ads`: Disable ad blocking (ads are blocked by default to save bandwidth and speed up rendering).
- `--premium-proxy`: Use a premium proxy (useful for complex websites).

### Examples

Fetch a website using a US proxy and wait 5 seconds:
```bash
uv run fetch.py --url "https://example.com" --country-code us --wait 5000
```

Fetch a complex website using a premium proxy:
```bash
uv run fetch.py --url "https://example.com" --premium-proxy
```

Fetch a simple website without rendering JavaScript:
```bash
uv run fetch.py --url "https://example.com" --no-render-js
```

## License

MIT
