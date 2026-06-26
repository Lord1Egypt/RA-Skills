# Sleep Quality Advisor（睡眠质量顾问）

## Overview
解析用户睡眠习惯，提供睡眠质量评估、改善建议和睡前仪式指导。

## Trigger
- 睡眠不好
- 失眠/入睡困难
- 睡眠质量
- 几点睡

## Workflow
1. 从用户描述中提取睡眠时间、质量和症状
2. 评估睡眠质量并打分
3. 给出针对性改善建议（按优先级排序）
4. 提供睡眠卫生基础原则

## Output
JSON: {sleepAssessment{}, recommendations[], sleepHygiene[], medicalAdvice{}}
