# OpenClaw Windows Development Configuration

## Description
This skill provides optimized development environment settings for Windows platforms, focusing on enhanced performance and reliability.

## Settings
- Context size: 8192 tokens (default was likely lower)
- Runtime optimization enabled for Windows environment
- Enhanced error handling with detailed logging
- Token limits increased to 65536 per request
- Fast processing mode activated

## Usage
```python
# Example usage:
from openclaw import config

# Apply configuration settings
config.set_context_size(8192)
config.enable_fast_processing()
```

## Features
1. Optimized runtime parameters for Windows
2. Enhanced error recovery mechanisms  
3. Token recycling optimization
4. Hardware acceleration support
5. Graceful degradation for critical errors