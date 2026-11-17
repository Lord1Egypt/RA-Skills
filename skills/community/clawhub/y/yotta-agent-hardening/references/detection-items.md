# 检测项说明（detection items）

> 元安全 yotta-agent-hardening 的静态检测项按 **提示注入防护（pi）/ 工具调用边界（tools）/ 数据隔离（isolation）**
> 三域组织。本文档说明每个检测器查什么、严重级与规则来源，供人工复核与加固排优先级。
> 所有命中都是**启发式发现**，需结合上下文人工确认；报告一律「类」表述，不回显命中原文。

## 规则总览

- **共享表（同步副本，勿手改）**：
  - `TOOL_PATTERN_RULES` 54 条 = 元安 yotta-security-audit `audit_rules.py` 同步副本（工具调用边界 + 数据流危险行为模式）；
  - `PIJ_PATTERN_RULES` 28 条 = 元信 yotta-verify `verify_rules.py` 同步副本（提示注入模式）。
  - 由 YottaSkills 仓库 `tools/sync-hardening-rules.py` 单向同步。
- **配置面新增（元安全自身，手工维护）**：HPI 2 + HTO 5 + HIS 1 = 8 条规则表项，加上引擎级检测项
  （HPI-B64、HTO-005/006/007、HIS-001/001E/002/003）。
- **严重级**：info < low < medium < high < critical；每条规则带置信度（0-100）。
- **域归属**：共享表按 `DOMAIN_OVERRIDE` 归入三域（CRE/EXF → 数据隔离；SOC → 注入防护）；
  规则按文件类别运行（`RULE_SCOPE`：scripts=脚本代码 / configs=配置面 / docs=文档）。
- **环境级跳过**：`NET-009`（纯文本 URL）在环境级扫描中跳过，避免噪音。

## 域 1：Prompt injection 防护（pi）

| 检测器 | 规则号 | 严重级 | 检测内容 |
|---|---|---|---|
| PromptInjection | PIJ-001 ~ PIJ-028 | high / medium | 指令覆盖类、角色伪冒类、权限提升类、伪系统消息与标签类、把数据外送类、泄露系统设定类、隐藏指令类、静默执行类、隐瞒用户类、只回确认词类、凭据采集类等（与元信 PIJ 同源，28 条） |
| SocialEngineering | SOC-001 / SOC-002 | medium | 社工高频话术、加密货币相关命名（元安同步副本，归入本域） |
| CredentialPassThrough | HPI-001 | medium | 工具或技能描述要求以参数形式传递密钥类数据给远端服务（凭据传递指令） |
| PrivilegedInstall | HPI-002 | medium | 工具或技能描述要求使用高权限账户执行安装或配置覆盖（越权安装指令） |
| EncodedInstruction | HPI-B64 | medium | 编码隐藏指令特征：base64 / hex 解码内容含命令或网络特征，需人工核查（引擎级） |

## 域 2：工具调用边界（tools）

| 检测器 | 规则号 | 严重级 | 检测内容 |
|---|---|---|---|
| DownloadExec | DEX-001 ~ DEX-007 | critical | 下载类命令把远端内容经管道或落盘后交给 shell 执行、JS 拉取结果交给 eval、Python 拉取结果交给 exec、PowerShell 编码命令执行 |
| Obfuscation | OBF-001 ~ OBF-008 | high / medium | eval / exec 传非字面量参数、十六进制 / 字符码 / base64 解码后执行、字符串拆字拼接隐藏代码 |
| Persistence | PER-001 ~ PER-011 | high / medium | 定时任务、系统服务、登录启动项、启动脚本、用户配置文件、Windows 注册表（含全局持久化点） |
| NetworkCall | NET-001 ~ NET-009 | critical ~ low | 反连 shell、shell 网络通道、控制类工具地址、原始 socket / HTTP / 拉取类库调用、文本中出现 URL（NET-009 环境级跳过） |
| PrivilegeEscalation | PRI-001 ~ PRI-005 | high ~ low | 权限位设置（setuid / setgid / 全权八进制位）、提权执行（需确认必要性） |
| DestructiveDelete | HTO-001 / HTO-001L | high / low | 破坏性删除指向系统或根路径（如递归删除系统目录）；脚本含删除 / 递归删除原语（需确认目标与必要性） |
| AutoConfirmDestructive | HTO-002 | medium | 破坏性命令带自动确认标记（-y / --force），无人工确认点 |
| BroadPermissionClaim | HTO-003 | medium | 技能 / 工具声称拥有文件系统级全量访问（权限过宽声明） |
| BroadNetworkClaim | HTO-004 | medium | 技能 / 工具声称可向不受限方向发送数据（网络出口无约束声明） |
| McpRemoteSource | HTO-005 | high | MCP 服务器来源为远程 http(s) 地址（不可信源，无哈希 / 签名锁定，需先过元信 / 元审） |
| McpNoVersionLock | HTO-006 | low | MCP 服务器未锁定版本（建议固定版本 / revision，防供应链漂移） |
| McpHighPrivilegeScope | HTO-007 | medium | MCP 服务器声明高权限 scope（全量权限 / 危险标记，建议最小权限） |

## 域 3：数据隔离（isolation）

| 检测器 | 规则号 | 严重级 | 检测内容 |
|---|---|---|---|
| CredentialTheft | CRE-001 ~ CRE-007 | critical ~ medium | macOS 系统凭据存储访问、SSH 私钥文件、AWS 凭据文件、Windows 凭据解密接口、口令库 / 凭据文件、Cookie / 会话相关操作 |
| Exfiltration | EXF-001 ~ EXF-005 | high | 打包压缩上传、归档上传、读取 .env 后外传、读取 SSH 私钥后外传、读取凭据后外传 |
| SensitiveRead | HIS-001 / HIS-001E | high / medium | 脚本读取高敏路径（SSH 私钥 / 云凭据 / 口令库等）；读取 .env / cookie / token 等敏感文件（引擎级，**默认开启、无关闭开关**） |
| CrossContextExfiltration | HIS-002 | high | 同一文件「敏感读取 + 网络原语」共现（跨上下文外传风险，需确认数据不随请求外发） |
| OutputSanitizationGap | HIS-003 | medium | 把密钥 / 令牌值打印或写入日志（输出脱敏缺口，建议先脱敏再输出） |
| HardcodedSecret | HIS-004 | medium | 配置文件疑似硬编码凭据值（密钥 / 令牌 / 口令字面量，建议改用环境变量或凭据管理器） |

## 规则工程说明

- **同步纪律**：TOOL / PIJ 两段是同步副本，改规则请改权威源（元安 `audit_rules.py` / 元信 `verify_rules.py`）
  再跑 `tools/sync-hardening-rules.py`；HPI / HTO / HIS 为本技能「配置面」新维度，手工维护。
- **文件类别作用域**（`RULE_SCOPE`）：破坏性删除 / 自动确认 / 敏感输出类只在脚本代码上跑；
  MCP 来源 / 版本锁定 / 高权限 scope / 硬编码凭据只在配置面跑；权限 / 网络过宽声明在文档 + 配置上跑。
- **置信度**：0-100，供复核优先级参考；静态扫描是启发式，命中项务必人工确认后再处置。
- **脱敏纪律**：检测描述与报告一律「类」表述，不收录可复制注入串，不回显命中原文。
