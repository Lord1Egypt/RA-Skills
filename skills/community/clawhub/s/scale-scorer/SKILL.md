---
name: scale-scorer
description: "自动识别量表维度（前缀+数字命名），计算各维度均分，支持反向计分和缺失处理。输入支持 Excel (.xlsx) 和 CSV"
argument-hint: "\"<数据文件路径>\" [--reverse 反向计分.json] [--min 1] [--max 5]"
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash, Read, Write, Grep
model: sonnet
effort: medium
---

# 量表维度均分自动计算工具

## 功能说明
针对心理学问卷/量表原始数据，自动执行以下操作：
1. **智能识别维度**：根据列名规则（维度前缀 + 末尾数字，如 `T1RZTD1`、`T1RZTD2`）自动将题目分组为不同维度（至少包含 2 题）
2. **反向计分处理**：支持通过配置文件指定需反向计分的题目，自动转换为正值（默认量表范围 1–5，可自定义）
3. **维度均分计算**：对每个维度内的题目计算平均值，缺失值≤50%时用剩余题目均值替代，超阈则标记为缺失
4. **输出结构化结果**：在原始数据右侧追加每个维度的均分列（列名为维度前缀，如 `T1RZTD`），不影响原有数据

支持输入格式：Excel（`.xlsx`）和 CSV（`.csv`），输出格式与输入一致，自动生成 `_scored` 文件。

## 使用方式

### 命令行调用（基础用法）
```bash
python scale-scorer.py "数据文件路径"