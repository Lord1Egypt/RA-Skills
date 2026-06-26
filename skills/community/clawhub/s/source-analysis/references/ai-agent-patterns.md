# AI Agent 分析参考手册

## 常见AI工具的分发模式

| 工具 | 分发方式 | 源码位置 | 提示词位置 |
|------|----------|----------|------------|
| Claude Code | npm壳子+原生二进制 | 闭源 | 二进制内嵌 |
| Cursor | Electron应用 | 闭源 | app.asar内 |
| GitHub Copilot | VS Code扩展 | 闭源 | 扩展JS内 |
| Aider | PyPI纯Python | 开源 | prompts/目录 |
| Continue | VS Code扩展 | 开源 | src/内 |
| OpenClaw | npm包 | 开源 | 系统提示词可配置 |

## 二进制提取技巧

### grep模式库

```bash
# 提取JSON格式的工具定义
grep -aoP '\{[^{}]*"name":"[^"]*"[^{}]*"description":"[^"]*"[^{}]*\}' binary

# 提取Markdown格式的指令
grep -aoP '# [A-Z][^\n]{10,200}' binary

# 提取CLI帮助文本
grep -aoP 'Usage: [^\n]{10,200}' binary

# 提取环境变量引用
grep -aoP 'process\.env\.[A-Z_]+' binary | sort -u

# 提取特性标志（实验性功能）
grep -aoP '(feature|flag|toggle|experiment)[_-]?[a-z_]+' binary | sort -u
```

### 常见壳子分发模式

1. **npm壳子+平台二进制**：`@scope/package` 是wrapper，实际代码在 `@scope/package-{platform}-{arch}`
2. **Electron应用**：源码打包在 `resources/app.asar` 或 `resources/app.asar.unpacked`
3. **Python wheel**：解压后查看 `*.dist-info/` 和 `*.data/`
4. **Docker镜像**：`docker export` 后分析文件系统

## 分析报告模板

```markdown
# {项目名} 源码分析报告

## 1. 架构概览
- 分发方式：
- 技术栈：
- 版本：

## 2. 系统提示词
### 核心身份
### 章节结构
### 行为指令

## 3. 工具定义
### 工具列表
### 输入/输出Schema

## 4. 权限系统

## 5. 记忆与上下文管理

## 6. 插件/扩展系统

## 7. 可借鉴的设计模式
```
