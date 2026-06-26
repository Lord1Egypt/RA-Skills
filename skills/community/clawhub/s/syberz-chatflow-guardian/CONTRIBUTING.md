# Contributing to ChatFlow Guardian

Thank you for your interest in contributing to ChatFlow Guardian! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an issue with:
1. Clear description of the bug
2. Steps to reproduce
3. Expected vs actual behavior
4. Screenshots if applicable
5. Environment information

### Suggesting Features
Feature suggestions are welcome! Please include:
1. Clear description of the feature
2. Use cases and benefits
3. Potential implementation approach
4. Any related issues or references

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

### Prerequisites
- Node.js >= 16.0.0
- OpenClaw >= 2026.3.0
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/openclaw/chatflow-guardian.git
cd chatflow-guardian

# Install dependencies
npm install

# Run tests
npm test
```

### Project Structure
```
chatflow-guardian/
├── src/              # Source code
│   ├── index.js      # Main entry point
│   ├── monitor.js    # Conversation monitoring
│   ├── analyzer.js   # Intent analysis
│   ├── responder.js  # Response generation
│   ├── optimizer.js  # Resource optimization
│   ├── logger.js     # Logging system
│   ├── platforms.js  # Multi-platform support
│   ├── predictive.js # Predictive response
│   └── deeplearning.js # Deep learning optimization
├── config/           # Configuration files
├── scripts/          # Utility scripts
├── tests/            # Test files
└── docs/             # Documentation
```

## Coding Standards

### JavaScript/Node.js
- Use ES6+ features where appropriate
- Follow Airbnb JavaScript Style Guide
- Use async/await for asynchronous operations
- Add JSDoc comments for public APIs

### Code Quality
- Write unit tests for new features
- Maintain test coverage above 80%
- Use ESLint for code linting
- Run tests before submitting PR

### Documentation
- Update README for new features
- Add JSDoc comments for new functions
- Update CHANGELOG for significant changes
- Keep configuration examples current

## Testing

### Running Tests
```bash
# Run all tests
npm test

# Run specific test
npm test -- --testNamePattern="intent recognition"

# Run with coverage
npm run test:coverage
```

### Test Structure
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- E2E tests in `tests/e2e/`
- Mock data in `tests/fixtures/`

## Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible new features
- PATCH: Backward-compatible bug fixes

### Release Steps
1. Update version in `package.json`
2. Update `CHANGELOG.md`
3. Create release branch
4. Run all tests
5. Create GitHub release
6. Update documentation

## Getting Help

- Check existing issues and discussions
- Join our [Discord community](https://discord.gg/openclaw)
- Email: 969027040@qq.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.