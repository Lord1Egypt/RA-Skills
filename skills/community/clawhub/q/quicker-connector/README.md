# Quicker Connector - OpenClaw 技能

[中文](README.md) | [English](README_EN.md)

一个强大的 OpenClaw 技能，用于集成 Quicker 自动化工具。支持读取、搜索和执行 Quicker 动作，通过 AI 智能匹配自然语言需求。

[English README](README_EN.md) | [GitHub Releases](https://github.com/awamwang/quicker-connector/releases)

---

## ✨ 核心功能

- 📊 **双数据源支持** - CSV 文件和 SQLite 数据库
- 🔍 **多字段搜索** - 按名称、描述、类型、面板搜索
- 🧠 **智能匹配** - AI 驱动的自然语言理解
- 🎯 **精准执行** - 同步/异步执行，支持参数传递
- 📈 **统计信息** - 完整的动作分类和面板分布
- 🔧 **编码自适应** - 自动检测 UTF-8/GBK 等编码
- 📤 **JSON 导出** - 一键导出完整动作列表

---

## 🚀 快速开始

### 安装方式

#### 方式 1: 通过 GitHub Release 安装（推荐）

```bash
# 下载最新版本
wget https://github.com/awamwang/quicker-connector/releases/download/v1.2.0/quicker-connector-1.2.0.tar.gz

# 解压
tar -xzf quicker-connector-1.2.0.tar.gz

# 复制到 OpenClaw 技能目录
cp -r quicker-connector/* ~/.openclaw/workspace/skills/quicker-connector/

# 重启 OpenClaw Gateway
openclaw gateway restart
```

#### 方式 2: 通过 ClawHub 安装

```bash
clawhub install quicker-connector
```

#### 方式 3: 通过 Git 安装（开发者）

```bash
git clone https://github.com/awamwang/quicker-connector.git ~/.openclaw/workspace/skills/quicker-connector
openclaw gateway restart
```

---

## 📊 数据结构

### QuickerAction（动作数据类）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | str | 动作唯一标识符 |
| `name` | str | 动作名称 |
| `description` | str | 动作描述 |
| `action_type` | str | 动作类型（XAction/SendKeys/RunProgram 等） |
| `uri` | str | 执行 URI（quicker:runaction:xxx） |
| `panel` | str | 所属面板/分类 |
| `exe` | str | 关联程序名 |
| `create_time` | str | 创建时间 |
| `update_time` | str | 更新时间 |

### QuickerActionResult（执行结果）

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 是否执行成功 |
| `output` | str | 标准输出内容 |
| `error` | Optional[str] | 错误信息（失败时） |
| `exit_code` | Optional[int] | 退出码 |

---

## ⚙️ 配置选项

配置文件路径：`~/.openclaw/workspace/skills/quicker-connector/config.json`

```json
{
  "csv_path": "/root/.openclaw/workspace/data/QuickerActions.csv",
  "db_path": "C:\\Users\\Administrator\\AppData\\Local\\Quicker\\data\\quicker.db",
  "starter_path": "C:\\Program Files\\Quicker\\QuickerStarter.exe",
  "default_source": "csv",
  "auto_select_threshold": 0.8,
  "max_results": 10
}
```

### 设置说明

| 设置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `csv_path` | 字符串 | "" | Quicker 动作 CSV 文件路径 |
| `db_path` | 字符串 | "" | Quicker 数据库路径 |
| `starter_path` | 字符串 | "C:\\Program Files\\Quicker\\QuickerStarter.exe" | QuickerStarter.exe 路径 |
| `default_source` | 字符串 | "csv" | 默认数据源类型（csv/db） |
| `auto_select_threshold` | 浮点数 | 0.8 | 自动执行阈值（0.5-1.0） |
| `max_results` | 整数 | 10 | 最大返回结果数量 |

---

## 🔧 高级功能

### 导出为 JSON

将完整动作列表导出为 JSON 文件：

```python
connector.export_to_json("actions.json")
```

### 获取统计信息

```python
stats = connector.get_statistics()
print(f"总计: {stats['total']} 个动作")
print("类型分布:", stats['by_type'])
print("面板分布:", stats['by_panel'])
```

---

## 📄 许可证

MIT License - 详情见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献指南

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与开发。

---

## 🔗 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Quicker 官网](https://getquicker.net/)
- [ClawHub](https://clawhub.ai)
- [GitHub 仓库](https://github.com/awamwang/quicker-connector)
- [English Documentation](README_EN.md)

---

## 📝 版本历史

### v1.2.0 (2026-03-28)
- ✅ Advanced Skill Creator 优化
- ✅ 完整的 OpenClaw 规范兼容
- ✅ 自然语言触发支持
- ✅ 系统提示和思考模型
- ✅ 增强的设置选项
- ✅ GitHub 发布准备
- ✅ 完整的中文文档

---

**注意**: 本技能需要 Windows 操作系统和 Quicker 软件才能正常使用。
