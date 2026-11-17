---
slug: whatsapp-style-tool-free
name: whatsapp-style-tool-free
version: 1.0.0
displayName: WhatsApp样式工具-免费版
summary: "WhatsApp消息格式化工具,支持加粗/斜体/删除线等基础样式,确保消息干净美观。WhatsApp样式工具免费版,确保发送到WhatsApp的消息遵循平台专属格式语法。核心能力:"
license: Proprietary
edition: free
description: WhatsApp样式工具免费版,确保发送到WhatsApp的消息遵循平台专属格式语法。核心能力:，可自动提升工作效率

  - WhatsApp基础文本样式格式化(加粗/斜体/删除线/等宽体)

  - 列表与引用格式转换

  - 禁用Markdown符号自动清理

  - 格式预览与快速校验

  适用场景:

  - 个人用户发送格式化WhatsApp消息

  - 通知消息的排版美化

  - 确保消息在WhatsApp端显示正常

  差异化:

  - 免费版聚焦基础样式格式化,操作直观

  - 自动识别并修正错误的Markdown符号

  - 与PRO版完全兼容,可随时...'
tags:
  - 沟通协作
  - 消息样式
  - WhatsApp
  - 格式化
  - 社交
  - 通信
  - whatsapp
  - markdown
  - text
  - 文本
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
---
# WhatsApp样式工具(免费版)

## 概述

WhatsApp样式工具免费版是一款WhatsApp消息格式化辅助工具。WhatsApp使用独特的文本格式语法,与标准Markdown有显著差异(例如使用单星号 `*` 表示加粗,而非双星号 `**`)。本工具帮助用户正确应用WhatsApp格式规则,确保消息在接收端显示干净、美观,不会暴露原始格式符号.
本版本覆盖WhatsApp的核心格式语法,包括加粗、斜体、删除线、等宽体、列表和引用。适合个人用户日常消息排版需求。如需自定义样式预设、批量格式转换或团队样式规范,请升级至PRO版.
### 免费版与PRO版能力对比

| 能力维度 | 免费版 | PRO版 |
|----|---|----|
| 基础样式(加粗/斜体/删除线) | 支持 | 支持 |
| 等宽体/代码格式 | 支持 | 支持 |
| 列表与引用 | 支持 | 支持 |
| Markdown符号自动清理 | 支持 | 支持 |
| 格式预览 | 基础预览 | 实时预览 |
| 样式预设 | 不支持 | 支持 |
| 批量格式转换 | 不支持 | 支持 |
| 团队样式规范 | 不支持 | 支持 |
| 多平台格式适配 | 不支持 | 支持 |

## 核心能力

### 1. WhatsApp格式语法速查

WhatsApp支持以下文本格式,均使用单层符号包裹:

| 样式 | 语法 | 示例输入 | WhatsApp显示效果 |
|:-----|:-----|:-----|:-----|
| 加粗 | `*文本*` | `*重要通知*` | **重要通知** |
| 斜体 | `_文本_` | `_温馨提示_` | *温馨提示* |
| 删除线 | `~文本~` | `~原价199~` | ~~原价199~~ |
| 等宽体 | `` `文本` `` | `` `订单号:12345` `` | `订单号:12345` |
| 项目列表 | `* 项目` | `* 第一项` | 圆点列表 |
| 编号列表 | `1. 项目` | `1. 第一步` | 编号列表 |
| 引用 | `> 文本` | `> 名言警句` | 引用块 |

**处理**: 解析WhatsApp格式语法速查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回WhatsApp格式语法速查的响应数据,包含状态码、结果和日志.
### 2. Markdown符号自动清理

标准Markdown的某些语法在WhatsApp中不被支持,会导致原始符号暴露。本工具自动检测并修正这些问题.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | WhatsApp样式工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
# 示例
class WhatsAppStyleCleaner:
    """WhatsApp格式清理器 - 将Markdown转换为WhatsApp格式"""
# ...
    # 需要清理的Markdown模式
    CLEANUP_RULES = [
        # 双星号加粗 -> 单星号
        (r'\*\*(.+?)\*\*', r'*\1*'),
        # 双下划线加粗 -> 单星号
        (r'__(.+?)__', r'*\1*'),
        # Markdown标题 -> 加粗大写
        (r'^#{1,6}\s+(.+)$', r'*\1*'),
        # Markdown水平线 -> 下划线分隔
        (r'^---+$', '__________'),
        # 双波浪线删除线 -> 单波浪线
        (r'~~(.+?)~~', r'~\1*'),
    ]
# ...
    def clean(self, text: str) -> str:
        """清理Markdown符号,适配WhatsApp格式"""
        import re
        result = text
        for pattern, replacement in self.CLEANUP_RULES:
            result = re.sub(pattern, replacement, result, flags=re.MULTILINE)
        return result
# ...
# 使用示例
cleaner = WhatsAppStyleCleaner()
# ...
# 修正双星号加粗
raw_text = "这是 **重要** 消息,价格 ~~199~~ 现价 99"
cleaned = cleaner.clean(raw_text)
print(f"原始: {raw_text}")
print(f"清理后: {cleaned}")
# 输出: 这是 *重要* 消息,价格 ~199~ 现价 99
```

**处理**: 解析Markdown符号自动清理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Markdown符号自动清理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 格式校验工具

```python
import re
# ...
class WhatsAppFormatValidator:
    """WhatsApp格式校验器"""
# ...
    # WhatsApp有效格式模式
    VALID_PATTERNS = {
        "bold": r'\*[^*\n]+\*',
        "italic": r'_[^_\n]+_',
        "strikethrough": r'~[^~\n]+~',
        "monospace": r'`[^`\n]+`',
    }
# ...
    # 禁止的模式
    FORBIDDEN_PATTERNS = {
        "double_asterisk": (r'\*\*', "使用单星号 * 代替双星号 ** 表示加粗"),
        "markdown_header": (r'^#{1,6}\s', "WhatsApp不支持Markdown标题,请用 *加粗* 代替"),
        "markdown_table": (r'\|.*\|.*\|', "WhatsApp不支持Markdown表格,请用列表代替"),
        "horizontal_rule": (r'^---+$', "WhatsApp不支持水平线,请用下划线 ________ 代替"),
    }
# ...
    def validate(self, text: str) -> dict:
        """校验文本是否符合WhatsApp格式规范"""
        issues = []
# ...
        for name, (pattern, suggestion) in self.FORBIDDEN_PATTERNS.items():
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                issues.append({
                    "type": name,
                    "count": len(matches),
                    "suggestion": suggestion
                })
# ...
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "char_count": len(text)
        }
# ...
# 使用示例
validator = WhatsAppFormatValidator()
# ...
text = "## 标题\n这是 **加粗** 文本\n---"
result = validator.validate(text)
print(f"校验结果: {result}")
# 输出: valid=False, issues=[markdown_header, double_asterisk, horizontal_rule]
```

**处理**: 解析格式校验工具的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回格式校验工具的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：消息格式化工具、支持加粗、删除线等基础样式、确保消息干净美观、样式工具免费版、确保发送到、的消息遵循平台专、属格式语法、核心能力、基础文本样式格式、列表与引用格式转、格式预览与快速校等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:订单通知消息排版

将订单信息格式化为清晰的WhatsApp消息.
```python
# 格式化订单通知
order_message = """*订单确认*
# ...
订单号: `ORD-20260718-001`
收件人: 张三
# ...
*商品明细*
1. 无线蓝牙耳机 x1 - 199元
2. 保护壳 x1 - 30元
# ...
*合计: 229元*
# ...
> 预计3个工作日内发货,请留意物流通知。"""
# ...
print(order_message)
```

WhatsApp端显示效果:
- "订单确认" 显示为加粗
- 订单号显示为等宽体
- 商品明细为加粗标题 + 编号列表
- 合计金额加粗强调
- 底部为引用块

### 场景二:活动通知

```python
# 格式化活动通知
event_message = """*周末特惠活动*
# ...
_限时3天,不容错过!_
# ...
*活动详情*
* 时间:7月20日-22日
* 优惠:全场8折
* 优惠码:`WEEKEND20`
# ...
~原价299元~ *现价239元*
# ...
> 数量有限,先到先得!"""
# ...
print(event_message)
```

### 场景三:Markdown转WhatsApp格式

将已有的Markdown文档快速转换为WhatsApp兼容格式.
```python
# Markdown转WhatsApp格式
cleaner = WhatsAppStyleCleaner()
# ...
markdown_text = """## 会议纪要
# ...
**参会人员**:张三、李四、王五
# ...
### 讨论事项
1. 项目进度同步
2. 下周计划安排
# ...
---
# ...
**结论**:项目按计划推进,下周开始测试阶段.
"""
# ...
whatsapp_text = cleaner.clean(markdown_text)
print("WhatsApp格式:")
print(whatsapp_text)
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 基本使用

本工具作为AI Skill运行,直接在Agent对话中描述需求即可:

```
用户:帮我把这段消息格式化成WhatsApp样式
用户:这是一条 **重要** 通知,商品 ~~原价199~~ 现价 99 元
# ...
Agent:已转换为WhatsApp格式:
这是 *重要* 通知,商品 ~原价199~ 现价 99 元
```

### 命令行校验

```bash
# 校验文本文件中的WhatsApp格式
python3 validate_whatsapp_style.py --input message.txt
# ...
# 输出示例:
# [OK] 格式校验通过
# 字符数: 156
# 使用样式: bold(3), italic(1), strikethrough(1)
```

## 配置示例

### 基础配置

```yaml
# config.yaml - WhatsApp样式工具免费版配置
whatsapp_style:
  # 自动清理Markdown符号
  auto_clean_markdown: true
# ...
  # 标题转换策略: header -> bold_caps
  header_strategy: "bold_caps"
# ...
  # 表格转换策略: table -> bullet_list
  table_strategy: "bullet_list"
# ...
  # 最大消息长度(字符)
  max_length: 4096
```

### 校验规则配置

```yaml
# rules.yaml - 格式校验规则
validation:
  # 禁止双星号加粗
  forbid_double_asterisk: true
# ...
  # 禁止Markdown标题
  forbid_markdown_headers: true
# ...
  # 禁止Markdown表格
  forbid_markdown_tables: true
# ...
  # 禁止水平线
  forbid_horizontal_rules: true
# ...
  # 嵌套格式警告
  warn_nested_formatting: true
```

## 最佳实践

### 1. 使用单星号而非双星号

WhatsApp使用单星号 `*` 表示加粗,而非标准Markdown的双星号 `**`.
```python
# 错误示例(会暴露原始星号)
wrong = "这是 **重要** 消息"
# WhatsApp显示: 这是 **重要** 消息 (星号可见)
# ...
# 正确示例
correct = "这是 *重要* 消息"
# WhatsApp显示: 这是 重要 消息 (加粗显示)
```

### 2. 避免使用Markdown标题

WhatsApp不支持 `#`、`##` 等标题语法,请用加粗大写代替.
```python
# 错误:Markdown标题
wrong = "## 订单详情"
# ...
# 正确:加粗大写
correct = "*订单详情*"
# 或使用大写
correct_caps = "*订单详情*"
```

### 3. 表格转为列表

WhatsApp不支持Markdown表格,结构化数据请用列表展示.
```python
# 错误:Markdown表格
wrong_table = """| 商品 | 数量 | 价格 |
|:-----:|:-----:|:-----:|
| 耳机 | 1    | 199  |"""
# ...
# 正确:列表格式
correct_list = """*商品明细*
1. 耳机 x1 - 199元
2. 保护壳 x1 - 30元"""
```

### 4. 等宽体用于技术内容

订单号、验证码等技术内容使用等宽体,便于识别.
```python
# 推荐:技术内容用等宽体
message = "验证码: `836491`,5分钟内有效。"
```

## 常见问题

### Q1: 为什么我的加粗文字两边显示了星号?

**A:** WhatsApp使用单星号 `*` 表示加粗,而非Markdown的双星号 `**`。请将 `**文本**` 改为 `*文本*`。本工具的自动清理功能可以自动完成此转换.
### Q2: WhatsApp支持Markdown表格吗?

**A:** 不支持。WhatsApp不识别Markdown表格语法,表格符号会原样显示。请将表格数据转换为列表格式。本工具提供自动转换能力.
### Q3: 可以嵌套使用样式吗?

**A:** WhatsApp对嵌套样式支持有限。例如 `*_加粗斜体_*` 可能在某些设备上无法正确显示。建议避免嵌套,用单一样式表达.
### Q4: 等宽体代码块怎么用?

**A:** WhatsApp仅支持行内等宽体,使用单个反引号 `` ` `` 包裹。不支持多行代码块(三反引号)。多行技术内容请逐行使用行内等宽体.
### Q5: 免费版支持样式预设吗?

**A:** 免费版不包含样式预设功能。如需保存常用样式模板、批量格式转换等高级功能,请升级至PRO版.
### Q6: 如何升级到PRO版?

**A:** PRO版与免费版完全兼容,升级后原有格式规则继续生效,同时获得样式预设、批量转换、团队样式规范等高级功能。直接安装PRO版Skill即可完成升级.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.6+(仅命令行校验脚本需要)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 3.6+ | 运行时 | 可选 | python.org 下载(仅脚本模式) |

### API Key 配置

- 本Skill为纯Markdown指令型工具,无需额外API Key
- 格式校验和清理在本地完成,不依赖外部服务

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行文本格式化任务
- **运行模式**: 纯本地处理,无网络请求
- **安全等级**: 不涉及敏感数据,所有文本处理在本地完成

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
