---
name: sausg
description: SAUSG（结构通用分析与设计软件）自动计算与操作工具。用于弹塑性计算、非线性分析、动力时程分析、隔震减震设计、钢结构分析等。当用户提及 SAUSG、SAUSAGE、OpenSAUSG、SAUSGDelta、SAUSGJG、SAUSGPI、SAUSGZeta 等相关软件，或要求进行弹塑性计算、读取计算结果时使用此技能。
---

# SAUSG 自动计算与操作指南

SAUSG（结构通用分析与设计软件）是一款专业的结构工程分析与设计软件，包含多个专业模块。

## 触发关键词

当用户提及以下内容时，自动使用本 Skill：
- 弹塑性计算、非线性分析、动力时程分析
- SAUSG、SAUSAGE 相关操作
- 隔震、减震、加固、钢结构分析
- 读取/查看计算结果

## 快速开始

### 命令格式

```bash
# 用指定模块打开模型（默认 OpenSAUSG）
python <skill>/scripts/sausg_open.py <模型路径> [模块名称] [软件目录]

# 运行结构计算
python <skill>/scripts/sausg_calc.py <模型路径> [软件目录] [--no-cleanup]

# 读取计算结果
python <skill>/scripts/sausg_result.py <模型目录> [模型名称]
```

> **注**：`<skill>` 指 `.claude/skills/sausg`

### 模块名称

| 输入 | 模块 |
|-----|------|
| open, 通用 | OpenSAUSG.exe |
| sausage, 非线性 | SAUSAGE.exe |
| delta, 钢结构 | SAUSGDelta.exe |
| jg, 加固 | SAUSGJG.exe |
| pi, 隔震 | SAUSGPI.exe |
| zeta, 减震 | SAUSGZeta.exe |

### 示例

```bash
# 用隔震模块打开模型
python .claude/skills/sausg/scripts/sausg_open.py Project/Model.ssg 隔震

# 运行计算
python .claude/skills/sausg/scripts/sausg_calc.py Project/Model.ssg

# 读取结果
python .claude/skills/sausg/scripts/sausg_result.py Project/Model Model
```

### 自然语言

用户可以直接说：
- "用隔震软件打开模型" → 调用 SAUSGPI.exe
- "运行非线性计算" → 调用 SAUSAGE.exe
- "读取P2的结果" → 调用结果读取脚本

## 软件信息

- **默认安装目录**: D:\SAUSG2027
- **计算程序**: FeaCalc64S.exe / FeaCalcOMP64.exe / FeaCalc64.exe
- **下载**: https://product.pkpm.cn/productDetails?productId=56

## 功能说明

### 1. 自动搜索软件

系统自动搜索 D 盘及其他盘符下的 SAUSGXXXX 文件夹，提取版本号并选择最新版本。

### 2. 计算清理

默认会清理模型目录下的旧结果文件（.BCR, .BEM, .MSG 等）和结果文件夹（StaticResult/, EarthQuakeResult/, DesignResult/）。使用 `--no-cleanup` 可跳过清理。

### 3. 结果输出

计算完成后自动输出：
- 基本周期 (T1, T2, T3...)
- 圆频率 (ω) 和频率 (f)
- 楼层总重、底部反力
- 基底剪力（含剪重比）
- 最大层间位移角
- 计算报告文件名

### 4. 批量计算

必须**顺序执行**，等待前一个计算完成后再启动下一个。系统会自动检测是否有计算程序正在运行。

## 注意事项

1. **禁止同时运行多个计算** - 系统会检测并阻止
2. **计算时间较长** - 请耐心等待，结果保存在模型同目录下
3. **编码兼容** - 支持 cmd 和 PowerShell，自动处理中文编码