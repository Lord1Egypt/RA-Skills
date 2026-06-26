# 虚拟用户 Skill（场景库版）

> 🎭 基于真实用户场景库的虚拟用户对话生成工具

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-username/virtual-user-skill)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## 🌟 快速开始

### 1. 安装依赖

```bash
cd virtual_user_skill
pip install -r requirements.txt
```

### 2. 初始化密钥

```bash
python src/encrypt.py
```

首次运行会自动生成加密密钥并保存在 `~/.virtual_user/.key`

### 3. 准备场景库数据

```bash
# 将你的 Excel 数据转换为加密格式
python scripts/prepare_data.py your_data.xlsx
```

### 4. 运行技能

```bash
# 基本用法
python src/main.py "用户预订机票时最关心什么？"

# 自动选择前 3 个用户类型
python src/main.py "用户预订机票时最关心什么？" --auto
```

---

## 📖 完整文档

详细使用说明请查看 [SKILL.md](SKILL.md)

---

## 🎯 功能特性

- ✅ **真实场景驱动** - 基于 1859+ 条真实用户研究数据
- ✅ **智能检索** - 向量化搜索最相关场景
- ✅ **多样化生成** - 自动生成 10 个虚拟用户类型
- ✅ **灵活选择** - 支持手动选择/反选用户类型
- ✅ **多轮对话** - 深度访谈和产品测评
- ✅ **报告输出** - 自动生成 Markdown 报告
- ✅ **数据加密** - 场景库加密存储，保护隐私

---

## 🔧 配置

编辑 `config.yaml` 自定义技能行为：

```yaml
defaults:
  user_types_count: 10      # 生成的用户类型数量
  auto_select_count: 3      # 自动选择的数量
  search_top_k: 20          # 搜索场景数量
```

---

## 📁 项目结构

```
virtual_user_skill/
├── src/                    # 源代码
├── data/                   # 数据文件（加密）
├── scripts/                # 工具脚本
├── examples/               # 使用示例
├── tests/                  # 单元测试
├── SKILL.md               # 技能文档
├── README.md              # 本文件
├── config.yaml            # 配置文件
└── requirements.txt       # 依赖
```

---

## 💡 使用场景

### 1. 用户访谈
```bash
python src/main.py "用户对机票预订流程有什么痛点？"
```

### 2. 产品测评
```bash
python src/main.py "评估这个新的退改签方案"
```

### 3. 需求验证
```bash
python src/main.py "用户是否需要动态规划提醒功能？"
```

---

## 🔒 数据安全

场景库数据使用 Fernet 对称加密：
- 密钥保存在 `~/.virtual_user/.key`（不提交到 Git）
- 加密数据文件可安全提交到 GitHub
- 运行时自动解密，不暴露原始数据

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
