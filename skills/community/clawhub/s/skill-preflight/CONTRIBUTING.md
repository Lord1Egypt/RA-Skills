# Contributing to skill-preflight

Thanks for wanting to improve skill-preflight! Here's how to contribute.

## Development Setup

```bash
git clone https://github.com/thekhemistai/openclaw-skill-preflight.git
cd openclaw-skill-preflight
npm install
```

## Building

The plugin is written in JavaScript. Build with:

```bash
npm run build
```

This compiles source to `dist/index.js`.

## Testing

Test the plugin locally in OpenClaw:

1. Enable it in `openclaw.json`:
```json
{
  "plugins": {
    "skill-preflight": {
      "enabled": true,
      "config": { "maxResults": 3 }
    }
  }
}
```

2. Run an agent and verify injection:
```bash
openclaw agent --local -m "your test prompt"
```

3. Check logs for:
```
skill-preflight: injecting N doc(s): Doc1, Doc2, ...
```

## Code Style

- Use standard JavaScript (ES modules)
- Follow the existing code structure
- Keep functions focused and pure where possible
- Add comments for complex logic

## Submitting Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push and create a pull request

## Reporting Bugs

Open a GitHub issue with:
- Reproduction steps
- Expected vs actual behavior
- OpenClaw version
- Plugin configuration
- Logs/output if relevant

## Ideas for Improvement

Have ideas? Feel free to open a [GitHub issue](https://github.com/thekhemistai/openclaw-skill-preflight/issues) to discuss features or improvements before implementing major changes.

## License

By contributing, you agree your code will be licensed under MIT.
