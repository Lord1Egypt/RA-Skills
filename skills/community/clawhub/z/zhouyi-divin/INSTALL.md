# 安装与使用指南

## 📥 安装步骤

### 1️⃣ 确认目录结构

```
C:\Users\Administrator\.copaw\workspaces\default\
├── customized_skills/
│   └── zhouyi-divination/      ← 技能目录
│       ├── SKILL.md
│       ├── README.md
│       ├── INSTALL.md          ← 本文件
│       ├── start.bat           ← Windows 启动器
│       └── scripts/
│           ├── divine.py       ← 主程序
│           └── bazi.py         ← 八字模块
└── gua.bat                     ← 快捷启动器
```

### 2️⃣ 环境要求

- ✅ Python 3.8 或更高版本
- ✅ 无需安装任何第三方库（纯标准库）
- ✅ 支持 Windows / Linux / macOS

### 3️⃣ 验证安装

打开命令行，运行：

```bash
cd C:\Users\Administrator\.copaw\workspaces\default
python customized_skills\zhouyi-divination\scripts\divine.py --help
```

如果看到参数列表，说明安装成功！🎉

---

## 🚀 快速开始

### 方法一：双击启动

直接双击 `start.bat` 文件，按屏幕提示操作即可。

### 方法二：命令行调用

```bash
gua.bat "您的问题"
```

或者带八字信息：

```bash
gua.bat -q "问题" --birth-year 1990 --birth-month 5 --birth-day 15 --birth-hour 14
```

### 方法三：Python 直接运行

```bash
cd customized_skills\zhouyi-divination\scripts
python divine.py --question "问题"
```

---

## 🎯 使用示例

### 场景一：日常娱乐起卦

```bash
gua.bat "今天出门会顺利吗？"
```

### 场景二：结合八字问事业

```bash
gua.bat -q "今年适合换工作吗？" ^
  --birth-year 1990 ^
  --birth-month 5 ^
  --birth-day 15 ^
  --birth-hour 14 ^
  --gender 男
```

### 场景三：只排八字不看卦

```bash
gua.bat --mode bazi --birth-year 1990 --birth-month 5 --birth-day 15 --birth-hour 14
```

### 场景四：JSON 输出保存

```bash
gua.bat -q "问题" --json > result.json
```

---

## 🛠️ 故障排除

### Q1: 显示 "python 不是内部命令"

**解决方案：**
- 确保已安装 Python
- 将 Python 添加到系统 PATH 环境变量
- 或者使用完整路径：`C:\Python39\python.exe ...`

### Q2: 中文乱码

**解决方案：**
```bash
chcp 65001
set PYTHONIOENCODING=utf-8
```

### Q3: 导入错误 `ModuleNotFoundError: No module named 'bazi'`

**解决方案：**
- 确保在正确的目录下运行
- 检查 `scripts` 文件夹内是否有 `bazi.py`

---

## 💡 进阶技巧

### 组合多个问题

可以连续提问多个问题：

```bash
for %%i in ("事业" "财运" "感情") do (
    echo === 问：%%i ===
    gua.bat "今年的%%i运势如何？" --birth-year 1990
)
```

### 批量生成报告

```bash
python scripts/divine.py --json > report_2026.txt
```

---

## 📞 技术支持

如有问题，请联系小艺～ 💕

---

*最后更新：2026-03-28*