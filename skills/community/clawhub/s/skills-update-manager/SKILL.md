---
name: skills-update-manager
description: 管理已安装技能的注册、版本跟踪与自动更新检查；当用户安装新技能、检查技能更新或配置更新策略时使用。
dependency:
  python:
    - requests==2.31.0
    - beautifulsoup4==4.12.2
    - packaging==23.2
    - PyYAML==6.0.1
---

# 技能更新管理器

## 任务目标
- 本 Skill 用于：统一管理所有已安装技能的注册信息与版本跟踪
- 能力包含：技能注册、版本记录、自动检查更新、更新配置管理
- 触发条件：安装新技能前、需要检查技能更新时、首次加载本技能

## 前置准备

### 依赖说明
scripts脚本所需的依赖包及版本：
```
requests==2.31.0
beautifulsoup4==4.12.2
packaging==23.2
PyYAML==6.0.1
```

### 配置文件初始化
首次使用本技能时，需要将已安装的技能注册到skills-update-manager，并需要在工作目录下 `MEMORY.md`文件添加以下：

```markdown
# 技能更新管理器配置

## 更新设置
- 启用更新检查：是/否
- 上次检查时间：YYYY-MM-DD HH:MM:SS

## 使用说明
1. 每次安装技能前优先加载 skills-update-manager
2. 更新开启时，启动技能前需加载本管理器检查更新
3. 更新关闭时，跳过更新检查
```

## 操作步骤

### 1. 注册新技能

**核心流程**：智能体自动从技能文件中提取元数据，无需用户提供详细信息。

#### 步骤1：提取技能元数据
当用户安装新技能时，智能体需要从技能文件中提取以下信息：

**方式A：从 .skill 或者.zip文件提取**
1. 解压 .skill 文件（ZIP格式）
2. 读取 `SKILL.md` 文件
3. 从 YAML 前言区提取：
   - `name`：技能名称
   - `version`：版本号（如果存在）
4. 从文件路径或内容推断更新地址

**方式B：从已解压的技能目录提取**
1. 读取 `SKILL.md` 文件
2. 从 YAML 前言区提取 name 字段

**调用脚本**：`scripts/skill_registry.py --action extract --skill-path <路径>`

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

#### 步骤2：识别来源和更新地址
智能体根据以下信息推断来源类型和更新地址：

**判断规则**：
- 如果用户提供 GitHub 仓库地址 → 来源：`github`
- 如果用户提供 ClawHub 页面链接 → 来源：`clawhub`
- 如果用户未提供 → 询问用户技能来源

**典型场景**：
```
用户："安装这个技能：https://github.com/user/skill-name"
智能体：识别来源为 github，提取仓库地址

用户："安装 xxx.skill 文件"
智能体：提取技能名称后询问："这个技能的来源是什么？(GitHub/ClawHub/其他)"
```

#### 步骤3：注册技能
**调用脚本**：`scripts/skill_registry.py --action register`

**必需参数**：
- `--name`：技能名称（从 SKILL.md 提取）

**可选参数**（智能体推断或询问用户）：
- `--version`：当前版本号（从 SKILL.md 提取，默认 "1.0.0"）
- `--source`：来源类型（github/clawhub，默认 "github"）
- `--update-url`：更新地址（根据来源推断或询问用户）

**执行示例**：
```bash
# 完整参数（智能体已提取所有信息）
python scripts/skill_registry.py \
  --action register \
  --name "pdf-processor" \
  --version "1.0.0" \
  --source "github" \
  --update-url "https://github.com/user/pdf-processor"

# 最小参数（仅需名称，其余使用默认值）
python scripts/skill_registry.py \
  --action register \
  --name "pdf-processor"
```

**智能体职责**：
- 自动从技能文件中提取名称和版本号
- 根据用户提供的信息推断来源和更新地址
- 信息不完整时主动询问用户
- 确保所有必需字段已填充后再调用注册

### 2. 检查技能更新
根据 MEMORY.md 中的配置，决定是否检查更新：

**调用脚本**：`scripts/skill_registry.py --action check_updates`

**执行逻辑**：
1. 读取 `MEMORY.md` 配置，判断更新检查是否启用
2. 如果启用，遍历所有已注册技能
3. 根据技能来源类型调用对应的版本检查逻辑：
   - **GitHub**：访问 `https://api.github.com/repos/{owner}/{repo}/releases/latest`
   - **ClawHub**：访问技能页面，解析 "Current version" 字段
4. 对比本地版本与远程版本
5. 返回有更新的技能列表

**输出格式**：
```json
{
  "has_updates": true,
  "updates": [
    {
      "name": "example-skill",
      "current_version": "v1.0.0",
      "latest_version": "v1.2.0",
      "source": "github",
      "update_url": "https://github.com/user/example-skill"
    }
  ]
}
```

**智能体职责**：
- 解析检查结果，向用户推送更新通知
- 询问用户是否执行更新操作
- 如果用户确认更新，使用 `git clone` 或下载方式获取新版本
- 更新本地技能记录

### 3. 查看已注册技能
列出所有已安装技能的详细信息：

**调用脚本**：`scripts/skill_registry.py --action list`

**输出内容**：
- 编号
- 名称
- 版本
- 来源
- 更新地址
- 是否可更新
- 更新状态

### 4. 更新配置
修改 MEMORY.md 中的更新设置：

**调用脚本**：`scripts/skill_registry.py --action update_config`

**参数说明**：
- `--enable-updates`: 是否启用更新检查（true/false）

**执行方式**：
```bash
python scripts/skill_registry.py --action update_config --enable-updates true
```

### 5. 更新技能记录
当技能完成更新后，更新本地记录的版本号：

**调用脚本**：`scripts/skill_registry.py --action update_record`

**参数说明**：
- `--name`: 技能名称
- `--version`: 新版本号

## 资源索引

### 核心脚本
- [scripts/skill_registry.py](scripts/skill_registry.py) - 技能注册与更新管理核心脚本

### 参考文档
- [references/registry_format.md](references/registry_format.md) - 技能记录数据格式规范，包含JSON结构定义、自动提取流程与示例

## 注意事项

### 技能元数据提取
- 优先从 SKILL.md 的 YAML 前言区提取 name 和 version
- 如果缺少版本号，使用默认值 "1.0.0"
- 如果缺少更新地址，必须询问用户或根据上下文推断

### 版本号格式
- 推荐使用语义化版本格式：`v1.0.0` 或 `1.0.0`
- 支持其他格式：`2024.01.01`、`v2.1` 等
- 版本比较遵循语义化版本规则

### GitHub更新检查
- 使用 GitHub API，无需认证
- 频率限制：每小时60次请求（未认证）
- 提取 `tag_name` 或 `name` 字段作为版本号

### ClawHub更新检查
- 需要解析HTML页面
- 定位 "Current version" 文本节点
- 提取版本号字符串

### 更新策略
- 建议在安装新技能前检查 MEMORY.md 配置
- 如果启用更新检查，每次加载技能前调用检查逻辑
- 批量检查更新时，注意频率限制

### 错误处理
脚本已包含以下错误处理：
- 网络请求失败
- JSON解析错误
- 版本号格式不正确
- 技能不存在

## 使用示例

### 示例1：首次使用技能更新管理器
**场景**：用户首次加载本技能

**执行步骤**：
1. 智能体读取当前工作目录，检查是否存在 `MEMORY.md`
2. 如果不存在，调用 `update_config` 创建配置文件
3. 询问用户是否启用更新检查
4. 根据用户选择写入配置

### 示例2：从 GitHub 安装新技能
**场景**：用户说"安装这个技能：https://github.com/user/pdf-processor"

**智能体执行流程**：
1. 识别来源为 GitHub
2. 克隆仓库或下载 .skill 文件
3. 读取 SKILL.md 提取元数据：name="pdf-processor", version="1.0.0"
4. 调用脚本注册：
   ```bash
   python scripts/skill_registry.py --action register \
     --name "pdf-processor" \
     --version "1.0.0" \
     --source "github" \
     --update-url "https://github.com/user/pdf-processor"
   ```
5. 继续安装流程

### 示例3：从本地文件安装技能
**场景**：用户上传 "data-analyzer.skill" 文件

**智能体执行流程**：
1. 解压 .skill 文件
2. 读取 SKILL.md 提取元数据：name="data-analyzer", version="2.0.0"
3. 询问用户："这个技能的来源是什么？(GitHub/ClawHub/其他)"
4. 用户回答："GitHub，地址是 https://github.com/user/data-analyzer"
5. 调用脚本注册：
   ```bash
   python scripts/skill_registry.py --action register \
     --name "data-analyzer" \
     --version "2.0.0" \
     --source "github" \
     --update-url "https://github.com/user/data-analyzer"
   ```

### 示例4：检查更新
**场景**：用户希望检查所有已安装技能是否有更新

**执行步骤**：
1. 智能体调用 `check_updates`
2. 解析返回结果
3. 向用户推送更新列表
4. 询问是否执行更新
5. 根据用户选择使用 `git clone` 或其他方式更新技能
6. 调用 `update_record` 更新本地记录
