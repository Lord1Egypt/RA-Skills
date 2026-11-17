# Changelog

## v0.3.3 (2026-11-05)

- 修复 PRI-001 特殊权限位正则误报；刷新家族规则表摘要；补齐测试接线。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.3.2 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.3.1 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.3.0 (2026-09-27)

新增教育版（--target edu）：学生数据隐私风险扫描，与技能模式 / 系统模式并列，仍为纯只读、零依赖。

- **15 条规则**（规则包 `scripts/student_data_rules.json`，版本化 JSON、只读数据）：身份证号（校验位）/ 手机号 / 邮箱 / 学籍号字段 / 姓名+成绩组合 / 出生日期 / 家庭住址 / 家长联系方式 / 健康与身心状况 / 资助与家庭境况 / 生物识别 / 显式未成年人标记 / 出本机路径 / 文件名疑似含姓名 / AI 工具与临时目录。
- **文件形态**：CSV / TSV / 文本 / JSON 等，以及 xlsx / docx（标准库只读轻解析）；PDF / 图片 / 旧版 Office / 压缩包不解析，计入报告「未解析 / 跳过」。
- **隐私约束**：报告一律脱敏（身份证 / 手机 / 学籍号保留末 4 位、姓名保留姓、地址保留前 3 个字符、邮箱保留首字符与域名），不提供明文回显；不做身份与年龄推断、不做跨文件个体关联、不联网、不缓存原文；报告不得写入被扫描目录。
- **参数纪律**：edu 模式 `--path` 必填（不做自动发现）；新增 `--edu-rules` 自定义规则包；退出码沿用 `0/1/2/3/4`。
- 新增 `references/student-data-scan.md`；新增 `scripts/test_yotta_audit_edu.py`（22 项），技能模式与系统模式回归全绿。

## v0.2.4 (2026-09-19)

版本对齐维护：修复历史发布元数据与包内版本不一致；无功能变更。

## v0.2.3 (2026-09-13)

- 文档 hygiene 清理：移除历史公开文档中的内部表述，版本同步 0.2.3。
- 发布工作流 `.github/workflows/publish.yml` 纳入版本库，标签推送可触发 GitHub Actions。
- 发布包排除测试脚本与 Python 缓存，避免 `__pycache__` / `.pyc` 进入 npm 包体。

## v0.2.2 (2026-08-30)

- 措辞规范：正文不再写版本号、统一对外表述。

## v0.2.0 (2026-08-30)

安全家族检测能力增强（8 检测点威胁捕获模型 + 13 行为项）：

- **威胁捕获模型**：官方 8 检测点 taxonomy（供应链 / 命令执行 / 网络请求与数据外传 / 文件操作与敏感路径访问 /
  Prompt 注入 / 远程脚本下载执行 / 可疑编码·混淆 / 其他）+ 13 行为项归口。
- **新检测器（规则 54 → 61）**：路径穿越（PathTraversal）/ MCP 命令执行（MCPCommandExec）/
  MCP 任意文件读写（MCPFileAccess）。
- **报告升级双视角综合报告**：安全健康度评分（0-100）+ 威胁捕获模型视图（8 类逐类 verdict）+
  行为项（13 项，text / JSON / Markdown）。
- 自扫 0 中高危；测试 24 / 24 全绿。

## v0.1.7 (2026-08-29)
## v0.1.7 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-security-audit --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-security-audit.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.7。
- 维护修复：签名数据文件跳过列表加入 hardening_rules.py。
- 无功能变更（仅文档与版本同步）。

## v0.1.6 (2026-08-29)

维护性修复（签名数据豁免）：

- 签名数据文件列表加入 `verify_rules.py`（yotta-verify 规则表）：元安扫描 yotta-verify 时
  规则表自身字面量不再误报为 critical/high（系统凭据存储 / SSH 密钥 / 平台凭据解密等检测模式属签名数据）。

## v0.1.5 (2026-08-28)


中英双语 README 对齐（英文门面 + 中文全档）：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 13 类检测器 / 命令 / 使用示例 / 安装 / 升级卸载 / 常见问题 / 相关技能 / 边界 / 开发校验全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，顶部加语言切换链接。
- **移除 npx --agent codex 安装行**：README 安装方式一不再出现 `npx -y @yottameta/... --agent <name>`（固定智能体名，违反安装规范；npx 用 -g 或 --dir，--agent 仅 install.sh 用）。
- **package.json**：description 改英文；files 加 README.zh-CN.md；版本 0.1.4 → 0.1.5。
- 版本四处对齐：package.json / SKILL frontmatter / 引擎 VERSION / 文档。
- 边界（B 方案）：references / CHANGELOG / 测试注释不翻译；SKILL 触发描述保持中文。

## v0.1.4 (2026-08-26)

系统基线新增 **CIS 合规检测器**（Linux，只读，接入 run_linux_baseline 尾部）：

- 空密码账号（/etc/shadow 密码字段为空 = 无需密码可登录，high）。
- sudo NOPASSWD 免密提权条目（/etc/sudoers 与 /etc/sudoers.d，medium）。
- 内核参数加固（sysctl 只读查询）：fs.suid_dumpable / kernel.randomize_va_space
  （ASLR）/ net.ipv4.conf.all.accept_redirects / send_redirects / ip_forward。
- 登录历史：lastb 失败登录（medium，暴力破解迹象）+ last 近期登录提示（low）。
- 不可读文件 / 命令缺失统一降级为 info 提示，不阻断基线扫描。

测试：新增 scripts/test_yotta_audit_cis.py（11 项，mock 只读命令，跨平台可跑）；
py3.8 + py3.13 全量 24/24 通过；自扫 exit 0 无中高危误报（新增 2 条 LOW 为 CIS 检测代码提及 sudo 的预期提示）。


## v0.1.3 (2026-08-26)

banner 大标题加功能后缀「元安安全审计」，与 YottaMeta 技能矩阵视觉统一；无功能变更。

## v0.1.2 (2026-08-26)

README 按标准补全：新增「这是什么 / 核心价值 / 核心优势 / 功能体系 / 常见问题 / 相关技能 / 升级卸载」等章节，与 YottaMeta 技能矩阵 README 标准对齐；无功能变更。


## v0.1.1 (2026-08-26)

包打包修正：移除误入的 __pycache__/*.pyc（Python 字节码缓存，运行时自动重建，不影响功能）。


## v0.1.0 (2026-08-26)

YottaMeta 自有实现首版（已完全重写）：

- 双模式：--target skill（默认，13 类技能恶意模式检测）/ --target system（系统安全基线，平台感知）。
- 13 类检测器全新实现：DownloadExec / Obfuscation / Persistence / Exfiltration / CredentialTheft /
  NetworkCall / PrivilegeEscalation / SocialEngineering / Base64 / IOCMatch / PostInstallHook /
  HiddenChar / Entropy。
- 系统安全基线（只读）：Windows（注册表启动项/计划任务/服务/防火墙/共享/管理员组/持久化点/浏览器凭据位置提示）、
  Linux（SUID-SGID/全局可写/启动项/SSH 配置/开放端口/用户 crontab/PATH 劫持）。
- 17 类智能体技能目录自动发现（与 install.js 权威映射一致）；签名数据文件豁免自扫。
- 报告：文本 / --json / --report report.md，默认脱敏（不打印私钥/环境变量值/完整凭据）。
- 零依赖（Python 3.8+ 标准库），Windows + Linux 通用，UTF-8 加固（GBK 控制台不崩）。
- exit code 语义：0=干净/仅 low，1=medium，2=high，3=critical，4=错误。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明。
