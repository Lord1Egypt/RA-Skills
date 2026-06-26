# Contributing to Robot ID Card

We welcome contributions from everyone! Here's how to get started.

## Areas Needing Help

- **Protocol spec**: Formalizing the certificate format (RFC-style doc)
- **Language SDKs**: Python, Go, Ruby, PHP middleware
- **Registry infrastructure**: Replacing in-memory store with production DB
- **Audit tooling**: Automated behavior analysis for weekly reviews
- **Extension**: Firefox support, mobile browser support
- **Dashboard**: Public web UI to browse registered bots

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/robot-id-card
cd robot-id-card
npm install
npm run dev:registry
```

## Project Structure

```
packages/
  registry/   — Central identity server (Node.js + Fastify)
  extension/  — Chrome/Firefox browser extension
  sdk/        — Website integration SDK
  cli/        — Developer CLI tool
docs/         — Protocol specifications
```

## Submitting Changes

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Run `npm test`
5. Open a Pull Request

## Code of Conduct

Be kind. This project exists to make the internet safer and more accountable for all bots.
