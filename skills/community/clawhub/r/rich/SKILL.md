---
name: rich
description: Rich - Python 终端富文本和美化格式库
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: 🎨
    homepage: https://rich.readthedocs.io
---

# Rich - Python 终端富文本和美化格式库

## 技能概述

本技能帮助用户使用 Rich 在 Python 终端程序中输出美观的富文本内容，支持以下场景：
- **彩色输出**: 使用标记语法为文本添加颜色、样式和表情符号
- **表格渲染**: 创建美观的 ASCII 表格，支持多种边框样式
- **进度条**: 显示任务进度、下载进度、批量操作进度
- **Markdown 渲染**: 在终端中渲染 Markdown 文本
- **语法高亮**: 对代码片段进行语法高亮显示
- **结构化日志**: 替换标准 logging，输出格式化日志
- **Python 对象美化打印**: 替代 pprint，输出带颜色和折叠的对象

**GitHub**: https://github.com/Textualize/rich（56k+ Stars）

## 使用流程

AI 助手将引导你完成以下步骤：
1. 安装 Rich（如未安装）
2. 选择合适的组件（Console、Table、Progress 等）
3. 编写代码并查看效果
4. 根据需求调整样式和配置

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述终端输出需求时，AI 会：
- 自动生成对应的 Rich 代码片段
- 选择最合适的 Rich 组件（Table/Panel/Progress 等）
- 调整颜色、样式等视觉参数
- 集成到现有项目代码中
- 处理不同终端环境的兼容性问题
- 将 print/logging 替换为 Rich 输出

## 核心功能

- 支持 Console 对象统一管理终端输出
- 支持标记语法（Markup）设置文本样式
- 支持 16/256/True Color 颜色模式
- 支持 Table（表格）、Panel（面板）、Tree（树形）等渲染组件
- 支持 Progress（进度条）和 Live（动态刷新）
- 支持 Syntax（语法高亮）和 Markdown（文档渲染）
- 支持 Traceback（美化异常追踪）
- 支持 Inspect（对象检查）
- 支持 Logging Handler 集成
- 支持导出 HTML/SVG 终端截图

## 快速示例

```python
# 最简单的用法 - 使用全局 print
from rich import print
print("[bold magenta]Hello[/bold magenta], [green]World[/green]! :sparkles:")

# 使用 Console 对象
from rich.console import Console
console = Console()
console.print("[bold]Rich[/bold] is [italic green]awesome[/italic green]!")

# 美化打印 Python 对象
from rich import pretty
pretty.install()
{"name": "rich", "stars": 56000, "features": ["color", "table", "progress"]}
```

```python
# 渲染表格
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Python 包对比")
table.add_column("名称", style="cyan", no_wrap=True)
table.add_column("Stars", style="magenta")
table.add_column("用途", style="green")
table.add_row("rich", "56k+", "终端美化")
table.add_row("click", "14k+", "命令行解析")
table.add_row("typer", "13k+", "CLI 框架")
console.print(table)
```

```python
# 进度条
from rich.progress import track

for step in track(range(100), description="处理中..."):
    # 执行任务
    pass
```

## 安装要求

- Python 3.8 或更高版本
- pip 包管理器
- 支持 ANSI 转义码的终端（macOS Terminal、iTerm2、Windows Terminal、Linux 各终端）

## 许可证

MIT License

## 项目链接

- GitHub: https://github.com/Textualize/rich
- 官方文档: https://rich.readthedocs.io
- PyPI: https://pypi.org/project/rich/
- 示例代码: https://github.com/Textualize/rich/tree/master/examples
