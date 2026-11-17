# OpenClaw 技能分类与统计

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.6-orange.svg)](CHANGELOG.md)
[![CI](https://github.com/kuntao2011/openclaw-skill-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/kuntao2011/openclaw-skill-manager/actions/workflows/ci.yml)

[English](README.md) | **简体中文**

> 增强版 OpenClaw 技能列表生成工具，采用模块化架构，支持多种输出格式和高级功能。

## ✨ 功能特性

### 核心功能
- ✅ **多格式输出**：Markdown / JSON / HTML
- ✅ **分类统计**：10 大类 48 子类自动归类，支持用户自定义覆盖层
- ✅ **状态图标**：✅ Ready / ⚠️ NeedSetup / ❌ Disabled
- ✅ **元数据**：版本号、作者、emoji、来源、主页链接
- ✅ **交互式 HTML 报告**：可搜索/筛选/表头排序的静态网页（无需服务器）

### 高级功能
- 🔄 **增量更新**：对比上次运行快照，只输出变化的技能
- 🤖 **自动分类**：基于规则的技能自动归类
- 🔍 **重复检测**：名称模式 + 描述相似度（SequenceMatcher）
- 🎯 **灵活过滤**：按状态、关键词、分类过滤
- 📦 **状态检测**：基于 OpenClaw CLI 输出识别缺失依赖（含 anyBins 组）
- 🌍 **描述汉化**：内置词表替换常见英文描述短语，附未汉化词报告
- 📊 **使用统计**：state 库 skill_usage 表 / curator 双数据源（`--usage`）
- 🔗 **依赖关系图**：缺失依赖边可视化（`--deps`）
- 🔁 **批量启停**：写 `skills.entries.<名>.enabled`，自动备份 + 写后验证
- ⬆️ **更新检查**：git 轨对比远端 HEAD，只报告不升级（`--check-updates`）
- 📤 **远端推送**：显式传参方触发的 Markdown 推送为飞书云文档 / Notion 页面（`--push`，执行前有隐私提示）

## 🏗️ 架构设计

```
openclaw-skill-manager/
├── data/                      # 数据层（CLI 封装、统计、依赖、更新、启停）
├── classifier/                # 分类层（映射表、覆盖层、重复检测）
├── exporter/                  # 导出层（Markdown/JSON/HTML/飞书/Notion）
├── utils/                     # 工具层（配置、汉化、差异、HTTP 客户端）
├── tests/                     # pytest 单测
├── generate_skill_list.py     # 主入口
└── __init__.py                # 包定义
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- OpenClaw 已安装并配置

### 安装

1. 通过 OpenClaw 技能安装功能安装（推荐）：
```bash
openclaw skills install git:https://github.com/kuntao2011/openclaw-skill-manager
```

2. 或手动克隆本仓库到 OpenClaw 技能目录：
```bash
git clone https://github.com/kuntao2011/openclaw-skill-manager
cp -r openclaw-skill-manager ~/.openclaw/workspace/skills/
```

### 使用方式

#### 基本用法
```bash
cd ~/.openclaw/workspace/skills/openclaw-skill-manager
python3 generate_skill_list.py
```

#### 指定输出格式
```bash
# Markdown（默认）
python3 generate_skill_list.py -f markdown

# JSON
python3 generate_skill_list.py -f json

# HTML（交互式界面）
python3 generate_skill_list.py -f html

# 全部格式
python3 generate_skill_list.py -f all
```

#### 过滤选项
```bash
# 只导出已激活技能
python3 generate_skill_list.py -F activated

# 只导出未激活技能
python3 generate_skill_list.py -F not_activated

# 按关键词搜索
python3 generate_skill_list.py -s "同花顺"

# 按分类过滤
python3 generate_skill_list.py -c "金融分析工具"
```

#### 高级选项
```bash
# 增量更新（只输出变化）
python3 generate_skill_list.py -i

# 检测重复技能
python3 generate_skill_list.py --check-duplicates

# 自定义输出目录（不存在时自动创建）
python3 generate_skill_list.py -o /path/to/output

# 简洁模式
python3 generate_skill_list.py -q

# 使用次数列
python3 generate_skill_list.py --usage

# 缺失依赖关系图
python3 generate_skill_list.py --deps

# 未汉化英文词报告
python3 generate_skill_list.py --i18n-report

# 更新检查（只报告，不自动升级）
python3 generate_skill_list.py --check-updates

# 批量启停（自动备份 openclaw.json，写后验证）
python3 generate_skill_list.py --disable skill-a,skill-b
python3 generate_skill_list.py --enable skill-a

# 推送本次导出的 Markdown 到飞书 / Notion
python3 generate_skill_list.py -f all --push feishu,notion
```

## 🔐 远端推送凭据（只走环境变量）

| 目标 | 必填 | 可选 |
|------|------|------|
| 飞书 | `FEISHU_APP_ID`、`FEISHU_APP_SECRET` | `FEISHU_FOLDER_TOKEN`（缺省写入云空间根目录） |
| Notion | `NOTION_TOKEN`、`NOTION_PAGE_ID` | — |

凭据一律从环境变量读取，任何凭据字面量不得写入本仓库。

> ⚠️ **隐私提示**：推送会把技能清单（名称、描述、来源、调用量）发送到你指定的第三方服务（飞书/Notion）。仅在显式传入 `--push` 时触发、运行前有提示；敏感/企业环境请勿使用。网络范围：飞书/Notion API（代码级主机白名单、强制 HTTPS）；`--check-updates` 会用 `git ls-remote` 访问技能安装记录中登记的 git 远端地址。

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
python3 generate_skill_list.py -o ~/my_skills
```

### 自定义分类覆盖层

新建 `~/.openclaw/skill_categories.json`（优先级高于内置映射表）：

```json
{
  "my-skill": ["开发工具", "编码与开发"]
}
```

## 📊 输出示例

> 节选自真实运行输出（2026-09-25，本机 64 个技能：31 ✅ / 5 ⚠️ / 28 ❌）。长描述自动压平换行并在 120 字处截断，完整内容见 JSON/HTML。

```
| 序号 | 状态 | 技能名称 | 版本 | 来源 | 调用量 | 描述 |
|------|------|----------|------|------|------|------|
| 1 | ✅ | [☔ weather](https://wttr.in/:help) |  | bundled | - | Current weather and forecasts with web_fetch, falling back to wttr.in curl for locations, rain, temperature, travel plan… |
| 2 | ✅ | kkk-ocr-local |  | agents-skills-personal | - | 本地图片预处理（纯 CPU）+ OCR 后备。主用途：①图片朝向检测与自动旋转 （auto_orient_ocr.py — 横放/倒置的文档照片先转正再送 MCP/云端识别，防旋转幻觉） ②空白裁剪（crop_whitespace.py —… |
| 3 | ❌ | [🔐 1password](https://developer.1password.com/docs/cli/get-started/) |  | bundled | - | 设置和使用 1Password CLI for sign-in, desktop integration, and reading or injecting secrets. |
```

### HTML 界面特性
- 🔍 实时搜索技能名称和描述
- 📂 按分类过滤、按状态筛选
- 🔃 表头点击排序（名称/版本/来源/调用量/分类）
- 🔗 缺失依赖关系 SVG 二部图
- 📈 实时统计面板
- 🎨 响应式布局，手机和电脑都可正常使用

## 📁 输出文件

运行后生成以下文件：
- `已激活技能列表.md` - Markdown 格式的已激活技能列表
- `未激活技能列表.md` - Markdown 格式的未激活技能列表
- `技能列表.json` - 完整结构化 JSON 数据（含 usage / dependency_edges）
- `已激活技能列表.html` - 交互式 HTML 网页
- `未激活技能列表.html` - 交互式 HTML 网页
- `未汉化词表.txt` - 使用 `--i18n-report` 时生成

## 🧪 开发与测试

```bash
python3 -m pytest -q          # 运行单测（47 个用例）
python3 -m compileall -q classifier data exporter utils generate_skill_list.py __init__.py
```

推送后 GitHub Actions 会自动跑编译检查 + pytest（Python 3.9 / 3.12）。

## 📝 注意事项

1. 首次运行会自动创建输出目录与缓存目录 `~/.openclaw/cache/skill_list/`
2. 增量更新（`-i`）依赖上次运行保存的快照；`--no-snapshot` 可跳过快照保存
3. 分类规则基于作者个人技能库定制，第三方技能大概率落入「其他」——用 `~/.openclaw/skill_categories.json` 覆盖层或修改 `classifier/category_map.py` 增补
4. 批量启停会修改 `~/.openclaw/openclaw.json`，每次改动前自动生成带时间戳的备份
5. 使用统计依赖 OpenClaw 的 `skill_usage` 记录，暂无数据时输出占位符 `-`
6. 无任何持久化机制：不注册 cron/开机自启，快照与分类覆盖层只是普通数据文件
7. 输出与分类标签为中文，面向中文用户（`metadata.language: zh-CN`）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 👤 作者

**kuntao2011**（[GitHub @kuntao2011](https://github.com/kuntao2011)）

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📋 更新日志

详见 [CHANGELOG.md](CHANGELOG.md) 了解各版本的变更历史。
