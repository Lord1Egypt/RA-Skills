# Changelog

## v0.3.3 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.3.2 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.3.1 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.3.0 (2026-09-25)

口径修正：安装边界 + 批量安装需显式确认（ClawHub LLM 复核）。

- SKILL.md 边界节新增安装边界：只写用户显式指定的目标，批量安装到全部已知智能体目录必须显式 `--yes`，不做静默多目录写入，符号链接目标一律拒绝。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。

## v0.2.9 (2026-09-19)

版本对齐维护：修复历史发布元数据与包内版本不一致；无功能变更。

## v0.2.8 (2026-09-13)

- 文档 hygiene 清理：移除历史公开文档中的内部表述，版本同步 0.2.8。
- 发布工作流 `.github/workflows/publish.yml` 纳入版本库，标签推送可触发 GitHub Actions。
- 发布包排除测试脚本与 Python 缓存，避免 `__pycache__` / `.pyc` 进入 npm 包体。

## v0.2.7 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-logwatch --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-logwatch.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.2.7。
- 无功能变更（仅文档与版本同步）。

## v0.2.6 (2026-08-27)

发布元数据同步（publish-metadata sync）：

- ClawHub 经网页后台「New version」流程重发至 v0.2.6（页面已确认展示名 `元察 yotta-logwatch` / slug `yotta-logwatch`）；为保持三源（ClawHub / GitHub / npm）版本一致，本仓库与 npm 同步升版 0.2.5 → 0.2.6。
- 无功能 / 引擎 / 规则 / 文档变更；纯版本对齐。

## v0.2.5 (2026-08-27)

发布元数据修正（publish-metadata patch）：

- 修复 ClawHub 展示名缺失中文：v0.2.4 发布时 `--name` 参数值在 shell 中被空格拆分（`--name 元察 yotta-logwatch` 未加引号），导致 `--name` 未生效、ClawHub 卡片展示名仍为裸 slug `yotta-logwatch`。0.2.5 改为带整体引号 `--name '元察 yotta-logwatch'` 三源重发，确认 ClawHub 展示名为「元察 yotta-logwatch」。
- 无功能 / 引擎 / 规则变更；版本 0.2.4 → 0.2.5（patch）三源同发。

## v0.2.4 (2026-08-27)

发布元数据修正（publish-metadata patch）：

- 尝试修复 ClawHub 展示名缺失中文：带 `--name 元察 yotta-logwatch` 三源重发；**但 `--name` 参数值未加引号、在 shell 中被拆分，实际未生效**，ClawHub 卡片展示名仍为裸 slug `yotta-logwatch`（详见 v0.2.5）。
- 无功能 / 引擎 / 规则变更；版本 0.2.3 → 0.2.4（patch）。


## v0.2.3 (2026-08-27)

发布洁净修正（republish patch）：

- v0.2.2 tarball 误含 `scripts/__pycache__/*.pyc`（测试后未清理，npm files 白名单下 .npmignore
  不生效）；0.2.3 清理后重发，内容与 0.2.2 一致（17 文件无 pyc），并 deprecate 0.2.2。
- 无功能 / 引擎 / 规则 / 文档变更；版本 0.2.2 → 0.2.3（patch）三源同发。

## v0.2.2 (2026-08-27)

文档修正（docs-only patch）：

- 从 README 双版「开发与校验」移除 `tools/validate-skill.py` 引用——该工具仅存在于 YottaSkills
  仓库（开发环境），不在发布技能包内；对外文档只保留技能包内可用的测试脚本。
- 无功能 / 引擎 / 规则变更；版本 0.2.1 → 0.2.2（patch）三源同发。

## v0.2.1 (2026-08-27)

文档中英对等补全（docs-only patch）：

- README.zh-CN.md 补齐「与 AI 智能体配合使用 / 检测规则一览 / 边界（安全红线）/ 开发与校验 /
  更新日志 / 许可」章节，与 README.md（英文门面）内容对等，中英双版章节结构一致。
- 无功能 / 引擎 / 规则变更；版本 0.2.0 → 0.2.1（patch）三源同发。

## v0.2.0 (2026-08-27)

新增 Windows 事件日志检测（winevt 类）+ 分析规范五块落地：

- **新日志类 winevt**：解析 Windows 事件日志（Security / System），支持 key=value、wevtutil 文本、
  XML 单行三种导出形态；嗅探标记 EventID= / ProviderName= / LogName= / EventRecordID= /
  Microsoft-Windows-Security-Auditing / Security ID / <Event 等；Event 4104/4103 脚本块记录仍走
  powershell 检测。
- **winevt 检测**：4625 登录失败聚合（爆破 / 撞库，复用 --max-fail / --window）/ 4624 异常·管理员·RDP
  登录 / 4720 账户创建 / 4726 账户删除 / 4740 账户锁定 / 4732·4728 组成员添加（管理员组 → high）/
  1102 安全日志清空（critical）/ 4688 可疑进程创建（LOLBin / 编码命令 / 凭据窃取等特征分级）/
  7045 新服务安装 / 4698 计划任务创建。
- **分析规范五块**：新增 references/analysis-spec.md（判型 / 字段提取 / 风险判定 / 分析流程 SOP /
  输出报告规范）与 references/windows-event-rules.md（EventID 语义与规则表，对照微软 Security
  Auditing 与 Sigma 社区惯例）；SKILL.md 检测规则一览与参考文档同步。
- **CLI / 输出**：--type 增加 winevt；文本 / Markdown 报告显示 EventID / 提供方 / 工作站。
- **测试**：66 项全绿（42 原 + 24 新增 winevt 嗅探 / 解析 / 检测 / 管线 / 输出 / CLI）。
- **版本**：0.1.0 → 0.2.0（新功能 minor），SKILL frontmatter / 引擎 VERSION / package.json 对齐。

## v0.1.0 (2026-08-27)

YottaMeta 自有实现首版（安全日志分析方向参考开源社区 detection-engineering / logging-monitoring 类技能思路，已完全重写，零依赖）：

- **零依赖自研引擎**（scripts/yotta_logwatch.py，Python 3.8+ 标准库）：解析 auth/secure、Web 访问日志（common/combined）、PowerShell 脚本块日志；类型自动嗅探；只读本地、离线检测。
- **auth 检测**：失败登录聚合 / 同源爆破（--max-fail）/ 时间窗内多账号撞库 / 异常登录（失败后成功）/ root 直登 / sudo 提权与越权（not in sudoers）。
- **web 检测**：404 洪峰（--404-threshold）/ 扫描器探测特征 / webshell 上传·访问轨迹 / 路径遍历 / SQL 注入 / 可疑 User-Agent。
- **powershell 检测**：编码命令 / 下载执行 / 反射加载 / AMSI 绕过 / 混淆启发式。
- **输出**：文本 / JSON（stdout 纯净）/ Markdown 报告；时间线 + 命中规则中文说明 + 复核建议。
- **CLI**：scan 子命令（--path / --recursive / --stdin / --type / --format / --json / --report / --output / --min-severity / --max-fail / --window / --404-threshold）；--version。
- **测试**：scripts/test_yotta_logwatch.py 42 项全绿（时间 / 嗅探 / 三类解析 / 三类检测 / 管线 / 输出 / CLI 退出码 0/1/4）。
- **文档**：SKILL.md / README.md（英文门面，GitHub/npm/ClawHub 首页）/ README.zh-CN.md（中文完整主文档）/ references（auth-log-rules / web-log-rules / powershell-log-rules）/ assets/banner.png。
- **边界**：只读本地日志；不联网、不主动扫描、不修改任何其内容；不提供利用细节。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明。
