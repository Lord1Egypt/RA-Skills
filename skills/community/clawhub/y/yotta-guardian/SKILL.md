---
name: yotta-guardian
slug: yotta-guardian
version: 0.1.10
displayName: 元盾·危险调用拦截
summary: 跨智能体危险调用拦截护栏：拦截危险命令、写入、提权等工具调用，输出审计日志。
description: '元盾 —— 跨智能体的危险调用拦截护栏：确定性规则引擎 + 可插拔意图验证（不绑模型），拦截危险 exec / write / edit / read / run / shell 工具调用，提供审计日志。触发：代理要执行高风险命令（递归删除、磁盘格式化、提权、防火墙改动、反向 shell、下载即执行等）、要写入系统敏感路径或修改系统配置、要在执行危险操作前做安全检查、或用户说 护栏/拦截/危险操作/安全检查 等。边界：默认只读评估，不自动执行也不放行危险操作；不替代用户决策；不隐藏审计记录；规则可配置。'
tags: [危险拦截, 命令防护, 审计日志, 安全护栏, guardian, 权限]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-guardian
---
# 元盾（yotta-guardian）

跨智能体的工具调用拦截护栏：**确定性规则引擎 + 可插拔意图验证**，对 exec / write / edit / read / run / shell 工具调用做安全评估，输出 allow / deny + 命中规则 + 审计日志。

零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用；Claude Code / Cursor / Codex / 通用 Agent 均可调用。

## 何时使用

- 代理要执行高风险命令：递归删除系统路径、磁盘格式化（mkfs / fdisk / dd 写设备）、提权（chmod 全权限 / chown 系统路径 / 账户管理）、防火墙改动（iptables 清空 / ufw disable / netsh 关闭）、反向 shell（netcat 执行 / bash /dev/tcp）、下载即执行（curl / wget 管道交给 shell）等；
- 代理要写入系统敏感路径（/etc/passwd、/etc/sudoers、SSH 授权文件、Windows hosts / 系统目录、注册表启动项）或修改系统配置；
- 需要在执行危险操作前做一次确定性安全检查（gate），并留下审计记录。

**Do NOT trigger**：

- 默认只读评估，不自动执行、不放行危险操作，也不替代用户最终决策；
- 不隐藏审计记录；被拦截时如实上报原因与命中规则；
- 已获明确授权的运维操作应显式放行（--allow / --allow-path / 自定义规则），而不是绕过检查。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 检查一条 exec（0 = 允许）
python3 scripts/yotta_guardian.py check exec --cmd "git status"

# 检查危险命令（默认拒绝，退出码 3）
python3 scripts/yotta_guardian.py check exec --cmd "rm -rf /"

# 检查写操作
python3 scripts/yotta_guardian.py check write --path /etc/passwd --content "..."

# 批量检查（agent 在执行前把待执行调用列表交给护栏）
python3 scripts/yotta_guardian.py check --batch calls.json --json

# 审计
python3 scripts/yotta_guardian.py check exec --cmd "..." --audit-log .yotta-guardian/audit.jsonl
python3 scripts/yotta_guardian.py audit --file .yotta-guardian/audit.jsonl --tail 20
```

## 工作流程（AI 智能体执行危险操作前）

1. **先检查**：把将要执行的工具调用交给护栏 `check`（单条或 `--batch` 批量）。
2. **看退出码**：0 = 允许；1 = 允许但带警告（建议人工复核）；2 / 3 = 拒绝（high / critical，不要执行）；4 = 用法错误 / 致命异常（引擎没跑起来 —— 绝不要当作放行）。
3. **被拒绝怎么办**：如实向用户报告原因与命中规则；确有授权的操作，用 `--allow` / `--allow-path` / 自定义规则文件放行并留审计记录；**不要绕过检查**。
4. **留痕**：高风险场景用 `--audit-log` 落审计日志，供追溯。

## 宿主接入（把护栏挂到「工具调用前」事件时）

`skill-manifest.json` 声明 `before_tool` + `fallback: explicit-unverified`。接入方按下面三条做，可避开实测踩过的坑：

1. **放行不要回「允许」**：只在拦截时输出拒绝判定（如 `permissionDecision: "deny"`）；放行时**不输出任何判定**，把决定权交回宿主。若放行时回「allow」，会覆盖宿主自身的权限流程，护栏就变成自动放行器 —— 护栏只该「拦」，不该「代批」。
2. **用文件接引擎输出**：部分 hook 进程环境里，用管道捕获子进程 stdout 会拿到空值（同一写法跑 `python -c "print(1)"` 却正常）；把引擎 stdout / stderr 重定向到临时文件再读回，判定即稳定（引擎自身的 stdout 是纯净的，`--json` 可直接解析）。
3. **stdin 先按 UTF-8 读**：hook 载荷里的命令文本常含中文，按本机默认码页解码会乱码；读 stdin 前先 `sys.stdin.reconfigure(encoding="utf-8")`（引擎已对自身 stdout / stderr 做 UTF-8 处理，stdin 由接入方负责）。

另外：引擎对「没跑起来」是 fail-closed 的 —— 规则表加载失败或运行期未预期异常一律以退出码 4 结束并在 stderr 写「致命异常: …」。接入方应把 4 当作**不放行 + 报告**处理，而不是放行。

## 策略（policy）

| 策略 | 行为 |
|---|---|
| default（默认） | 拒绝 critical / high；中危警告（exit 1） |
| strict | 拒绝 medium 及以上；低危也提示 |
| loose | 仅拒绝 critical；高危仅警告 |

## 可插拔意图验证（不绑模型）

- 默认纯确定性规则，不调用任何模型、零外部依赖；
- `--heuristic`：启用内置本地启发式验证（对高影响动词升级为需人工确认）；
- `--verifier "命令"` 或配置文件：外接任意意图验证器（如 LLM 网关），协议见 references/intent-verifier.md。

## 参考文档

- references/rules.md — 规则目录与匹配说明
- references/policies.md — 策略 / 退出码 / 使用姿势
- references/intent-verifier.md — 意图验证器协议

## 使用范围、授权与法律红线

- **范围**：本技能只对工具调用做执行前风险评估，并输出 allow / deny 与审计记录；它不是操作系统沙箱，不执行、不放行、不修改目标系统，也不替代宿主自身的权限控制。
- **授权**：仅用于你拥有或已获得明确授权的系统、账户与数据。被拒绝的操作必须由有权限的人确认；显式放行只用于已确认的合法运维场景。
- **法律与合规红线**：不得用于未授权访问、破坏、规避安全控制或其他违法用途；使用者应遵守适用法律、监管要求与组织安全政策。评估结果只作为决策辅助，最终责任由操作者承担。
