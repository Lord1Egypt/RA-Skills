---
name: tia-portal-openness
description: "Automate TIA Portal via Openness API for PLC project engineering"
tags: [domain-specific, plc, cli, api-integration, file-based]
version: 1.0.0
---

## 功能简�?
通过 TIA Portal V21 Openness API（PowerShell + .NET），实现对博途项目的自动化操控�?
**支持两种主要场景�?*

| 场景 | 工作�?|
|------|--------|
| 新建工程 | �?`scl/` 文件 �?`create`（建项目+CPU）→ `import`（导入SCL+编译）→ 循环修改直到 BUILD OK |
| 已有工程 | `open`（打开项目）→ `export` �?AI 修改 `scl/` �?`import` �?循环直到 BUILD OK |

> ⚠️ **`create` 不自动导�?scl/**：TIA Portal 创建项目时会接管整个项目目录，之后再单独运行 `import` 导入 SCL 文件�?> 当用户提供一个已有项目路径并要求"检查编�?�?修改程序"�?新增功能�?时，直接进入 export→import 工作流�?
---

## 环境信息

| 项目 | �?|
|------|------|
| TIA Portal | V21 |
| API 类型 | Openness API (.NET, PowerShell 5.1) |
| **环境配置文件** | `references/env.json`（本 skill 目录内） |
| **脚本目录** | `scripts/tools/` |
| **项目工作目录** | `scripts/workspace/<ProjectName>/` |

> ⚠️ **路径绝不能硬编码**：所有路径从 `references/env.json` 读取�?
---

## 加载方式（每次使用前确认一次）

定位 `run_script.ps1` 并用它执行操作：

```powershell
# 以管理员身份运行 PowerShell
$runScript = "D:\Users\liran46\.agents\skills\tia-portal-openness\scripts\tools\run_script.ps1"

# 探测/刷新环境
powershell -ExecutionPolicy Bypass -File $runScript -Action env
```

执行后确�?`references/env.json` �?`tia_exe` �?`api_path` 正确�?
详细说明�?`references/prompts/ENV_SETUP.md`�?
---

## env.json 控制字段

| 字段 | 说明 |
|------|------|
| `tia_exe` | TIA Portal EXE 路径 |
| `api_path` | Openness API DLL 目录 |
| `skill_dir` | �?skill 根目�?|
| `active_project` | 当前活跃项目�?|
| `workspace_dir` | 当前活跃项目工作目录（scl/ 在此下） |

---

## 动词速查

| Action | 说明 | 脚本 |
|--------|------|------|
| `env` | 自动探测 TIA 安装路径，更�?env.json | `env_setup.ps1` |
| `create` | 新建项目 + 添加 CPU + 编译验证 + 保存 | `create_project.ps1` |
| `open` | 打开已有 .ap21 项目，更�?env.json | `open_project.ps1` |
| `export` | 导出所有块 �?`workspace_dir/scl/` | `export_blocks.ps1` |
| `import` | 自动修补 BOM �?导入 `scl/` �?编译 �?保存 | `import_scl.ps1` |
| `compile` | 仅编译，输出错误/警告（含路径/详情�?| `compile_check.ps1` |

---

## SCL 文件关键规则

1. **编码**：UTF-8 with BOM（`[System.Text.Encoding]::UTF8`�?2. **注释**：只�?`(* *)`�?*禁用 `//`**（会导致解析失败�?3. **文件�?= 块名**（去掉扩展名�?4. **定时�?*：使�?`TON`（不�?`TON_TIME`），每个实例独立声明，只调用一�?5. **块头属�?*：`TITLE`、`AUTHOR`、`FAMILY`、`NAME`、`VERSION` 等旧式元数据 **TIA V21 不支�?*，会导致语法错误，不要写
6. **数据类型**：写 `TIME`（全大写），不写 `Time`
7. **`VAR CONSTANT`**：TIA SCL 不支持，常量直接写字面量或用 `VAR_INPUT` 传入

---

## 前置条件（必读）

1. TIA Portal V21 已安装（�?Openness 组件�?2. **以管理员身份运行 PowerShell**
3. **当前用户已加�?`Siemens TIA Openness` �?*（一次性操作）�?   ```powershell
   net localgroup "Siemens TIA Openness" <用户�? /add
   # 之后注销重新登录
   ```
4. 同一时间只能有一个脚本实例连�?Openness API
