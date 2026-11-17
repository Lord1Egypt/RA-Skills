---
slug: ue-audit
name: ue-audit
displayName: UE 工程体检
version: 0.4.0
runtime_version: 0.4.0
summary: 只读 UE 工程体检/验收：基线 diff、日志与打包就绪度、蓝图/DataTable/UMG/材质/AnimBP 结构检查，输出 JSON/Markdown/HTML/JUnit 与证据包。
description: UE 工程体检 / UE 审计 / UE 验收（Unreal Engine Audit / UE5 Audit / Project Health Check）：只读检查工程结构、基线变更、日志、打包就绪度，以及 Blueprint/DataTable/UMG/Material/AnimBP 结构；输出 JSON/Markdown/HTML/JUnit 与可携带证据包。不写工程、不自动修复、不主动编译；在线检查需本地编辑器桥。适用于 UE 5.1+ 工程，Windows 优先。
license: Apache-2.0
requires_api_key: false
homepage: https://github.com/miracle1814/ue-audit
tags:
  - unreal-engine
  - ue5
  - ue-audit
  - ue_audit
  - audit
  - verification
  - ci
  - blueprint
  - datatable
  - umg
  - 虚幻引擎
  - 工程体检
  - 验收
  - windows
---

# UE 工程体检

只读的 Unreal Engine 工程体检/验收工具。它不写工程、不自动修复、不主动编译，只回答五个问题：

1. 工程结构是否完整？
2. 相对基线改了什么？
3. 有没有异常文件、日志错误、打包配置问题？
4. 选中的 Blueprint / DataTable / UMG / 材质 / AnimBP 结构是否可读？
5. 这次审计本身有没有观察到工程内容变化？

> 这是**评估报告**，不是认证，也不是“保证无写入”的法律证明。  
> 所有检查都区分 `pass / warn / fail / skip / unknown`；`unknown` 不会被当成 `pass`。

## 30 秒路由

| 你的处境 | 直接做 |
|---|---|
| 第一次用，先确认能跑 | `python scripts/run_audit.py doctor <项目>` |
| 给工程做一次离线体检 | `python scripts/run_audit.py audit <项目> --out <输出目录>` |
| 对比“改之前 / 改之后” | 先 `--save-baseline`，再 `--baseline` |
| 验收 AI/队友改了什么 | `verify --task task.json --baseline before.json` |
| 检查 Blueprint/DataTable/UMG/材质/AnimBP | 加 `--live` + 对应 `--blueprint/--datatable/--widget/--material/--animbp` |
| 接进 CI | 用 `junit.xml` + `--fail-on error` |
| 想知道审计期间有没有写入 | 看 `SAFE001` / `SAFE002` 和 `evidence/` |

## 何时使用

当用户提出以下需求时使用：

- “帮我体检一下这个 UE 工程 / 看看有没有明显问题”
- “和上个版本比，改了什么 / 有没有多改资产”
- “验收一下 AI/外包这次改动”
- “检查日志、打包配置、地图引用、GameDefaultMap”
- “读一下这个蓝图/DataTable/UMG/材质/AnimBP 的结构”
- “生成一份可以给甲方/CI 看的报告”
- “证明这次审计有没有写工程”

触发词：UE、UE5、Unreal、虚幻引擎、工程体检、工程审计、验收、基线、Blueprint、蓝图、DataTable、UMG、Widget、Material、AnimBP、JUnit、CI、证据包。

## 何时不要用

以下场景不属于本 Skill，强行使用只会得到假成功：

- **需要自动修复、自动改图、自动保存** → 本 Skill 只读，不写资产。
- **需要主动编译蓝图/材质** → 本 Skill 只读 `compile_status`，不调用编译。
- **需要实际 cook / pak / 打包上架** → `PKG001` 只做静态打包就绪度检查。
- **判断玩法、数值、美术、设计质量** → 本 Skill 不做语义/审美判断。
- **没有 baseline 却要求“验收改了什么”** → 只能给 `unknown`，不能假装通过。
- **没有本地编辑器桥却要求在线资产检查** → 在线项会 `skip/unknown`，离线检查仍可用。
- **需要认证/法律意义上的只读证明** → 本 Skill 只记录观察结果，不做认证。

## 5 分钟最小成功路径

### Step 1 · 环境自检

```bash
python scripts/run_audit.py doctor C:/Projects/MyGame
```

确认能读到 `.uproject`、Content/Config，输出 manifest 摘要。

### Step 2 · 离线体检

```bash
python scripts/run_audit.py audit C:/Projects/MyGame --out D:/audit/run1
```

打开 `D:/audit/run1/report.html`。

### Step 3 · 建立基线

```bash
python scripts/run_audit.py audit C:/Projects/MyGame \
  --out D:/audit/run1 \
  --save-baseline D:/audit/baseline.json
```

### Step 4 · 对比基线

```bash
python scripts/run_audit.py audit C:/Projects/MyGame \
  --out D:/audit/run2 \
  --baseline D:/audit/baseline.json
```

### Step 5 · 验收 AI 任务

```bash
python scripts/run_audit.py verify C:/Projects/MyGame \
  --task task.json \
  --baseline D:/audit/baseline.json
```

`task.json` 最小示例：

```json
{
  "task_id": "ai-task-001",
  "idempotency_key": "ai-task-001",
  "expected_write_set": [
    "Content/Blueprints/BP_Test.uasset",
    "/Game/Data/DT_Items"
  ]
}
```

## 检查项

| ID | 检查 | 模式 | 说明 |
|---|---|---|---|
| PRJ001 | 工程结构 / EngineAssociation / 插件声明 | 离线 | `.uproject`、Content、Config、Source、插件描述 |
| PRJ002 | 确定性 manifest + 基线 diff | 离线 | SHA256、size/mtime、新增/删除/修改 |
| PRJ003 | 异常文件事实 | 离线 | 零字节、大文件、无法哈希、重复 hash |
| GIT001 | Git 卫生 | 离线可选 | 未提交、未跟踪、冲突、超大 tracked 文件 |
| PKG001 | 打包就绪度 | 离线 | GameDefaultMap / StartupMap / MapsToCook 与 manifest 对照 |
| LOG001 | 日志错误/崩溃 | 离线 | `Saved/Logs`，只把 error/fatal 变成 finding |
| LIVE001 | 桥/编辑器健康 | 在线可选 | `bridge_loaded`、项目名、引擎版本 |
| BP001 | 蓝图状态 + 图统计 | 在线可选 | compile_status / graph / node / connection |
| DT001 | DataTable 结构 | 在线可选 | 行数、RowStruct、CSV 支持 |
| UMG001 | Widget 树 | 在线可选 | 控件数、根节点、空树 |
| MAT001 | 材质结构 | 在线可选 | expression 数量 |
| ANIM001 | AnimBP 结构 | 在线可选 | graph/node 统计 |
| PIE001 | PIE smoke | 在线 opt-in | 启动 PIE、读新日志、`finally` 停止 |
| SAFE001 | manifest 证据 | 全程 | 前后内容/元数据对比 |
| SAFE002 | during-write 监控 | 全程 | Windows 目录事件；不可用如实标记 |
| VER001 | 任务写集验收 | verify | expected write set 对照 |

## 在线模式

在线检查是**可选增强**，需要本机运行 UE 编辑器和本地 HTTP 编辑器桥（默认 `127.0.0.1:8889`）。桥不随 Skill 捆绑。

token 优先级：

```text
--token → UE_AUDIT_BRIDGE_TOKEN → UE_AUDIT_BRIDGE_TOKEN_FILE → %APPDATA%\ue-audit\bridge-token
```

没有桥时：

- `LIVE001` / `BP001` / `DT001` / `UMG001` / `MAT001` / `ANIM001` / `PIE001` 标记 `skip` 或 `unknown`；
- 离线检查仍然完整完成；
- 不会因为在线失败而伪造 `pass` 或 `fail`。

## 输出

```text
<out>/
  report.json
  report.md
  report.html
  junit.xml
  evidence/
    manifest-before.json
    manifest-after.json
    manifest-diff.json
    readonly-proof.json
    write-events.json
    checks.json
    index.json
```

- `report.html`：给人看，自包含，无外部 CDN
- `report.json`：给工具/CI 读
- `junit.xml`：CI 使用
- `evidence/`：manifest、diff、只读证据、目录事件、带 SHA256 的索引

## 如何读报告

- `pass`：检查跑完，没发现问题
- `warn`：有非阻塞问题
- `fail`：有应当阻断验收的问题
- `skip`：未请求/不适用
- `unknown`：当前无法判断（无 baseline、无日志、桥不可用、API 不可用、文件太大无法哈希）

> **`unknown` 不是 `pass`。** 报告里看到 `unknown`，必须说明“未验证”，不能写成“通过”。

## 只读边界

`SAFE001` 比较审计开始/结束的 manifest；`SAFE002` 在 Windows 上监听 Content/Config/Source/Plugins 的目录事件。

它们能发现：

- 文件新增/删除/内容变化；
- size/mtime 变化；
- 审计期间的目录写入事件；
- 部分无法哈希的大文件（标记 `unknown`）。

它们**不能**证明绝对没有写入：

- 写入后又恢复到相同字节和 metadata；
- 排除规则之外的文件；
- 编辑器内存、注册表、DDC、外部进程；
- 内核级 ETW/USN 事件。

所以报告写的是“**未观察到差异/事件**”，不是“绝对只读”。

## 常见任务

### 1. 只做工程体检

```bash
python scripts/run_audit.py audit C:/Projects/MyGame --out D:/audit/run1
```

### 2. 验收 AI 改动

```bash
python scripts/run_audit.py verify C:/Projects/MyGame \
  --task task.json \
  --baseline D:/audit/baseline.json
```

### 3. 检查单个资产

```bash
python scripts/run_audit.py audit C:/Projects/MyGame --live \
  --blueprint /Game/Blueprints/BP_Player \
  --datatable /Game/Data/DT_Items \
  --widget /Game/UI/WBP_HUD \
  --material /Game/Materials/M_Test \
  --animbp /Game/Anims/ABP_Test
```

### 4. 接 CI

```bash
python scripts/run_audit.py audit C:/Projects/MyGame \
  --out D:/audit/ci \
  --fail-on error
```

使用 `D:/audit/ci/junit.xml` 作为测试报告。

## 限制

- 离线不解析 `.uasset` 二进制，只做文件级事实。
- `PKG001` 是静态检查，不执行 cook/pak。
- `MAT001` / `ANIM001` 只看结构，不做材质/动画语义判断。
- `UMG001` 只看控件树，不判断文本、绑定、布局或视觉质量。
- UE 5.1 的 `DT001` 可能因 RowStruct/CSV 不可读而保持 `unknown`。
- `PIE001` 是 stateful、opt-in，不保存资产，但不能替代完整自动化测试。
- 不做自动修复、不做认证、不做内核级 USN/ETW。

## 版本与许可

- Skill 版本：`0.4.0`
- 运行代码版本：`0.4.0`
- 许可证：Apache-2.0
- 源码：https://github.com/miracle1814/ue-audit
- 样例报告：`examples/sample-report/report.html`
