---
name: skill-dedup-scanner
description: 扫描已安装的技能，检测重复和命名冲突。发现可能导致模型混淆的相似技能。适用于发布新技能前或排查触发冲突。支持中英文（自动检测或 --lang 参数切换）。
---

# 技能查重扫描仪 🔍

检测可能导致模型混淆的重复或相似技能。

## 使用场景

- 发布新技能前检查
- 技能触发异常时排查
- 审查现有技能集合
- 解决命名冲突问题
- 检查相似的技能名称/描述

## 使用方法

### 基础扫描

```bash
# 自动检测语言
python3 scripts/main.py ~/.openclaw/workspace/skills/

# 指定语言
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang en
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang zh
```

### 高级选项

```bash
# 自定义阈值 (0-1)
python3 scripts/main.py ~/.openclaw/workspace/skills/ --threshold 0.8

# 输出到文件
python3 scripts/main.py ~/.openclaw/workspace/skills/ -o audit_report.md

# JSON 格式输出
python3 scripts/main.py ~/.openclaw/workspace/skills/ --json

# 详细模式
python3 scripts/main.py ~/.openclaw/workspace/skills/ -v
```

### 选项说明

| 选项 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--lang` | `-l` | 语言：en, zh, auto | auto |
| `--threshold` | `-t` | 相似度阈值 (0-1) | 0.7 |
| `--output` | `-o` | 输出文件路径 | 标准输出 |
| `--json` | `-j` | JSON 格式输出 | false |
| `--verbose` | `-v` | 详细输出 | false |

## 输出内容

生成详细报告，包含：
- 相似度评分（名称 + 描述）
- 冲突分析
- 可操作建议
- 安全/独特技能列表

## 相似度阈值

| 分数 | 级别 | 建议操作 |
|------|------|----------|
| > 0.85 | 🔴 高 | 考虑合并或重命名 |
| 0.7-0.85 | 🟡 中 | 明确描述区分 |
| < 0.7 | ✅ 安全 | 无需操作 |

## 语言支持

- **英文** (`--lang en`)
- **中文** (`--lang zh`)
- **自动检测** (`--lang auto`) - 根据系统语言自动选择

## 使用示例

### 示例 1: 快速扫描

```bash
$ python3 scripts/main.py ~/.openclaw/workspace/skills/
🔍 扫描目录：/home/user/.openclaw/workspace/skills
📦 技能总数：15

✅ 未发现重复技能

所有技能的名称和描述都有明显差异，无需优化。
```

### 示例 2: 查找冲突

```bash
$ python3 scripts/main.py ~/.openclaw/workspace/skills/ --threshold 0.6
🔍 扫描目录：/home/user/.openclaw/workspace/skills
📦 技能总数：15

⚠️ 发现 2 组相似技能

### 1. 🔴 高相似度警告

**技能 A:** `tushare-finance`
**技能 B:** `stock-analyzer`

**相似度:** 85%

**问题分析:**
- 名称相似度：60%
- 描述相似度：85%

**建议:**
- 在 description 中明确区分定位
- 修改名称使其更清晰
```

## 项目结构

```
skill-auditor/
├── scripts/
│   ├── main.py                 # 主入口
│   ├── skill_scanner.py        # 技能扫描器
│   ├── similarity_checker.py   # 相似度检查器
│   ├── report_generator.py     # 报告生成器
│   └── locale_loader.py        # 多语言支持
├── locales/
│   ├── en.json                 # 英文翻译
│   └── zh.json                 # 中文翻译
├── references/
│   └── best_practices.md       # 技能命名最佳实践
└── output/                     # 生成的报告
```

## 依赖要求

- Python 3.7+
- PyYAML (`pip install pyyaml`)

## 许可证

MIT
