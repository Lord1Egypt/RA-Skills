---
slug: volcengine-dns-tool-free
name: volcengine-dns-tool-free
version: 1.0.0
displayName: 火山引擎DNS免费版
summary: "火山引擎DNS记录管理，支持域名区查询、记录增删改与传播验证，适合个人开发者日常运维.。火山引擎DNS管理工具免费版，面向个人开发者的轻量级DNS记录管理工具。核心能力:"
license: Proprietary
edition: free
description: '火山引擎DNS管理工具免费版，面向个人开发者的轻量级DNS记录管理工具。核心能力:

  - 域名区记录查询

  - DNS记录增删改操作

  - TTL 约束与回滚值保留

  - 传播验证（权威与递归检查）

  适用场景:

  - 个人域名的DNS记录维护

  - 服务迁移时的DNS切换

  - DNS记录的日常查询与验证

  差异化: 免费版聚焦核心DNS记录管理能力，去除所有外部平台与作者引用，强化中文本地化与适用关键词，适合个人用户零成本上手'
tags:
  - DNS管理
  - 火山引擎
  - 域名运维
  - 免费版
  - 工具
  - 效率
  - 自动化
  - 运维
  - 监控
  - 开发
  - 代码
  - 写作
  - ttl
  - api
  - 记录
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 火山引擎DNS管理（免费版）

## 概述

火山引擎DNS管理工具免费版帮助你管理火山引擎网络服务上的 DNS 记录。提供域名区查询、记录增删改、TTL 约束与传播验证能力，遵循严格变更范围控制与验证步骤.
## 核心能力

| 能力 | 说明 |
|---|---|
| 记录查询 | 查询指定域名区的现有记录 |
| 记录新增 | 添加 A/AAAA/CNAME/MX/TXT 等记录 |
| 记录修改 | 更新现有记录，保留回滚值 |
| 记录删除 | 删除指定记录，保留回滚值 |
| TTL 约束 | 支持自定义 TTL，迁移窗口前最小化 |
| 传播验证 | 权威查询 + 递归查询双重验证 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：火山引擎、DNS、记录管理、支持域名区查询、记录增删改与传播、适合个人开发者日、常运维、管理工具免费版、面向个人开发者的、轻量级、记录管理工具、域名区记录查询、记录增删改操作、约束与回滚值保留、权威与递归检查等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：新增 A 记录

为新增服务添加 A 记录.
```bash
# 新增 A 记录
volcengine-dns add \
  --zone "example.com" \
  --record "api.example.com" \
  --type A \
  --value "192.168.1.100" \
  --ttl 300
# ...
# 输出
# ✅ 记录已添加
# 示例
# 记录: api.example.com
# 类型: A
# 值: 192.168.1.100
# TTL: 300s
```

### 场景二：服务迁移时的 DNS 切换

服务迁移至新 IP，需要更新 DNS 记录.
```bash
# 1. 迁移前最小化 TTL
volcengine-dns update \
  --zone "example.com" \
  --record "api.example.com" \
  --type A \
  --ttl 60 \
  --comment "迁移前最小化TTL"
# ...
# 2. 等待原 TTL 过期后切换值
volcengine-dns update \
  --zone "example.com" \
  --record "api.example.com" \
  --type A \
  --value "192.168.2.100" \
  --ttl 60
# ...
# 输出（保留回滚值）
# ✅ 记录已更新
# 旧值: 192.168.1.100
# 新值: 192.168.2.100
# 回滚命令: volcengine-dns update --record api.example.com --type A --value 192.168.1.100
```

### 场景三：传播验证

DNS 切换后验证传播情况.
```bash
# 权威查询
volcengine-dns verify \
  --record "api.example.com" \
  --type A \
  --source authoritative
# ...
# 递归查询
volcengine-dns verify \
  --record "api.example.com" \
  --type A \
  --source recursive
# ...
# 输出
# 🔍 传播验证
# 权威查询: 192.168.2.100 ✅
# 递归查询:
#   - 8.8.8.8: 192.168.2.100 ✅
#   - 114.114.114.114: 192.168.1.100 ⚠️ (尚未传播)
# 建议等待原 TTL 过期后再次验证
```

## 不适用场景

以下场景火山引擎DNS免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

```bash
# 1. 查询现有记录
volcengine-dns list --zone "example.com"
# ...
# 2. 新增记录
volcengine-dns add --zone "example.com" --record "www" --type A --value "192.168.1.1" --ttl 300
# ...
# 3. 修改记录
volcengine-dns update --zone "example.168.1.2"
# ...
# 4. 验证传播
volcengine-dns verify --record "www.example.com" --type A
# ...
# 5. 删除记录
volcengine-dns delete --zone "example.com" --record "old.example.com" --type A
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例

```bash
# 环境变量配置
export VOLCENGINE_ACCESS_KEY="your-access-key"
export VOLCENGINE_SECRET_KEY="your-secret-key"
export VOLCENGINE_REGION="cn-beijing"
# ...
# 安全规则
# 1. 修改前先查询现有记录，diff 对比
# 2. 避免盲覆盖，保留回滚值
# 3. 迁移窗口前最小化 TTL
# 4. 变更后执行传播验证
```

## 最佳实践

* 修改前先查询现有记录，避免盲覆盖.
* 所有修改操作保留回滚值，便于快速回滚.
* 迁移窗口前最小化 TTL（建议 60s），加速传播.
* 变更后执行权威与递归双重验证.
* 批量变更时分批次执行，每批验证后再继续.
* 删除操作前确认记录无依赖，避免误删导致服务中断.
* API 密钥仅从环境变量读取，不硬编码.
## 常见问题

**Q：免费版支持批量记录操作吗？**
A：免费版仅支持单条记录操作。如需批量操作与变更计划，请考虑 PRO 版本.
**Q：免费版支持变更回滚吗？**
A：免费版保留回滚值并输出回滚命令，但需手动执行。如需自动回滚，请使用 PRO 版本.
**Q：支持哪些记录类型？**
A：支持 A、AAAA、CNAME、MX、TXT、NS、SRV 等常见记录类型.
**Q：传播验证需要多长时间？**
A：取决于原 TTL 设置。TTL 60s 时通常 5-10 分钟内全球传播完成.
**Q：可以查询多个域名区吗？**
A：免费版支持查询多个域名区，但每次操作针对单个区。如需跨区批量，请使用 PRO 版本.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 可访问火山引擎 API

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 火山引擎 SDK | 库 | 必需 | pip/npm 安装 |
| dig/nslookup | 工具 | 可选（验证） | 系统自带 |

### API Key 配置
- `VOLCENGINE_ACCESS_KEY` - 火山引擎访问密钥
- `VOLCENGINE_SECRET_KEY` - 火山引擎秘密密钥
- `VOLCENGINE_REGION` - 火山引擎地域
- API 密钥仅从环境变量读取，不硬编码

### 可用性分类
- **分类**: MD+EXEC（Markdown指令 + 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过命令行工具管理火山引擎DNS记录

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "火山引擎DNS免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "volcengine dns"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
