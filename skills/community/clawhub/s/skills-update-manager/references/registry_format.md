# 技能注册数据格式规范

## 目录
- [数据结构](#数据结构)
- [版本号格式](#版本号格式)
- [来源类型](#来源类型)
- [更新地址格式](#更新地址格式)
- [自动提取流程](#自动提取流程)
- [完整示例](#完整示例)

## 数据结构

### 注册表文件
**文件路径**：`./skills_registry.json`

**JSON结构**：
```json
{
  "skills": [
    {
      "id": 1,
      "name": "技能名称",
      "version": "v1.0.0",
      "source": "github",
      "update_url": "https://github.com/owner/repo",
      "can_update": true,
      "update_status": "未检查",
      "registered_at": "2024-01-01 12:00:00",
      "updated_at": "2024-01-02 14:30:00"
    }
  ],
  "next_id": 2
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | integer | 是 | 唯一编号，自动递增 |
| name | string | 是 | 技能名称，唯一标识 |
| version | string | 是 | 当前版本号 |
| source | string | 是 | 来源类型：github 或 clawhub |
| update_url | string | 是 | 更新地址，用于检查版本更新 |
| can_update | boolean | 是 | 是否可更新，默认 true |
| update_status | string | 是 | 更新状态：未检查/有更新/已是最新版本/检查失败 |
| registered_at | string | 是 | 注册时间，格式：YYYY-MM-DD HH:MM:SS |
| updated_at | string | 否 | 最后更新时间，格式：YYYY-MM-DD HH:MM:SS |

## 版本号格式

### 支持的格式
脚本支持多种版本号格式，使用语义化版本规范进行比较：

1. **语义化版本**（推荐）
   - 格式：`v1.0.0` 或 `1.0.0`
   - 示例：`v1.2.3`, `2.0.0`, `v3.1.0`

2. **日期版本**
   - 格式：`YYYY.MM.DD` 或 `YYYY-MM-DD`
   - 示例：`2024.01.15`, `2024-01-15`

3. **简化版本**
   - 格式：`vX.Y` 或 `X.Y`
   - 示例：`v1.2`, `3.0`

### 版本比较规则
- 使用 `packaging.version.parse()` 进行语义化比较
- 自动去除 `v` 前缀
- 比较规则：主版本号 > 次版本号 > 补丁版本号

**示例**：
```
v1.2.0 < v1.3.0
v1.2.9 < v1.3.0
v2.0.0 > v1.9.9
```

## 来源类型

### GitHub (github)
- 标识符：`github`
- 版本获取方式：访问 GitHub API
- API端点：`https://api.github.com/repos/{owner}/{repo}/releases/latest`
- 返回字段：`tag_name` 或 `name`

**注意事项**：
- 无需认证即可访问公开仓库
- 频率限制：每小时60次请求（未认证）
- 私有仓库需要配置认证

### ClawHub (clawhub)
- 标识符：`clawhub`
- 版本获取方式：解析HTML页面
- 定位方式：查找 "Current version" 文本节点
- 提取规则：正则表达式匹配版本号字符串

**注意事项**：
- 需要解析HTML结构
- 页面结构变化可能导致解析失败
- 建议添加错误处理和重试机制

## 更新地址格式

### GitHub仓库地址
**格式**：`https://github.com/{owner}/{repo}`

**示例**：
```
https://github.com/coze-dev/coze-studio
https://github.com/microsoft/vscode
https://github.com/openai/gpt-3
```

**验证规则**：
- 必须以 `https://github.com/` 开头
- 必须包含 `{owner}/{repo}` 两级路径
- 不应以 `.git` 结尾
- 不应包含 `/releases` 等额外路径

### ClawHub技能地址
**格式**：`https://clawhub.ai/skills/{skill-id}` 或具体技能页面URL

**示例**：
```
https://clawhub.ai/skills/example-skill
https://clawhub.ai/skills/12345
```

**验证规则**：
- 必须以 `https://clawhub.ai/` 开头
- 必须是有效的技能详情页面

## 自动提取流程

### 概述
智能体在注册技能时，需要自动从技能文件中提取元数据，减少用户输入负担。

### 提取源

#### 1. 从 .skill 文件提取
**文件结构**：
```
example-skill.skill (ZIP格式)
├── SKILL.md              # 元数据入口
├── scripts/
│   └── process.py
├── references/
│   └── guide.md
└── assets/
```

**提取步骤**：
1. 解压 .skill 文件（使用 zipfile）
2. 查找并读取 `SKILL.md` 文件
3. 解析 YAML 前言区（`---` 包围的部分）
4. 提取以下字段：
   - `name`：技能名称
   - `version`：版本号（如果存在）

**YAML 前言区示例**：
```yaml
---
name: pdf-processor
description: PDF文件处理技能
version: 1.0.0
dependency:
  python:
    - PyPDF2==3.0.0
---
```

#### 2. 从技能目录提取
**目录结构**：
```
example-skill/
├── SKILL.md
├── scripts/
└── references/
```

**提取步骤**：
1. 直接读取目录下的 `SKILL.md` 文件
2. 解析 YAML 前言区
3. 提取 name 和 version 字段

### 提取规则

#### 必需字段
- **name**：必须存在，从 YAML 前言区的 `name` 字段提取
- 如果缺少 name，提取失败

#### 可选字段
- **version**：如果 YAML 中没有 version 字段，使用默认值 `"1.0.0"`
- **source**：无法从文件中提取，需要智能体根据上下文推断或询问用户
- **update_url**：无法从文件中提取，需要智能体根据用户提供的信息确定

### 脚本调用示例

**提取元数据**：
```bash
python scripts/skill_registry.py --action extract --skill-path "./example-skill.skill"
```

**输出示例**：
```json
{
  "success": true,
  "metadata": {
    "name": "pdf-processor",
    "version": "1.0.0",
    "source": null,
    "update_url": null
  }
}
```

### 智能体职责

#### 信息提取阶段
1. 接收用户提供技能文件或路径
2. 调用 `extract` 操作提取元数据
3. 解析返回结果，获取 name 和 version

#### 信息补全阶段
如果缺少 source 或 update_url，智能体需要：

**场景1：用户提供 GitHub 地址**
```
用户："安装这个技能：https://github.com/user/skill-name"

智能体推断：
- source: github
- update_url: https://github.com/user/skill-name
```

**场景2：用户提供 ClawHub 地址**
```
用户："安装这个技能：https://clawhub.ai/skills/skill-name"

智能体推断：
- source: clawhub
- update_url: https://clawhub.ai/skills/skill-name
```

**场景3：用户仅提供文件**
```
用户：上传 example-skill.skill 文件

智能体询问："请提供这个技能的来源地址（GitHub或ClawHub）"
用户回答："GitHub: https://github.com/user/example-skill"

智能体推断：
- source: github
- update_url: https://github.com/user/example-skill
```

## 完整示例

### 示例1：从 GitHub 安装并注册技能

**用户输入**：
```
安装这个技能：https://github.com/user/pdf-processor
```

**智能体执行流程**：

1. **克隆仓库或下载 .skill 文件**
   ```bash
   git clone https://github.com/user/pdf-processor.git
   ```

2. **提取元数据**
   ```bash
   python scripts/skill_registry.py --action extract --skill-path "./pdf-processor"
   ```
   
   **输出**：
   ```json
   {
     "success": true,
     "metadata": {
       "name": "pdf-processor",
       "version": "1.0.0",
       "source": null,
       "update_url": null
     }
   }
   ```

3. **推断来源信息**
   - 从用户提供的地址识别：source = "github"
   - update_url = "https://github.com/user/pdf-processor"

4. **注册技能**
   ```bash
   python scripts/skill_registry.py --action register \
     --name "pdf-processor" \
     --version "1.0.0" \
     --source "github" \
     --update-url "https://github.com/user/pdf-processor"
   ```

**注册表记录**：
```json
{
  "id": 1,
  "name": "pdf-processor",
  "version": "1.0.0",
  "source": "github",
  "update_url": "https://github.com/user/pdf-processor",
  "can_update": true,
  "update_status": "未检查",
  "registered_at": "2024-01-15 10:30:00"
}
```

### 示例2：从本地 .skill 文件注册

**用户输入**：
```
上传文件：data-analyzer.skill
```

**智能体执行流程**：

1. **提取元数据**
   ```bash
   python scripts/skill_registry.py --action extract --skill-path "./data-analyzer.skill"
   ```
   
   **输出**：
   ```json
   {
     "success": true,
     "metadata": {
       "name": "data-analyzer",
       "version": "2.0.0",
       "source": null,
       "update_url": null
     }
   }
   ```

2. **询问用户来源**
   ```
   智能体："请提供这个技能的来源地址"
   用户："GitHub: https://github.com/user/data-analyzer"
   ```

3. **推断来源信息**
   - source = "github"
   - update_url = "https://github.com/user/data-analyzer"

4. **注册技能**
   ```bash
   python scripts/skill_registry.py --action register \
     --name "data-analyzer" \
     --version "2.0.0" \
     --source "github" \
     --update-url "https://github.com/user/data-analyzer"
   ```

### 示例3：检查更新结果

**返回格式**：
```json
{
  "success": true,
  "message": "检查完成，发现 1 个技能有更新",
  "has_updates": true,
  "updates": [
    {
      "name": "pdf-processor",
      "current_version": "v1.2.0",
      "latest_version": "v1.3.0",
      "source": "github",
      "update_url": "https://github.com/user/pdf-processor"
    }
  ]
}
```

## 配置文件格式

### MEMORY.md 结构
**文件路径**：`./MEMORY.md`

```markdown
# 技能管理器配置

## 更新设置
- 启用更新检查：是/否
- 上次检查时间：YYYY-MM-DD HH:MM:SS

## 使用说明
1. 每次安装技能前优先加载 skills-manager
2. 更新开启时，启动技能前需加载本管理器检查更新
3. 更新关闭时，跳过更新检查
```

### 字段说明

| 字段 | 可选值 | 说明 |
|------|--------|------|
| 启用更新检查 | 是/否 | 控制是否自动检查更新 |
| 上次检查时间 | 时间戳 | 记录最后一次检查更新的时间 |

## 错误处理

### 常见错误

1. **技能已存在**
   ```json
   {
     "success": false,
     "message": "技能 'xxx' 已存在，请使用 update_record 更新版本"
   }
   ```

2. **版本获取失败**
   ```json
   {
     "update_status": "版本检查失败"
   }
   ```

3. **网络请求超时**
   ```json
   {
     "update_status": "检查出错: Connection timeout"
   }
   ```

4. **技能不存在**
   ```json
   {
     "success": false,
     "message": "未找到技能 'xxx'"
   }
   ```

5. **元数据提取失败**
   ```json
   {
     "success": false,
     "message": "未找到 SKILL.md 文件"
   }
   ```

## 验证规则

### 注册验证
- [x] 技能名称不能为空
- [x] 技能名称唯一性检查
- [x] 版本号格式正确（可选，有默认值）
- [x] 来源类型为 github 或 clawhub（可选，有默认值）
- [x] 更新地址格式正确（可选）

### 版本验证
- [x] 版本号不为空
- [x] 版本号格式可解析
- [x] 版本比较逻辑正确

### URL验证
- [x] GitHub URL符合格式要求
- [x] ClawHub URL符合格式要求
- [x] URL可访问性检查（可选）

### 元数据提取验证
- [x] .skill 文件为有效 ZIP 格式
- [x] SKILL.md 文件存在
- [x] YAML 前言区格式正确
- [x] name 字段存在且非空
