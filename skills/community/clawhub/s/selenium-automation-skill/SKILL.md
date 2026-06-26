---
name: selenium-automation
description: Browser automation skill using Selenium for web scraping, form filling, and UI testing. Use when Codex needs to automate browser interactions including: (1) Filling forms and submitting data, (2) Web scraping and data extraction, (3) UI testing and validation, (4) Clicking buttons and navigating pages, (5) Handling alerts and popups, (6) Taking screenshots of web pages
---

# Selenium Browser Automation Skill

This skill provides comprehensive browser automation capabilities using Selenium WebDriver.

## Quick Start

Basic form filling example:
```python
# Fill and submit a form
python scripts/form_filler.py --url https://example.com/login --username testuser --password testpass
```

Web scraping example:
```python
# Extract data from a webpage
python scripts/web_scraper.py --url https://example.com/data --output results.csv
```

## Installation Requirements

Before using this skill, install the required dependencies:
```bash
pip install selenium webdriver-manager beautifulsoup4 pandas
```

## Supported Browsers

- **Chrome**: Full support with ChromeDriver
- **Firefox**: Full support with GeckoDriver  
- **Edge**: Full support with EdgeDriver
- **Safari**: Limited support (macOS only)

## Core Scripts

### Form Filling (`scripts/form_filler.py`)
Automatically fill forms and submit data:
```python
python scripts/form_filler.py --url https://example.com/login --username testuser --password testpass
python scripts/form_filler.py --url https://example.com/contact --name "John Doe" --email "john@example.com" --message "Hello"
```

### Web Scraper (`scripts/web_scraper.py`)
Extract data from web pages:
```python
python scripts/web_scraper.py --url https://example.com/products --output products.csv
python scripts/web_scraper.py --url https://example.com/news --output news.json --format json
```

### UI Tester (`scripts/ui_tester.py`)
Perform UI testing and validation:
```python
python scripts/ui_tester.py --url https://example.com --element "login-button" --action click
python scripts/ui_tester.py --url https://example.com --element "username" --action type --text "testuser"
```

## Usage Examples

See [examples/](examples/) for comprehensive examples including:
- Form filling with various input types
- Web scraping with pagination
- UI testing workflows
- Error handling and retries
- Browser configuration options

## Browser Configuration

The scripts support various browser configurations:
- Headless mode for background automation
- Different viewport sizes
- Custom user agents
- Proxy support
- Download directory configuration

## Error Handling

Comprehensive error handling for:
- Element not found
- Page load timeouts
- Network issues
- Browser crashes
- Form validation errors

## Advanced Features

- **Wait strategies**: Explicit waits, implicit waits, fluent waits
- **Element locators**: ID, CSS selectors, XPath, name, class
- **JavaScript execution**: Run custom JavaScript in browser
- **File uploads**: Handle file input fields
- **Cookies management**: Get, set, and manage cookies
- **Screenshots**: Capture full page or element screenshots

## Integration with Other Skills

This skill can be combined with:
- **browser-opener**: Open browsers programmatically
- **data-processing**: Process scraped data
- **file-operations**: Save and manage output files