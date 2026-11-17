# 腾讯地图JSAPI GL开发技能

[English Documentation](README.md)

本仓库专门存放**腾讯地图 JSAPI** 相关的 AI 助手 Skills，供 [Claude](https://claude.ai)、[Cursor](https://cursor.com)、[CodeBuddy](https://codebuddy.ai) 等在使用腾讯地图相关 API 时加载，以提供准确的 API 说明与示例。

## 包含的 Skill

| Skill | 说明 |
|-------|------|
| **tencentmap-jsapi-gl-skill** | 腾讯地图 JSAPI GL 开发技能版：地图初始化、覆盖物（标注/折线/多边形）、事件、图层、控件、可视化、工具、检索、路线规划、查地址、行政区划、ip定位、几何计算、三维模型展示、性能优化等。适用于使用 WebGL 的 2D、3D 地图页面开发。 |

## 如何使用

### 1. 克隆本仓库

```bash
git clone https://github.com/TencentLBS/tencentmap-jsapi-gl-skill.git
cd tencentmap-jsapi-gl-skill
```

### 2. 将 Skill 注册到你的 AI 助手

把 `tencentmap-jsapi-gl-skill` 目录链接或复制到当前环境对应的 skills 目录，这样 AI 在对话时会自动读取这些文档。

**Claude Desktop（本地）**

- Skills 目录一般为：`~/.claude/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)/tencentmap-jsapi-gl-skill" ~/.claude/skills/tencentmap-jsapi-gl-skill
  ```
- 或直接把 `tencentmap-jsapi-gl-skill` 文件夹复制到 `~/.claude/skills/` 下。

**Cursor**

- Skills 目录一般为：`~/.cursor/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)/tencentmap-jsapi-gl-skill" ~/.cursor/skills/tencentmap-jsapi-gl-skill
  ```
- 或直接把 `tencentmap-jsapi-gl-skill` 文件夹复制到 `~/.cursor/skills/` 下。

**CodeBuddy**

- Skills 目录一般为：`~/.codebuddy/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)/tencentmap-jsapi-gl-skill" ~/.codebuddy/skills/tencentmap-jsapi-gl-skill
  ```
- 或直接把 `tencentmap-jsapi-gl-skill` 文件夹复制到 `~/.codebuddy/skills/` 下。

### 3. 在对话中使用

在支持 Skills 的客户端里，当你的问题涉及「腾讯地图」「TMap」「jsapi-gl」等时，助手会优先参考本仓库中对应 skill 的文档来回答，从而给出更贴合腾讯地图 JSAPI 的代码与用法。

## 仓库结构

```
.
├── tencentmap-jsapi-gl-skill/          # tencentmap-jsapi-gl-skill
│   ├── SKILL.md            # Skill 入口与索引
│   └── references/         # API 参考文档和示例
│       ├── jsapigl/        # JS API GL 文档和示例
│       └── visualization/  # 可视化 API 文档和示例
└── README.md
```

`SKILL.md` 中会列出其下所有参考文档，便于 AI 按需读取。
