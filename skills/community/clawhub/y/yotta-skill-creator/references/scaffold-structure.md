# 脚手架目录结构说明

> 配套技能：元造 yotta-skill-creator v0.1.4
> 完整模式生成的文件清单与用途；自用模式对照见文末。

## 完整模式（默认）

| 路径 | 用途 |
|---|---|
| SKILL.md | 技能入口：frontmatter（name / version / description / license / metadata.zh_name）+ 正文骨架（一句话 / 触发与边界 / 核心流程 / 渐进披露） |
| README.md | 英文门面：四方式安装 + 徽章 + 语言切换标识 |
| README.zh-CN.md | 中文全档：四方式安装 |
| package.json | npm 发布：name=@yottameta/<slug>、files 字段、bin（--skip-installer 时去掉 bin） |
| CHANGELOG.md | 版本历史（顶部 `## v0.1.0`） |
| LICENSE | MIT 许可 |
| NOTICE | 品牌与归属声明 |
| install.sh | 多智能体一键安装脚本（bash） |
| bin/install.js | npx 安装器（node，走 npm 源） |
| .gitignore | git 忽略（__pycache__ 等） |
| .npmignore | npm 忽略 |
| .github/workflows/publish.yml | GitHub Actions 发布工作流（OIDC 可信发布） |
| references/README.md | 渐进披露占位：开发时新增 *.md 并在 SKILL.md 登记 |
| assets/README.md | banner 等素材占位（--no-banner 跳过） |
| scripts/<cli_module>.py | CLI 骨架（--with-cli 时生成，可 `--version` 运行） |
| scripts/test_<cli_module>.py | CLI 测试骨架（--with-cli 时生成） |

## 占位符替换

`create` 一次性替换的模板变量：`skill_name` / `zh_name` / `cli_module` / `description` /
`summary` / `year`；`scripts/` 文件名中的 `<cli_module>` 同步重命名。
模板内的 `SKILL.md.tmpl` / `.gitignore.tmpl` / `.npmignore.tmpl` 在生成目录分别
映射为标准文件名 `SKILL.md` / `.gitignore` / `.npmignore`。
生成后不允许存在残留双花括号占位符（结构自检会拦截）。

## 自用模式（--self-use）

只生成 SKILL.md / references/（加 --with-cli 时含 scripts/ 与测试）；README 中英 /
package / CHANGELOG / LICENSE / NOTICE / install.sh / bin / publish.yml / assets 一律不生成。

## 与发布件的关系

完整模式脚手架即 S4 发布件的基础：README 中英、package.json、CHANGELOG、LICENSE、NOTICE、
install.sh、bin、publish.yml 已按发布规范生成；发布前用元守（publish-guard）`check` 全档复核，
再 `pack` / `versions` / `names` / `publish`。
