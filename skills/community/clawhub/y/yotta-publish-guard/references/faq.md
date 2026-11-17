# 元守常见问题

## 速查索引

- **校验**：check BLOCKED · versions 不一致 · pack 报 pyc
- **发布**：publish 是 dry-run 吗 · --force 什么时候用 · 网络不可用
- **归属**：非 YottaMeta 怎么配置 · Windows 平台差异
- **安装**：装到哪 · 与元造/元信分工

---

## 1. `check` 返回 BLOCKED 怎么办？

先看报告里的 ERROR 项，按提示逐条修：SKILL 字段缺失、占位符、围栏不平衡、版本不一致等。WARN 通常不阻断，但建议按列表自查。修完后重跑 `check`，不要用 `--force` 绕过未修的问题。

## 2. `versions` 报 package/SKILL/CHANGELOG/CLI 不一致？

按报告显示的五个位置逐一对齐：package.json、SKILL.md frontmatter、SKILL 正文版本行（如有）、CHANGELOG 顶部、CLI `VERSION` 常量。版本号必须完全一致，不要只在 README 里改。

## 3. `pack` 报包内混入 pyc / __pycache__？

删掉 `__pycache__` 和 `*.pyc`（发布规范要求零 pyc），确认 package.json `files` 含 `!**/__pycache__`、`!**/*.pyc`；也检查目录里是否残留 .tgz、.bak、临时文件。修完重跑 `pack`。

## 4. `names` 网络失败怎么处理？

失败会明确降级为“需手动查重”，不会伪造结果。此时按提示到 npm / GitHub / ClawHub 手动确认名称；跳过这一步直接发布可能撞名。

## 5. `publish` 会不会直接发布？

默认是 dry-run，只打印发布计划。确认计划后用 `--exec` 执行；`--force` 只在显式授权跳过推送闸门时使用，且应先确认所有校验已通过。

## 6. 只推 GitHub，不做 npm/ClawHub 可以吗？

可以。用 `publish --github-only`，校验档会自动切到 github 模式，不强制要求 npm 发布件；需要哪几个渠道用 `--channels github,npm` 等显式指定。

## 7. 非 YottaMeta 组织怎么用？

通过 CLI 参数或环境变量配置自己的 npm scope / GitHub org / ClawHub owner / topic 后，check/pack/names/publish 会按新归属执行。不持有、不读取任何平台凭据。

## 8. Windows 和 Linux 行为一样吗？

核心校验相同；Windows 下调用 .cmd/.bat 子进程会经 cmd.exe，npm 命令使用可写 --cache 目录。命令本身零依赖 Python 3.8+，不需要额外安装扫描器。

## 9. 和元造 yotta-skill-creator 怎么配合？

元造负责“造”：生成合规脚手架；元守负责“守”：发布前 check/pack/versions/names/publish。推荐链路是 元造 create → 人工开发 → 元守 全量校验 → 发布。

## 10. 安装不上/没识别怎么办？

用 `npx -y @yottameta/yotta-publish-guard --agent <名称>` 或 `--dir <技能目录>`；未收录智能体用 `--dir`。装完在新会话中调用；发布命令需要本机已装 gh/npm/clawhub 凭据，校验本身不需要网络。

## 11. 元守和元信怎么分工？

元信是对“要安装的其它技能/包”做装前确定性安全扫描并出 verdict；元守是对“自己准备发布的技能包”做发布就绪校验与发布命令封装。方向相反但可串联：先元信审别人，再元守发自己。

## 12. 发布命令封装和直接跑 gh/npm 有什么区别？

元守把已踩过的坑固化成顺序与检查：git 代理/描述/topic、ClawHub --name、分类 slug、npm cache、传播延迟核验等。照命令走能避免遗漏，但最终发布决策仍由人确认。
