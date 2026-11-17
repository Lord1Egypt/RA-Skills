---
name: readme-gen
description: Use when user wants to generate a README.md for their project.
triggers: ["readme", "README", "生成说明", "项目文档"]
version: 1.0.0
author: VBot
---

# README Generator

> Generate a polished README.md from project structure

## Scan Project

1. Check package.json for name, description, scripts
2. Check for: .gitignore, LICENSE, tests/, docs/
3. Detect language from file extensions
4. Count total files and lines

## Output Template

```markdown
# {project-name}

{description}

## Features

- Feature 1
- Feature 2

## Install

\`\`\`bash
npm install
\`\`\`

## Usage

\`\`\`bash
npm start
\`\`\`

## Structure

\`\`\`
{file-tree}
\`\`\`

## License

MIT
```

## Tips

- Use shields.io for badges
- Include demo/screenshots if available
- Add contribution guidelines if complex
