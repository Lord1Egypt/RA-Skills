# Unified Memory Documentation

**English** · [中文](../zh/index.md)

Welcome to the Unified Memory v5.2.0 documentation. This documentation provides comprehensive guides, API references, and architecture details for the Unified Memory system.

## 📚 Documentation Structure

### Getting Started
- **[Quick Start Guide](./getting-started/quickstart.md)** - Get up and running in 5 minutes
- **[Installation Guide](./getting-started/installation.md)** - Detailed installation instructions
- **[Configuration Guide](./getting-started/configuration.md)** - System configuration options

### User Guides
- **[Basic Usage](./guides/basic-usage.md)** - Everyday operations and common tasks
- **[Advanced Features](./guides/advanced-features.md)** - Power features and optimizations
- **[Plugin System](./guides/plugins.md)** - Extending functionality with plugins
- **[Troubleshooting](./guides/troubleshooting.md)** - Solving common problems

### API Documentation
- **[API Overview](./api/overview.md)** - Introduction to the Unified Memory API
- **[Storage API](./api/storage-api.md)** - Memory storage and retrieval operations
- **[Vector API](./api/vector-api.md)** - Vector search and similarity operations
- **[Plugin API](./api/plugin-api.md)** - Plugin development and integration

### Architecture
- **[Architecture Overview](./architecture/overview.md)** - System design and components
- **[Atomic Transactions](./architecture/atomic-transactions.md)** - Data consistency guarantees
- **[Vector Search](./architecture/vector-search.md)** - Search algorithms and optimizations
- **[Plugin System](./architecture/plugin-system.md)** - Plugin architecture and design

### Reference
- **[CLI Reference](./reference/cli-reference.md)** - Command-line interface documentation
- **[Configuration Reference](./reference/configuration.md)** - Complete configuration options
- **[Changelog](./reference/changelog.md)** - Version history and changes
- **[FAQ](./reference/faq.md)** - Frequently asked questions
- **[Contributing Guide](./reference/contributing.md)** - How to contribute to the project

## 🎯 Key Features Documentation

### Atomic Data Consistency
- **Two-Phase Commit Protocol**: Guarantees atomic writes for JSON and vector storage
- **Transaction Recovery**: Automatic recovery of incomplete transactions
- **fsync Guarantee**: Ensures data is written to disk

### High-Performance Search
- **Hybrid Search**: BM25 + Vector + RRF fusion for best results
- **Optimized Algorithms**: 5-10x faster query performance
- **Intelligent Caching**: Memory caching for frequent queries

### Plugin System
- **Sync Bridge**: Synchronize with Workspace Memory
- **Unified Query**: Cross-system search interface
- **Health Monitoring**: Real-time system monitoring

## 🔧 Development Resources

### Code Examples


### Testing


### Building


## 📖 Reading Order

### For New Users
1. Start with the **[Quick Start Guide](./getting-started/quickstart.md)**
2. Read **[Basic Usage](./guides/basic-usage.md)** for everyday tasks
3. Explore **[Advanced Features](./guides/advanced-features.md)** as needed

### For Developers
1. Review the **[Architecture Overview](./architecture/overview.md)**
2. Study **[Atomic Transactions](./architecture/atomic-transactions.md)** for data consistency
3. Check the **[API Documentation](./api/overview.md)** for integration

### For Contributors
1. Read the **[Contributing Guide](./reference/contributing.md)**
2. Understand the **[Architecture](./architecture/overview.md)**
3. Review existing **[Code Examples](../shared/examples/)**

## 🔗 Related Resources

### External Links
- **[GitHub Repository](https://github.com/mouxangithub/unified-memory)** - Source code and issues
- **[npm Package](https://www.npmjs.com/package/unified-memory)** - Package distribution
- **[ClawHub Skill](https://clawhub.ai/)** - Skill marketplace

### Community
- **[GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)** - Community discussions
- **[Issue Tracker](https://github.com/mouxangithub/unified-memory/issues)** - Bug reports and feature requests
- **[Contributing Guide](./reference/contributing.md)** - How to contribute

## 📄 License

This documentation is part of the Unified Memory project and is licensed under the MIT License. See the [LICENSE](https://github.com/mouxangithub/unified-memory/blob/main/LICENSE) file for details.

## 🤝 Contributing to Documentation

We welcome contributions to improve this documentation! Please see our [Contributing Guide](./reference/contributing.md) for details on how to:

1. Report documentation issues
2. Suggest improvements
3. Submit documentation updates
4. Translate documentation

## 📞 Support

- **Documentation Issues**: Open an issue on [GitHub](https://github.com/mouxangithub/unified-memory/issues)
- **Questions**: Use [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)
- **Bugs**: Report via the [Issue Tracker](https://github.com/mouxangithub/unified-memory/issues)

---

**Last Updated**: 2026-04-15  
**Version**: v5.2.0  
**Documentation Version**: 1.0.0  

[← Back to Main Documentation](../README.md)
