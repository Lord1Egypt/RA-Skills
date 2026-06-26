# Seedream5

OpenClaw 技能：使用火山引擎豆包 Seedream 5.0 生成或编辑图片。

## 安装

### 方式一：ClawHub 官方商店（推荐）

```bash
clawhub install seedream5
```

**命令行配置 API Key**（安装后执行）：

```bash
openclaw config set skills.entries.seedream5.apiKey "你的火山引擎API_KEY"
```


### 方式二：手动安装

仓库结构为 `openclaw-seedream5/seedream5/`（技能内容在 `seedream5` 子目录内）。

1. 从 [GitHub](https://github.com/zealman2025/openclaw-seedream5) 下载或克隆本仓库
2. 将 `seedream5` 文件夹复制到 OpenClaw 的 `workspace/skills/` 目录内

   ```bash
   git clone https://github.com/zealman2025/openclaw-seedream5.git
   cp -r openclaw-seedream5/seedream5 /path/to/workspace/skills/
   ```

   最终路径：`workspace/skills/seedream5/`（含 SKILL.md、scripts/、README.md）

   若放置在其他路径，可在 `openclaw.json` 的 `skills.load.extraDirs` 中指向该目录的父级。

## 配置 API Key

本技能需要火山引擎 API Key。任选以下一种方式：

### 方式一：环境变量

```bash
export VOLC_API_KEY="你的API_KEY"
# 或
export ARK_API_KEY="你的API_KEY"
```

### 方式二：openclaw.json（推荐）

编辑 `~/.openclaw/openclaw.json`，在 `skills.entries` 下添加：

```json
{
  "skills": {
    "entries": {
      "seedream5": {
        "apiKey": "你的火山引擎API_KEY"
      }
    }
  }
}
```

### 方式三：ClawPanel / Control UI

在 Skills 页面找到 seedream5，在凭证字段中填写 API Key。

### 获取 API Key

前往 [火山引擎控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 获取。

## 依赖

- [uv](https://docs.astral.sh/uv/)（Python 包管理）
- 脚本会自动安装 `requests`、`pillow`

## 使用示例

详见 [SKILL.md](./SKILL.md)。
