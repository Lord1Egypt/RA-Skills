---
name: stardew-modding
description: 星露谷物语 Mod 制作助手。用于创建 Content Patcher (CP) Mod 或 SMAPI Mod，包括：创建项目结构、编写 JSON、添加 NPC/事件/对话、验证格式、编译 SMAPI Mod。当用户说"做星露谷 mod"、"创建 Stardew Valley Mod"、"星露谷 Mod 制作"时触发。
---

# Stardew Valley Mod 制作助手

## ⚠️ 工具依赖

使用本技能前，请确保有以下工具：

| 工具 | 用途 | 检查命令 |
|------|------|----------|
| **文本编辑器** | 编辑文件 | 已有 |
| **Python** | 验证 JSON | `python3 --version` |
| **.NET SDK** | 编译 SMAPI Mod | `dotnet --version` |

### 检查工具可用性

```python
import subprocess
import shutil

def check_tools():
    errors = []
    
    # 检查 Python
    if not shutil.which('python3'):
        errors.append("❌ Python 未安装")
    
    # 检查 .NET (可选，用于 SMAPI Mod)
    if not shutil.which('dotnet'):
        errors.append("⚠️ .NET SDK 未安装（SMAPI Mod 需要，CP Mod 不需要）")
    
    if errors:
        return errors
    return ["✅ 所有工具就绪"]
```

---

## 🔧 自动判断 Mod 类型

根据用户需求自动选择：

| 需求 | 类型 | 需要 .NET |
|------|------|----------|
| 添加 NPC/对话/立绘 | **CP Mod** | ❌ 不需要 |
| 修改游戏数据 | **CP Mod** | ❌ 不需要 |
| 添加新地图 | **CP Mod** | ❌ 不需要 |
| 修改游戏机制 | **SMAPI Mod** | ✅ 需要 |
| 添加孩子功能 | **SMAPI Mod** | ✅ 需要 |
| 代码级 Hook | **SMAPI Mod** | ✅ 需要 |

### 自动判断逻辑

```python
def determine_mod_type(user_request):
    request = user_request.lower()
    
    smapi_keywords = ["孩子", "孩子功能", "hook", "修改机制", "代码", "dll", "编译"]
    cp_keywords = ["对话", "立绘", "npc", "剧情", "事件", "地图", "json"]
    
    for keyword in smapi_keywords:
        if keyword in request:
            return "SMAPI"
    
    for keyword in cp_keywords:
        if keyword in request:
            return "CP"
    
    return "CP"  # 默认 CP
```

---

## 快速开始

### Content Patcher Mod

1. 创建项目文件夹结构
2. 编写 manifest.json
3. 编写 content.json
4. 添加资源文件（对话、立绘、地图等）

### SMAPI Mod (C#)

1. 创建 C# 项目
2. 引用 SMAPI DLL
3. 编写 Mod 代码
4. 编译 DLL

## 项目结构

### CP Mod 标准结构

```
ModName/
├── manifest.json           # Mod 信息
├── content.json          # 内容定义
└── assets/              # 资源文件夹
    ├── Dialogue/        # 对话文件
    ├── Image/           # 图片资源
    ├── Maps/            # 地图文件
    ├── Schedule/        # 行程文件
    └── i18n/           # 多语言
```

### SMAPI Mod 标准结构

```
ModName/
├── ModName.csproj       # 项目文件
├── ModEntry.cs          # 主代码
└── manifest.json        # Mod 信息
```

## 常用代码片段

### manifest.json 模板

```json
{
  "Name": "ModName",
  "Author": "YourName",
  "Version": "1.0.0",
  "Description": "Mod 描述",
  "UniqueID": "YourName.ModName",
  "ContentPackFor": {
    "UniqueID": "Pathoschild.ContentPatcher",
    "MinimumVersion": "2.0"
  }
}
```

### content.json 基础结构

```json
{
  "Format": "2.3.0",
  "Changes": [
    {
      "LogName": "说明",
      "Action": "EditData/Load/EditImage",
      "Target": "目标路径",
      "Entries": {}
    }
  ]
}
```

### 婚后对话格式

```json
{
  "Action": "EditData",
  "Target": "Characters/Dialogue/MarriageDialogueNPC名",
  "Entries": {
    "Rainy_Day_0": "对话内容",
    "Indoor_Night_0": "对话内容"
  }
}
```

### Event 触发条件

| 条件 | 代码 |
|------|------|
| 结婚 | `Spouse NPC名` |
| 好感度 | `Friendship NPC名 数字` (2500 = 10心) |
| 时间 | `Time 600 1000` |
| 天气 | `Weather rainy` |
| 季节 | `Season summer` |
| 雨天 | `Weather rainy` |
| 晴天 | `Weather sunny` |

## 工具

### 验证 JSON

```bash
python3 -c "import json; json.load(open('file.json'))"
```

### 编译 SMAPI Mod

```bash
dotnet build
```

## 资源路径

- 游戏目录：`~/Library/Application Support/Steam/steamapps/common/Stardew Valley/`
- Mods：`.../Stardew Valley/Contents/MacOS/Mods/`
- SMAPI DLL：`.../Stardew Valley/Contents/MacOS/smapi-internal/`

## 参考

- Wiki: https://stardewvalleywiki.com/Modding:Index
- SMAPI: https://smapi.io/
- Content Patcher: https://smapi.io/mods/1915
