# 测试报告模板（Report Template）

测试结束后，按以下 Markdown 结构生成报告。占位符用 `<...>` 表示，实际值在执行后填充。

## 语言 / Language

- 报告语言跟随用户输入语言：用户用中文 → 中文报告；用户用英文 → 英文报告。
- 下方先给中文模板（默认），再给英文模板（English Template）。按用户语言选用其一，字段结构一致。

```markdown
# 网页回归测试报告

## 概览
- **目标网址**：<url>
- **测试范围**：<登录 / 下单 / ...>
- **执行时间**：<YYYY-MM-DD HH:mm>
- **耗时**：<Xs>
- **用例总数**：<N>
- **通过**：<P> ｜ **部分通过**：<Q> ｜ **失败**：<F>
- **通过率**：<(P+Q*0.5)/N * 100%>（部分通过按 0.5 计）

## 步骤明细

### 步骤 1：<动作描述，如"打开登录页">
- **操作**：打开 <url>
- **预期**：登录表单可见
- **实际**：登录表单可见
- **断言**：元素[登录按钮]存在 ✅
- **截图**：<screenshot_1.png>

### 步骤 2：<动作描述>
- **操作**：输入邮箱、密码，点击登录
- **预期**：跳转首页
- **实际**：跳转 /home
- **断言**：URL 包含 /home ✅
- **截图**：<screenshot_2.png>

### 步骤 N：<失败示例>
- **操作**：点击"提交订单"
- **预期**：显示订单号
- **实际**：停留原页，提示"库存不足"
- **断言**：文本包含"订单号" ❌
- **截图**：<screenshot_n.png>
- **现场**：URL=<...> ｜ 控制台=<...>

### 步骤 M：<部分通过示例>
- **操作**：登录后断言跳转"订单管理"
- **预期**：登录直接落在订单管理页
- **实际**：登录落在后台首页 /console，经侧边栏导航到达 /orders
- **断言**：订单管理页可达 ✅｜ 但直接跳转未达成 ⚠️（部分通过）
- **说明**：属实现差异（默认落地页非订单管理），非功能缺陷；建议产品侧确认是否调整默认页。

## 缺陷清单
| # | 步骤 | 现象 | 复现线索 | 严重度 |
|---|------|------|----------|--------|
| 1 | 步骤 N | 提交订单未生成订单号 | 库存不足提示；截图 screenshot_n.png | 高 |

## 结论与建议
- 整体结论：<通过率> 通过，<关键路径是否可用>。
- 建议：
  1. <针对缺陷的修复建议>
  2. <建议人工复核的关键路径>
- 说明：本报告为自动化测试结论，建议人工复核关键业务路径。
```

## English Template

当用户用英文提出需求时，按以下英文结构生成报告（字段与中文模板一一对应）。

```markdown
# Web Regression Test Report

## Overview
- **Target URL**: <url>
- **Scope**: <login / checkout / ...>
- **Executed**: <YYYY-MM-DD HH:mm>
- **Duration**: <Xs>
- **Total cases**: <N>
- **Pass**: <P> ｜ **Partial**: <Q> ｜ **Fail**: <F>
- **Pass rate**: <(P+Q*0.5)/N * 100%> (partial counts as 0.5)

## Step Details

### Step 1: <action, e.g. "Open login page">
- **Action**: open <url>
- **Expected**: login form visible
- **Actual**: login form visible
- **Assertion**: element[login button] exists ✅
- **Screenshot**: <screenshot_1.png>

### Step 2: <action>
- **Action**: enter email, password, click login
- **Expected**: redirect to home
- **Actual**: redirected to /home
- **Assertion**: URL contains /home ✅
- **Screenshot**: <screenshot_2.png>

### Step N: <failure example>
- **Action**: click "Submit order"
- **Expected**: order number shown
- **Actual**: stayed on page, message "Out of stock"
- **Assertion**: text contains "order number" ❌
- **Screenshot**: <screenshot_n.png>
- **Context**: URL=<...> ｜ console=<...>

### Step M: <partial example>
- **Action**: after login assert redirect to "Orders"
- **Expected**: land directly on Orders page after login
- **Actual**: landed on dashboard /console, reached /orders via sidebar
- **Assertion**: Orders page reachable ✅｜ direct redirect not achieved ⚠️ (partial)
- **Note**: implementation difference (default landing is not Orders), not a defect; suggest product team confirm default page.

## Defect List
| # | Step | Symptom | Repro clue | Severity |
|---|------|---------|------------|----------|
| 1 | Step N | order number not generated | "out of stock" message; screenshot screenshot_n.png | High |

## Conclusion & Suggestions
- Overall: <pass rate> passed, <key flows usable?>.
- Suggestions:
  1. <fix suggestion for defects>
  2. <key paths recommended for manual review>
- Note: This is an automated test conclusion; manual review of critical paths is recommended.
```

## 报告存放与发布打包

- 生成的报告是**每次测试的产物**，建议存到技能目录下的 `run-reports/`（如 `run-reports/<站点>-<日期>-live.md`），仅作本地复盘与回归留证，**不要写入任何用户账号密码**。
- **发布打包时排除 `run-reports/`**：官方 `package_skill.py` 用 `rglob('*')` 无排除选项，会把测试报告一起打进 zip。请用一次性脚本（按相对路径跳过 `run-reports/`）重新打包，产物只含 `SKILL.md` + `PUBLISH.md` + `references/`。这能避免把私有测试记录、截图随技能包外泄，也减小体积。
- 截图同样视为报告产物：若截图放在 `run-reports/`，会随上条规则一并被排除。

## 报告撰写要求

- 状态分三档（中文／English）：✅ 通过 PASS ／ ⚠️ 部分通过 PARTIAL（目标可达但路径/落地与预期不符，属实现差异）／ ❌ 失败 FAIL。部分通过在概览单独计数。
- 客观描述"预期 vs 实际"，不替开发下定论。
- 失败项必须带现场信息（URL / 控制台 / 截图），便于复现。
- 严重度按"阻断主流程 / 影响功能 / 体验瑕疵"三档标注。
- 末尾固定标注"自动化测试结论，建议人工复核关键路径"。
