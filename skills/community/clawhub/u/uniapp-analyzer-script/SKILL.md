---
name: uniapp-analyzer-script
display_name: "uniapp项目分析器 (脚本版)"
author: include
description: "脚本版 (PowerShell) - 精确统计离线分析，依赖 skill-seekers"
description_zh: "智能分析 uni-app 和 Vue 项目，量化技术债务，发现代码隐患，自动生成项目分析报告。当用户需要分析 Vue 2/3、uni-app 项目结构、检查代码质量、评估技术债务、生成项目文档时使用。不适用于 React、Angular、Svelte、Python、Java、原生小程序或其他非 Vue 技术栈项目。"
description_en: "Intelligently analyze uni-app and Vue projects, quantify technical debt, detect code issues, auto-generate project analysis reports. Use when analyzing Vue 2/3 or uni-app project structure, checking code quality, evaluating technical debt, or generating project documentation. Do NOT use for React, Angular, Svelte, Python, Java, native mini-programs, or non-Vue projects."
version: 1.0.0
---

# uniapp-analyzer-script | uni-app/Vue 项目分析器 (脚本版)

> PowerShell 脚本驱动，精确统计分析，依赖 skill-seekers

专为 uni-app 和 Vue 项目打造的智能代码分析工具。5 分钟生成项目体检报告，量化技术债务，发现代码隐患，让项目架构一目了然。

## 核心能力

- 📊 **技术债务评分** - 0-100 分量化代码健康度，A-F 等级评定
- 🔍 **代码隐患扫描** - 自动发现大文件、低注释、旧语法、复杂函数
- 🏗️ **架构可视化** - 识别设计模式（Module/Observer/Factory/Strategy），梳理模块关系
- 📋 **项目元信息提取** - 解析 manifest/pages.json（uni-app）或 package.json/router（Vue）
- 📝 **生成体检报告** - 人类可读的 report.md + AI 可用的 SKILL.md

## 何时使用此 Skill

当用户需要以下帮助时触发此 skill：

- "分析这个项目"
- "分析 uni-app 项目"
- "分析 Vue 项目"
- "帮我理解这个项目的结构"
- "生成项目文档"
- "分析代码架构"
- "查看项目依赖关系"
- "检查代码质量"
- "评估技术债务"
- "项目体检"
- "代码审查"
- "重构建议"

## 核心功能

### 1. 智能项目检测
自动识别项目类型（uni-app / Vue），无需手动指定。

**检测依据：**
- **uni-app**: manifest.json、pages.json、uni.scss、appid 等特征
- **Vue**: vue.config.js、vite.config.js、package.json 中的 vue 依赖、.vue 文件等

### 2. 精准排除规则
基于项目类型自动应用最佳排除配置，避免分析非核心文件。

**排除内容：**
- 依赖目录：node_modules、uni_modules、vendor
- 构建产物：dist、build、unpackage、.output
- 测试文件：*.test.js、*.spec.js、test/、tests/
- 日志文件：*.log、logs/
- 锁文件：package-lock.json、yarn.lock
- 临时文件：*.tmp、.cache、temp/
- 配置文件：.env、tsconfig.json（保留核心代码）

### 3. 预览模式
分析前先预览将要处理的文件列表，确认无误后再执行。

### 4. 结构化输出
生成完整的分析报告：
- **SKILL.md**: 项目技能文档，包含架构概览和使用指南
- **code_analysis.json**: 详细的代码分析数据
- **code_quality.json**: 代码质量评分与技术债务分析
- **references/**: API 文档、依赖关系、配置模式等参考文档
- **report.md**: AI 解读报告（需 AI 生成）

### 代码质量分析

自动分析以下指标：

| 指标 | 说明 | 阈值 |
|------|------|------|
| **技术债务评分** | 综合评分 0-100 分 | ≥80 优秀，<60 需改进 |
| **文件大小检测** | 标记超大文件 | >500 行警告，>1000 行严重 |
| **函数长度检测** | 标记超长函数 | >100 行警告 |
| **注释覆盖率** | 注释行占比 | <5% 警告，<1% 严重 |
| **变量声明分析** | var/let/const 分布 | var >20% 建议改进 |
| **条件编译复杂度** | #ifdef 等指令统计 | 过多时建议重构 |
| **设计模式识别** | Module/Observer/Factory/Strategy | 识别项目架构风格 |

## 使用方法

### Windows (PowerShell)

```powershell
# 分析当前目录项目（自动检测类型）
.\analyze-project.ps1

# 分析指定路径项目
.\analyze-project.ps1 -ProjectPath "D:\my-uniapp-project"

# 指定项目类型（跳过自动检测）
.\analyze-project.ps1 -ProjectPath "D:\project" -ProjectType uniapp

# 先预览将要分析的文件
.\analyze-project.ps1 -ProjectPath "D:\project" -Preview

# 跳过确认提示
.\analyze-project.ps1 -ProjectPath "D:\project" -SkipConfirm

# 启用深度分析（解析 manifest.json、pages.json 等配置）
.\analyze-project.ps1 -ProjectPath "D:\project" -DeepAnalysis

# 查看帮助
.\analyze-project.ps1 -Help
```

### Linux/macOS (Bash)

```bash
# 分析当前目录项目（自动检测类型）
./analyze-project.sh

# 分析指定路径项目
./analyze-project.sh -p /path/to/my-uniapp-project

# 指定项目类型（跳过自动检测）
./analyze-project.sh -p /path/to/project -t uniapp

# 先预览将要分析的文件
./analyze-project.sh -p /path/to/project --preview

# 跳过确认提示
./analyze-project.sh -p /path/to/project -y

# 启用深度分析
./analyze-project.sh -p /path/to/project -d

# 查看帮助
./analyze-project.sh -h
```

## 工作流程

```
1. 项目检测 → 2. 配置加载 → 3. 预览确认 → 4. 执行分析 → 5. 生成报告
```

### 详细流程

1. **项目类型检测**
   - 扫描关键文件（manifest.json、package.json 等）
   - 根据特征匹配确定项目类型
   - 无法检测时默认使用 Vue 配置

2. **配置加载**
   - 加载基础排除配置（base.json）
   - 加载项目类型专属配置（uniapp.json / vue.json）
   - 合并自定义配置（如有）

3. **预览确认（可选）**
   - 显示将要分析的文件统计
   - 显示文件类型分布
   - 列出部分文件示例
   - 用户确认后继续

4. **执行分析**
   - 复制项目文件到临时目录（应用排除规则）
   - 调用 skill-seekers 进行深度分析
   - 生成 SKILL.md 和 code_analysis.json

5. **生成报告**
   - 输出目录结构
   - 显示生成的文件列表
   - 创建 report.md 占位符，等待 AI 解读

### AI 解读要求

分析完成后，AI 需要：
1. 读取 `SKILL.md` 和 `code_analysis.json`
2. 如果启用了深度分析，同时读取 `project_metadata.json`
3. 生成适合人类阅读的项目分析报告
4. 将报告内容写入 `report.md`

报告应包含：项目概览、核心模块分析、代码质量评估、架构特点、改进建议。

### 深度分析（-DeepAnalysis）

启用深度分析后，工具会额外解析项目配置文件：

**uni-app 项目：**
- **manifest.json**: 应用名称、AppID、版本、权限、原生插件、广告 SDK
- **pages.json**: 页面路由、TabBar 配置、全局样式

**Vue 项目：**
- **package.json**: 项目名、版本、依赖列表、Vue 版本
- **router/index.js**: 路由配置、页面列表
- **vite.config.js**: Vite 插件、构建配置
- **UI 框架检测**: Element UI/Plus、Ant Design Vue、Vuetify、Vant 等
- **状态管理检测**: Vuex、Pinia

这些信息会保存到 `project_metadata.json`，帮助 AI 生成更全面的报告。

## 配置文件

### 基础配置 (config/base.json)
通用排除规则，适用于所有项目类型：
- 排除目录：node_modules、.git、dist、build、logs 等
- 排除文件：*.log、package-lock.json、.env 等
- 文件大小限制：最大 1MB
- 文件类型白名单：代码文件和文档

### uni-app 配置 (config/uniapp.json)
uni-app 项目专属规则：
- 排除：uni_modules、unpackage、nativeplugins
- 排除：各平台组件目录（wxcomponents、mycomponents 等）
- 识别：pages/、components/、mixins/、utils/、api/

### Vue 配置 (config/vue.json)
Vue 项目专属规则：
- 排除：public/、assets/、tests/、cypress/、.nuxt/
- 排除：配置文件（vue.config.js、vite.config.ts 等）
- 识别：views/、components/、composables/、stores/、router/

## 最佳实践

### 1. 分析前预览
首次分析新项目时，建议先使用 `-Preview` 参数查看将要分析的文件，确保排除规则正确。

### 2. 自定义排除规则
如需添加自定义排除规则，可创建配置文件：

```json
{
  "exclude": {
    "directories": ["my-custom-dir"],
    "files": ["custom.log"],
    "patterns": ["**/temp/**"]
  }
}
```

然后使用 `-CustomConfig` 参数加载。

### 3. 处理大型项目
对于文件数量超过 1000 的大型项目：
- 考虑调整 `max_files` 配置
- 或分模块多次分析

### 4. 查看分析报告
分析完成后，重点查看以下文件：
- **SKILL.md**: 项目整体概览，适合快速了解项目
- **references/api_reference/**: API 文档，了解代码接口
- **references/dependencies/**: 依赖关系图
- **references/architecture/**: 架构分析

## 依赖要求

### 必需依赖
- **PowerShell 5.0+**
- **skill-seekers**: 核心分析引擎

### 安装 skill-seekers

如果系统未安装 skill-seekers，脚本会自动提示并尝试安装：

```powershell
# 手动安装
pip install skill-seekers

# 或使用特定 Python 版本
python -m pip install skill-seekers
py -3 -m pip install skill-seekers
```

### 自动安装
运行脚本时如果检测到 skill-seekers 未安装，会提示是否自动安装。选择 `y` 后脚本会尝试使用上述命令自动安装。

## 用户配置

### 配置文件位置
用户配置保存在：`~/.workbuddy/skills/uniapp-vue-analyzer/user-config.json`

### 自定义文件大小限制

默认文件大小限制为 1MB，可以通过以下方式自定义：

```powershell
# 临时调整（仅本次运行）
.\analyze-project.ps1 -ProjectPath "D:\project" -MaxFileSize 5

# 调整并保存为默认值
.\analyze-project.ps1 -ProjectPath "D:\project" -MaxFileSize 5 -SaveConfig

# 查看当前使用的限制
# 运行时会显示："Using user-defined file size limit: 5 MB"
```

### 手动编辑配置

直接编辑配置文件：

```json
{
  "max_file_size": 5242880,
  "max_file_size_mb": 5,
  "saved_at": "2026-04-11 17:00:00"
}
```

## 故障排除

### 问题：无法检测项目类型
**解决**: 手动指定 `-ProjectType` 参数

### 问题：排除了不该排除的文件
**解决**: 使用 `-Preview` 查看排除效果，调整配置文件

### 问题：分析的文件太多/太少
**解决**: 
- 检查配置文件中的 `max_file_size` 设置
- 检查 `include_extensions` 白名单
- 使用 `-Preview` 查看实际处理的文件

### 问题：skill-seekers 安装失败
**解决**: 
1. 确保已安装 Python 3.7+
2. 尝试手动安装: `pip install skill-seekers`
3. 检查 pip 是否可用: `pip --version`
4. 如果使用虚拟环境，确保已激活

## 技术细节

### 依赖工具
- **skill-seekers**: 核心分析引擎
- **PowerShell**: 脚本执行环境

### 项目结构
```
uniapp-vue-analyzer/
├── SKILL.md                      # 本文件
├── analyze-project.ps1           # 主分析脚本 (Windows)
├── analyze-project.sh            # 主分析脚本 (Linux/macOS)
├── _skillhub_meta.json           # SkillHub 元数据
├── config/
│   ├── base.json                # 基础排除配置
│   ├── uniapp.json              # uni-app 专属配置
│   └── vue.json                 # Vue 专属配置
├── scripts/
│   └── code-quality-analyzer.ps1  # 代码质量分析模块
├── references/
│   └── api_reference.md          # API 参考文档
└── assets/
    └── example_asset.txt         # 示例资源
```

### 输出结构
```
analysis-output/
└── {project-name}/
    ├── SKILL.md               # 项目技能文档（AI 使用）
    ├── code_analysis.json     # 代码分析数据
    ├── report.md              # AI 解读报告（人类阅读）
    ├── project_metadata.json  # 项目元数据（深度分析时生成）
    └── references/
        ├── api_reference/     # API 文档
        ├── dependencies/      # 依赖关系
        ├── architecture/      # 架构分析
        └── ...
```

---

**提示**: 此 skill 是分析项目的第一步，生成的 SKILL.md 可以被加载为技能，帮助 AI 更好地理解和使用项目代码。
