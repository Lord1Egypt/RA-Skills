# Webpage Downloader Skill for OpenClaw

## Skill Description

The Webpage Deader skill is a powerful tool that allows you to download and analyze webpage content using Google Chrome's headless browser. This skill can:

- Check if Google Chrome is installed on your system
- Automatically attempt to install Chrome if it's not found (on supported platforms)
- Download webpage content using Chrome's headless mode with optimized parameters
- Read and process the downloaded HTML content
- Generate a summary of the webpage content
- Safely handle temporary files to protect your privacy

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser (will be automatically detected, with installation assistance provided if missing)

### Installation Steps

1. **Install the skill** in OpenClaw:
   - Open OpenClaw
   - Go to Skills Manager
   - Click "Add Skill"
   - Select the directory where you downloaded this skill
   - Click "Install"

### Platform-Specific Notes

- **Windows**: Chrome installation requires manual download from [Google Chrome](https://www.google.com/chrome/)
- **macOS**: Requires Homebrew for automatic installation. If Homebrew is not installed, manual installation is required.
- **Linux**: Supports automatic installation on Ubuntu/Debian and Fedora/CentOS/RHEL distributions. For other distributions, manual installation is required.

## Usage Examples

### Basic Usage

```python
from webpage_reader import main

result = main("https://example.com")

if result['success']:
    print("Webpage downloaded successfully!")
    print("Summary:")
    print(result['summary'])
    print("\nContent preview:")
    print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
else:
    print(f"Error: {result['message']}")
```

### Command Line Usage

```bash
python webpage_reader.py https://example.com
```

### OpenClaw Interface Usage

1. Open OpenClaw
2. Select the Webpage Downloader skill
3. Enter the URL in the input field
4. Click "Run"
5. View the results in the output panel

## Technical Details

### Chrome Command Parameters

The skill uses the following Chrome command parameters for optimal performance:

```bash
google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --virtual-time-budget=8000 --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" --hide-scrollbars --blink-settings=imagesEnabled=true --dump-dom <url>
```

### Output Format

The skill returns a dictionary with the following structure:

```python
{
    "success": bool,          # Whether the operation succeeded
    "message": str,           # Status message
    "content": str,           # Full HTML content of the webpage
    "summary": str            # Summary of the webpage content
}
```

## Troubleshooting

### Common Issues

1. **Chrome not found**
   - **Solution**: Install Google Chrome manually from [https://www.google.com/chrome/](https://www.google.com/chrome/)

2. **Permission errors**
   - **Solution**: Run the skill with appropriate permissions, especially when installing Chrome on Linux

3. **Timeout errors**
   - **Solution**: The skill has a 60-second timeout. For large webpages, this may not be sufficient. You can modify the timeout in the `download_webpage` function.

4. **Empty content**
   - **Solution**: Check if the URL is accessible and not blocked by CAPTCHA or other anti-scraping measures

5. **Encoding errors**
   - **Solution**: The skill uses UTF-8 encoding. For webpages with different encodings, you may need to modify the encoding handling in the `read_webpage_content` function.

### Logging

The skill generates detailed logs to help diagnose issues. Logs are output to the console by default, but can be configured to write to a file if needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This skill is released under the MIT License. See the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.