# 安装指南

**适用场景**: 首次使用 Rich，需要安装和配置环境

---

## 一、安装前准备

### 目标
确保系统具备运行 Rich 的基础环境

### 前置条件
- Python 3.8 或更高版本
- pip 包管理器
- 支持 ANSI 的终端（大多数现代终端均支持）

### 检查 Python 环境

**AI 执行说明**: AI 将自动检查你的 Python 版本

```bash
# 检查 Python 版本
python --version
# 或
python3 --version

# 检查 pip
pip --version
# 或
pip3 --version
```

**期望结果**:
- Python 3.8+ ✅
- pip 已安装 ✅

---

## 二、安装 Rich

### 方法1: 使用 pip 安装（推荐）

**AI 执行说明**: AI 可以直接执行安装命令

```bash
pip install rich
```

**验证安装**:
```bash
python -c "import rich; print(rich.__version__)"
```

**期望结果**:
```
13.9.4
```

### 方法2: 使用 conda 安装

```bash
conda install -c conda-forge rich
```

### 方法3: 从源码安装（最新开发版）

```bash
pip install git+https://github.com/Textualize/rich.git
```

### 方法4: 使用 uv 安装（推荐用于现代项目）

```bash
uv add rich
```

### 方法5: 添加到项目依赖

```bash
# 写入 requirements.txt
echo "rich>=13.0.0" >> requirements.txt
pip install -r requirements.txt
```

或在 `pyproject.toml` 中添加：
```toml
[project]
dependencies = [
    "rich>=13.0.0",
]
```

---

## 三、验证安装

### 运行 Rich 内置演示

**AI 执行说明**: AI 将运行演示命令确认安装成功

```bash
# 运行 Rich 自带演示（展示所有功能）
python -m rich
```

这将在终端中展示 Rich 的全部功能，包括颜色、表格、Markdown、代码高亮等。

### 代码验证

```python
# 新建 test_rich.py
from rich.console import Console

console = Console()
console.print("[bold green]Rich 安装成功！[/bold green] :white_check_mark:")
console.print(f"Rich 版本: [bold cyan]{__import__('rich').__version__}[/bold cyan]")
```

运行：
```bash
python test_rich.py
```

**成功标志**:
- 终端显示绿色加粗的"Rich 安装成功！"
- 显示 Rich 版本号

---

## 四、配置终端环境

### Windows 终端配置

Windows 10 版本 1903+ 的 Windows Terminal 默认支持 ANSI。
旧版 Windows CMD 需要额外配置：

```python
# 在代码中强制启用颜色
from rich.console import Console
console = Console(force_terminal=True)
```

或设置环境变量：
```bash
# PowerShell
$env:FORCE_COLOR = "1"

# CMD
set FORCE_COLOR=1
```

### 检查终端是否支持颜色

```python
from rich.console import Console
console = Console()
print(f"终端支持颜色: {console.is_terminal}")
print(f"颜色深度: {console.color_system}")
# 可能输出: None, "standard", "256", "truecolor"
```

### Jupyter Notebook 支持

```bash
pip install rich[jupyter]
```

```python
# Jupyter 中使用
from rich import print
print("[bold]Hello[/bold] Jupyter!")
```

---

## 五、可选依赖

### Markdown 渲染依赖

```bash
# 安装 Markdown 渲染支持
pip install rich[markdown]
```

### 完整依赖（所有功能）

```bash
pip install "rich[all]"
```

**包含内容**:
- `markdown-it-py`: Markdown 解析
- `pygments`: 语法高亮
- `typing_extensions`: 类型扩展

---

## 六、版本管理

### 查看已安装版本

```bash
pip show rich
```

**输出示例**:
```
Name: rich
Version: 13.9.4
Summary: Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
Home-page: https://github.com/Textualize/rich
Author: Will McGugan
License: MIT
```

### 升级 Rich

```bash
pip install --upgrade rich
```

### 安装特定版本

```bash
# 安装最新稳定版
pip install rich==13.9.4

# 安装最低版本约束
pip install "rich>=13.0.0,<14.0.0"
```

---

## 七、虚拟环境安装（最佳实践）

**AI 执行说明**: 建议在虚拟环境中安装 Rich

```bash
# 创建虚拟环境
python -m venv venv

# 激活（macOS/Linux）
source venv/bin/activate

# 激活（Windows CMD）
venv\Scripts\activate.bat

# 激活（Windows PowerShell）
venv\Scripts\Activate.ps1

# 安装 Rich
pip install rich

# 验证
python -c "from rich.console import Console; Console().print('[green]OK[/green]')"
```

---

## 完成确认

### 检查清单
- [ ] Python 3.8+ 已安装
- [ ] pip 可用
- [ ] Rich 已成功安装（`pip show rich` 显示版本）
- [ ] `python -m rich` 演示运行成功
- [ ] 终端支持颜色输出

### 下一步
继续阅读 [快速开始](02-quickstart.md) 学习 Rich 的基本用法
