# 腾讯地图小程序开发技能

[English Documentation](README.md)

本仓库专门存放**腾讯地图小程序** 相关的 AI 助手 Skills，供 [Claude](https://claude.ai)、[Cursor](https://cursor.com)、[CodeBuddy](https://codebuddy.ai) 等在使用腾讯地图相关 API 时加载，以提供准确的 API 说明与示例。

## 包含的 Skill

| Skill | 说明 |
|-------|------|
| **tencentmap-miniprogram-skill** | 腾讯地图微信小程序：小程序地图开发的完整指导，包括地图组件使用、位置服务、标记点管理、路线规划、地理编码、POI搜索、点聚合和可视化图层等功能。适用于微信小程序地图开发，涵盖内置地图组件和腾讯位置服务 SDK。 |

## 如何使用

### 1. 克隆本仓库

```bash
git clone https://github.com/TencentLBS/tencentmap-miniprogram-skill.git
cd tencentmap-miniprogram-skill
```

### 2. 将 Skill 注册到你的 AI 助手

把 `tencentmap-miniprogram-skill` 目录链接或复制到当前环境对应的 skills 目录，这样 AI 在对话时会自动读取这些文档。

**Claude Desktop（本地）**

- Skills 目录一般为：`~/.claude/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)/tencentmap-miniprogram-skill" ~/.claude/skills/tencentmap-miniprogram-skill
  ```
- 或直接把 `tencentmap-miniprogram-skill` 文件夹复制到 `~/.claude/skills/` 下。

**Cursor**

- Skills 目录一般为：`~/.cursor/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)/tencentmap-miniprogram-skill" ~/.cursor/skills/tencentmap-miniprogram-skill
  ```
- 或直接把 `tencentmap-miniprogram-skill` 文件夹复制到 `~/.cursor/skills/` 下。

**CodeBuddy**

- Skills 目录一般为：`~/.codebuddy/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)/tencentmap-miniprogram-skill" ~/.codebuddy/skills/tencentmap-miniprogram-skill
  ```
- 或直接把 `tencentmap-miniprogram-skill` 文件夹复制到 `~/.codebuddy/skills/` 下。

### 3. 在对话中使用

在支持 Skills 的客户端里，当你的问题涉及「腾讯地图」、「微信小程序」、「小程序地图」、「TMap」等时，助手会优先参考本仓库中对应 skill 的文档来回答，从而给出更贴合腾讯地图小程序 API 的代码与用法。

## 仓库结构

```
.
├── tencentmap-miniprogram-skill/          # 腾讯地图小程序开发技能
│   ├── SKILL.md               # Skill 入口与索引
│   ├── quick_start_and_best_practices.md  # 快速开始指南与最佳实践
│   ├── assets/                # 示例项目和 SDK 库
│   │   ├── examples/          # 完整的小程序示例项目
│   │   └── libs/              # 腾讯位置服务 SDK
│   └── references/            # API 参考文档
│       ├── map_component_guide.md          # 地图组件文档
│       ├── mapContext_api/     # MapContext API 文档（32个API）
│       ├── wx_location_api/    # 微信位置 API 文档（12个API）
│       └── lbs_service_guide/  # 腾讯位置服务文档（9个API）
└── README.md
```

`SKILL.md` 中会列出其下所有参考文档，便于 AI 按需读取。

