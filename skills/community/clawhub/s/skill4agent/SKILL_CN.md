---
name: skill4agent
description: 当需要搜索、查阅和安装在线技能库中的 skills 时使用此技能，支持中文。
requirements:
  - node.js: ">=16.0.0"
  - npm: "*"
  - npx: "*"
external_dependencies:
  - npm: https://www.npmjs.com/package/skill4agent
  - api: https://skill4agent.com/api
source: https://www.skill4agent.com
---

## 技能目的
使用skill4agent平台提供CLI命令或API接口，实现搜索技能、查阅技能详情、安装技能的完整工作流。

## 使用选项
此技能提供两种的使用方式：
1. **CLI 选项**：需要 Node.js 环境，使用 `npx skill4agent` 命令
2. **API 选项**：无外部依赖，使用直接的 HTTPS 请求访问 skill4agent.com

根据可用环境选择一种方式。如果有 Node.js 可用，优先使用 CLI 选项以获得便利。如果没有 Node.js，使用 API 选项。

## 三种核心操作

### 1. 搜索技能（search）
**用途**：查找相关技能，支持中文、英文或中英混合关键词

#### CLI 命令（需要Node.js环境）
```bash
# 基础搜索（建议使用-j，返回JSON格式）
npx skill4agent search <关键词> -j

# 控制返回结果数量（建议使用-j，返回JSON格式）
npx skill4agent search <关键词> -j -l <数量>
```

#### API 接口
```
https://skill4agent.com/api/search?keyword=<关键词>
```

**参数说明**：
- `keyword`（必填）：搜索关键词（支持中文、英文、中英混合）
- `limit`（可选）：返回结果数量，默认 10，最大 50

**重要返回字段**：
- `skillId`：技能ID
- `source`：技能源仓库
- `skill_name`：技能名称
- `description`：技能描述
- `tags`：技能标签
- `totalInstalls`：安装次数
- `read_skill_url`：技能详情查阅地址
- `download_zip_url`：技能下载地址
- `translation`：翻译信息（原版语言、是否有翻译版、翻译版语言）
- `script`：脚本检查信息（是否包含脚本、是否含有敏感代码、敏感代码具体位置）

### 2. 查阅技能（read）
**用途**：查看技能的详细信息和SKILL.md完整内容

#### CLI 命令（需要Node.js环境）
```bash
# 查阅原版内容（建议使用-j，返回JSON格式）
npx skill4agent read <source> <skill_name> -j

# 查阅翻译版内容（建议使用-j，返回JSON格式）
npx skill4agent read <source> <skill_name> --type translated -j
```

#### API 接口
```
https://skill4agent.com/api/skills/info?source=<source>&skill_name=<skill_name>
```

**参数说明**：
- `source`（必填）：技能源仓库（在搜索结果中获取）
- `skill_name`（必填）：技能名称（在搜索结果中获取）
- `type`（可选）：内容类型（`original`/`translated`），默认 `original`

**重要返回字段**：
- `skillId`：技能ID
- `source`：技能源仓库
- `skill_name`：技能名称
- `download_zip_url`：技能下载地址
- `translation`：翻译信息（原版语言、是否有翻译版、翻译版语言）
- `script`：脚本检查信息（是否包含脚本、是否含有敏感代码、敏感代码具体位置）
- `content`：技能详细内容（SKILL.md的完整内容）

### 3. 安装技能（install）
**用途**：将技能安装到本地项目

#### CLI 命令（需要Node.js环境）
```bash
# 安装原版技能
npx skill4agent install <source> <skill_name>

# 安装翻译版技能
npx skill4agent install <source> <skill_name> --type translated
```

#### API 接口
```
https://skill4agent.com/api/download/<skillId>?type=<type>
```

**参数说明**：
- `skillId`（必填）：技能ID（在搜索结果或查阅技能详情中获取）
- `type`（可选）：内容类型（`original`/`translated`），默认 `original`

#### 安装说明
- CLI命令：安装位置为当前目录下的 `.agents/skills/<skill_name>` 目录
- API接口：下载 ZIP 文件后解压得到 `<skill_name>` 目录
- 如需把skill安装到其他路径（如用户指定的或所在应用要求的路径），则自行转移到目标目录

## 脚本安全检查
通过返回的 `script` 字段，了解技能是否包含脚本并是否存在敏感代码。

- `has_script`：`true` 表示包含脚本
- `script_check_result`：
  - `safe`：脚本安全
  - `need attention`：存在敏感代码
- `script_check_notes`：敏感代码的具体位置，安装后需复检

注：对于包含脚本并存在敏感代码的技能，在安装前必须得到用户同意，安装后需对`script_check_notes`中列出的敏感代码所在位置并结合代码上下文进行复检，确保无恶意程序、获取用户私密信息、修改或删除本地文件、修改系统配置等风险。

## 场景化工作流

### 场景 1：仅了解相关技能
- **操作**：使用关键词搜索相关技能
- **输出**：总结搜索结果，等待用户进一步指示

### 场景 2：寻找合适技能完成任务
1. **搜索**：使用关键词搜索相关技能
2. **筛选**：根据 `description`、`tags`、`totalInstalls` 初步筛选
3. **查阅**：查阅候选技能的详细信息，分析技能是否符合任务需求
4. **推荐**：将最终合适的技能推荐给用户（如技能包含脚本并存在敏感代码，必须告知用户）

### 场景 3：搜索并安装技能
1. **搜索**：使用关键词搜索相关技能
2. **筛选**：根据搜索结果筛选合适技能
3. **查阅**（如需）：进一步了解技能详情，分析技能是否符合任务需求
4. **安装**：安装技能到所需目录（对于包含脚本并存在敏感代码的技能，不能自行安装，必需得到用户同意后才可安装）
5. **脚本安全复检**：如技能包含脚本并存在敏感代码，安装后需对`script_check_notes`中列出的敏感代码所在位置并结合代码上下文进行复检，确保无恶意程序、获取用户私密信息、修改或删除本地文件、修改系统配置等风险。

## 搜索优化建议
当搜索不出结果时：
1. **优化关键词**：使用更通用或更精简的关键词
2. **切换语言**：
   - 英文搜不到 → 尝试中文或中英混合
   - 中文搜不到 → 尝试英文或中英混合

## 最佳实践
- **JSON 格式**：搜索和查阅命令应该添加 `-j` 参数以返回json格式，方便解析
- **语言版本选择**：根据用户的常用语言选择合适的版本（通过`translation`字段了解原版和翻译版的语言）
