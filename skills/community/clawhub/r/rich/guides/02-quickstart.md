# 快速开始

**适用场景**: 已安装 Rich，开始学习基本用法

---

## 一、最简单的用法

### 使用 Rich 的 print 函数

**AI 执行说明**: AI 可以直接生成并运行以下代码

```python
from rich import print

# 使用标记语法添加样式
print("[bold magenta]Hello[/bold magenta], [green]World[/green]! :sparkles:")

# 渲染 Python 对象
print({"name": "rich", "awesome": True})

# 渲染列表
print([1, 2, 3, "four", "five"])
```

**期望效果**:
- "Hello" 显示为加粗品红色
- "World" 显示为绿色
- 闪光表情 ✨
- Python 对象以彩色语法高亮形式显示

---

## 二、Console 对象

`Console` 是 Rich 的核心对象，提供完整的终端输出控制。

**AI 执行说明**: AI 将使用 Console 对象管理所有输出

```python
from rich.console import Console

# 创建 Console 实例（通常创建一次，全局复用）
console = Console()

# 基本打印
console.print("Hello, World!")

# 带样式打印
console.print("[bold red]错误[/bold red]: 文件未找到")
console.print("[yellow]警告[/yellow]: 内存使用率较高")
console.print("[green]成功[/green]: 任务已完成")

# 打印到 stderr
error_console = Console(stderr=True)
error_console.print("[bold red]严重错误[/bold red]: 数据库连接失败")
```

### Console 常用参数

```python
# 禁用颜色（用于日志文件等纯文本场景）
console = Console(no_color=True)

# 强制设置终端宽度
console = Console(width=120)

# 写入文件
with open("output.txt", "w") as f:
    console = Console(file=f)
    console.print("写入文件的内容")

# 输出 HTML（用于保存截图）
console = Console(record=True)
console.print("[bold]Rich 输出[/bold]")
html = console.export_html()
```

---

## 三、标记语法（Markup）

Rich 使用类似 BBCode 的标记语法来设置样式。

### 基本样式

```python
from rich.console import Console
console = Console()

# 加粗、斜体、下划线
console.print("[bold]加粗文本[/bold]")
console.print("[italic]斜体文本[/italic]")
console.print("[underline]下划线文本[/underline]")
console.print("[strikethrough]删除线文本[/strikethrough]")

# 组合样式
console.print("[bold italic red]加粗红色斜体[/bold italic red]")
```

### 颜色设置

```python
# 使用颜色名称
console.print("[red]红色[/red]")
console.print("[green]绿色[/green]")
console.print("[blue]蓝色[/blue]")
console.print("[yellow]黄色[/yellow]")
console.print("[cyan]青色[/cyan]")
console.print("[magenta]品红[/magenta]")
console.print("[white]白色[/white]")

# 使用十六进制颜色
console.print("[#ff0000]十六进制红色[/#ff0000]")
console.print("[color(9)]ANSI 颜色9[/color(9)]")

# 设置背景色
console.print("[on red]红色背景[/on red]")
console.print("[white on blue]蓝底白字[/white on blue]")
```

### 转义标记

```python
# 如果需要显示方括号，使用转义
console.print("\\[不是标记]")
# 或使用 escape 函数
from rich.markup import escape
console.print(escape("[这是字面量方括号]"))
```

---

## 四、渲染表格

**AI 执行说明**: AI 可以根据数据自动生成表格代码

```python
from rich.console import Console
from rich.table import Table

console = Console()

# 创建表格
table = Table(title="城市人口统计")

# 添加列
table.add_column("城市", style="cyan", no_wrap=True)
table.add_column("省份", style="magenta")
table.add_column("人口（万）", justify="right", style="green")
table.add_column("GDP（亿）", justify="right")

# 添加行
table.add_row("上海", "上海市", "2489", "44652")
table.add_row("北京", "北京市", "2154", "40270")
table.add_row("广州", "广东省", "1882", "28839")
table.add_row("深圳", "广东省", "1756", "32388")

console.print(table)
```

### 表格样式

```python
from rich import box

# 不同边框样式
table = Table(box=box.ROUNDED)      # 圆角边框
table = Table(box=box.SIMPLE)       # 简单样式
table = Table(box=box.MINIMAL)      # 极简样式
table = Table(box=box.MARKDOWN)     # Markdown 表格格式
table = Table(show_header=False)    # 隐藏表头
table = Table(show_lines=True)      # 显示行分隔线
```

---

## 五、Panel 面板

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# 基本面板
console.print(Panel("Hello, World!"))

# 带标题的面板
console.print(Panel("任务执行完成", title="状态"))

# 带副标题的面板
console.print(Panel(
    "[green]所有测试通过[/green]",
    title="[bold]测试报告[/bold]",
    subtitle="pytest v7.4.0"
))

# 自定义边框样式
from rich import box
console.print(Panel("内容", border_style="blue"))
console.print(Panel("内容", box=box.DOUBLE))
```

---

## 六、进度条

### 使用 track 函数（最简单）

**AI 执行说明**: AI 可以为循环操作自动添加进度条

```python
from rich.progress import track
import time

# 最简单的进度条
for item in track(range(20), description="处理中..."):
    time.sleep(0.1)  # 模拟工作
```

### 使用 Progress 类（更多控制）

```python
from rich.progress import Progress
import time

with Progress() as progress:
    task1 = progress.add_task("[red]下载...", total=100)
    task2 = progress.add_task("[green]处理...", total=100)
    task3 = progress.add_task("[blue]上传...", total=100)

    while not progress.finished:
        progress.update(task1, advance=0.9)
        progress.update(task2, advance=0.6)
        progress.update(task3, advance=0.3)
        time.sleep(0.02)
```

---

## 七、美化打印 Python 对象

**AI 执行说明**: AI 可以安装 Rich 为默认的 pretty printer

```python
# 方式1: 使用 pprint 函数
from rich.pretty import pprint

my_dict = {
    "name": "Rich",
    "version": "13.9.4",
    "features": ["color", "table", "progress", "markdown"],
    "nested": {"key": "value", "number": 42}
}
pprint(my_dict)

# 方式2: 全局安装（替换 Python 内置 pprint）
from rich import pretty
pretty.install()

# 之后所有 Python REPL 输出都会自动美化
[1, 2, 3, "hello", {"key": "value"}]
```

---

## 八、Inspect 对象检查

```python
from rich import inspect

# 检查对象的属性和方法
class MyClass:
    """示例类"""
    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        """返回问候语"""
        return f"Hello, {self.name}!"

obj = MyClass("Rich")
inspect(obj, methods=True)
# 显示对象的所有属性、方法、类型信息和文档字符串
```

---

## 九、Markdown 渲染

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

markdown_text = """
# Rich 库介绍

Rich 是一个 **Python 库**，可以在终端中渲染 *富文本*。

## 主要功能

- 颜色和样式
- 表格渲染
- 进度条
- 代码高亮

## 代码示例

```python
from rich import print
print("[bold]Hello[/bold]!")
```

> 更多信息请访问 [Rich 文档](https://rich.readthedocs.io)
"""

md = Markdown(markdown_text)
console.print(md)
```

---

## 十、Rule 分隔线

```python
from rich.console import Console
from rich.rule import Rule

console = Console()

# 基本分隔线
console.print(Rule())

# 带标题的分隔线
console.print(Rule("分隔标题"))

# 自定义样式
console.print(Rule("[bold red]错误报告[/bold red]", style="red"))
console.print(Rule("完成", align="left"))
```

---

## 完成确认

### 检查清单
- [ ] 成功使用 `print` 函数输出彩色文本
- [ ] 创建了 `Console` 对象并使用标记语法
- [ ] 渲染了一个表格
- [ ] 添加了进度条
- [ ] 使用了 Panel 面板

### 下一步
继续阅读 [高级用法](03-advanced-usage.md) 学习语法高亮、日志集成、Live 动态渲染等高级功能
