# 依赖安装与配置指南

## 快速开始（推荐）

### 方式 1：使用 SkillHub 一键安装（最简单）

```bash
# 自动检测环境、安装所有依赖、配置 Python 环境
skillhub_install install_skill sql-dataviz
skillhub_install install_skill sql-report-generator
```

**优点：**
- ✓ 自动处理所有依赖
- ✓ 跨平台支持（Windows/Linux/macOS）
- ✓ 自动配置环境变量
- ✓ 一步完成

---

## 手动安装指南

### 前置要求

- **Python 3.8+**
- **pip 20.0+**
- **操作系统**：Windows / Linux / macOS

### 步骤 1：检查 Python 环境

```bash
# 检查 Python 版本
python3 --version

# 检查 pip 版本
pip3 --version

# 如果命令不存在，请先安装 Python
# Windows: https://www.python.org/downloads/
# Linux: sudo apt-get install python3 python3-pip
# macOS: brew install python3
```

### 步骤 2：安装核心依赖

```bash
# 升级 pip（推荐）
pip3 install --upgrade pip

# 安装核心依赖
pip3 install \
    matplotlib \
    seaborn \
    pandas \
    numpy \
    pillow
```

**预期输出：**
```
Successfully installed matplotlib-3.x.x seaborn-0.x.x pandas-2.x.x numpy-1.x.x pillow-x.x.x
```

### 步骤 3：安装可选依赖

#### 树状图支持（可选）

```bash
pip3 install squarify
```

#### 地理数据支持（可选）

```bash
pip3 install geopandas shapely
```

#### 交互式图表支持（可选）

```bash
pip3 install plotly
```

#### PDF 导出支持（可选）

```bash
pip3 install reportlab pypdf2
```

### 步骤 4：验证安装

```bash
# 验证核心依赖
python3 << 'EOF'
import matplotlib
import seaborn
import pandas
import numpy
from PIL import Image
print("✓ 所有核心依赖验证成功")
EOF

# 验证 sql-dataviz
python3 << 'EOF'
from sql_dataviz.charts import ChartFactory
factory = ChartFactory()
print("✓ sql-dataviz 验证成功")
EOF

# 验证 sql-report-generator
python3 << 'EOF'
from sql_report_generator.scripts.interactive_components import ReportBuilder
report = ReportBuilder()
print("✓ sql-report-generator 验证成功")
EOF
```

---

## 国内镜像加速（可选）

如果 pip 下载速度慢，可以使用国内镜像：

### 临时使用镜像

```bash
# 使用阿里云镜像
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ matplotlib seaborn pandas numpy pillow

# 使用清华大学镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib seaborn pandas numpy pillow

# 使用豆瓣镜像
pip3 install -i http://pypi.douban.com/simple matplotlib seaborn pandas numpy pillow
```

### 永久配置镜像

**Linux/macOS：**

```bash
# 编辑 ~/.pip/pip.conf
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
EOF
```

**Windows：**

```bash
# 编辑 %APPDATA%\pip\pip.ini
# 或创建 C:\Users\<username>\AppData\Roaming\pip\pip.ini

[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
```

---

## 常见问题排查

### Q1: "command not found: python3"

**解决方案：**

```bash
# 检查 Python 是否安装
which python3

# 如果未安装，请下载安装
# https://www.python.org/downloads/

# 或使用包管理器
# Ubuntu/Debian: sudo apt-get install python3
# CentOS: sudo yum install python3
# macOS: brew install python3
```

### Q2: "pip3: command not found"

**解决方案：**

```bash
# 使用 python3 -m pip 替代
python3 -m pip install --upgrade pip

# 或重新安装 Python
```

### Q3: "ModuleNotFoundError: No module named 'matplotlib'"

**解决方案：**

```bash
# 重新安装依赖
pip3 install --force-reinstall matplotlib

# 或检查 Python 环境
python3 -m pip list | grep matplotlib
```

### Q4: 权限错误 "Permission denied"

**解决方案：**

```bash
# 方式 1：使用 --user 标志
pip3 install --user matplotlib seaborn pandas numpy pillow

# 方式 2：使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

pip3 install matplotlib seaborn pandas numpy pillow
```

### Q5: 版本冲突

**解决方案：**

```bash
# 查看已安装的包
pip3 list

# 卸载冲突的包
pip3 uninstall matplotlib

# 重新安装指定版本
pip3 install matplotlib==3.7.1
```

---

## 虚拟环境设置（推荐用于生产环境）

### 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv dataviz_env

# 激活虚拟环境
# Linux/macOS:
source dataviz_env/bin/activate

# Windows:
dataviz_env\Scripts\activate
```

### 在虚拟环境中安装依赖

```bash
# 激活虚拟环境后
pip3 install matplotlib seaborn pandas numpy pillow squarify

# 验证
python3 -c "import matplotlib; print(matplotlib.__version__)"
```

### 导出依赖列表

```bash
# 生成 requirements.txt
pip3 freeze > requirements.txt

# 在其他环境中安装
pip3 install -r requirements.txt
```

---

## Docker 容器化（可选）

如果需要在 Docker 中运行，可以使用以下 Dockerfile：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 运行演示
CMD ["python3", "scripts/demo.py"]
```

**构建和运行：**

```bash
# 构建镜像
docker build -t sql-dataviz:latest .

# 运行容器
docker run -v $(pwd)/output:/app/output sql-dataviz:latest
```

---

## 性能优化

### 1. 使用 NumPy 加速

```bash
# 安装优化版本的 NumPy
pip3 install numpy --upgrade
```

### 2. 使用 Conda（可选）

```bash
# 安装 Conda
# https://docs.conda.io/projects/conda/en/latest/user-guide/install/

# 创建环境
conda create -n dataviz python=3.11

# 激活环境
conda activate dataviz

# 安装依赖
conda install matplotlib seaborn pandas numpy pillow
```

### 3. 使用 PyPy（可选，用于高性能）

```bash
# 安装 PyPy
# https://www.pypy.org/

# 使用 PyPy 安装依赖
pypy3 -m pip install matplotlib seaborn pandas numpy pillow
```

---

## 验证完整安装

运行完整演示脚本：

```bash
# 进入 sql-dataviz 目录
cd sql-dataviz

# 运行演示
python3 scripts/demo.py

# 查看输出
ls -la output/
```

**预期输出：**
```
✓ 所有演示完成！

输出文件位置: ./output/

生成的文件:
  - 24 种图表 PNG 文件
  - 表格、矩阵、切片器、导航按钮
  - demo_report.html (完整报告)
```

---

## 支持的 Python 版本

| Python 版本 | 支持状态 | 备注 |
|-----------|--------|------|
| 3.8 | ✓ 支持 | 最低要求 |
| 3.9 | ✓ 支持 | 推荐 |
| 3.10 | ✓ 支持 | 推荐 |
| 3.11 | ✓ 支持 | 最新稳定版 |
| 3.12 | ⚠ 测试中 | 部分依赖可能不兼容 |

---

## 依赖版本要求

| 包名 | 最低版本 | 推荐版本 | 用途 |
|------|--------|--------|------|
| matplotlib | 3.5.0 | 3.7.1+ | 图表绘制 |
| seaborn | 0.12.0 | 0.13.0+ | 统计图表 |
| pandas | 1.5.0 | 2.0.0+ | 数据处理 |
| numpy | 1.23.0 | 1.24.0+ | 数值计算 |
| pillow | 9.0.0 | 10.0.0+ | 图像处理 |
| squarify | 0.4.3 | 0.4.3+ | 树状图（可选） |
| geopandas | 0.12.0 | 0.13.0+ | 地理数据（可选） |
| plotly | 5.0.0 | 5.14.0+ | 交互图表（可选） |

---

## 获取帮助

- 📧 Email: support@example.com
- 💬 Discord: https://discord.gg/example
- 🐛 Issues: https://github.com/example/sql-dataviz/issues
- 📖 文档: https://docs.example.com

---

## 更新日志

- **2026-03-26** - 初始版本发布
- **2026-03-27** - 添加国内镜像加速指南
- **2026-03-28** - 添加 Docker 支持
