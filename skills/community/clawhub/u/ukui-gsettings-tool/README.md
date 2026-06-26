# GSettings Tool Skill (UKUI)

本目录是一个可发布到 ClawHub / OpenClaw 的 gsettings skill 示例，主要功能是：

- 导出指定 gsettings schema 的所有 key/value 为 JSON
- 一键导出常见 UKUI 相关 schema 的配置
- 从 `presets/*.json` 批量应用一整套配置
- 精细到单个 schema/key 的读取与设置（`get` / `set`）

## 目录结构

```text
gsettings-skill/
  ├─ gsettings_tool.py        # 主脚本
  ├─ SKILL.md                 # 对 IDE / ClawHub 友好的 skill 描述
  ├─ README.md                # 本文件
  └─ presets/                 # 预设 JSON
       └─ example.json
```

## 快速开始

### 导出 UKUI 配置

```bash
python3 /tmp/gsettings-skill/gsettings_tool.py export-ukui \
  -o /tmp/gsettings-skill/presets/ukui-current.json
```

### 应用预设

```bash
python3 /tmp/gsettings-skill/gsettings_tool.py apply ukui-current
```

默认会从 `/tmp/gsettings-skill/presets/ukui-current.json` 读取。

### 单项读取 / 设置

```bash
python3 /tmp/gsettings-skill/gsettings_tool.py get \
  org.ukui.power-manager brightness-ac

python3 /tmp/gsettings-skill/gsettings_tool.py set \
  org.ukui.power-manager brightness-ac 80
```

## 预设文件

`presets/` 目录下可以放多份不同的 JSON 预设，例如：

- `ukui-current.json`：你当前机器导出的 UKUI 配置（可不提交）
- `ukui-yhkylin-default.json`：你整理好、愿意公开分享的一套 UKUI 默认配置

JSON 结构示例：

```json
{
  "org.ukui.power-manager": {
    "brightness-ac": "80"
  }
}
```

值统一按照 `gsettings get` 输出的原始字符串格式保存，布尔为 `true/false`，字符串需包含单引号，如 `"'Adwaita-dark'"`。

