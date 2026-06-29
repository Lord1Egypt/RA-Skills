# 静态审计清单（54 项）

> Layer 1：所有 Skill 必经，秒级完成。来源：CSA 2026 / Snyk 2026 / MiniScope 2025 / Design Patterns 2025 / 腾讯科恩 2026

## 使用说明

逐项检查，命中即扣分。每项标注：行号（若可定位）、风险类型（R1-R12）、扣分值。一票否决项命中 → 直接终止审查输出 🚫。

---

## 一、元数据检查（7 项，共 14 分）

| # | 检查项 | 检测方法 | 扣分 | 风险 |
|:---|:---|:---|:---|:---|
| M1 | 发布者身份 | 无 GPG 签名或已验证身份 → 扣分 | -2 | — |
| M2 | 版本号规范 | 无版本号或跳跃 ≥3 个主版本号 → 扣分 | -2 | R4 |
| M3 | 依赖声明完整 | 未声明依赖或版本未锁定 → 扣分 | -2 | R4 |
| M4 | 权限声明显式 | 未声明所需权限（文件/网络/进程）→ 扣分 | -2 | R6 |
| M5 | 自述文件 | 无 README 或用法说明 → 扣分 | -2 | — |
| M6 | 数据声明完整 | 未声明是否收集/缓存用户数据、数据留存期限 → 标记 flag:data_policy_missing | -2 | — |
| M7 | 合规声明存在 | 未声明适用的合规框架（GDPR/PIPL 等）或数据处理法律依据 → 标记 flag:compliance_undeclared | -2 | — |

---

## 二、SKILL.md 内容检查（17 项，共 68 分）🔴 含一票否决项

| # | 检查项 | 正则/关键词 | 扣分 | 风险 | 否决 |
|:---|:---|:---|:---|:---|:---|
| C1 | 直接提示注入 | 7 种提示注入正则签名（详见 core/patterns.json 中 C1_injection 区块） | -10 | R1 | ✅ |
| C2 | 间接注入触发源 | 间接注入源检测模式（详见 core/patterns.json 中 C2_indirect_injection 区块） | -4 | R1 | — |
| C3 | 凭证访问模式 | 凭证模式检测（详见 core/patterns.json 中 C3_credential 区块） | -10 | R3 | ✅ |
| C4 | 数据外传目标 | 同时出现 文件读指令 + 外传通道检测模式 | -10 | R5 | ✅ |
| C5 | 系统级危险命令 | 系统级危险命令模式（详见 core/patterns.json 中 C5_dangerous_cmd 区块） | -10 | R2 | ✅ |
| C6 | 权限提升指令 | 权限提升指令模式（详见 core/patterns.json 中 C6_privilege 区块） | -4 | R6 | — |
| C7 | 持久化路径 | 持久化写入路径模式（详见 core/patterns.json 中 C7_persistence 区块） | -10 | R7 | ✅ |
| C8 | 隐蔽 Unicode | `\u200B\|\u200C\|\u200D\|\u202E\|\uFEFF` 零宽/控制字符 | -4 | R8 | — |
| C9 | 条件触发 | `if date\|if time\|after \d{4}\|wait until\|when.*then\|trigger.*when` | -4 | R8 | — |
| C10 | 编码/混淆载荷 | Base64 字符串长度 > 40 且解码后含危险关键词 | -4 | R2/R8 | — |
| C11 | 参数校验缺失 | 检测是否含 user_input / args 等参数接收但无 validate/sanitize 逻辑 → 标记 flag:no_input_validation | -4 | R1/R2 | — |
| C12 | 上下文污染源 | 检测是否含 conversation_history / chat_context / previous_messages 等跨轮引用 → 标记 flag:context_pollution_risk | -4 | R1/R8 | — |
| C13 | 输出安全风险 | 检测是否含 generate / output / reply 等输出路径但无内容过滤声明 → 标记 flag:unfiltered_output | -4 | R10 | — |
| C14 | 版权复述风险 | 检测是否含 reproduce / copy_full_text / verbatim 等完整复述指令 → 标记 flag:copyright_risk | -4 | R10 | — |
| C15 | 模型边界模糊 | 检测是否含角色扮演类指令（要求Agent切换身份/扮演角色/模拟场景的语句），此类指令可能被用于绕过安全护栏 → 标记 flag:roleplay_override | -4 | R1 | — |
| C16 | 外部信息源引用无校验 | 检测是否含 `fetch_url` / `https?://` 等外部引用但无 HTTPS 强制/证书固定/内容哈希校验 → 标记 flag:unverified_external_source | -4 | R11 | — |
| C17 | 持久化配置写入无验证 | 检测是否含 `write.*config` / `append.*bashrc` / `add.*startup` 等持久化写入但无用户确认门控 → 标记 flag:persistent_config_no_verify | -4 | R12 | — |

**C1/C3/C4/C5/C7** 任意命中 → 一票否决，直接裁定 🚫 恶意，终止审查。

---

## 三、辅助脚本检查（12 项，共 48 分）🔴 含一票否决项

| # | 检查项 | 检测方法 | 扣分 | 风险 | 否决 |
|:---|:---|:---|:---|:---|:---|
| S1 | 子进程调用 | `subprocess\|os\.system\|os\.popen\|exec\|spawn\|ShellExecute` | -4 | R2 | — |
| S2 | 网络出站 | `socket\|requests\.(get\|post)\|urllib\|http\.client\|fetch.*http` | -4 | R5 | — |
| S3 | 敏感路径读写 | `/etc/passwd\|C:\\\\Windows\|~/.ssh\|/root/` | -4 | R2 | — |
| S4 | 动态代码执行 | `eval\(\|exec\(\|compile\(` | -4 | R2 | — |
| S5 | 依赖 CVE | 与 CVE DB 交叉比对命中的依赖 | -2 | R4 | — |
| S6 | 安装脚本恶意行为 | `curl.*\|.*bash` 或 `wget.*\|.*sh` 链式执行模式 | -10 | R2 | ✅ |
| S7 | 文件权限修改 | `chmod\|chown\|icacls\|Set-Acl` | -4 | R6 | — |
| S8 | 配置篡改 | `reg add\|regedit\|Set-ItemProperty\|defaults write` | -4 | R7 | — |
| S9 | 文件上传逻辑 | 检测是否含 file_upload / multipart / read_file + 写入路径组合 → 标记 flag:unchecked_upload | -4 | R4/R7 | — |
| S10 | 外部 API 无校验 | 检测 HTTP 出站调用是否无响应签名验证、无回调白名单 → 标记 flag:unverified_api_call | -4 | R5 | — |
| S11 | 数据收集静默 | 检测是否含 log / collect / analytics / telemetry 等静默数据采集 → 标记 flag:silent_data_collection | -4 | R9 | — |
| S12 | 第三方 SDK 引入 | 检测是否含非官方源的 import/require 且无安全评估声明 → 标记 flag:unvetted_sdk | -4 | R4 | — |

**S6** 命中 → 一票否决，直接裁定 🚫 恶意。

---

## 四、权限声明检查（11 项，共 30 分）

| # | 检查项 | 判定逻辑 | 扣分 | 风险 |
|:---|:---|:---|:---|:---|
| P1 | 最小权限原则 | 权限声明范围 > 任务描述范围 → 扣分 | -3 | R6 |
| P2 | 网络权限必要性 | 声明网络权限但任务无联网需求 → 扣分 | -3 | R6 |
| P3 | 文件读写范围过宽 | 声明 `/**` 全局读写 → 扣分 | -3 | R6 |
| P4 | 进程管理权限 | 声明 `process_kill`/`service_control` 无合理场景 → 扣分 | -3 | R6 |
| P5 | 权限传递风险 | 存在权限串联提升路径（A→B→C→获取更高权限）→ 扣分 | -3 | R6 |
| P6 | 用户确认门控 | 高风险操作（删除/支付/发邮件）未声明 `confirm_required` → 扣分 | -2 | — |
| P7 | 沙箱化标记 | 未声明 `sandbox: required` → 扣分 | -1 | — |
| P8 | 越权访问防护 | 是否声明了租户/用户级数据隔离机制，无隔离声明 → 标记 flag:no_tenant_isolation | -3 | R6/R9 |
| P9 | 资源配额声明 | 是否声明 CPU/内存/API 频次上限，无限制声明 → 标记 flag:no_resource_quota | -3 | — |
| P10 | 超时控制声明 | 是否声明外部调用/内部处理的超时阈值，无超时机制 → 标记 flag:no_timeout_control | -3 | — |
| P11 | 工具调用链路完整性 | 是否声明中间结果签名/哈希校验机制，无校验声明 → 标记 flag:no_chain_integrity | -3 | — |

---

## 五、数据安全声明检查（7 项，共 14 分）

| # | 检查项 | 检测方法 | 扣分 | 风险 |
|:---|:---|:---|:---|:---|
| D1 | PII 收集声明 | 检测是否声明收集/处理的个人数据类型及法律依据 | -2 | R9 |
| D2 | 敏感数据脱敏 | 检测日志/响应/缓存中是否含明文 email/phone/ID card 模式 | -2 | R9 |
| D3 | 传输加密声明 | 检测是否声明 TLS 1.2+ 且静态数据 AES-256 加密 | -2 | R9 |
| D4 | 密钥管理方式 | 检测是否含硬编码 token/password/api_key | -2 | R9 |
| D5 | 数据删除接口 | 检测是否声明用户数据删除/导出机制 | -2 | R9 |
| D6 | 数据保留期限 | 检测是否声明各类数据保留策略与自动销毁机制 | -2 | R9 |
| D7 | 数据跨域传输 | 检测是否声明数据跨境传输的合规依据 | -2 | R9 |

---

## Layer 1 总分

```
Layer1_Score = 100 - Σ(扣分)
```

满分 100。命中一票否决项 → 直接 0 分 + 🚫。

---

## 检测优先级

1. **先跑否决项**（C1/C3/C4/C5/C7/S6）→ 命中即终止
2. **再跑高危项**（C2/C6/C8/C9/C10/S1-S4/S7-S8/C11-C17/S9-S12/P8-P11）
3. **再跑数据安全项**（D1-D7）
4. **最后跑中危项**（M1-M7/P1-P7/S5）
