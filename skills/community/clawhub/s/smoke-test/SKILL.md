---
name: webapp-qa-workflow
description: Multi-modal LLM-assisted iterative QA and fixing workflow for web applications. Covers comprehensive testing (all views, DOM assertions, API truth comparison, forbidden-string scanning), root cause analysis, code-level fixes, regression verification, and evidence-chain reporting. Trigger when the user asks to "test", "audit", "regression test", "fix bugs", "functional test", "quality assurance", "smoke test" a web application, or mentions "WebUI testing", "comprehensive testing", "测试", "回归", "修复验证", "功能测试", "冒烟测试".
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
disable: false
author: 大雪块
display_name: "冒烟测试"
display_name_en: "Smoke Test"
description_zh: "多模态大模型辅助的 Web 应用「测试—修复」迭代工作流：覆盖全面测试（全视图、DOM 断言、API 真值比对、禁止串扫描）、根因审核、代码级修复、回归验证与证据链报告。当用户要做测试、回归、修复验证、功能测试或冒烟测试时触发。"
description_en: "Multi-modal LLM-assisted iterative QA and fixing workflow for web applications: comprehensive testing, root-cause audit, code-level fixes, regression verification, and evidence-chain reporting."
visibility: "public"
agent_created: true
---

# 冒烟测试（Smoke Test）

多模态大模型辅助的 Web 应用「测试—修复」迭代工作流。抽象自对一个大中型 Web 应用的多轮实战经验，通用到适用于**任何需要系统化 QA 的 Web 应用**，不绑定特定技术栈或业务领域。

> 作者：大雪块 ｜ 版本：1.0.0 ｜ 许可证：Apache-2.0

## 五阶段迭代闭环

```
测试 → 审核 → 修复 → 回归 → 报告
  ↑                        │
  └── 发现问题 → 进入下一轮 ┘
```

闭环是**收敛的**：每一轮都减少缺陷数量，证据逐轮收紧。当回归报告显示 0 控制台错误、0 禁止串、关键断言全部通过时停止。

---

## 阶段一：全面功能测试

### 前置条件

- 确认测试目标可达（用真实 URL，不要用代理或已断开的隧道）
- 枚举全部视图/页面：grep 主 HTML 中的 `id="view-"` 或等价选择器
- 若计划做破坏性测试，先建立 DB/数据快照基线（见阶段三准备）

### 测试矩阵

| 级别 | 说明 | 示例 |
|------|------|------|
| A — 展示/只读 | 遍历视图，检查可见性，读取关键 DOM 值，确认无 JS 错误 | 全部视图可见、无 console/pageerror |
| B — 可逆写 | 开关按钮、改配置、暂停/恢复——状态须可观测且可逆 | 暂停引擎 → 状态显示 "paused" → 可恢复 |
| C — 破坏性 | 真实提交/创建/删除/撤销等破坏性操作，全链路触达后端 | 资源出现在列表，计数或状态随之变化 |

### 测试脚本模板

用 Playwright（或等价浏览器自动化），接托管 Node 运行时。`scripts/smoke_views.js` 模板：

- 通过 `switchView(id)` 遍历每个已知视图
- 每视图：等待 DOM、抓取 `.metric-value` 文本、扫描 innerText 禁止串、截图
- 全局收集 `console` 错误与 `pageerror` 事件
- 输出 JSON 断言表

### C 级破坏性测试协议

1. **测试前快照**：停服务，冷拷贝 DB 文件（sqlite `.db` + 配置 `.json`）到带日期的备份目录
2. **执行破坏性测试**：先暂停自主引擎（`/api/pause` 或等价暂停端点），再执行提交/创建/删除/撤销
3. **前后态断言**：比对「前/后」计数（资源、订单、余额等）验证真实后端影响
4. **还原**：拷回快照文件，重启服务，验证基线已恢复

---

## 阶段二：审核与根因定位

当用户提交修复/测试报告时，不要照单全收，务必用以下方式核验：

1. **截屏 vs API 比对**：对屏幕上每张指标卡，curl 对应后端接口并比对数值
2. **区分缺陷类型**：真缺陷 / 测试脚本误报 / 设计占位（静态 demo HTML 不是 bug）
3. **多 loader 竞争检测**：对有多 JS 补丁层（如 `app.js` + `fixes_v2.js` + `fixes_v3.js`）的应用，运行时用 `window.fn.toString()` 检查实际执行的是哪个函数——后加载层可能覆盖先前的修复
4. **根因聚类**：按共同根因归类缺陷（如「10 个 onclick 失效全因一个 IIFE 闭包」），而非当成独立问题

---

## 阶段三：代码级修复

### 前端（磁盘静态文件，改盘即生效无需重启）

1. 下载真实生产文件到本地 `fixesN/` 目录
2. 本地编辑
3. 语法检查 `node --check file.js`
4. 上传到生产静态目录
5. 建带时间戳的备份：`file.js.bak.fixN_YYYYMMDD`

### 后端（需重启服务）

1. 编辑 `.py`/`.go`/`.rs` 源
2. 语法/lint 检查
3. 上传、重启服务、验证 health 端点返回 200

### 关键约定（血泪教训）

- **禁止任何补丁层无共享归一化函数而直接 `*100`**。若多层写同一指标卡，必须统一用同一归一化工具（如 `asPctFraction` / `pfFrac`）。后加载层一个 `*100` 就会覆盖先前的正确值。
- **数据源路由**：每个视图 loader 必须调正确的 API 端点。用 `window.fn.toString()` 确认运行时函数打的是预期端点。
- **所有破坏性按钮必须接真实后端 API**。绝不留 `alert("success")` 桩——这比显式「未实现」更危险，因为用户以为操作成功了。

---

## 阶段四：回归验证

每轮修复后重跑全套测试。`scripts/smoke_views.js` 模板应断言：

- `consoleErrors.length === 0`
- `pageErrors.length === 0`
- `forbiddenHits.length === 0`（扫描已知 bug 特征串：`NaN%`、`undefined%`、放大的 `12300%` 等）
- 关键指标断言：特定 DOM 值须匹配 API 真值（如 `metricX === "预期值"`）

### 校验方案 V1–V11

完整参考见 `references/verification-schemes.md`。要点：

| # | 方案 | 工具 | 捕获的缺陷 |
|---|------|------|-----------|
| V1 | DOM 文本断言 | `page.evaluate` 读 `.metric-value` | 错值、格式化错误 |
| V2 | 禁止串扫描 | `innerText.includes(bad)` | 已知 bug 特征复现 |
| V3 | 截屏证据链 | 每视图 `page.screenshot()` | 布局、图表、模态问题 |
| V4 | API 真值比对 | `curl` 后端接口 | 100× 放大、数据源错接 |
| V5 | 函数探针+运行时源码核验 | `window.fn.toString()` | 多 loader 竞争、端点错接 |
| V6 | 控制台/页面/网络监控 | `page.on('console'/'pageerror')` | JS 错误、404、CORS |
| V7 | 并发压测 | 16 并发请求 | 事件循环阻塞回归 |
| V8 | 协议一致性审计 | 比对 `openapi.json` 与前端调用体 | 缺必填字段、错误枚举 |
| V9 | DB 快照还原 | 冷备→测试→还原 | 干净的 C 级测试环境 |
| V10 | 降级横幅校验 | 检查 `#degraded-banner` 可见性 | 静默 mock 数据回退 |
| V11 | 前后态断言 | 比对前后计数 | 验证真实后端影响 |

**工具选择速查**：怀疑数值错 → V1+V4；怀疑旧 bug 复现 → V2；不确定跑的是哪段代码 → V5；布局破损 → V3；静默失败 → V6；接口超时 → V7；前后端协议不符 → V8；需要干净环境 → V9；看到陈旧/mock 数据 → V10；操作是否真生效 → V11。

---

## 阶段五：工作报告

产出**自包含 HTML 报告**，内嵌：

- 摘要网格（错误数、禁止串命中、关键断言）
- 修复历史表（文件、改动、备份）
- 每视图断言表（样例指标、禁止串命中）
- 修复前后截图（base64 内嵌 PNG）
- 根因叙述与经验总结
- 改动文件清单与备份路径

上传到项目 `docs/` 目录，并将结论追加到项目长期记忆/知识库。

---

## 工具链参考

以下为参考实现所用工具，按需适配当前项目等价物：

- **Playwright**：浏览器自动化，读 DOM、截图、监控控制台
- **curl**：直连 API 真值核验
- **SSH (paramiko)**：后端修复的远程上传/备份/重启
- **node --check**：上传前 JS 语法校验
- **Python**：报告生成、脚本编排、协议审计

### 托管运行时约定

使用托管运行时（非系统安装）时，始终用绝对路径：

- Playwright：`NODE_PATH=<托管node_modules> <托管node.exe> script.js`
- Python：`<托管python.exe> script.py`

---

## 换项目复用

本技能自带两个脚本模板，替换顶部 CONFIG 即可适配任意项目：

| 变量 | 位置 | 含义 |
|------|------|------|
| `VIEWS[]` | `scripts/smoke_views.js` | 当前项目的视图 ID 列表 |
| `FORBIDDEN[]` | `scripts/smoke_views.js` | 旧 bug 特征串（如 `'NaN%'`、`'12300%'`） |
| `SPECIFIC_ASSERTS[]` | `scripts/smoke_views.js` | 必须满足的特定指标断言 |
| `BASE_URL` | `scripts/*.js` | 目标地址 |
