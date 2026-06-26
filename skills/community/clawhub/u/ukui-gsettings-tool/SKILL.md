---
name: ukui-gsettings-tool
description: A skill for exporting, inspecting and applying UKUI desktop gsettings presets, with fine-grained get/set support.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["gsettings", "python3"] }
      }
  }
---

# GSettings Tool Skill (UKUI)

## 简介

**GSettings Tool Skill** 提供导出与批量应用 gsettings 配置的能力，并针对 UKUI 桌面做了预设支持。

核心能力：

- 导出指定 schema 的所有 key/value 为 JSON
- 一键导出常见 UKUI 相关 schema（键盘、鼠标、电源、字体、SettingsDaemon 插件等）
- 从预设 JSON（presets）批量写入 gsettings，快速应用一套配置
- 精细到单个 schema/key 的读取与设置（适合 brightness-ac 这类单项调节）

## 目录结构

```text
gsettings-skill/
  ├─ gsettings_tool.py        # 主脚本：export / export-ukui / apply / get / set
  ├─ SKILL.md                 # 本文件：skill 描述
  ├─ README.md                # 详细说明（可选）
  └─ presets/                 # 预设 JSON 存放目录
       └─ example.json
```

## 使用方式

> 下列命令假设你在仓库根目录，且本 skill 位于 `gsettings-skill/` 中；如果你把目录放在别处，请相应调整路径。

### 1. 导出指定 schema 的配置

导出一个或多个 schema 的全部 key/value：

```bash
python3 gsettings_tool.py export \
  --schema org.gnome.desktop.interface \
  --schema org.gnome.desktop.wm.preferences \
  -o presets/my-current-setup.json
```

- `--schema`：可重复多次，导出多个 schema
- `-o`：输出文件路径，不指定则打印到 stdout

### 2. 一键导出 UKUI 相关配置

本 skill 预置了一组 UKUI 相关的 gsettings schema，包括但不限于：

- org.ukui.peripherals-keyboard
- org.ukui.peripherals-mouse
- org.ukui.peripherals-touchpad
- org.ukui.peripherals-touchscreen
- org.ukui.font-rendering
- org.ukui.SettingsDaemon.plugins.media-keys
- org.ukui.SettingsDaemon.plugins.power
- org.ukui.SettingsDaemon.plugins.sound
- org.ukui.SettingsDaemon.plugins.color
- org.ukui.SettingsDaemon.plugins.keyboard
- org.ukui.SettingsDaemon.plugins.xrandr

导出当前机器的 UKUI 配置：

```bash
python3 gsettings_tool.py export-ukui \
  -o presets/ukui-current.json
```

### 3. 应用预设（整套配置）

从 `presets/<name>.json` 读取并批量写入：

```bash
python3 gsettings_tool.py apply ukui-current
# 等价于读取 presets/ukui-current.json
```

或者直接指定 preset 文件路径：

```bash
python3 gsettings_tool.py apply interface \
  --path presets/interface.json
```

### 4. 单项读取 / 设置（例如 UKUI 亮度键）

读取单个键：

```bash
python3 gsettings_tool.py get \
  org.ukui.power-manager brightness-ac
```

设置单个键（例如接电时亮度为 80）：

```bash
python3 gsettings_tool.py set \
  org.ukui.power-manager brightness-ac 80
```

对于字符串类型的键，需要使用 gsettings 语法包一层单引号：

```bash
python3 gsettings_tool.py set \
  org.ukui.power-manager some-string-key "'my-value'"
```

## 适用场景

- 在多台机器之间同步 UKUI / GNOME 等环境的 gsettings 配置
- 为 OpenClaw / CoderClaw 等代理提供：
  - “读取当前 UKUI 设置”的能力（export-ukui）
  - “应用一套 UKUI 预设”的能力（apply）
  - “精细修改某个具体配置项”的能力（get/set）

## 权限说明

本 skill 需要：

- 在本机执行 `gsettings` 命令
- 读写当前用户的 gsettings/dconf 配置（通过 `gsettings` 间接完成）
- 读写 skill 目录下的 `presets/*.json` 文件

不会：

- 主动访问网络
- 直接读写除 gsettings/dconf 之外的系统配置文件，除非你在 preset 中定义了指向这些路径的键值

## 预设 JSON 结构说明

preset JSON 顶层结构为：

```json
{
  "schema.name": {
    "key-name": "gsettings 原始值字符串"
  }
}
```

例如：

```json
{
  "org.ukui.power-manager": {
    "brightness-ac": "80"
  }
}
```

建议：

- 只将“通用配置”（主题、键盘布局、常用快捷键等）写入公开的 preset
- 避免把包含用户名、绝对路径等隐私信息的键值提交到公共仓库或发布到 ClawHub

