# Proxy Detector Skill

## Description
A skill that detects system proxy settings and provides proxy information in JSON format.

## Usage
Run the proxy detector to get current proxy settings:

```bash
python proxy_detector.py
```

## Output Format
The tool outputs proxy information in JSON format with the following structure:

```json
{
  "address": "http://localhost:15236",
  "isActive": true
}
```

## Features
- Detects system proxy settings for Windows and macOS
- Tests if the detected proxy is actually running
- Falls back to common proxy addresses if no system proxy is found
- Provides clear JSON output for easy parsing

## Requirements
- Python 3.6+
- No external dependencies