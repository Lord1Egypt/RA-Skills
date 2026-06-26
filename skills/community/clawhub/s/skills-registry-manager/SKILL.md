---
name: skill-registry-manager
description: "管理和安装 Claude Code skills 的工具。Use when: 列出可用skills、有哪些skills、安装skill、管理skills、添加订阅、列出订阅、查看订阅、删除订阅、取消订阅。NOT for: 与 skill 管理无关的任务。"
---

# Skill Registry

管理和安装 Claude Code skills 的工具。维护一份常用 skills 注册表，支持订阅远程注册表或本地注册表文件，便于共享和分发 skills 列表。

## 触发条件

当用户提到以下意图时激活：
- "列出可用 skills"、"有哪些 skills"
- "安装 skill"、"装一下 xxx skill"
- "管理 skills"
- "添加订阅"、"订阅 xxx URL"
- "列出订阅"、"查看订阅"
- "删除订阅"、"取消订阅 xxx"

## 工作流程

### 1. 读取注册表

读取本技能目录下的 `registry.yaml`，解析本地 skills 和订阅列表。

#### 1.1 加载订阅注册表

遍历 `subscriptions` 列表，根据 `url` 字段判断来源类型并加载：

**判断来源类型**：
- 以 `http://` 或 `https://` 开头 → 远程注册表，使用 WebFetch 获取
- 其他情况 → 本地文件路径，按以下规则解析后使用 Read 工具读取文件内容，按 YAML 解析

**本地路径解析规则**（按优先级）：
1. 展开环境变量（`$HOME`、`$HOSTNAME` 等）和 `~`
2. 如果展开后是相对路径（不以 `/` 开头），则基于**当前注册表文件所在目录**解析为绝对路径

**加载流程**：
1. **防止循环引用**: 维护已加载路径/URL 集合，跳过重复的条目
2. **递归加载**: 注册表格式统一，支持嵌套的 subscriptions（递归加载，本地和远程可互相引用）
3. **合并 skills**: 将订阅 skills 合并到总列表，为每个 skill 标注来源（本地 / 订阅名称）
4. **处理重名**: 本地 skills 优先，后订阅覆盖前订阅
5. **错误处理**: 单个订阅加载失败时记录警告，继续处理其他订阅

### 2. 展示可用列表

以带编号的表格形式展示所有可用 skills，方便用户通过编号快速选择：

```
| # | 名称 | 描述 | 来源 | 状态 |
|---|------|------|------|------|
| 1 | [skill-name](repo-url) | ...  | 本地 | ...  |
| 2 | [skill-name](repo-url) | ...  | official | ...  |
```

"名称" 列如有 `repo` 字段则渲染为链接，方便用户查看项目详情。"来源" 列显示 skill 的注册表来源：本地 skills 显示 "本地"，订阅的 skills 显示订阅名称。

编号从 1 开始，按 registry.yaml 中的顺序递增。同时检查 `~/.claude/skills/` 和当前项目 `.claude/skills/` 下是否已存在同名目录，标注已安装状态。

### 3. 用户选择

使用 AskUserQuestion 工具让用户选择要安装的 skill。用户可以通过编号（如 "1"）或名称指定。如果用户在触发时已经指定了名称或编号，跳过此步。

### 4. 选择安装位置

使用 AskUserQuestion 询问安装位置：
- **全局安装** (`~/.claude/skills/`) — 所有项目可用
- **项目安装** (`.claude/skills/`) — 仅当前项目可用

### 5. 执行安装

安装前检查该 skill 的 `depends` 字段。如果存在依赖且依赖的 skill 尚未安装，先按相同流程安装依赖的 skill（递归处理），全部依赖就绪后再安装目标 skill。

根据 registry.yaml 中的 `source` 类型执行安装：

- **npx**: 在目标 skills 目录下运行 install 命令
  ```bash
  cd <target_skills_dir> && <install_command>
  ```
- **git**: 克隆仓库到目标 skills 目录
  ```bash
  git clone <install_url> <target_skills_dir>/<skill_name>
  ```
- **local**: 复制本地目录到目标位置。`install` 路径解析规则与订阅 `url` 一致：先展开环境变量和 `~`，若为相对路径则基于**当前注册表文件所在目录**解析。
  ```bash
  cp -r <resolved_source_path> <target_skills_dir>/<skill_name>
  ```

### 6. 确认结果

检查目标目录下是否存在安装后的 skill 目录，报告安装结果。

## 订阅管理

### 添加订阅

当用户触发 "添加订阅" 或 "订阅 URL" 时：

1. 获取订阅名称和 URL/路径（通过用户输入或 AskUserQuestion）
2. 验证订阅源可访问且格式正确（应包含 skills 列表）：
   - **远程 URL**（`http://` / `https://` 开头）：使用 WebFetch 验证
   - **本地文件路径**：展开环境变量（`$HOME`、`~`），使用 Read 工具验证文件存在且为合法 YAML
3. 将新订阅追加到 registry.yaml 的 subscriptions 列表（`url` 字段保留用户原始输入，如 `$HOME/xxx.yaml`）
4. 报告添加结果

### 列出订阅

当用户触发 "列出订阅" 或 "查看订阅" 时：

1. 读取 registry.yaml 中的 subscriptions 列表
2. 对每个订阅，检查可用性：
   - **远程 URL**：使用 WebFetch 获取远程注册表
   - **本地文件路径**：展开环境变量后使用 Read 工具检查文件是否存在且可读
3. 以表格形式展示：

```
| 名称 | URL/路径 | 类型 | 状态 | skills 数量 |
|------|----------|------|------|-------------|
| official | https://... | 远程 | 可用 | 15 |
| local-team | $HOME/team-skills.yaml | 本地 | 可用 | 8 |
| team | https://... | 远程 | 不可用 | - |
```

### 删除订阅

当用户触发 "删除订阅" 或 "取消订阅 xxx" 时：

1. 读取当前 subscriptions 列表
2. 找到匹配的订阅（按名称匹配）
3. 使用 AskUserQuestion 确认删除
4. 从 registry.yaml 中移除该订阅
5. 报告删除结果

## 注册表格式

订阅注册表采用统一的 YAML 格式，可以是远程 URL 或本地文件：

```yaml
# 可选：嵌套订阅（支持递归加载，本地和远程可混用）
subscriptions:
  - name: upstream
    url: https://another-registry.yaml
  - name: local-shared
    url: $HOME/shared-skills/registry.yaml
  - name: team
    url: ~/team/skills-registry.yaml

# skills 列表
skills:
  - name: example-skill
    description: 示例 skill
    source: npx
    install: "npx skills add owner/repo@skill-name -y -g"
    repo: https://github.com/owner/repo/tree/main/skills/skill-name  # 可选

  - name: local-skill
    description: 本地 skill（相对路径，基于本注册表文件所在目录）
    source: local
    install: ./local-skill
```

### 本地路径说明

`url`（订阅）和 `install`（local source）字段支持以下路径格式：
- `$HOME/path/to/file.yaml` — 使用 `$HOME` 环境变量
- `~/path/to/file.yaml` — 使用 `~` 简写
- `/absolute/path/to/file.yaml` — 绝对路径
- `./relative/path` 或 `../sibling/path` — 相对路径，基于当前注册表文件所在目录解析
- 路径中可包含任意环境变量，如 `$HOSTNAME`、`$USER` 等

路径展开规则：
1. 将 `~` 展开为用户主目录，将 `$VAR` 格式的环境变量通过 shell `echo` 展开为实际值
2. 展开后若为相对路径（不以 `/` 开头），则以当前注册表文件所在目录为基准拼接为绝对路径
3. registry.yaml 中保留用户原始输入的路径格式
