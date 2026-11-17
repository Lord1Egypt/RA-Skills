# Skill Template Examples

`examples/` 是面向**技术人员与 AI 编程工具**的**核心实现案例**目录：提供可运行、可测试、可复制的参考代码，用于指导新技能的 `scripts/` 应如何编写。

**`examples/` 不是完整 skill 仓库。** 不要整包照搬 `examples/<mode>/` 到新技能根目录。应按各 example README 的 **copy map**，**选择性复制**到新技能的 `scripts/`（及按需的 `tests/`）。

根 `README.md`、`SKILL.md`、`references/`、`development/` 仍按模板主目录规则编写，**不要**从 `examples/` 复制。

## 四类外部交互方式

一级目录固定为四种模式（不可删除、不可移动）：

| 目录 | 类型 | 状态 | 适用场景 |
|---|---|---|---|
| `real_browser_rpa` | 真实浏览器 RPA | **已有案例** | 真实第三方网站、登录态、人工验证、滚动采集 |
| `simulator_browser_rpa` | 仿真浏览器 RPA | **已有案例** | 自有 sandbox、可控页面、表单 RPA、adapter 分层 |
| `real_api` | 真实 API | **占位** | 真实系统接口、token、权限、限流（尚未沉淀可复制实现） |
| `simulator_api` | 仿真 API | **占位** | mock/sandbox API、无需浏览器（尚未沉淀可复制实现） |

## 两类浏览器 RPA 的区别

| | real_browser_rpa | simulator_browser_rpa（修正后） |
|---|---|---|
| 目标 | 真实第三方网页 | 自有仿真页面 / sandbox / jc2009 类 |
| 风控 | 高（验证码、登录态、反爬） | 低（DOM 可控） |
| 账号 | account-manager + profile | account-manager + profile（`simulator_rpa` 档） |
| 用途 | 生产级真实采集/操作参考 | adapter 分层 + 表单 RPA 教学 |

### 工程范式对比

| 工程范式 | real_browser_rpa | simulator_browser_rpa（修正后） |
|---|---|---|
| async Playwright | ✅ | ✅ |
| 薄 adapter + `*_playwright.py` | `task_rpa.py` | `simulator_playwright.py` |
| account-manager subprocess | ✅ | ✅（`simulator_rpa` 档位） |

两者工程范式一致，差异在目标系统（真实站 vs 仿真站/本地 demo）。

## 如何选择示例

| 你的场景 | 参考目录 |
|---|---|
| 真实网站 + 浏览器 + 登录/验证码/滚动 | **real_browser_rpa** |
| 仿真页面 + 浏览器 + 表单/批量提交 | **simulator_browser_rpa** |
| 真实系统 API | **real_api**（当前占位，不可作为实现参考） |
| mock / sandbox API（无浏览器） | **simulator_api**（当前占位，不可作为实现参考） |

## 轻量结构约定

每个 `examples/<mode>/` 推荐结构：

```text
examples/<mode>/
  README.md
  scripts/
    service/
    util/
  tests/
```

- 仅 `simulator_browser_rpa` 可额外包含 `sandbox/`
- 仅未来确实需要样例数据时可加 `fixtures/`
- **不要**在 `examples/<mode>/` 下要求或添加：`SKILL.md`、根市场 `README.md`、`references/`、`development/`、`assets/`、`.github/`、release workflow 等完整 skill 仓库层文件

## `scripts/` 与 `examples/` 边界

| | `scripts/` | `examples/` |
|---|---|---|
| 定位 | 真实技能业务逻辑的标准骨架 | 核心实现案例与复制参考 |
| 内容 | 干净的技能骨架，无教学/demo 代码 | 可运行参考实现，非完整 skill |
| 旧示例 | **不得**出现 `example_*` 目录或文件 | 四类一级目录固定保留 |

复制规则：

- 真实浏览器 RPA → 参考 `examples/real_browser_rpa/`
- 仿真浏览器 RPA → 参考 `examples/simulator_browser_rpa/`（adapter 分层权威参考：`scripts/service/adapter/`）
- `real_api/`、`simulator_api/` 当前为规划占位，**不得**作为实现参考

> 示例提供的是**参考架构与边界**，不是业务代码原样复制。复制前先读对应 README 的 copy map 与「禁止照抄」章节。
