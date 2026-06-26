---
name: source-analysis
description: "GitHub源码与架构分析工具。用于：1) 下载GitHub仓库/npm包源码 2) 分析AI Agent架构与工具定义 3) 研究开源项目的提示词工程与设计模式 4) 生成结构化分析报告。触发词：源码分析、代码架构分析、github源码、项目分析、agent架构分析"
---

# Source Analysis

从GitHub仓库和npm包中提取、分析AI Agent的源码与系统提示词。

## 适用场景

- 分析AI工具（如Claude Code、Cursor、Copilot等）的架构设计
- 从npm/PyPI包中下载并分析源码结构
- 研究Agent的工具定义、权限系统、记忆机制
- 生成对比分析报告

## 工作流程

### Phase 1: 信息收集

1. **GitHub仓库探索**
   ```bash
   # 获取README
   curl -s -L --max-time 15 "https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
   
   # 获取仓库结构（如果API可达）
   curl -s -L --max-time 15 "https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
   
   # 检查关键文件
   for path in "package.json" "src/index.ts" "CLAUDE.md" ".claude/CLAUDE.md" "plugins/README.md"; do
     code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://raw.githubusercontent.com/{owner}/{repo}/main/$path")
     echo "$path → HTTP $code"
   done
   ```

2. **npm包下载**
   ```bash
   # 下载wrapper包
   cd /tmp && npm pack @{scope}/{package-name}
   tar xzf {package-name}-*.tgz
   
   # 检查是否为壳子分发（常见模式）
   ls -lh package/bin/
   file package/bin/*  # 如果是小文件（<1KB），只是占位符
   
   # 下载平台特定二进制
   npm pack @{scope}/{package-name}-linux-x64
   tar xzf *-linux-x64-*.tgz
   ```

### Phase 2: 二进制提取

当源码被打包为单一可执行文件时：

```bash
# 检查二进制大小
ls -lh package/claude

# 提取身份声明
grep -aoP 'You are [^"]{0,500}' /path/to/binary | sort -u

# 提取系统提示词章节
grep -aoP '"# [A-Z][^"]{0,200}"' /path/to/binary | sort -u

# 提取工具定义
grep -aoP '"tool_name":"[^"]*"' /path/to/binary | sort -u

# 提取行为指令
grep -aoP '(Prefer|Avoid|Be |Do not|Never|Always|When |If |Use |Keep |Make sure)[^"]{0,300}' /path/to/binary | sort -u

# 提取配置参数
grep -aoP '--system-prompt[^"]{0,200}' /path/to/binary | head -10

# 提取特性标志
grep -aoP 'tengu_[a-z_]+' /path/to/binary | sort -u
```

### Phase 3: 工具定义分析

从TypeScript定义文件（如`sdk-tools.d.ts`）中提取：
- 工具名列表
- 输入/输出Schema
- 权限模型
- 并发安全性标记

### Phase 4: 报告生成

输出结构化报告，包含：
1. 架构概览（分发方式、技术栈）
2. 系统提示词（身份、章节、核心指令）
3. 工具定义（完整列表、Schema）
4. 权限系统（模式、分类器）
5. 记忆/上下文管理机制
6. 插件/扩展系统
7. 配置与环境变量
8. 可借鉴的设计模式

## 注意事项

- GitHub API可能被限流，优先使用`raw.githubusercontent.com`
- 打包文件的分析是近似的，可能有碎片化
- `strings`命令在某些环境不可用，用`grep -aoP`替代
- 打包内容可能是动态拼接的，提取的是片段而非完整提示词
- 保存所有提取结果到`/tmp/`目录便于后续分析

## 输出格式

报告保存为 `{workspace}/source-analysis-{project-name}.md`，使用Markdown结构化格式。
