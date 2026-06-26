# Weeko CLI Skill

[English](./README.md) | 中文文档

一个 AI 代理技能，用于 [Weeko CLI](https://github.com/nicepkg/weeko) —— 让 AI 编程助手（Claude、Cursor、OpenCode 等）能够通过命令行管理书签和分组。

## 这个 Skill 能做什么

激活后，AI 代理将获得以下能力：

- **搜索和浏览**书签（按标题、URL、描述关键词搜索）
- **添加、更新、删除**书签，支持设置标题、URL、分组和描述
- **管理分组** —— 创建、重命名、更改颜色、列表、删除
- **批量操作** —— 批量移动或删除多个书签
- **账户概览** —— 获取用户状态和分组结构作为上下文

## 前置条件

- 主机已安装 [Bun](https://bun.sh) v1.0 或更高版本
- 已全局安装 [weeko-cli](https://www.npmjs.com/package/weeko-cli)（`bun install -g weeko-cli`）
- 有效的 Weeko API Key（从 [weeko.blog/dashboard](https://weeko.blog/dashboard) 获取）

## 使用方式

代理应先完成认证，再获取上下文，然后执行操作：

```bash
weeko login              # 使用 API Key 认证
weeko status             # 获取账户概览
weeko tree               # 了解分组结构
```

建立上下文后，代理可以执行任何书签或分组操作。所有命令都支持 `--format toon` 以获得 token 高效输出，以及 `--dry-run` 进行安全测试。

## Skill 文件说明

| 文件 | 描述 |
|------|------|
| `SKILL.md` | 完整的代理指令 —— 工作流、最佳实践、错误处理 |
| `references/commands.md` | 详细的命令参考、数据 Schema、API 端点、架构说明 |

## 安装 Skill

此 skill 可加载到支持技能文件的 AI 代理框架中（如 [OpenCode](https://opencode.ai)）。将 `skills/weeko/` 目录放入代理的技能路径即可。

## 许可证

MIT
