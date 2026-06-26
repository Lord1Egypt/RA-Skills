# README Grader

The `readme-grader` skill acts as an expert Open Source Maintainer and Developer Advocate. It evaluates a project's README file text content, scores it out of 100 based on standard open-source best practices, and provides specific, actionable improvement suggestions.

## Features

- **Comprehensive Scoring:** Evaluates five dimensions: Project Overview, Quick Start/Installation, Usage/Examples, Contributing & Community, and Structure & Formatting.
- **Actionable Feedback:** Tells you exactly what is missing and how to fix it to attract more contributors and users.
- **Optimization Examples:** Provides Markdown snippets showing the suggested improvements.
- **Security First:** Requires direct text input to prevent indirect prompt injection risks associated with fetching untrusted external URLs.

## Example Usage

When reviewing a short, incomplete README like:

> "# My Project\nThis is a project.\n## Install\nnpm install"

The skill will point out the lack of a proper description, usage examples, contribution guidelines, and licensing information, scoring it accordingly and providing a robust template.

## Output Format

The skill provides its review in a structured Markdown format, primarily in Chinese:

- **📊 README 评分报告 (README Evaluation Report):** Total score out of 100.
- **1. 评分详情 (Score Breakdown):** Breakdown of scores by category.
- **2. 优点 (What's Good):** Highlighting the current strengths.
- **3. 改进建议 (Improvement Suggestions):** Actionable tips for better documentation.
- **4. 优化示例 (Optimization Example):** A rewritten or augmented README snippet.

## Installation

```bash
/plugin install readme-grader@anthropic-agent-skills
```
