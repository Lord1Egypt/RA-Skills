# OpenClaw 技能分类与统计

> 增强版 OpenClaw 技能列表生成工具，采用模块化架构，支持多种输出格式和高级功能。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.1-orange.svg)](__init__.py)

## ✨ 功能特性

### 核心功能
- ✅ **多格式输出**：Markdown / JSON / HTML
- ✅ **分类统计**：9 大类 30+ 子类自动分类
- ✅ **状态图标**：✅ Ready / ⚠️ NeedSetup / ❌ Disabled
- ✅ **元数据**：版本号、作者、目录大小、安装时间
- ✅ **Web 界面**：交互式 HTML，支持搜索、筛选、排序

### 高级功能
- 🔄 **增量更新**：对比历史快照，只输出变化的技能
- 🤖 **自动分类**：基于规则的新技能自动分类
- 🔍 **重复检测**：发现功能重复的技能
- 🎯 **灵活过滤**：按状态、关键词、分类过滤
- 📦 **依赖检查**：检测技能的依赖是否满足
- 🌍 **自动翻译**：英文描述自动翻译为中文

## 🏗️ 架构设计

```
kt_skill_list_skill/
├── data/                      # 数据层
│   ├── openclaw.py            # OpenClaw CLI 封装
│   ├── filesystem.py          # 文件系统扫描
│   └── meta_reader.py         # 元数据读取
├── classifier/                # 分类层
│   ├── category_map.py        # 分类映射表
│   └── auto_classify.py       # 自动分类与学习
├── exporter/                  # 导出层
│   ├── markdown.py            # Markdown 导出
│   ├── json_exporter.py       # JSON 导出
│   └── html_exporter.py       # HTML 交互式导出
├── utils/                     # 工具层
│   ├── config.py              # 配置管理（可自定义输出目录）
│   ├── translator.py          # 翻译工具
│   └── diff.py                # 差异对比
├── generate_skill_list.py     # 主入口
└── __init__.py                # 包定义
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- OpenClaw 已安装并配置

### 安装

1. 将技能文件夹复制到 OpenClaw 技能目录：
```bash
cp -r kt_skill_list_skill ~/.openclaw/workspace/skills/
```

2. 或通过 OpenClaw 技能安装功能安装

### 使用方式

#### 基本用法
```bash
cd ~/.openclaw/workspace/skills/kt_skill_list_skill
python generate_skill_list.py
```

#### 指定输出格式
```bash
# Markdown（默认）
python generate_skill_list.py -f markdown

# JSON
python generate_skill_list.py -f json

# HTML（交互式界面）
python generate_skill_list.py -f html

# 全部格式
python generate_skill_list.py -f all
```

#### 过滤选项
```bash
# 只导出已激活技能
python generate_skill_list.py -F activated

# 只导出未激活技能
python generate_skill_list.py -F not_activated

# 按关键词搜索
python generate_skill_list.py -s "同花顺"

# 按分类过滤
python generate_skill_list.py -c "金融分析工具"
```

#### 高级选项
```bash
# 增量更新（只输出变化）
python generate_skill_list.py -i

# 检测重复技能
python generate_skill_list.py --check-duplicates

# 自定义输出目录
python generate_skill_list.py -o /path/to/output

# 简洁模式
python generate_skill_list.py -q
```

## ⚙️ 配置说明

### 输出目录配置

编辑 `utils/config.py` 自定义输出目录：

```python
# 默认输出目录
OUTPUT_DIR = os.path.join(USER_PROFILE, 'openclaw_out')

# 修改为其他目录
# OUTPUT_DIR = '/your/custom/path'
```

或通过命令行参数临时指定：
```bash
python generate_skill_list.py -o "D:\my_skills"
```

## 📊 输出示例

### Markdown 表格
```
| 序号 | 状态 | 技能名称 | 版本 | 描述 |
|------|------|----------|------|------|
| 1 | ✅ | 问财选A股 | 1.0.0 | A股智能选股 |
| 2 | ⚠️ | futuapi | 2.1.0 | 富途行情API |
```

### HTML 界面特性
- 🔍 实时搜索技能名称和描述
- 📂 按分类过滤
- 📊 按状态筛选
- 📈 实时统计面板
- 🎨 现代化 UI 设计

## 📁 输出文件

运行后生成以下文件：
- `已激活技能列表.md` - Markdown 格式的已激活技能列表
- `未激活技能列表.md` - Markdown 格式的未激活技能列表
- `技能列表.json` - 完整结构化 JSON 数据
- `已激活技能列表.html` - 交互式 HTML 网页
- `未激活技能列表.html` - 交互式 HTML 网页

## 📝 注意事项

1. 首次运行会自动创建缓存目录 `~/.openclaw/cache/skill_list/`
2. 快照默认 24 小时后过期，可强制全量更新
3. 分类学习数据会自动保存，用于后续新技能分类
4. HTML 界面支持响应式布局，手机和电脑都可正常使用

## 🔮 后续规划

- [ ] 支持导出到飞书文档
- [ ] 支持导出到 Notion
- [ ] 技能使用频率统计
- [ ] 技能依赖关系图
- [ ] 批量启用/禁用技能
- [ ] 自动更新检查

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 👤 作者

**Kun. Tao**

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📋 更新日志

详见 [CHANGELOG.md](CHANGELOG.md) 了解各版本的变更历史。
