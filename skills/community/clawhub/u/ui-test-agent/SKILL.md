---
name: ui-test-agent
description: >
  This skill should be used when the user wants to perform UI automation testing on web pages.
  It enables a full "record-then-report" workflow: execute real browser operations via
  agent-browser CLI, capture screenshots at every step, record each action into a session file,
  and finally generate a replayable test script plus a standalone HTML test report with embedded
  screenshot evidence. Trigger when the user mentions: UI自动化测试, 网页测试, 自动化测试,
  browser automation test, record and replay, 录制回放, test report, 测试报告, agent-browser测试.
---

# UI 自动化测试 Agent Skill

> **核心工作模式**：录制-生成（Record & Report）
> 先执行真实浏览器操作并逐步录制，最终生成可重放测试脚本 + 带截图证据的 HTML 报告。

---

## 角色定位

作为 **网页 UI 自动化测试 Agent**，职责是将用户的自然语言测试需求转化为：
1. 逐步执行的 agent-browser 操作序列
2. 可重放的 shell/JSON 测试脚本
3. 含截图证据的完整 HTML 测试报告

---

## 四步工作流程

### 第一步：分析用户意图

- 理解用户要测试的功能点
- 拆解为具体的浏览器操作步骤（导航、点击、输入、断言等）
- 确定被测 URL 和预期结果
- 初始化 session 文件路径（推荐：`{output_dir}/session.json`）

### 第二步：循环执行操作（每步三连击）

对每一个测试步骤，**严格按以下顺序**执行三个动作：

#### 动作 A：执行 agent-browser 命令

```bash
agent-browser <命令> <参数>
```

常用命令参考：

| 操作 | 命令示例 |
|------|---------|
| 打开页面 | `agent-browser navigate --url "https://example.com"` |
| 点击元素 | `agent-browser click --selector "#btn-login"` |
| 输入文本 | `agent-browser type --selector "#username" --value "admin"` |
| 选择下拉 | `agent-browser select --selector "#role" --value "admin"` |
| 断言文本 | `agent-browser assert-text --selector ".title" --expected "欢迎"` |
| 等待元素 | `agent-browser wait-for --selector ".loading" --state hidden` |
| 滚动页面 | `agent-browser scroll --direction down --amount 300` |

#### 动作 B：截图（必须用 `get_screenshot` 工具）

> ⚠️ **禁止** 用 `agent-browser screenshot` 命令截图。必须调用 `get_screenshot` 工具获取当前页面截图，将返回的截图路径保存备用。

#### 动作 C：录制步骤

调用脚本 `record_step.py` 将本步操作记录到 session 文件：

```bash
python "{SKILL_DIR}/scripts/record_step.py" \
  --session "{session_file}" \
  --step-num {N} \
  --description "步骤描述" \
  --command "执行的完整 agent-browser 命令" \
  --screenshot "{截图路径}" \
  --status "passed|failed|skipped" \
  --selector "目标元素选择器（如有）" \
  --input-value "输入值（如有）" \
  --url "当前页面 URL"
```

> 若 agent-browser 命令执行失败，`--status` 设为 `failed` 并填写 `--error-msg`；
> 失败后仍须继续录制，不要中断整体流程。

### 第三步：生成测试脚本

所有步骤录制完毕后，调用 `save_test_script.py`：

```bash
python "{SKILL_DIR}/scripts/save_test_script.py" \
  --session "{session_file}" \
  --output-dir "{output_dir}" \
  --test-name "测试用例名称" \
  --description "测试描述" \
  --format both
```

将生成：
- `{test_name}.sh`：Linux/macOS 可直接执行的 shell 脚本
- `{test_name}.bat`：Windows 可直接执行的批处理脚本
- `{test_name}.test.json`：结构化 JSON 测试用例

### 第四步：生成 HTML 测试报告

调用 `save_test_report.py` 生成完整报告：

```bash
python "{SKILL_DIR}/scripts/save_test_report.py" \
  --session "{session_file}" \
  --output "{output_dir}/test_report.html" \
  --test-name "测试用例名称" \
  --description "测试描述" \
  --tester "Auto Agent" \
  --base-url "https://example.com"
```

报告特性：
- 📸 截图内嵌为 Base64，单 HTML 文件无外部依赖
- 🎨 步骤颜色标注（绿=通过/红=失败/黄=跳过）
- 📊 汇总统计（总步骤、通过数、失败数、通过率）
- 🔍 命令详情可折叠展开

---

## 输出目录约定

推荐统一输出到：

```
{workspace}/ui-test-results/{test_name}_{timestamp}/
├── session.json          # 录制的原始 session
├── screenshots/          # 各步截图
├── {test_name}.sh        # Shell 回放脚本
├── {test_name}.bat       # Windows 回放脚本
├── {test_name}.test.json # JSON 用例文件
└── test_report.html      # HTML 测试报告
```

---

## 关键约束

1. **每步必须截图**：动作 B（`get_screenshot`）不可跳过，截图是报告的主要证据
2. **先录制后生成**：必须等所有步骤录制完毕，再执行第三步和第四步
3. **失败不中断**：单步失败时记录错误继续，最终在报告中标红，不要提前终止整体流程
4. **session 路径一致**：第二步中所有 `record_step.py` 调用必须使用同一个 session 文件路径
5. **SKILL_DIR 变量**：脚本路径应使用该 skill 目录的绝对路径（`~/.workbuddy/skills/ui-test-agent/`）

---

## 脚本路径速查

| 脚本 | 用途 |
|------|------|
| `scripts/record_step.py` | 录制单步操作到 session |
| `scripts/save_test_script.py` | 将 session 导出为可重放脚本 |
| `scripts/save_test_report.py` | 将 session 导出为 HTML 报告 |
