---
name: verify-code-change
version: 1.0.0
description: Run application to verify code changes meet expectations
whenToUse: When you need to verify functionality after code changes
---

## Overview

Run application or test commands to verify code changes do not break existing functionality.

## Core Functionality

- **Test command execution**: Run specified test commands
- **Timeout control**: Prevent test from hanging
- **Result parsing**: Check if test passes
- **Error capture**: Capture and display error information
- **Log output**: Display detailed execution logs

## Usage

Provide test command, script will automatically execute and check results.

## Parameters

- `test_command`: Test command (required, e.g., `npm test`)
- `expected_behavior`: Expected behavior description (optional)
- `timeout`: Timeout in seconds (optional, default 60)

## Example

```bash
python scripts/verify_code.py --test-command "npm test"
python scripts/verify_code.py --test-command "python -m pytest" --timeout 120
python scripts/verify_code.py --test-command "cargo test" --expected-behavior "All tests passed"
```

## Output Format

- **Test passed**: ✓ Display success message
- **Test failed**: ✗ Display error message and stack trace
- **Timeout**: ✗ Display timeout warning

## Tech Stack

- Python 3.11+
- asyncio
- subprocess

## Supported Test Frameworks

- JavaScript: npm test, jest, mocha, vitest
- Python: pytest, unittest
- Rust: cargo test
- Go: go test
- Java: mvn test
- Others: Custom commands

## Notes

1. Must be executed in project root directory
2. Ensure test environment is properly configured
3. Timeout should be adjusted based on test complexity
4. Error log will include complete stack trace

## Integration Suggestions

- Integrate to CI/CD pipeline
- Use in pre-commit hook
- Combine with code review process
- Configure automated test reports

## Legal Disclaimer

This skill is for learning and research purposes only.

Users must comply with the following principles when using this skill:
1. Not for any commercial use
2. Comply with project open source license
3. Do not use for any illegal or improper purposes

By using this skill, you agree to comply with the above principles.
