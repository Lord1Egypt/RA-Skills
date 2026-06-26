# OpenClaw SKILL.md 格式完整规范

> 来源：https://docs.openclaw.ai/clawhub/skill-format
> 提取日期：2026-06-04

## 一、目录结构

一个 Skill 就是一个文件夹：

### 必需文件
- `SKILL.md`（或 `skill.md`）

### 可选文件
- 任何支持的文本类文件
- `.clawhubignore` — 发布/同步时的忽略规则
- `.gitignore` — 同样被尊重

### CLI 写入的元数据文件
- `<skill>/.clawhub/origin.json` — 本地安装元数据
- `<workdir>/.clawhub/lock.json` — 工作目录安装状态

## 二、YAML Frontmatter 字段

### 基础字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `string` | 推荐 | 技能名称 |
| `description` | `string` | 推荐 | 技能简短摘要，用于 UI 和搜索结果 |
| `version` | `string` | 推荐 | 语义化版本号（如 `1.0.0`） |

### metadata.openclaw 子字段

> 别名：`metadata.clawdbot`、`metadata.clawdis`

| 字段 | 类型 | 说明 |
|------|------|------|
| `requires.env` | `string[]` | 必需的环境变量列表 |
| `requires.bins` | `string[]` | CLI 二进制文件，全部必须已安装 |
| `requires.anyBins` | `string[]` | CLI 二进制文件，至少一个必须存在 |
| `requires.config` | `string[]` | 技能读取的配置文件路径 |
| `primaryEnv` | `string` | 技能的主要凭证环境变量 |
| `envVars` | `array` | 环境变量声明数组，每项：name(必填)、required(选填bool)、description(选填) |
| `always` | `boolean` | 若 true，技能始终活跃（无需显式安装） |
| `skillKey` | `string` | 覆盖技能的调用键 |
| `emoji` | `string` | 显示表情符号 |
| `homepage` | `string` | 技能主页或文档 URL |
| `os` | `string[]` | 操作系统限制 |
| `install` | `array` | 依赖安装规格 |
| `nix` | `object` | Nix 插件规格 |
| `config` | `object` | Clawdbot 配置规格 |

### install 规格

```yaml
metadata:
  openclaw:
    install:
      - kind: brew      # brew, node, go, uv
        formula: jq
        bins: [jq]
      - kind: node
        package: typescript
        bins: [tsc]
```

### envVars 声明

```yaml
metadata:
  openclaw:
    primaryEnv: TODOIST_API_KEY
    envVars:
      - name: TODOIST_API_KEY
        required: true
        description: Todoist API token.
      - name: TODOIST_PROJECT_ID
        required: false
        description: Optional default project ID.
```

**重要**：可选变量必须用 envVars + required: false，不能放入 requires.env

## 三、文件类型限制

- 只有文本类文件被接受
- 扩展名白名单定义在 `packages/schema/src/textFiles.ts`
- MIME 类型以 text/ 开头的均视为文本
- 额外白名单：JSON、YAML、TOML、JS、TS、Markdown、SVG
- PowerShell 文件（.ps1/.psm1/.psd1）被接受为文本

## 四、包大小限制

- 总包大小上限：**50MB**
- 嵌入文本含 SKILL.md + 最多约 **40 个非 .md 文件**

## 五、Slug 规则

- 默认从文件夹名称派生
- 必须小写且 URL 安全：匹配 `^[a-z0-9][a-z0-9-]*$`

## 六、安全审核

- ClawScan 检查代码行为与 frontmatter 声明是否一致
- 代码中引用的环境变量必须在 frontmatter 中声明
- 声明准确有助通过审核

## 七、许可证

- 所有 ClawHub 发布的 Skill 默认 **MIT-0** 许可
- 不支持自定义许可
- 不要在 SKILL.md 中添加冲突的许可条款

## 八、付费限制

- ClawHub 不支持付费 Skill
- 不要添加定价元数据
