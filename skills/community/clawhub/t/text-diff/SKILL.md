---
name: text-diff
description: Show line-by-line differences between two text files using Python's difflib. Supports unified, context, and side-by-side comparison modes with configurable context lines.
version: v1.0.0
tags: diff, text-comparison, developer-tools, file-comparison
---
# text-diff

Show line-by-line differences between two text files using Python's difflib.


## Usage Scenarios

### Scenario 1: Compare Configuration File Versions
**User input:** "比较两个版本的配置文件有什么不同。"

**Expected output:** Unified diff output showing added lines with `+`, removed lines with `-`, and context around changes for old_config.ini vs new_config.ini.

### Scenario 2: Side-by-Side Comparison
**User input:** "帮我并排对比这两份文案的差异。"

**Expected output:** Side-by-side layout with original on left, revised on right, differences highlighted. Changed lines shown aligned with their counterparts.

### Scenario 3: Check if Files Are Identical
**User input:** "检查这两个文件是不是完全一样。"

**Expected output:** Exit code 0 with message "Files are identical" if no differences found, or exit code 1 with detailed diff output showing all changes if files differ.
### Scenario 4: 合同版本对比
**User input:** "我把租房合同改了几个地方发给中介了，他怎么改的我没看出来，帮我对比一下两版合同的区别。"
**Expected output:** 对原始版和修改版进行逐行差异对比（diff），高亮增删改的部分。用颜色标注：红色删除、绿色新增、黄色修改。支持word/PDF/markdown格式。输出差异摘要：几处新增、几处删除、几处修改。针对合同中的关键条款（租金、违约责任、租期等）的变更做特别标注。

## Description

A utility skill for comparing two text files and displaying their differences in a readable format. Supports unified diff output and side-by-side comparison modes.

## Usage

```bash
# Show unified diff between two files
python ~/.openclaw/skills/text-diff/text_diff.py unified file1.txt file2.txt

# Show side-by-side comparison
python ~/.openclaw/skills/text-diff/text_diff.py side-by-side file1.txt file2.txt

# Show context diff (3 lines of context)
python ~/.openclaw/skills/text-diff/text_diff.py context file1.txt file2.txt

# Compare with custom context lines
python ~/.openclaw/skills/text-diff/text_diff.py unified file1.txt file2.txt -c 5
```

## Options

- `unified`: Show unified diff format (default)
- `context`: Show context diff format
- `side-by-side`: Show line-by-line comparison
- `-c, --context`: Number of context lines (default: 3)
- `-o, --output`: Save diff to file instead of stdout
- `--no-color`: Disable colored output

## Examples

```bash
# Basic unified diff
python ~/.openclaw/skills/text-diff/text_diff.py unified old.txt new.txt

# Side-by-side comparison with no colors (for piping)
python ~/.openclaw/skills/text-diff/text_diff.py side-by-side old.txt new.txt --no-color

# Save diff to file
python ~/.openclaw/skills/text-diff/text_diff.py unified old.txt new.txt -o diff.txt

# Compare with 10 lines of context
python ~/.openclaw/skills/text-diff/text_diff.py context old.txt new.txt -c 10
```

## Output Format

### Unified Diff
```
--- old.txt
+++ new.txt
@@ -1,5 +1,5 @@
 line 1
 line 2
-line 3 (removed)
+line 3 (added)
 line 4
 line 5
```

### Side-by-Side
```
OLD                          | NEW
---------------------------- | ----------------------------
line 1                       | line 1
line 2                       | line 2
line 3 (removed)             | line 3 (added)
line 4                       | line 4
```

## Exit Codes

- `0`: Files are identical
- `1`: Files differ
- `