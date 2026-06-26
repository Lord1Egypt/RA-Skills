---
name: release-checker
description: "一体化发版兼容性检查工具。自动分析 Git diff 检测发版兼容性，通过代码智能识别推送中心/Gateway/配置变更，自动检测 SQL 脚本兼容性并生成多数据库版本，输出完整的 TODO 清单和 Markdown 报告。"
category: development
risk: safe
source: custom
date_added: "2026-04-07"
author: user
tags: [release, compatibility, java, sql, dml, ddl, config, git-diff, multi-db, mybatis, push-center, Gateway, nacos]
tools: [git, python, glob, grep, read, write, bash]
compatibility: opencode
---

# Release Checker - 一体化发版兼容性检查工具

## 概述

**完全自动化的发版兼容性检查工具**，整合以下核心功能：

1. **Git Diff 分析** - 自动分析变更文件，分类统计
2. **智能组件识别** - 通过代码内容自动识别推送中心、Gateway、配置变更
3. **发布组件确认** - 结合自动识别结果，让用户最终确认
4. **SQL 兼容性检查** - 检测 MySQL/PostgreSQL/Oracle 兼容性问题
5. **SQL 多数据库转换** - 内置转换逻辑，将 MySQL SQL 转换为 PostgreSQL/Oracle 版本
6. **TODO 清单确认** - 生成完整的待办事项清单并让用户最终确认
7. **Markdown 报告生成** - 输出完整的发版兼容性报告

适用于：
- **MyBatis-Plus 项目**（代码中写 SQL）
- **Spring Cloud 项目**（Feign 调用、Nacos 配置）
- **传统 Java 项目**（Java 代码 + SQL 脚本）
- **多数据库项目**（MySQL/PostgreSQL/Oracle）

## 何时使用此技能

- 用户说"检查发版兼容性"、"release check"、"发版检查"时使用
- 用户想要分析 git diff 中的代码和脚本变更时使用
- 用户需要生成发版 TODO 清单时使用
- 用户需要生成 Markdown 格式的兼容性报告时使用
- 用户需要将 MySQL SQL 转换为多数据库版本时使用
- **不要**用于普通代码审查；请使用适当的代码审查技能

## 工作原理

### 模式判断

执行前首先判断是单项目还是批量模式：

- **单项目模式**：用户提供单个项目路径和对比分支
- **批量模式**：用户提供多个项目路径，或使用配置文件

### 第 1 步：Git Diff 分析（自动）

**单项目模式：**
执行 `git diff <基准分支>..HEAD --name-only` 获取所有变更文件。

**批量模式：**
对每个项目并行执行 git diff 分析，收集所有项目的变更信息。

识别：
- 变更的 Java 文件（新增/修改/删除）
- 变更的 SQL 脚本（DML/DDL）
- 变更的配置文件（yml/properties）
- 变更的 MyBatis Mapper XML 文件

### 第 2 步：智能组件识别（自动）

**本步骤通过代码内容分析自动检测以下组件：**

#### 2.1 推送中心配置识别

检测变更的 Java 文件中是否包含以下内容：

- **推送相关日志/注释**：包含"推送"、"push"、"spush"、"发送消息"等关键词
- **EVENT 定义**：包含 `extends ApplicationEvent` 或 `@EventListener` 的类，且类名包含"Push"、"Push"相关
- **Push Feign 调用**：包含 `@FeignClient` 注解，且 value 或 url 包含"push"、"spush"关键词

检测模式：
```
// 日志/注释检测
推送|push|spush|发送消息|消息推送

// EVENT 检测
extends ApplicationEvent
@EventListener
*PushEvent*
*Push*Event*

// Feign 检测
@FeignClient.*[Pp]ush
value.*=.*"\$\{[^}]*push
url.*=.*"\$\{[^}]*push
```

如果检测到相关文件，在后续用户确认时显示"自动识别到推送中心相关变更"。

#### 2.2 Gateway 配置识别

检测变更的 Java 文件中是否包含以下内容：

- **新 Feign 定义**：包含 `@FeignClient` 注解的接口
- **通过注解指定服务名**：value 属性使用 `${openfeign.xxx.name:}` 格式
- **服务名包含 spush**：检测到 `spush` 或类似推送服务名称

检测模式：
```
// Feign Client 检测
@FeignClient

// 服务名检测
value\s*=\s*"\$\{openfeign\.[^}]+name:
value\s*=\s*"\$\{[^}]*spush
url\s*=\s*"\$\{openfeign\.[^}]+url:
```

如果检测到新的 Feign 定义且包含服务名配置，在后续用户确认时显示"自动识别到 Gateway 相关变更"。

#### 2.3 配置变更识别

**检测方式：**

- **本地配置文件变更**：检测 yml/properties 文件是否有变更
- **注解形式引入配置属性**：检测 Java 文件中是否包含：
  - `@Value("${xxx}")` 注解
  - `@ConfigurationProperties` 注解
  - `@PropertySource` 注解
- **配置类变更**：检测包含 `@Configuration` 或 `@Bean` 的类是否有变更

检测模式：
```
// 配置属性注入
@Value("${

// 配置属性类
@ConfigurationProperties

// 配置类
@Configuration
@Bean
```

如果检测到配置属性相关代码变更，在后续用户确认时显示"自动识别到配置变更（注解/配置类）"。

#### 2.4 其他组件识别

- **ES 变更**：检测是否有 ES 实体类、ES 注解、ES Repository 变更
- **SQL 脚本**：检测是否有 .sql 文件变更
- **字典变更**：检测是否有枚举类、字典配置类变更
- **Redis 配置**：检测 Redis 相关配置、RedisTemplate、@Cacheable 等
- **MQ 消息**：检测 MQ 注解、Listener、Producer 相关变更
- **文件存储**：检测文件上传、存储路径相关变更
- **API 接口**：检测 Controller、@RequestMapping 相关变更
- **Java 代码**：其他 Java 代码变更

### 第 3 步：发布组件确认（用户交互 - 第一轮）

使用 Question 工具，**必须设置 multiple=true** 让用户一次性选择多个组件。

显示自动识别结果供用户参考：

**options 参数**：
```json
[
  {"label": "推送中心配置", "description": "推送中心服务相关配置变更（自动识别: 检测到相关代码）"},
  {"label": "Gateway 配置", "description": "统一网关相关配置（自动识别: 检测到新 Feign 定义）"},
  {"label": "ES 变更", "description": "Elasticsearch 索引或查询变更"},
  {"label": "SQL 脚本", "description": "数据库脚本变更（DML/DDL）"},
  {"label": "字典变更", "description": "数据字典或枚举配置变更"},
  {"label": "配置文件变更", "description": "应用配置文件变更（自动识别: 检测到注解/配置类）"},
  {"label": "Redis 配置", "description": "Redis 缓存或数据结构变更"},
  {"label": "MQ 消息", "description": "消息队列 topic 或消息格式变更"},
  {"label": "文件存储", "description": "文件上传、存储路径变更"},
  {"label": "API 接口", "description": "对外 API 接口变更"},
  {"label": "Java 代码", "description": "Java 代码变更"}
]
```

### 第 4 步：SQL 转换询问（用户交互）

**只有当用户选择"SQL 脚本"时才执行：**

#### 4.1 询问是否需要转换

使用 Question 工具询问：

**Question**: "检测到 SQL 脚本变更。是否需要将现有 SQL 脚本转换为多数据库版本（MySQL → PostgreSQL/Oracle）？"

**options**: 
```json
[
  {"label": "是，我需要生成多数据库版本", "description": "将 MySQL SQL 转换为 PostgreSQL 和 Oracle 版本"},
  {"label": "否，SQL 脚本已就绪", "description": "已有完整的多数据库 SQL 脚本，无需转换"}
]
```

#### 4.2 询问文件路径（用户选择"是"后必须执行）

**⚠️ 重要：此步骤必须使用 Question 工具执行，不能跳过，不能用普通文本询问。**

如果用户选择"是，我需要生成多数据库版本"，**立即使用 Question 工具询问文件路径**：

**Question**: "请提供需要转换的 MySQL SQL 文件路径（多个文件用逗号或换行分隔）"

**options**: 
```json
[
  {"label": "使用 git diff 检测到的 SQL 文件", "description": "自动使用变更文件中的 SQL 文件路径"},
  {"label": "手动输入文件路径", "description": "自己输入需要转换的文件路径"}
]
```

**如果用户选择"使用 git diff 检测到的 SQL 文件"：**
- 自动使用第 1 步中检测到的 SQL 变更文件路径
- 列出文件路径供用户确认
- 确认后直接进入第 5 步

**如果用户选择"手动输入文件路径"：**
- 让用户直接输入文件路径（支持多个，用逗号或换行分隔）
- 示例输入：
  ```
  scripts/db/v1.0.0/mysql-ddl.sql,
  scripts/db/v1.0.0/mysql-dml.sql
  ```
- 确认后进入第 5 步

#### 4.3 用户未选择"SQL 脚本"时的处理

如果用户没有选择"SQL 脚本"但 git diff 中检测到 .sql 文件变更：
- 列出检测到的 SQL 变更文件
- 主动询问："检测到以下 SQL 文件变更，是否需要为这些文件生成多数据库版本？"
- 如果用户确认，回到 4.2 步骤

### 第 5 步：SQL 兼容性分析（Python 脚本自动执行）

调用 Python 脚本对检测到的 SQL 文件进行兼容性分析：

```bash
python scripts/release_checker.py \
  --project <项目路径> \
  --branch <对比分支> \
  --report <报告输出路径>
```

Python 脚本自动检测以下兼容性问题：

| 兼容性问题 | 检测模式 | 建议解决方案 |
|------------|----------|--------------|
| NOW() 不支持 | `NOW\(\)` | 使用 SYSTIMESTAMP (Oracle) |
| LIMIT 不支持 | `LIMIT \d+` | 使用 OFFSET...ROWS FETCH NEXT |
| IF NOT EXISTS | `IF NOT EXISTS` | Oracle 不支持，需手动处理 |
| AUTO_INCREMENT | `AUTO_INCREMENT` | 使用 SERIAL (PG) 或 SEQUENCE (Oracle) |
| ENUM 类型 | `ENUM\(` | 使用 VARCHAR + CHECK |
| IFNULL | `IFNULL\(` | 使用 NVL 或 COALESCE |
| TINYINT | `TINYINT` | PostgreSQL: SMALLINT, Oracle: NUMBER(3) |
| DATETIME | `DATETIME` | PostgreSQL: TIMESTAMP, Oracle: TIMESTAMP |
| 反引号 | `` ` `` | PostgreSQL/Oracle: 双引号 |

### 第 6 步：SQL 多数据库转换（Python 脚本自动执行）

**当用户在第 4 步选择"是"时执行。**

调用 Python 脚本 `scripts/release_checker.py` 进行 SQL 转换（使用 SQLGlot）：

```bash
python scripts/release_checker.py --convert-sql \
  --sql-files <MySQL SQL 文件路径> \
  --output-dir <输出目录>
```

Python 脚本使用 **SQLGlot** 库进行专业 SQL 解析和转换，支持：
- MySQL → PostgreSQL 转换
- MySQL → Oracle 转换
- 自动生成 SEQUENCE + TRIGGER（Oracle 自增）
- 自动校验转换结果

### 第 6.5 步：SQL 转换验证（Python 脚本自动执行 + 人工确认）

**Python 脚本在转换完成后自动执行验证（10+ 项规则），确保生成的 SQL 可执行。**

#### 6.5.1 Python 自动语法验证

转换完成后，Python 脚本自动执行以下语法检查（已集成在 `--convert-sql` 模式中）：

**PostgreSQL 语法验证规则（10 项）：**
- ✅ 反引号检查
- ✅ AUTO_INCREMENT 检查
- ✅ ENGINE 检查
- ✅ NOW() 函数检查
- ✅ IFNULL 函数检查
- ✅ TINYINT 类型检查
- ✅ DATETIME 类型检查
- ✅ DEFAULT CHARSET 检查
- ✅ UNSIGNED 检查
- ✅ COMMENT 语法检查

**Oracle 语法验证规则（11 项）：**
- ✅ 反引号检查
- ✅ AUTO_INCREMENT 检查
- ✅ ENGINE 检查
- ✅ NOW() 函数检查
- ✅ IFNULL 函数检查
- ✅ TINYINT 类型检查
- ✅ DATETIME 类型检查
- ✅ IF NOT EXISTS 检查
- ✅ LIMIT 检查
- ✅ DEFAULT CHARSET 检查
- ✅ UNSIGNED 检查

Python 脚本输出验证结果汇总，显示通过/失败/警告数量。

#### 6.5.2 人工审查清单

**转换完成后，显示以下验证提醒，要求用户确认：**

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  AI 生成的 SQL 需要人工审查                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  验证清单：                                                  │
│  □ 确认目标表结构与转换后的字段匹配                          │
│  □ 确认字段顺序和约束条件                                    │
│  □ 在测试环境先执行，验证兼容性                              │
│  □ 检查索引和视图定义是否正确                                │
│  □ 确认 Oracle 的 SEQUENCE/TRIGGER 语法                    │
│  □ 确认 PostgreSQL 的 SERIAL 类型是否正确                    │
│  □ 确认视图中的字段类型与目标数据库兼容                      │
│  □ 确认索引语法正确（PostgreSQL/Oracle 差异）                │
│                                                             │
│  测试建议：                                                  │
│  1. 在测试环境创建临时表验证 DDL                             │
│  2. 执行 DESCRIBE/DESC 确认字段结构                          │
│  3. 插入测试数据验证约束条件                                 │
│  4. 执行查询验证视图和索引                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 6.5.3 验证确认（用户交互）

使用 Question 工具让用户确认验证结果：

**Question**: "SQL 转换已完成，请确认以下验证状态："

**options**：
```json
[
  {"label": "已验证，可以生成报告", "description": "已在测试环境验证，SQL 可执行"},
  {"label": "需要修改", "description": "发现语法或逻辑问题，需要调整"},
  {"label": "跳过验证，直接生成", "description": "信任 AI 转换结果，直接生成报告"}
]
```

如果用户选择"需要修改"：
- 询问具体问题所在
- 手动调整转换后的 SQL
- 重新执行验证步骤

### 第 7 步：TODO 生成（自动）

根据用户确认的发布组件自动生成结构化 TODO 清单。

### 第 8 步：TODO 清单确认（用户交互 - 第二轮）

**必须执行此步骤，让用户最终确认 TODO 清单：**

使用 Question 工具展示生成的 TODO 清单：

**Question**: "请确认以下发版 TODO 清单，如有需要可调整："

**options**：
```json
[
  {"label": "确认 TODO 清单", "description": "确认当前 TODO 清单，开始生成报告"},
  {"label": "需要修改", "description": "需要添加或删除某些 TODO 项"}
]
```

如果用户选择"需要修改"，则：
- 询问用户需要添加或删除哪些 TODO 项
- 重新生成清单后再次确认

### 第 9 步：Markdown 报告生成（自动）

**单项目模式：**
生成完整的 Markdown 格式报告，包含：
- 发布组件确认状态（包括自动识别结果）
- 变更文件汇总
- SQL 兼容性分析
- SQL 多数据库转换结果（如有）
- Java 代码变更说明
- 待处理 TODO 清单（已确认版本）

**批量模式：**
1. 为每个项目生成独立的项目级报告
2. 汇总所有项目结果，生成全局批量报告，包含：
   - 项目汇总表格（每个项目的变更统计）
   - 全局变更统计
   - 各项目 SQL 兼容性分析汇总
   - 全局 TODO 清单（按项目分组）
   - 各项目报告文件链接

## 使用方法

### 命令模式

**单项目模式：**
```
release-checker --project <路径> --branch <对比分支>
```

**批量模式（多项目）：**
```
release-checker --projects <路径1> --branches <分支1> --projects <路径2> --branches <分支2>
```

或者使用配置文件：
```
release-checker --config <配置文件路径>
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --project | -p | 项目路径（单项目模式必填） | 无 |
| --branch | -b | 对比分支（单项目模式必填） | 无 |
| --projects | -P | 多个项目路径（批量模式，可重复使用） | 无 |
| --branches | -B | 多个对比分支（批量模式，与 projects 一一对应） | 无 |
| --config | -c | 批量配置文件路径（JSON/YAML） | 无 |
| --report | -r | Markdown 报告输出路径 | release-check-report.md |

### 批量配置文件格式

**JSON 格式：**
```json
{
  "projects": [
    {
      "path": "/path/to/your/project-a",
      "branch": "release/v1.0.0",
      "report": "report-project-a.md"
    },
    {
      "path": "/path/to/your/project-b",
      "branch": "release/v1.0.0",
      "report": "report-project-b.md"
    },
    {
      "path": "/path/to/your/project-c",
      "branch": "release/v1.0.0",
      "report": "report-project-c.md"
    }
  ],
  "global_report": "batch-release-report.md",
  "parallel": true
}
```

**YAML 格式：**
```yaml
projects:
  - path: "/path/to/your/project-a"
    branch: "release/v1.0.0"
    report: "report-project-a.md"
  - path: "/path/to/your/project-b"
    branch: "release/v1.0.0"
    report: "report-project-b.md"
  - path: "/path/to/your/project-c"
    branch: "release/v1.0.0"
    report: "report-project-c.md"
global_report: "batch-release-report.md"
parallel: true
```

### 使用示例

**示例 1：单项目**
```
release-checker -p /path/to/your/project -b release/v1.0.0
```

**示例 2：批量模式（命令行）**
```
release-checker -P /path/to/project-a -B release/v1.0.0 -P /path/to/project-b -B release/v1.0.0
```

**示例 3：批量模式（配置文件）**
```
release-checker -c release-config.json
```

**示例 4：自然语言触发（批量）**
```
用户：检查以下项目的发版兼容性，对比分支都是 release/v1.0.0：
- /path/to/your/project-a
- /path/to/your/project-b
- /path/to/your/project-c
```

### 批量执行流程

```
1. AI 解析批量配置（命令行参数或配置文件）
2. 对每个项目并行/串行执行：
   a. git diff 分析
   b. 智能组件识别
   c. 发布组件确认（可批量确认或逐个确认）
   d. SQL 转换（如需要）
   e. SQL 语法验证
   f. 生成项目级报告
3. 汇总所有项目结果
4. 生成全局批量报告（包含所有项目的汇总）
```

### 批量确认模式

**Question**: "检测到 N 个项目需要检查，请选择确认模式："

**options**：
```json
[
  {"label": "批量确认（所有项目使用相同组件）", "description": "所有项目选择相同的发布组件"},
  {"label": "逐个确认", "description": "每个项目单独选择发布组件"},
  {"label": "使用智能识别结果", "description": "直接使用 AI 自动识别的组件，无需手动确认"}
]
```

### 使用示例

```
用户：检查 /path/to/your/project 本次 next 分支和上次 release/v1.0.0 分支的发版兼容性

AI 自动执行：
1. git diff release/v1.0.0..next --name-only
2. 分析变更文件，智能识别推送中心/Gateway/配置变更
3. 通过 Question 让用户选择确认涉及哪些组件（第一轮）
4. 如果用户选择"SQL 脚本"，询问是否需要转换为多数据库版本
5. 如果用户需要转换，询问 SQL 文件路径
6. 分析 SQL 兼容性，生成多数据库版本（如需要）
7. **执行 SQL 语法验证（自动）**
8. **显示人工审查清单，要求用户确认**
9. 生成初步 TODO 清单
10. 通过 Question 让用户确认 TODO 清单（第二轮）
11. 生成完整 Markdown 报告
```

### 交互流程

```
1. AI 分析 git diff，显示变更文件统计
2. AI 自动识别推送中心、Gateway、配置变更等组件
3. AI 弹出 Question 让用户选择发布组件（第一轮，包含自动识别结果）
4. 如果用户选择"SQL 脚本"：
   - AI 询问是否需要转换为多数据库版本
   - 如果是，询问 SQL 文件路径
   - 生成 PostgreSQL 和 Oracle 版本
5. AI 分析 SQL 兼容性
6. AI 执行 SQL 语法验证（自动检查）
7. AI 显示人工审查清单，要求用户确认
8. AI 生成初步 TODO 清单
9. AI 弹出 Question 让用户确认 TODO 清单（第二轮）
10. 用户确认后，AI 生成完整 Markdown 报告
```

## 智能识别详解

### 推送中心识别流程

```
1. 获取 git diff 变更的 Java 文件列表
2. 对每个文件执行内容检测：
   a) 检测是否包含推送相关关键词（推送、push、spush）
   b) 检测是否定义 EVENT 类（extends ApplicationEvent）
   c) 检测是否包含 Push 相关 Feign Client
3. 如果检测到任意一项，标记为"推送中心配置"
4. 在用户确认阶段显示自动识别结果和依据
```

### Gateway 识别流程

```
1. 获取 git diff 变更的 Java 文件列表
2. 对每个文件执行内容检测：
   a) 检测是否包含新的 @FeignClient 注解
   b) 检测 value 属性是否使用 ${xxx.xxx.name:} 格式
   c) 检测服务名是否包含 spush 或其他服务标识
3. 如果检测到新的 Feign 定义且包含服务配置，标记为"Gateway 配置"
4. 在用户确认阶段显示自动识别结果和依据
```

### 配置变更识别流程

```
1. 获取 git diff 变更的文件列表
2. 检测配置文件变更：
   a) 检测 yml/properties 文件是否有变更
3. 检测注解形式配置：
   a) 对 Java 文件检测 @Value、@ConfigurationProperties、@PropertySource
   b) 对 Java 文件检测 @Configuration、@Bean 类
4. 综合判定，标记为"配置文件变更"
5. 在用户确认阶段显示自动识别结果（区分本地配置还是注解配置）
```

## SQL 转换内置逻辑

### Python 脚本执行

**本 skill 使用 Python 脚本进行 SQL 转换和校验，确保可靠性。**

脚本位置：`scripts/release_checker.py`

#### 转换功能

```
python release_checker.py --convert-sql --sql-files <文件1> <文件2> ... [--output-dir <输出目录>]
```

**参数说明：**
| 参数 | 说明 |
|------|------|
| --convert-sql | 启用 SQL 转换模式 |
| --sql-files | 需要转换的 MySQL SQL 文件（可多个） |
| --output-dir | 输出目录（默认与源文件同目录） |

#### 校验功能

Python 脚本自动执行以下校验：

**PostgreSQL 校验规则（10 项）：**
- ✅ 反引号检查
- ✅ AUTO_INCREMENT 检查
- ✅ ENGINE 检查
- ✅ NOW() 函数检查
- ✅ IFNULL 函数检查
- ✅ TINYINT 类型检查
- ✅ DATETIME 类型检查
- ✅ DEFAULT CHARSET 检查
- ✅ UNSIGNED 检查
- ✅ COMMENT 语法检查

**Oracle 校验规则（11 项）：**
- ✅ 反引号检查
- ✅ AUTO_INCREMENT 检查
- ✅ ENGINE 检查
- ✅ NOW() 函数检查
- ✅ IFNULL 函数检查
- ✅ TINYINT 类型检查
- ✅ DATETIME 类型检查
- ✅ IF NOT EXISTS 检查
- ✅ LIMIT 检查
- ✅ DEFAULT CHARSET 检查
- ✅ UNSIGNED 检查

#### 转换函数实现

Python 脚本内置以下转换函数：

```
SQLConverter.convert_to_postgresql(sql_content):
    - 替换 AUTO_INCREMENT → SERIAL
    - 替换 NOW() → CURRENT_TIMESTAMP
    - 替换 DATETIME → TIMESTAMP
    - 替换 TINYINT → SMALLINT
    - 替换反引号 → 双引号
    - 移除 ENGINE=InnoDB
    - 移除 DEFAULT CHARSET
    - 移除 UNSIGNED

SQLConverter.convert_to_oracle(sql_content):
    - 替换 DATETIME → TIMESTAMP
    - 替换 TINYINT → NUMBER(3)
    - 替换反引号 → 双引号
    - 替换 LIMIT → 需手动处理
    - 移除 AUTO_INCREMENT，创建 SEQUENCE + TRIGGER
    - 替换 NOW() → SYSTIMESTAMP
    - 移除 ENGINE=InnoDB
    - 移除 DEFAULT CHARSET
    - 移除 UNSIGNED
```

### 转换输出

转换后生成：
- `<原始文件名>-postgres.sql`
- `<原始文件名>-oracle.sql`

每个文件头部包含转换说明注释。

**Python 脚本执行流程：**
```
1. 读取 MySQL SQL 文件
2. 执行 PostgreSQL 转换 → 输出 .postgres.sql
3. 执行 Oracle 转换 → 输出 .oracle.sql
4. 校验 PostgreSQL 版本（10 项规则）
5. 校验 Oracle 版本（11 项规则）
6. 显示校验结果汇总
7. 保存转换后的文件
```

## 输出示例

### 智能识别结果

```
🔍 智能识别结果
===========================================================
推送中心配置: ✅ 自动识别到
  - 检测到文件: XXXXEvent.java (包含 EVENT 定义)
  - 检测到文件: PushFeignClient.java (包含 push 相关 Feign)

Gateway 配置: ✅ 自动识别到
  - 检测到新的 Feign 定义: PushFeignClient
  - 服务名配置: ${xxx.xxx.name:xxxx-server}

配置文件变更: ✅ 自动识别到
  - 检测到注解配置: @Value("${xxx}")
  - 检测到配置类: XxxProperties.java
```

### 用户确认（第一轮）

```
请确认本次发版涉及哪些组件？（自动识别结果仅供参考）

[ ] 推送中心配置 - 推送中心服务相关配置变更（自动识别: 检测到相关代码）
[✓] Gateway 配置 - 统一网关相关配置（自动识别: 检测到新 Feign 定义）
[ ] ES 变更 - Elasticsearch 索引或查询变更
[✓] SQL 脚本 - 数据库脚本变更（DML/DDL）
[ ] 字典变更 - 数据字典或枚举配置变更
[✓] 配置文件变更 - 应用配置文件变更（自动识别: 检测到注解/配置类）
[ ] Redis 配置 - Redis 缓存或数据结构变更
[ ] MQ 消息 - 消息队列 topic 或消息格式变更
[ ] 文件存储 - 文件上传、存储路径变更
[✓] API 接口 - 对外 API 接口变更
[✓] Java 代码 - Java 代码变更
```

### SQL 转换询问

```
检测到 SQL 脚本变更。是否需要将现有 SQL 脚本转换为多数据库版本？

[ ] 是，我需要生成多数据库版本
[✓] 否，SQL 脚本已就绪
```

**用户选择"是"后，Python 脚本自动执行：**

```bash
# 执行 SQL 转换
python scripts/release_checker.py \
  --convert-sql \
  --sql-files scripts/db/v1.0.0/mysql-ddl.sql \
  --output-dir scripts/db/v1.0.0/
```

**Python 脚本输出示例：**

```
🔄 SQL 多数据库转换
===========================================================

📄 处理文件: scripts/db/v1.0.0/mysql-ddl.sql
  ✅ PostgreSQL 转换完成 (8 项变更)
    - 反引号 → 双引号
    - AUTO_INCREMENT → SERIAL
    - NOW() → CURRENT_TIMESTAMP
    - DATETIME → TIMESTAMP
    - TINYINT → SMALLINT
    - IFNULL() → COALESCE()
    - 移除 ENGINE=InnoDB
    - 移除 DEFAULT CHARSET

  ✅ Oracle 转换完成 (8 项变更)
    - 反引号 → 双引号
    - NOW() → SYSTIMESTAMP
    - DATETIME → TIMESTAMP
    - TINYINT → NUMBER(3)
    - IFNULL() → NVL()
    - AUTO_INCREMENT → SEQUENCE + TRIGGER
    - 移除 ENGINE=InnoDB
    - 移除 DEFAULT CHARSET

  🔍 PostgreSQL 验证:
    通过: 8/10, 失败: 0, 警告: 2
    ⚠️  NOW() 函数检查: 建议使用 CURRENT_TIMESTAMP 替代 NOW()
    ⚠️  COMMENT 语法检查: PostgreSQL 支持 COMMENT ON COLUMN 语法

  🔍 Oracle 验证:
    通过: 9/11, 失败: 0, 警告: 2
    ⚠️  IF NOT EXISTS 检查: Oracle 不支持 IF NOT EXISTS，需手动处理
    ⚠️  LIMIT 检查: 需手动转换为 ROWNUM 或 FETCH FIRST

  💾 PostgreSQL 已保存: scripts/db/v1.0.0/mysql-ddl-postgres.sql
  💾 Oracle 已保存: scripts/db/v1.0.0/mysql-ddl-oracle.sql

✅ SQL 转换完成
```

### 用户确认（第二轮）- TODO 清单确认

```
请确认以下发版 TODO 清单：

## 📋 发版 TODO 清单

### SQL 脚本相关
- [ ] 执行 Oracle DDL 脚本: scripts/db/v1.0.0/oracle-ddl.sql
- [ ] 执行 PostgreSQL DDL 脚本: scripts/db/v1.0.0/postgres-ddl.sql
- [ ] 验证 SQL 兼容性（Oracle: IF NOT EXISTS 需手动处理）

### 推送中心配置
- [ ] 验证推送 API 客户端配置
- [ ] 检查推送事件处理逻辑

### Gateway 配置
- [ ] 验证 API 接口变更
- [ ] 检查接口权限配置

### 配置文件变更
- [ ] 检查 @Value 注解配置
- [ ] 验证配置类加载

### Java 代码
- [ ] 执行单元测试: mvn test
- [ ] 编译验证: mvn compile

[✓] 确认 TODO 清单
[ ] 需要修改
```

### Markdown 报告

```markdown
# 📋 发版兼容性检查报告

> 项目: /path/to/your/project
> 对比分支: release/v1.0.0 → feature/next
> 生成时间: 2026-04-07 12:00:00

---

## 一、智能识别结果

| 组件 | 自动识别 | 用户确认 |
|------|----------|----------|
| 推送中心配置 | ✅ 检测到相关代码 | ✅ 是 |
| Gateway 配置 | ✅ 检测到新 Feign | ✅ 是 |
| 配置文件变更 | ✅ 检测到注解/配置类 | ✅ 是 |
| SQL 脚本 | - | ✅ 是 |
| Java 代码 | - | ✅ 是 |

## 二、变更文件汇总

| 类型 | 数量 |
|------|------|
| Java 代码 | 32 |
| SQL 脚本 | 2 |
| 其他 | 1 |

## 三、SQL 兼容性分析

### 变更的 SQL 文件
- scripts/db/v1.0.0/oracle-ddl.sql
- scripts/db/v1.0.0/postgres-ddl.sql

### 兼容性问题
- ⚠️ [LOW] IF NOT EXISTS not supported in Oracle

## 四、待处理 TODO（已确认）

- [ ] SQL 脚本：执行 DDL，验证兼容性
- [ ] 推送中心配置：验证推送 API
- [ ] Gateway 配置：验证接口变更
- [ ] 配置变更：检查注解配置
- [ ] Java 代码：执行测试和编译验证

---

*报告生成工具: release-checker*
```

## 支持的数据库

| 数据库 | 文件后缀 | 特性 |
|--------|----------|------|
| MySQL | `-mysql.sql` / `mysql/*.xml` | AUTO_INCREMENT, NOW(), 反引号 |
| PostgreSQL | `-postgres.sql` / `postgresql/*.xml` | SERIAL, CURRENT_TIMESTAMP, 双引号 |
| Oracle | `-oracle.sql` / `oracle/*.xml` | SEQUENCE+TRIGGER, SYSTIMESTAMP, VARCHAR2 |

## 限制说明

- 需要 git 仓库进行 diff 分析
- **不执行实际 SQL 验证**（AI 生成的 SQL 需要在测试环境人工验证）
- 不执行 Java 代码编译验证
- 生成的脚本需要人工审查
- MyBatis Mapper 转换需要确保有对应的目录结构
- 智能识别基于代码模式匹配，可能存在误判，需用户最终确认
- **SQL 转换验证规则库仅覆盖常见语法，复杂 SQL（存储过程、函数、触发器）需人工审查**
- **AI 无法验证数据兼容性和业务逻辑正确性**

## 跨平台兼容性

### 工具适配

本 skill 设计为**平台无关**，不依赖特定平台的专属工具。

| 工具 | 用途 | 兼容性 |
|------|------|--------|
| `git` | Git diff 分析 | 全平台 |
| `bash` | 执行 shell 命令 | 全平台 |
| `grep` | 内容搜索 | 全平台 |
| `glob` | 文件匹配 | 全平台 |
| `read` | 读取文件 | 全平台 |
| `write` | 写入文件 | 全平台 |

### Question 工具降级策略

**优先使用 Question 工具**（OpenCode/Claude Code 原生支持），**当平台不支持时自动降级为文本交互**。

#### 降级规则

```
IF Question 工具可用:
    → 使用 Question 工具（multiple=true）
ELSE:
    → 使用文本确认格式，让用户直接回复数字或选项字母
```

#### 文本确认格式（降级方案）

**单项目模式：**
```
请选择本次发版涉及的组件（回复数字，多个用逗号分隔）：

  1. 推送中心配置 - 推送中心服务相关配置变更
  2. Gateway 配置 - 统一网关相关配置
  3. ES 变更 - Elasticsearch 索引或查询变更
  4. SQL 脚本 - 数据库脚本变更（DML/DDL）
  5. 字典变更 - 数据字典或枚举配置变更
  6. 配置文件变更 - 应用配置文件变更
  7. Redis 配置 - Redis 缓存或数据结构变更
  8. MQ 消息 - 消息队列 topic 或消息格式变更
  9. 文件存储 - 文件上传、存储路径变更
  10. API 接口 - 对外 API 接口变更
  11. Java 代码 - Java 代码变更

示例回复: 1,4,6,11
```

**SQL 转换询问：**
```
检测到 SQL 脚本变更。是否需要转换为多数据库版本？

  1. 是，我需要生成多数据库版本
  2. 否，SQL 脚本已就绪

请选择 (1/2):
```

**TODO 清单确认：**
```
请确认以下发版 TODO 清单：

## 📋 发版 TODO 清单
（此处列出 TODO 项）

请选择：
  1. 确认 TODO 清单，开始生成报告
  2. 需要修改（请说明需要调整的内容）
```

**批量确认模式：**
```
检测到 3 个项目需要检查，请选择确认模式：

  1. 批量确认（所有项目使用相同组件）
  2. 逐个确认（每个项目单独选择）
  3. 使用智能识别结果（无需手动确认）

请选择 (1/2/3):
```

## 最佳实践

1. 每次发版前运行检查
2. 仔细确认智能识别结果和用户选择的组件
3. 如果有 SQL 变更且需要多数据库支持，使用内置转换功能
4. **执行 SQL 语法验证（自动检查）**
5. **在测试环境人工验证生成的 SQL 脚本**
6. 确认生成的 TODO 清单是否符合实际需求
7. 生成 Markdown 报告留存
8. 合并到主分支前审查 TODO 项
