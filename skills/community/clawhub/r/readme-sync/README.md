# README

让 AI 在代码工作前后自动同步 README.md，保持项目文档最新。

## 特性

- **按需加载**：只读任务相关的 README 章节，节省 token
- **增量更新**：只改相关章节，不重写整个文件
- **跨平台**：兼容 Claude Code、OpenClaw、Trae、Cursor 等主流 AI 编程工具
- **历史追踪**：维护近期修改记录，方便同事 review 和 AI 理解项目

## 安装

```bash
clawhub install readme
```

或手动安装到 `~/.agents/skills/readme/` 目录。

## 使用方法

### 自动触发（推荐）

在 OpenClaw 或 Claude Code 中，直接开始工作：

- 询问项目相关问题时，AI 会自动读取 README
- 代码工作结束后，AI 会询问是否更新 README

### 手动命令

```bash
# 初始化 README（首次使用）
python scripts/readme_operations.py init              # 空模板
python scripts/readme_operations.py auto-init          # 扫描代码生成

# 读取章节（节省 token）
python scripts/readme_operations.py read "技术栈"       # 读单个章节
python scripts/readme_operations.py read all            # 读整个 README

# 扫描项目结构（预览）
python scripts/readme_operations.py scan

# 待更新管理
python scripts/readme_operations.py pending            # 查看待更新
python scripts/readme_operations.py add changelog "完成登录功能" --related src/auth/
python scripts/readme_operations.py sync               # 同步到 README
python scripts/readme_operations.py clear               # 清空待更新
```

## README 标准格式

```markdown
# 项目名称

## 一句话定位
[项目是干什么的]

## 技术栈
- 语言/框架：xxx

## 项目结构
├── src/
└── tests/

## 当前进度
- [x] 完成：xxx
- [ ] 进行中：xxx

## 踩坑记录
- ⚠️ xxx 容易搞错，要注意 xxx

## 近期修改记录
| 日期 | 修改内容 | 相关文件/模块 |
|------|---------|--------------|
| 2026-04-14 | 完成用户认证 | src/auth/ |
```

## 工作流程

1. **工作前**：AI 按需读取 README 相关章节（不打断）
2. **工作中**：缓存值得记录的变更
3. **工作后**：展示变更摘要，用户确认后写入

## 读取策略

| 问题类型 | 读取章节 |
|---------|---------|
| 项目概况 | 一句话定位 + 项目结构 |
| Bug 相关 | 踩坑记录 + 近期修改记录 |
| 技术方案 | 技术栈 + 项目结构 |
| 代码修改 | 近期修改记录 + 相关代码 |

## 平台兼容性

| 平台 | 支持 |
|------|------|
| Claude Code | ✅ |
| OpenClaw | ✅ |
| Trae | ✅ |
| Cursor | ✅ |

## License

MIT
