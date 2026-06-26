---
name: visual-bug-hunter
description: 视觉 Bug 定位与修复 Skill。当用户描述 GUI App 或 Web App 存在视觉 Bug（按钮点不了、元素重叠、布局错位、样式异常），或 AI 反复修 Bug 但无法自检验证效果，或需要对应用进行 UI 自动化测试时触发。通过截图感知 + UI 交互测试 + 控制台捕获 + 代码精准定位的闭环流程，让 AI 像人一样"眼睛看 + 手点击"来发现和修复 Bug，并以省 token 的最小 Diff 方式生成代码修复方案。不适用于纯后端逻辑 Bug、数据库问题或无 UI 界面的 API 报错。
install_type: skill
env_vars: []
no_external_credentials: true
scope: project_directory_only
---

# Visual Bug Hunter Skill

## 一句话定位

让 AI 像人一样「眼睛看 + 手点击」来测试 GUI/Web App，精准定位 Bug 并映射到代码行，同时以省 token 的方式生成和自检代码。

---

## 安全与权限声明

**安装方式**：本 Skill 是纯 AI 指令集，通过 ClawHub 平台一键安装，无需 pip install、npm install 或任何本地依赖包。README 中提及的 Python 脚本仅为可选的独立 CLI 工具，与本 Skill 的 AI 工作流完全独立。

**无需外部凭证**：截图分析（视觉感知）使用 AI 平台内置的多模态理解能力（understand_media），该能力由 AI 平台自身提供，不调用任何外部 Vision API，不需要 API Key、Token 或环境变量。

**文件访问范围**：本 Skill 仅读取用户明确指定的项目目录下的源代码文件（.py、.ts、.tsx、.js、.jsx、.vue、.css 等）。不访问以下敏感路径：~/.ssh、~/.env、~/.bashrc、~/.zshrc、/etc、系统日志、浏览器 Cookie、密钥文件或任何项目目录之外的文件。

**截图用途**：截图仅用于识别当前 App 的 UI 异常，截图数据在本地 AI 会话内处理，不上传至外部服务器。

---

## 触发条件

当用户满足以下任意一项时触发本 Skill：

- 描述 GUI App / Web App 存在视觉 Bug（布局错位、按钮点不了、元素重叠、样式异常）
- 要求对已有应用进行自动化 UI 测试或自检
- 要求 AI 帮助修 Bug 但反复改不好（AI 只能读代码、无法看到界面效果）
- 要求生成代码时防止臃肿、节省 token

**不触发场景**：纯后端逻辑 Bug、数据库问题、API 报错（无 UI 界面）

---

## 核心能力矩阵

| 能力 | 说明 | 技术实现 |
|------|------|---------|
| 视觉感知 | 截图 App 界面，AI 多模态能力识别 UI 异常 | macOS screencapture / pyautogui + AI 内置 Vision |
| UI 交互测试 | 自动点击按钮/输入框，捕获响应 | pyautogui / AppleScript / accessibility API |
| 控制台捕获 | 捕获 App 运行时的 stderr/stdout/崩溃日志（仅限用户指定项目） | subprocess + log tail |
| 代码精准定位 | 将视觉问题映射到具体文件+行号（仅限项目目录） | grep_search + AST 分析 |
| 防臃肿生成 | 写代码时遵循最小改动原则，禁止无关重构 | Diff-only 策略 + token 预算控制 |
| 视觉自检 | 修改后自动截图对比，确认 Bug 是否消失 | 截图前后对比 + AI Vision 二次验证 |

---

## 工作流（标准 Bug 修复流程）

```
Step 1: 接收问题描述 + 用户截图（可选）
Step 2: 启动目标 App，截图当前界面
Step 3: AI Vision 分析截图，生成「视觉 Bug 清单」（位置 + 类型 + 严重度）
Step 4: 对每个 Bug 执行 UI 交互测试（点击、输入、滚动）
Step 5: 捕获运行时日志（仅限目标 App 的 stderr/崩溃信息）
Step 6: 将视觉问题映射到代码（文件路径 + 行号 + 问题代码片段，仅限项目目录）
Step 7: 输出「精准 Bug 报告」（问题描述 + 截图证据 + 代码位置）
Step 8: 按「最小 Diff 原则」修复代码（只改有问题的行，不重构无关代码）
Step 9: 重新截图，AI Vision 自检验证修复是否生效
Step 10: 输出验证报告（修复前后截图对比 + 结论）
```

---

## 省 Token 策略

### 代码生成原则

1. **Diff-only 输出**：只输出需要修改的代码块，不输出整个文件
2. **上下文窗口控制**：每次只加载与 Bug 相关的文件，不全量读取项目
3. **问题优先队列**：先修最高优先级 Bug，逐个验证，不批量盲改
4. **禁止预防性重构**：修 Bug 时严禁顺手重构无关代码（这是 AI 代码臃肿的主因）

### 自检原则

1. **视觉验证优先**：修完必须截图，用 AI Vision 确认，不只靠代码逻辑推理
2. **单一变量原则**：每次只改一处，截图确认后再改下一处
3. **回归检测**：修复后检查周边元素是否受影响

---

## 技术栈

- **截图**：mcp_runtime system_capabilities screen.capture（macOS 原生，无需外部服务）
- **UI 自动化**：pyautogui（跨平台）/ AppKit + accessibility（macOS 精准）
- **Vision 分析**：AI 平台内置多模态能力（understand_media），无需外部 API 凭证
- **代码定位**：grep_search + ast 模块（仅限用户指定项目目录）
- **日志捕获**：subprocess.Popen + stderr 重定向（仅限目标 App 进程）
- **Diff 生成**：difflib + unified_diff

---

## 输出格式

### Bug 报告（JSON）

```json
{
  "bug_id": "BUG-001",
  "visual_description": "搜索输入框点击无响应",
  "location_on_screen": {"x": 120, "y": 45, "w": 200, "h": 30},
  "code_location": {
    "file": "src/ui/sidebar.py",
    "line": 87,
    "snippet": "self.search_input.setEnabled(False)"
  },
  "root_cause": "setEnabled(False) 导致输入框被禁用",
  "fix": "将 False 改为 True，或移除该行",
  "severity": "HIGH",
  "screenshot_evidence": "screenshots/bug_001_before.png"
}
```

### 修复验证报告

```
[OK]  BUG-001 搜索输入框 - 已修复（截图对比确认）
[FAIL] BUG-002 重复Tab - 未修复（截图仍显示两个气泡）
```

---

## 能力边界说明

本 Skill 专注于 UI 表现层问题，包括：元素重叠、布局错位、按钮禁用/点击无响应、样式异常、重复渲染等。

以下问题超出本 Skill 范围：后端 API 逻辑错误、数据库查询问题、网络请求失败、性能优化、内存泄漏。

---

## 与同类工具的差异

| 工具 | 支持桌面 GUI | 需要写测试脚本 | 面向人群 |
|------|------------|-------------|--------|
| Visual Bug Hunter | 是 | 否 | Vibe Coding 用户 |
| browser-use | 否（仅 Web） | 否 | Web 自动化 |
| Playwright | 否（仅 Web） | 是 | 专业测试工程师 |
| Applitools | 否（仅 Web） | 是 | 专业 QA 团队 |
