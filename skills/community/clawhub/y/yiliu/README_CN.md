# 忆流 (Yiliu)

> 随时捕捉、自动整理、按需浮现的 AI 笔记知识库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/DamingDong/yiliu)

[English](./README.md)

## 简介

忆流是一个 OpenClaw Skill，专注于个人知识管理。通过 AI 能力实现自动整理和语义搜索，让知识像水一样流动。

## 特性

- ⚡ **零门槛记录** - 3 秒内完成记录，无需分类
- 🧠 **AI 自动整理** - 自动生成摘要和标签
- 🔍 **语义搜索** - 理解意图，找你想找
- 📱 **随时捕捉** - 微信即入口
- 💾 **本地存储** - 数据主权，一键导出

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/DamingDong/yiliu.git
cd yiliu

# 安装依赖
npm install

# 编译
npm run build
```

### 配置

```bash
# 可选：配置 OpenAI API Key（启用 AI 增强功能）
export OPENAI_API_KEY=your-api-key
```

**注意**：无 API Key 时，自动降级使用本地嵌入模型（`@huggingface/transformers`），基础记录和搜索功能仍可使用。

### 使用

```bash
# 启动
npm start

# 或使用内置命令
./yiliu "记录 今天的收获"
./yiliu "搜索 CRDT"
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `/记 <内容>` | 记录笔记 |
| `/搜 <关键词>` | 搜索笔记 |
| `/列表` | 查看所有笔记 |
| `/历史 <id>` | 查看版本历史 |
| `/统计` | 查看统计信息 |
| `/导出` | 导出数据 |
| `/删除 <id>` | 删除笔记 |
| `/帮助` | 查看帮助 |

## 项目结构

```
yiliu/
├── src/
│   ├── index.ts          # 入口
│   ├── commands/         # 命令处理
│   ├── storage/          # 存储层
│   ├── ai/               # AI 能力
│   └── types/            # 类型定义
├── dist/                 # 编译输出
├── data/                 # 数据存储
├── SKILL.md              # 使用文档
└── package.json
```

## 技术栈

- **存储**: LibSQL (SQLite)
- **嵌入**: OpenAI / HuggingFace Transformers
- **框架**: OpenClaw Skill
- **语言**: TypeScript

## 配置项

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `OPENAI_BASE_URL` | API 端点 | https://api.openai.com/v1 |
| `YILIU_DATA_PATH` | 数据目录 | ./data |

## 开发

```bash
# 开发模式（监听变化）
npm run dev

# 测试
npm test

# 构建
npm run build
```

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md)

## 路线图

### v1.3（计划中）
- embedjs 完整集成
- 数据迁移脚本
- 单元测试

### v2.0（未来）
- WebDAV 同步
- 网页抓取（readability）
- PDF 处理
- Yjs 实时同步
- Web 画布界面

## 贡献

欢迎提交 Issue 和 PR！

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 联系方式

- 作者：董大明 (Daming Dong)
- Email：dmdong@gmail.com
- GitHub：https://github.com/DamingDong/yiliu
