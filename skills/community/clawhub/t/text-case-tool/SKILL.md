---
slug: text-case-tool
name: Text Case Converter
description: "Convert text between different cases: UPPER, lower, Title, Sentence, camelCase, PascalCase, snake_case, kebab-case, CONSTANT_CASE. Pure Python, no API key required."
keywords: text, case, convert, uppercase, lowercase, camelcase, snake_case, kebab-case
version: "1.0.0"
author: Qiance
language: en
---

# Text Case Converter

Convert text between different case formats. Useful for programming, writing, and data transformation.

## Features

- **UPPER CASE**: ALL CAPS
- **lower case**: all lowercase
- **Title Case**: First Letter Of Each Word
- **Sentence case**: First letter only
- **camelCase**: firstLetterLower
- **PascalCase**: FirstLetterUpper
- **snake_case**: words_with_underscores
- **kebab-case**: words-with-hyphens
- **CONSTANT_CASE**: WORDS_WITH_UNDERSCORES

## Usage

```bash
# Upper case
python3 scripts/text_case.py "hello world" --upper

# Lower case
python3 scripts/text_case.py "HELLO WORLD" --lower

# Title case
python3 scripts/text_case.py "hello world" --title

# camelCase
python3 scripts/text_case.py "hello world" --camel

# snake_case
python3 scripts/text_case.py "HelloWorld" --snake

# kebab-case
python3 scripts/text_case.py "Hello World" --kebab
```

## Examples

| Input | Mode | Output |
|-------|------|--------|
| hello world | --upper | HELLO WORLD |
| HELLO WORLD | --lower | hello world |
| hello world | --title | Hello World |
| hello world | --camel | helloWorld |
| hello world | --pascal | HelloWorld |
| HelloWorld | --snake | hello_world |
| hello world | --kebab | hello-world |

---

## 中文说明

文本大小写转换工具，支持多种格式：大写、小写、标题、驼峰、蛇形、短横线等。
