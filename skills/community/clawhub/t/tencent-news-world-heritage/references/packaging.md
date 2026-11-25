# 打包自检与沙箱准备

## 生成交付包

在仓库根目录执行 `pnpm run zip <skill-name>` 和 `pnpm run zip:test <skill-name>`。源码 frontmatter 声明 `shared_resources: ["tencent-news-cli"]`，并在业务流程前链接 `references/cli-environment.md`；无需修改 Skill 名单。打包器自动补齐共享脚本、环境、安装、更新和 Key 指南；未知资源、遗漏声明/入口、共享文件的本地副本和失效的包内 Markdown 链接会导致打包失败。

ZIP 根目录包含 `SKILL.md`、`_skillhub_meta.json`、`scripts/` 和 `references/`。打包在暂存目录完成，保留展示字段和 examples，过滤安装缓存并重新生成元数据，不修改源码。不要直接把尚未补齐资源的源码目录当作交付包。test 包名称和元数据 slug 带 `-test`，安装与 Key 页面 URL 一并切换；正式和测试环境使用各自的 CLI 构建及凭证，不混用渠道。

## 解压后检查

在包含 `SKILL.md` 的目录执行：

```sh
sh scripts/run-cli.sh
sh scripts/run-cli.sh --help
sh scripts/cli-state.sh --help
sh scripts/cli-state.sh status
```

Windows 使用 `powershell` 与对应 `.ps1`。前三条无需 CLI/Key，应显示本地帮助并退出 0；最后一条输出当前真实环境诊断，必须检查 `success`、`status` 和 `error.code`。保留当前账号、PATH、HOME、安装目录和凭证上下文，不因为解压而清空环境。Key 误报按 [CLI 环境与失败处理](cli-environment.md) 恢复。

## 新增、更新和提交前验证

1. 运行打包与共享运行时回归：`pnpm --filter @qqnews/agent-skills test`。共享资源变更须覆盖所有接入 Skill 的正式包和测试包；无 CLI 的 Skill 不应被注入 CLI 资源。
2. 用独立测试夹具覆盖缺少 CLI、缺少 Key、鉴权失败、正常状态和真实退出码；不要通过清空实际业务环境来制造失败。验证本地帮助无需依赖、诊断 JSON 脱敏、已有 shell 配置可恢复，以及失败不被解释成业务结果。
3. 在实际沙箱验证 Shell/PowerShell、下载服务 `mat1.gtimg.com` 和业务服务可用；预装 CLI 或允许按 [安装指南](installation-guide.md) 安装。由凭证持有人按 [配置指南](env-setup-guide.md) 在沙箱运行账号配置对应渠道的 Key，不把真实 Key 放入包、示例或报告。
4. 状态就绪后读取当前 CLI 帮助，按目标 Skill 对已确认 examples 执行真实业务回归；保留实际返回，不预置答案。共享环境指引通过后仍需验证各能力的成功输出规则。
5. 平台不允许安装、配置凭证或联网时，明确未执行项并确认平台支持方式；帮助、诊断和打包检查只能证明对应环节。只有取得真实业务返回及平台复审结果后，才能分别宣称通过相应验证。
