# SKILL 执行结构审查模式

基于技能目录进行静态结构分析，识别规范性问题，输出优化方案。

## 审查检查清单

### SKILL.md 检查

| 检查项 | 标准 | 问题信号 |
|--------|------|----------|
| 行数 | < 500 行 | 正文过长，应拆分 |
| frontmatter | 有 name + description | 缺少必要字段 |
| name 一致性 | 与目录名相同 | name 与目录名不匹配 |
| description | 包含「能做什么」+「何时触发」 | 只写功能，未写触发场景 |
| 章节层级 | 最多三级 | 嵌套过深 |

### Agent 兼容性检查

| 检查项 | 标准 | 问题信号 |
|--------|------|----------|
| 工具名称绑定 | 不绑定特定 Agent 工具 | 出现「Qoder」「ClaudeCode」「OpenClaw」「Cursor」等硬编码 |
| description 中立性 | 不限定特定工具 | 「在 Qoder 中」「仅适用于 ClaudeCode」|
| API 依赖 | 不使用特定工具独有 API | 调用特定工具的私有接口、CLI 命令 |
| 路径耦合 | 不依赖特定工具目录结构 | 硬编码 `.qoder/`、`.claude/`、`.cursor/` 等路径 |
| 配置格式 | 不依赖特定工具配置格式 | 使用特定工具独有的配置文件格式 |
| 脚本依赖 | 脚本不依赖特定工具 CLI | 调用 `qoder`、`claude`、`cursor` 等命令 |

### 执行确定性检查

| 检查项 | 标准 | 问题信号 |
|--------|------|----------|
| 目录路径明确 | 指定具体目录名 | 「合适的目录」「相关目录」「目标目录」「适当的位置」 |
| 脚本引用明确 | 指明具体脚本文件 | 「运行脚本」「执行脚本」「相关脚本」（未跟具体脚本名） |
| 工具指令明确 | 明确工具/函数名 | 「使用工具」「调用工具」「合适的工具」（未跟具体工具名） |
| 程度副词控制 | 避免模糊程度词 | 「可能」「也许」「适当」「尽量」「大约」「左右」 |
| 工作目录明确 | 使用相对路径时指定工作目录 | 使用 `./scripts/`、`./dist/` 等相对路径但未说明工作目录 |

### scripts/ 检查

| 检查项 | 标准 | 问题信号 |
|--------|------|----------|
| 参数校验 | 有参数检查和用法提示 | 直接执行无提示 |
| 错误处理 | `set -euo pipefail` | 无错误处理 |
| 输出友好 | 有进度和结果提示 | 静默执行 |

### references/ 检查

| 检查项 | 标准 | 问题信号 |
|--------|------|----------|
| 文档命名 | 语义化命名 | `doc1.md`、`notes.md` |
| 内容类型 | 查阅类、参考类 | 核心工作流混入 |
| 加载时机 | 按需加载 | 所有内容都在 SKILL.md |

### assets/ 检查

| 检查项 | 标准 | 问题信号 |
|--------|------|----------|
| 文件类型 | 模板、图片、样板代码 | 脚本文件混入 |
| 引用方式 | 相对路径引用 | 绝对路径或外部链接 |

## 问题优先级定义

| 优先级 | 定义 | 示例 |
|--------|------|------|
| P0 | 阻塞性问题，影响技能正常使用 | SKILL.md 缺少 frontmatter、脚本无法执行 |
| P1 | 结构问题，影响可维护性 | SKILL.md 过长、资源文件位置错误 |
| P2 | 优化建议，提升质量 | 脚本缺少错误处理、文档命名不规范 |

## 常见问题与解决方案 {#拆分策略}

### 问题：SKILL.md 过长

**诊断**：正文超过 500 行，包含大量详细说明

**解决方案**：

| 内容类型 | 拆分目标 | 示例 |
|----------|----------|------|
| API 文档 | `references/api.md` | 接口列表、参数说明 |
| 工作流详解 | `references/workflows.md` | 多步骤流程、决策树 |
| 输出模板 | `references/structure-patterns.md` | 格式示例、代码模板 |
| 常见问题 | `references/faq.md` | Q&A、故障排查 |

**拆分原则**：
- SKILL.md 保留核心工作流（做什么、怎么做）
- references/ 存放详细信息（具体是什么）

### 问题：固定行为未脚本化 {#脚本化方案}

**诊断**：SKILL.md 中反复出现相同的确定性操作描述

**信号识别**：

```markdown
# 以下内容说明应该脚本化
1. 每次都需要执行相同的命令序列
2. LLM 需要反复推理相同的转换逻辑
3. 操作步骤固定，但容易遗漏
```

**解决方案**：

```bash
# 创建脚本
scripts/
├── convert.py      # 格式转换
├── validate.py     # 结构验证
└── process.py      # 数据处理
```

**Python 脚本模板**：

```python
#!/usr/bin/env python3
"""
{功能描述}

用法:
    {script}.py <参数>

示例:
    {script}.py input.txt
"""

import sys
from pathlib import Path


def main():
    # 参数校验
    if len(sys.argv) < 2:
        print("用法: {script}.py <参数>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    # 检查输入
    if not input_path.exists():
        print(f"❌ 错误: 文件不存在: {input_path}")
        sys.exit(1)
    
    # 核心逻辑
    # ...
    
    print("✅ 完成")


if __name__ == "__main__":
    main()
```

### 问题：资源文件位置错误 {#资源归位}

**诊断**：模板、图片等散落在根目录或错误位置

**解决方案**：

```bash
# 移动资源文件
mv template.docx assets/
mv diagram.png assets/
mv example/ assets/

# 更新 SKILL.md 中的引用
# 原：使用 template.docx 模板
# 改：使用 assets/template.docx 模板
```

### 问题：参考文档混入正文 {#文档分离}

**诊断**：SKILL.md 包含大量查阅类信息

**信号识别**：

```markdown
# 以下内容应移至 references/
- API 完整参数列表
- 错误码对照表
- 配置项说明
- Schema 定义
```

**解决方案**：

```bash
# 创建参考文档
mkdir -p references/

# 移动内容
# 1. 从 SKILL.md 剪切相关章节
# 2. 粘贴到 references/api.md
# 3. 在 SKILL.md 添加引用说明
```

### 问题：绑定特定 Agent 工具 {#Agent兼容性}

**诊断**：技能内容绑定特定 Agent 工具，无法跨工具使用

**信号识别**：

```markdown
# 以下内容说明绑定了特定工具

## SKILL.md 中
- 硬编码工具名：「在 Qoder 中执行」「使用 ClaudeCode 的...」
- 限定触发条件：「仅适用于 OpenClaw」
- 硬编码路径：「读取 .qoder/config.json」「写入 .claude/settings.json」

## 脚本中
- 调用特定工具 CLI：`qoder install`、`claude config`
- 依赖特定工具环境变量：`QODER_*`、`CLAUDE_*`
```

**解决方案**：

| 问题类型 | 修改前 | 修改后 |
|----------|--------|--------|
| 工具名硬编码 | 「在 Qoder 中执行」 | 「执行」或「在 Agent 中执行」 |
| description 限定 | 「仅适用于 ClaudeCode」 | 删除工具限定 |
| 路径硬编码 | `.qoder/skills/` | `<skill-root>/` 或使用相对路径 |
| CLI 依赖 | `qoder install` | 使用通用命令或参数化 |

**修复示例**：

```markdown
# 修改前
---
name: my-skill
description: 在 Qoder 中处理 PDF 文件，当用户提到 PDF 时触发。
---

读取 `.qoder/config.json` 获取配置...

# 修改后
---
name: my-skill
description: 处理 PDF 文件，当用户提到 PDF 时触发。
---

读取配置文件获取配置...
```

**脚本修复示例**：

```python
# 修改前：硬编码路径
config_path = Path.home() / ".qoder" / "config.json"

# 修改后：参数化或使用环境变量
import os
config_path = os.environ.get("SKILL_CONFIG_PATH", "config.json")

# 或使用相对路径
config_path = Path(__file__).parent.parent / "config.json"
```

**特殊情况处理**：

| 场景 | 处理方式 |
|------|----------|
| 必须引用工具特性 | 在 references/ 中说明兼容性要求 |
| 脚本需要检测环境 | 提供多工具兼容逻辑 |
| 配置文件格式不同 | 提供格式适配层 |

### 问题：提示词模糊，执行缺少确定性 {#执行确定性}

**诊断**：SKILL.md 中使用模糊指代，导致 LLM 执行时缺少确定性，容易跑偏

**信号识别**：

```markdown
# 目录路径模糊
❌ 将输出文件放到合适的目录
❌ 在相关目录中查找配置
❌ 保存到目标目录

# 脚本引用模糊
❌ 运行脚本处理数据
❌ 执行脚本进行转换
❌ 使用相关脚本完成操作

# 工具指令模糊
❌ 使用工具提取内容
❌ 调用合适的工具进行分析
❌ 使用相关工具生成报告

# 程度副词模糊
❌ 可能需要检查配置
❌ 尽量保持格式一致
❌ 适当调整参数
❌ 大约需要 5 个步骤
```

**解决方案**：

| 问题类型 | 修改前 | 修改后 |
|----------|--------|--------|
| 目录路径模糊 | 「将输出文件放到合适的目录」 | 「将输出文件保存到 `output/` 目录」 |
| 脚本引用模糊 | 「运行脚本处理数据」 | 「执行 `python3 scripts/process_data.py input.csv`」 |
| 工具指令模糊 | 「使用工具提取内容」 | 「调用 `extract_content()` 函数提取内容」 |
| 程度副词模糊 | 「可能需要检查配置」 | 「必须检查配置文件是否存在」 |
| 程度副词模糊 | 「尽量保持格式一致」 | 「保持格式一致」 |
| 工作目录缺失 | 「执行 `./scripts/xxx.py`」 | 「在技能根目录执行：`cd <skill-root> && python3 ./scripts/xxx.py`」 |

**修复示例**：

```markdown
# 修改前
## 执行流程

1. 将配置文件放到合适的目录
2. 运行脚本进行数据转换
3. 使用工具生成报告
4. 可能需要检查输出结果

# 修改后
## 执行流程

1. 将配置文件移动到 `config/` 目录：`mv config.yml config/`
2. 执行数据转换脚本：`python3 scripts/transform.py --input data.csv --output output/`
3. 调用 `generate_report()` 函数生成报告
4. 验证输出文件是否存在：检查 `output/report.md`
```

**检测规则**（脚本自动检测）：

| 类别 | 检测模式 | 示例 |
|------|----------|------|
| 目录路径 | `合适的目录`、`相关目录`、`目标目录`、`适当的位置` | 「放到合适的目录」 |
| 脚本引用 | `运行脚本`、`执行脚本`（后不跟具体脚本名） | 「运行脚本处理」 |
| 工具指令 | `使用工具`、`调用工具`（后不跟具体工具名） | 「使用工具提取」 |
| 程度副词 | `可能`、`也许`、`适当`、`尽量`、`大约`、`左右` | 「可能需要检查」 |
| 工作目录 | 使用相对路径但未说明工作目录 | 「执行 `./scripts/xxx.py`」但未说明在哪个目录执行 |

## 审查报告示例

```markdown
# 技能审查报告：pdf-editor

## 结构概览

| 目录/文件 | 状态 | 说明 |
|-----------|------|------|
| SKILL.md | ⚠️ | 623 行，过长 |
| scripts/ | ✅ | 3 个脚本 |
| references/ | ❌ | 不存在 |
| assets/ | ❌ | 不存在 |

## 问题清单

| 优先级 | 问题 | 建议 |
|--------|------|------|
| P1 | SKILL.md 623 行，超过 500 行限制 | 将 API 参数说明移至 references/api.md |
| P2 | 缺少 references/ 目录 | 创建并移入查阅类文档 |
| P2 | 模板文件 template.pdf 在根目录 | 移动到 assets/template.pdf |

## 优化方案

1. 创建目录结构
   mkdir -p references assets

2. 移动资源文件
   mv template.pdf assets/

3. 拆分 SKILL.md
   - 将「API 参数说明」章节移至 references/api.md
   - 在 SKILL.md 保留简要说明和引用

4. 验证结构
   bash scripts/validate.sh .
```
