# Contributing to Volcengine Skill

Thank you for your interest in contributing to the Volcengine OpenClaw skill! This document provides guidelines and instructions for contributing.

## Development Process

### 1. Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/openclaw/skills.git
cd skills/volcengine

# Install dependencies (if any)
npm install

# Run tests
npm test
```

### 2. Making Changes

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards:
   - Use consistent formatting (PowerShell scripts should follow best practices)
   - Update documentation for any API or behavior changes
   - Add tests for new functionality

3. **Test your changes**:
   ```bash
   # Run the full test suite
   ./scripts/run-tests.ps1 -ApiKey YOUR_TEST_API_KEY
   
   # Or run specific tests
   ./scripts/test-connection.ps1 -ApiKey YOUR_TEST_API_KEY
   ```

4. **Update documentation**:
   - Update `SKILL.md` for user-facing changes
   - Update `references/` files for API or configuration changes
   - Update `ROADMAP.md` if completing planned work

### 3. Submitting Changes

1. **Commit your changes** with descriptive commit messages:
   ```bash
   git add .
   git commit -m "Add: Description of your changes"
   ```

2. **Push to your fork** and create a Pull Request

## Contribution Guidelines

### Documentation Updates
- Follow the existing documentation structure
- Include practical examples where applicable
- Reference official Volcengine documentation when possible
- Keep language clear and concise

### Code Contributions
- PowerShell scripts should include proper error handling
- Use consistent naming conventions
- Include comments for complex logic
- Follow security best practices (never hardcode API keys)

### Testing Requirements
- All new features should include tests
- Existing tests must continue to pass
- Test both success and failure scenarios
- Consider edge cases and error conditions

### Skill Structure
Maintain the standard skill directory structure:
```
volcengine/
├── SKILL.md                 # Main skill documentation
├── package.json            # Skill metadata
├── LICENSE                 # License file
├── README.md              # Quick start guide
├── references/            # Detailed documentation
├── scripts/              # Utility scripts
└── recon/               # Research and analysis files
```

## Areas for Contribution

### High Priority
1. **Bug fixes** - Critical issues affecting functionality
2. **Security updates** - Vulnerabilities or security improvements
3. **Documentation corrections** - Errors or outdated information

### Medium Priority
1. **New feature implementation** - Features from the roadmap
2. **Test coverage improvements** - Additional test cases
3. **Performance optimizations** - Faster or more efficient code

### Low Priority
1. **Code refactoring** - Improvements to code structure
2. **Documentation enhancements** - Better explanations or examples
3. **Tooling improvements** - Development workflow enhancements

## Reporting Issues

### Bug Reports
When reporting bugs, please include:
1. **Description** - Clear explanation of the issue
2. **Steps to reproduce** - Step-by-step instructions
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - OpenClaw version, OS, PowerShell version
6. **Error messages** - Complete error output

### Feature Requests
For new features, please describe:
1. **Use case** - Why this feature is needed
2. **Proposed solution** - How it should work
3. **Alternatives considered** - Other approaches you've considered
4. **Impact** - Who will benefit and how

## Code Review Process

1. **Initial review** - Core maintainers review for functionality and quality
2. **Testing** - Automated tests run on the PR
3. **Feedback** - Reviewers provide feedback and request changes if needed
4. **Approval** - At least one maintainer approves the changes
5. **Merge** - PR is merged into the main branch

## Release Process

1. **Version bump** - Update version in `package.json`
2. **Changelog** - Document changes in `ROADMAP.md`
3. **Testing** - Full test suite passes
4. **Publish** - Release to ClawHub registry

## Code of Conduct

Please follow the [OpenClaw Community Code of Conduct](https://docs.openclaw.ai/community/code-of-conduct).

## Getting Help

- **Documentation**: [OpenClaw Docs](https://docs.openclaw.ai)
- **Discussions**: [GitHub Discussions](https://github.com/openclaw/skills/discussions)
- **Issues**: [GitHub Issues](https://github.com/openclaw/skills/issues)

## License

By contributing to this project, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

*Thank you for contributing to the OpenClaw ecosystem!*