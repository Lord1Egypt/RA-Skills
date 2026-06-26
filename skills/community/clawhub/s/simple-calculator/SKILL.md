---
name: simple-calculator
description: 简易命令行计算器，支持加减乘除和幂运算。Use this skill when user needs to do math calculations.
tags: [calculator, math, tool]
---

# Simple Calculator

## 概述

极简命令行计算器，支持基本四则运算和幂运算。

## 核心命令

```bash
python3 scripts/calc.py "6 + 2"
python3 scripts/calc.py "10 / 4"
python3 scripts/calc.py "2 ** 10"
```

## 支持运算

| 运算 | 符号 | 示例 |
|------|------|------|
| 加 | + | `5 + 3` → 8 |
| 减 | - | `10 - 4` → 6 |
| 乘 | * | `3 * 7` → 21 |
| 除 | / | `10 / 3` → 3.3333 |
| 幂 | ** | `2 ** 8` → 256 |
| 取余 | % | `10 % 3` → 1 |

## 验证

```bash
python3 scripts/calc.py "1 + 1"
# 输出: 2
```
