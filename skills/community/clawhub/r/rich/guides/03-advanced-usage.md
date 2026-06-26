# 高级用法

**适用场景**: 掌握 Rich 基础后，学习语法高亮、日志集成、Live 动态渲染、自定义主题等高级功能

---

## 一、语法高亮（Syntax）

Rich 使用 Pygments 对代码进行语法高亮。

**AI 执行说明**: AI 可以将代码片段以语法高亮形式输出

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()

# 高亮显示代码字符串
code = '''
def fibonacci(n: int) -> int:
    """计算斐波那契数列第 n 项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

### 从文件读取并高亮

```python
from rich.syntax import Syntax
from rich.console import Console

console = Console()

# 直接读取并高亮文件
syntax = Syntax.from_path(
    "my_script.py",
    theme="dracula",
    line_numbers=True,
    line_range=(1, 50),   # 只显示第 1-50 行
    highlight_lines={10, 20, 30}  # 高亮特定行
)
console.print(syntax)
```

### 常用主题

```python
# 可用主题（Pygments 主题）:
# "monokai"       - 深色，最流行
# "dracula"       - 深色紫色系
# "github-dark"   - GitHub 暗色
# "solarized-dark" - Solarized 暗色
# "friendly"      - 浅色

# 列出所有可用主题
from pygments.styles import get_all_styles
for style in get_all_styles():
    print(style)
```

---

## 二、日志集成（Logging）

将 Rich 集成到 Python 标准 logging 系统中。

**AI 执行说明**: AI 可以将现有日志代码替换为 Rich 日志格式

```python
import logging
from rich.logging import RichHandler

# 配置使用 Rich Handler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("应用启动")
log.warning("磁盘空间不足: %s%%", 85)
log.error("连接数据库失败")

try:
    1 / 0
except ZeroDivisionError:
    log.exception("发生异常")
```

### 高级日志配置

```python
import logging
from rich.logging import RichHandler
from rich.console import Console

# 自定义 Console（写入文件）
file_console = Console(file=open("app.log", "w"))

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s: %(message)s",
    handlers=[
        RichHandler(
            rich_tracebacks=True,       # 美化异常追踪
            tracebacks_show_locals=True, # 显示局部变量
            show_time=True,              # 显示时间
            show_path=True,              # 显示文件路径
            markup=True,                 # 启用标记语法
        ),
        logging.FileHandler("app.log")
    ]
)
```

---

## 三、美化异常追踪（Traceback）

**AI 执行说明**: AI 可以在项目中安装 Rich traceback 替换默认异常输出

```python
from rich.traceback import install

# 全局安装（替换 Python 默认异常输出）
install(
    show_locals=True,   # 显示局部变量值
    width=120,          # 设置输出宽度
    extra_lines=5,      # 显示额外上下文行数
    theme="monokai",    # 代码高亮主题
    word_wrap=True,     # 启用自动换行
)

# 之后所有未捕获的异常都会以 Rich 格式显示
def process_data(data: dict):
    result = data["missing_key"]  # KeyError
    return result

process_data({})
```

### 手动捕获并渲染异常

```python
from rich.console import Console
console = Console()

try:
    x = 1 / 0
except ZeroDivisionError:
    console.print_exception(show_locals=True)
```

---

## 四、Live 动态渲染

`Live` 允许在终端中动态更新内容，适用于实时监控、仪表板等场景。

**AI 执行说明**: AI 可以将静态输出改造为动态实时显示

```python
from rich.console import Console
from rich.live import Live
from rich.table import Table
import time

console = Console()

def generate_table(iteration: int) -> Table:
    """生成动态更新的表格"""
    table = Table(title=f"实时监控 - 迭代 {iteration}")
    table.add_column("服务")
    table.add_column("状态")
    table.add_column("响应时间")

    import random
    services = ["API 服务", "数据库", "缓存", "消息队列"]
    for service in services:
        status = "[green]正常[/green]" if random.random() > 0.2 else "[red]异常[/red]"
        latency = f"{random.randint(10, 200)}ms"
        table.add_row(service, status, latency)

    return table

with Live(generate_table(0), refresh_per_second=2) as live:
    for i in range(10):
        time.sleep(0.5)
        live.update(generate_table(i))
```

### Live 与 Progress 结合

```python
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
import time

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True,  # 完成后清除进度条
) as progress:
    task = progress.add_task("下载数据...", total=100)
    for i in range(100):
        time.sleep(0.05)
        progress.advance(task)
```

---

## 五、布局（Layout）

`Layout` 用于创建多区域布局，适合构建复杂 TUI 界面。

```python
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel

console = Console()
layout = Layout()

# 垂直分割（上下）
layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="footer", size=3),
)

# 水平分割（左右）
layout["body"].split_row(
    Layout(name="sidebar", size=30),
    Layout(name="main"),
)

# 填充内容
layout["header"].update(Panel("[bold]应用标题[/bold]", style="white on blue"))
layout["sidebar"].update(Panel("导航菜单\n- 首页\n- 设置\n- 帮助"))
layout["main"].update(Panel("主内容区域"))
layout["footer"].update(Panel("[dim]状态: 就绪[/dim]"))

console.print(layout)
```

---

## 六、树形结构（Tree）

```python
from rich.console import Console
from rich.tree import Tree
from rich import print

console = Console()

# 创建目录树
tree = Tree("[bold]项目结构[/bold]")

src = tree.add("[bold cyan]src/[/bold cyan]")
src.add("[green]main.py[/green]")
src.add("[green]config.py[/green]")

tests = src.add("[bold cyan]tests/[/bold cyan]")
tests.add("[green]test_main.py[/green]")
tests.add("[green]test_config.py[/green]")

utils = src.add("[bold cyan]utils/[/bold cyan]")
utils.add("[green]helpers.py[/green]")
utils.add("[green]validators.py[/green]")

tree.add("[yellow]README.md[/yellow]")
tree.add("[yellow]pyproject.toml[/yellow]")

console.print(tree)
```

---

## 七、Columns 列布局

```python
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

console = Console()

# 多列显示
items = [
    Panel("Python", style="cyan"),
    Panel("JavaScript", style="yellow"),
    Panel("Rust", style="red"),
    Panel("Go", style="blue"),
    Panel("TypeScript", style="blue"),
    Panel("Java", style="magenta"),
]

console.print(Columns(items))

# 列布局文本
languages = ["Python", "JavaScript", "Rust", "Go", "TypeScript", "Java", "C++", "Kotlin"]
console.print(Columns(languages, padding=(0, 2), equal=True))
```

---

## 八、自定义主题（Theme）

**AI 执行说明**: AI 可以为项目创建统一的样式主题

```python
from rich.console import Console
from rich.theme import Theme

# 定义自定义主题
custom_theme = Theme({
    "info": "bold cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold white on blue",
    "dim.text": "dim",
    "url": "underline blue",
})

console = Console(theme=custom_theme)

# 使用自定义样式
console.print("[info]信息[/info]: 服务已启动")
console.print("[warning]警告[/warning]: 配置文件未找到，使用默认配置")
console.print("[error]错误[/error]: 无法连接数据库")
console.print("[success]成功[/success]: 数据导出完成")
console.print("[highlight]重要提示[/highlight]")
```

---

## 九、导出 HTML 和 SVG

```python
from rich.console import Console

# 创建记录模式的 Console
console = Console(record=True, width=100)

console.print("[bold red]Rich 输出演示[/bold red]")
console.print("[green]这是一段绿色文本[/green]")

from rich.table import Table
table = Table("列1", "列2", "列3")
table.add_row("A", "B", "C")
table.add_row("D", "E", "F")
console.print(table)

# 导出为 HTML
html = console.export_html(inline_styles=True)
with open("output.html", "w") as f:
    f.write(html)

# 导出为 SVG（更精准的截图）
svg = console.export_svg(title="Rich 演示")
with open("output.svg", "w") as f:
    f.write(svg)

# 导出为纯文本
text = console.export_text()
with open("output.txt", "w") as f:
    f.write(text)
```

---

## 十、自定义进度条

```python
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
    SpinnerColumn,
    FileSizeColumn,
    TotalFileSizeColumn,
    TransferSpeedColumn,
    DownloadColumn,
)
import time

# 完整自定义进度条
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
) as progress:
    task = progress.add_task("[cyan]处理文件...", total=200)
    for _ in range(200):
        time.sleep(0.01)
        progress.advance(task)

# 文件下载进度条
with Progress(
    TextColumn("[bold blue]{task.fields[filename]}"),
    BarColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
    TimeRemainingColumn(),
) as progress:
    task = progress.add_task(
        "下载中",
        total=1024 * 1024,  # 1MB
        filename="large_file.zip"
    )
    for _ in range(1024):
        time.sleep(0.001)
        progress.advance(task, 1024)
```

---

## 十一、Status 状态指示器

```python
from rich.console import Console
from rich.status import Status
import time

console = Console()

# 显示加载状态
with console.status("[bold green]正在连接数据库...", spinner="dots") as status:
    time.sleep(2)
    status.update("[bold blue]正在加载数据...")
    time.sleep(1)
    status.update("[bold yellow]正在处理...")
    time.sleep(1)

console.print("[bold green]操作完成！[/bold green]")

# 可用的 spinner 名称:
# "dots", "dots2", "dots12", "line", "pipe",
# "star", "star2", "flip", "arrow", "bouncingBar",
# "bouncingBall", "clock", "earth", "moon"
```

---

## 十二、Prompt 交互输入

```python
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt

# 文本输入（带默认值）
name = Prompt.ask("请输入你的姓名", default="匿名用户")

# 带选择限制的输入
color = Prompt.ask(
    "选择颜色",
    choices=["red", "green", "blue"],
    default="blue"
)

# 整数输入
age = IntPrompt.ask("请输入年龄", default=18)

# 浮点数输入
score = FloatPrompt.ask("请输入分数", default=0.0)

# 确认提示
if Confirm.ask("确认执行操作吗？"):
    print("执行操作")
else:
    print("已取消")

# 密码输入
from rich.prompt import Prompt
password = Prompt.ask("请输入密码", password=True)
```

---

## 十三、与 print 和 pprint 集成

**AI 执行说明**: AI 可以在入口文件中一次性替换所有输出函数

```python
# 在项目入口文件顶部添加
from rich import pretty, traceback

# 替换 pprint
pretty.install()

# 替换 traceback
traceback.install(show_locals=True)

# 可选: 替换 print（注意可能影响性能）
# from rich import print  # 不建议全局替换，仅在需要时局部使用
```

---

## 常用参数速查

| 功能 | 类/函数 | 关键参数 |
|------|---------|---------|
| 基本输出 | `Console.print()` | `style`, `justify`, `end`, `highlight` |
| 表格 | `Table` | `title`, `box`, `show_header`, `show_lines` |
| 进度条 | `Progress` | `transient`, `auto_refresh`, `refresh_per_second` |
| 面板 | `Panel` | `title`, `subtitle`, `border_style`, `box` |
| 语法高亮 | `Syntax` | `theme`, `line_numbers`, `line_range` |
| 实时更新 | `Live` | `refresh_per_second`, `transient`, `auto_refresh` |
| 日志 | `RichHandler` | `rich_tracebacks`, `show_time`, `show_path` |
| 主题 | `Theme` | 自定义样式字典 |

---

## 完成确认

### 检查清单
- [ ] 学会使用语法高亮显示代码
- [ ] 将 Rich Handler 集成到 logging
- [ ] 使用 Traceback 替换默认异常输出
- [ ] 使用 Live 创建动态更新界面
- [ ] 创建自定义主题
- [ ] 使用 Prompt 实现交互式输入

### 下一步
如遇到问题，查看 [常见问题](../troubleshooting.md)
