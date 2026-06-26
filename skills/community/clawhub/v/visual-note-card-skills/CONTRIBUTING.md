# Contributing

Thanks for your interest in contributing to Visual Note Card Generator!

## How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/my-feature`)
3. **Commit** your changes (`git commit -m 'Add my feature'`)
4. **Push** to the branch (`git push origin feature/my-feature`)
5. **Open** a Pull Request

## Guidelines

- Keep the single-file HTML output approach — no build tools or frameworks
- Maintain the existing CSS variable system for theming
- Test generated cards in multiple browsers (Chrome, Firefox, Safari)
- If modifying the template, ensure the export (html2canvas) still works correctly

## Reporting Issues

Please open a GitHub issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Browser/environment info if relevant

## Code Style

- HTML/CSS follows the conventions in `assets/template.html`
- SKILL.md uses standard Claude Code skill frontmatter format
