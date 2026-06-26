# Code Documentor Skill

## Overview
Automatically generate comprehensive documentation for codebases.

## Capabilities

### 1. Documentation Generation
- README files
- API documentation
- Code comments
- Function docs

### 2. Language Support
- Python
- JavaScript/TypeScript
- Swift
- Go
- Rust
- Java
- And more...

### 3. Documentation Types
- Project READMEs
- API references
- Architecture docs
- Contributing guides
- Changelogs

### 4. Best Practices
- Follow language conventions
- Include examples
- Add type hints
- Document parameters

## Usage

### Commands
- `document this code`
- `generate README for [project]`
- `document function [name]`
- `create API docs for [endpoint]`
- `add comments to [file]`

## Output Templates

### README Template
```
# Project Name

## Description
[Brief description]

## Installation
```bash
[Installation commands]
```

## Usage
```[language]
[Code examples]
```

## API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/... | ... |

## Contributing
[Guidelines]

## License
[License info]
```

### Function Doc Template
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Short description.
    
    Longer explanation of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this happens
    
    Example:
        >>> function_name(...)
        ...
    """
```

## Configuration
- Documentation style: [default/stripe/google]
- Include examples: [true/false]
- Language: [target language]
- Output format: [markdown/html/pdf]
