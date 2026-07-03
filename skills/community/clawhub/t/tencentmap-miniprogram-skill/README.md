# tencentmap-miniprogram-skill

[中文文档](README_zh.md)

This repository provides AI assistant **Skills** for Tencent Map development in WeChat Mini Programs. Use them with [Claude](https://claude.ai), [Cursor](https://cursor.com), [CodeBuddy](https://codebuddy.ai), or other clients that support skills so the AI can reference accurate API docs and examples when you work with Tencent Map in WeChat Mini Programs.

## Included Skills

| Skill | Description |
|-------|-------------|
| **tencentmap-miniprogram-skill** | Tencent Map WeChat Mini Program: Complete guidance for mini program map development, including map component usage, location services, marker management, route planning, geocoding, POI search, marker clustering, and visualization layers. For WeChat Mini Program map development using the built-in map component and Tencent Location Service SDK. |

## How to Use

### 1. Clone the repo

```bash
git clone https://github.com/TencentLBS/tencentmap-miniprogram-skill.git
cd tencentmap-miniprogram-skill
```

### 2. Register the skill with your AI assistant

Link or copy the `tencentmap-miniprogram-skill` directory into your environment's skills folder so the AI can load its docs during conversations.

**Claude Desktop (local)**

- Skills directory is usually: `~/.claude/skills/`
- Register via symlink (recommended):
  ```bash
  ln -sfn "$(pwd)/tencentmap-miniprogram-skill" ~/.claude/skills/tencentmap-miniprogram-skill
  ```
- Or copy the `tencentmap-miniprogram-skill` folder into `~/.claude/skills/`.

**Cursor**

- Skills directory is usually: `~/.cursor/skills/`
- Register via symlink (recommended):
  ```bash
  ln -sfn "$(pwd)/tencentmap-miniprogram-skill" ~/.cursor/skills/tencentmap-miniprogram-skill
  ```
- Or copy the `tencentmap-miniprogram-skill` folder into `~/.cursor/skills/`.

**CodeBuddy**

- Skills directory is usually: `~/.codebuddy/skills/`
- Register via symlink (recommended):
  ```bash
  ln -sfn "$(pwd)/tencentmap-miniprogram-skill" ~/.codebuddy/skills/tencentmap-miniprogram-skill
  ```
- Or copy the `tencentmap-miniprogram-skill` folder into `~/.codebuddy/skills/`.

### 3. Use it in chat

When your questions mention "Tencent Map", "WeChat Mini Program", "mini program map", "TMap", or similar in the context of WeChat Mini Programs, the assistant will use this skill's docs to give answers and code that match the Tencent Map Mini Program APIs.

## Repo structure

```
.
├── tencentmap-miniprogram-skill/          # Tencent Map Mini Program skill
│   ├── SKILL.md               # Skill entry and index
│   ├── quick_start_and_best_practices.md  # Quick start guide and best practices
│   ├── assets/                # Example projects and SDK libraries
│   │   ├── examples/          # Complete mini program example projects
│   │   └── libs/              # Tencent Location Service SDK
│   └── references/            # API reference docs
│       ├── map_component_guide.md          # Map component documentation
│       ├── mapContext_api/     # MapContext API documentation (32 APIs)
│       ├── wx_location_api/    # WeChat location API documentation (12 APIs)
│       └── lbs_service_guide/  # Tencent Location Service documentation (9 APIs)
└── README.md
```

`SKILL.md` lists all reference files so the AI can load them as needed.
