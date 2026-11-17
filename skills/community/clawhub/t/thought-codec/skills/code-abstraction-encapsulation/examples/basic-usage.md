# Code Abstraction And Encapsulation Example / 代码与组件重构示例

## Scenario

A user has three scripts that parse similar product review JSON files, but each script hardcodes file paths and prints inside parsing functions.

用户有三个脚本都在解析相似的产品评价 JSON，但每个脚本都硬编码路径，并在解析函数里直接打印。

## Prompt

```text
Use the Code Abstraction And Encapsulation Skill.

Source:
- parse_amazon_reviews.py
- parse_shopify_reviews.py
- parse_manual_reviews.py

Problem:
- The parsing logic is duplicated.
- File paths are hardcoded.
- Core parsing functions print output directly.

Goal:
Extract a reusable parser module and keep printing in a separate CLI layer.

Output:
- Observed pattern
- Abstraction candidate
- Proposed interface
- Implementation steps
- Tests or verification
- Reusable engineering rule
```

## Expected Output Shape

- Identify shared parsing behavior and real domain differences.
- Propose a pure parsing function such as `parse_reviews(source, schema) -> list[Review]`.
- Keep CLI output in a separate command or presentation layer.
- Preserve existing behavior through fixtures or before/after sample outputs.
- Add a reusable rule about computation-presentation separation.

## Review Checks

- The abstraction does not hide important source-specific differences.
- Core parsing returns data instead of printing.
- Hardcoded paths become parameters.
- Behavior is verified before replacing call sites.
