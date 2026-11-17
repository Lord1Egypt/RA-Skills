---
name: yotta-publish-guard
slug: yotta-publish-guard
version: 0.4.5
displayName: 元守·发布前守门
summary: 发布前守门：聚合安全校验、npm 包体检、版本五件对齐、名称查重，一键检查发布就绪度。
description: '元守 —— 通用发布前守门（默认 YottaMeta 归属，可自定义为任意发布组织）：check 聚合校验（full / github / self 三档模式，可聚合元安/元审/元信 verdict）+ pack（npm pack 无 pyc / 关键文件在包内）+ versions（package/SKILL frontmatter/SKILL 正文版本行/CHANGELOG/CLI 五件对齐）+ names（npm/GitHub/ClawHub 三通道查重）+ publish 命令封装（--channels / --github-only 渠道可选，默认 dry-run，--exec 执行，--force 显式跳过推送闸门；归属经 CLI 参数或环境变量自定义，缺省 YottaMeta 开箱即用）。触发：发布技能前、改完技能准备推 GitHub / npm / ClawHub 时、想批量核对版本或查重名称时；或用户说 元守 / 发布守门 / 发布前检查 / publish-guard / 推前检查 / 查重 / 版本对齐 等。边界（Do NOT trigger）：不替用户做发布决策与人工审查；网络不可用时只降级提示、不伪造结果；不做技能内容开发（脚手架用元造 yotta-skill-creator，正文需人工开发）；不持有、不读取任何平台凭据（发布鉴权由各平台 CLI 按使用者本机配置完成）。'
tags: [发布检查, 版本校验, 包体校验, 名称查重, publish, release]
category: dev-programming
license: MIT
homepage: https://github.com/YottaMeta/yotta-publish-guard
metadata:
  zh_name: 元守
---
# 元守（yotta-publish-guard）

**通用发布前守门**：把「发布规范 + 已踩过的坑」固化成确定性 CLI——`check` 聚合校验、
`pack` 打包检查、`versions` 版本五件对齐、`names` 名称三通道查重、`publish` 发布命令封装，
任何开发者 / 团队照流程走不踩坑。**零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用。**
默认归属 YottaMeta 开箱即用；其他发布组织按自己的归属配置即可（不持有、不读取任何平台凭据）。

```bash
python3 scripts/yotta_publish_guard.py check ./yotta-my-tool
```

## 何时使用

- 新技能发布前，把校验 / 版本对齐 / 查重 / 打包检查 / 发布命令一次性跑完；
- 仅发布到 GitHub（npm / ClawHub 不启用），或只想给自用技能做本体检查；
- 改完既有技能准备升版本、重新三源发布前的复核。

**Do NOT trigger**：
- 不替用户做发布决策与最终人工审查——报告与命令只是辅助，是否发布由用户决定；
- 网络不可用时只降级为「需手动查重」提示，不伪造查重结果；
- 不做技能内容开发——造脚手架用元造（yotta-skill-creator），正文 / 脚本需人工开发。

## 快速使用

```bash
# 1) 发布就绪检查（full 档：完整发布件；可聚合元安 / 元审 / 元信 verdict）
python3 scripts/yotta_publish_guard.py check ./yotta-my-tool
python3 scripts/yotta_publish_guard.py check ./yotta-my-tool --with-audit --with-vetter --with-verify
python3 scripts/yotta_publish_guard.py check ./yotta-private --self-use

# 2) 打包检查 / 版本五件对齐 / 名称三通道查重
python3 scripts/yotta_publish_guard.py pack ./yotta-my-tool
python3 scripts/yotta_publish_guard.py versions ./yotta-my-tool
python3 scripts/yotta_publish_guard.py names ./yotta-my-tool

# 3) 发布命令封装（默认 dry-run 打印计划；--exec 直接执行；--force 显式跳过闸门）
python3 scripts/yotta_publish_guard.py publish ./yotta-my-tool
python3 scripts/yotta_publish_guard.py publish ./yotta-my-tool --github-only
python3 scripts/yotta_publish_guard.py publish ./yotta-my-tool --channels github,npm --exec
```

## 宿主 hook 声明

`skill-manifest.json` 声明 `before_publish` / `publish_gate`。wrapper 已注册时，发布门禁失败会阻断；
wrapper 未注册时按 `fallback: wrapper` 降级为 `explicit-unverified`，不会被误报为已验证。

## 三档校验模式

| 模式 | 触发方式 | 要求 |
|---|---|---|
| full | `check` 默认 / `publish` 全渠道 | SKILL.md + LICENSE + README 中英四方式 + package.json + CHANGELOG（建议）+ 版本五件 + 无占位符 + 围栏 |
| github | `publish --github-only` | SKILL.md + LICENSE + README.md（英文）；不强制 package.json / 中英 README / publish.yml 等 npm 发布件 |
| self | `check --self-use` | 只查技能本体：SKILL.md + frontmatter + 无占位符 + 围栏（安全家族加 Defense Triple） |

## 子命令速览

- **check**：内置校验（三档模式）+ 可选聚合元安 / 元审 / 元信 verdict（未安装自动降级提示），输出发布就绪报告。
- **pack**：`npm pack --dry-run` 检查——包内无 pyc / __pycache__、关键文件（SKILL / LICENSE / README 中英）在包内；npm 不可用本地回退列举。
- **versions**：package.json / SKILL.md / CHANGELOG 顶部 / CLI `VERSION` 常量 / SKILL 正文版本行（如有）五件对齐。
- **names**：npm view / gh repo view / clawhub search 三通道查重；网络失败降级为手动查重提示。
- **publish**：生成发布命令计划（git init/add/commit → gh repo create --description + topic → npm publish → clawhub publish），归属（npm scope / GitHub org / ClawHub owner / topic）按配置生成，默认 YottaMeta；默认 dry-run，`--exec` 按序执行，`--force` 显式跳过推送闸门。

## 归属配置（可自定义）

本技能默认校验 / 发布命令面向 YottaMeta 归属（npm `@yottameta` / GitHub `YottaMeta` / ClawHub `yottameta` / topic `yottaskills`），开箱即用。
其他发布组织可将其改为自己的归属（npm scope / GitHub org / ClawHub owner / topic），改后校验、查重、发布命令全部按新归属生成。
归属通过 CLI 参数或环境变量指定；使用本技能的 AI 会按需引导配置。
本技能不持有、不读取任何平台凭据——npm / gh / clawhub 的发布鉴权由各平台 CLI 按使用者本机配置完成。

## 发布渠道（可选）

`publish --channels github,npm,clawhub`（缺省全渠道）或 `--github-only`——npm / ClawHub
都不是必选，只推 GitHub 时闸门用 github 档。详见 references/publish-flow.md。

## 推送闸门

`publish` 前先跑内置校验：有 ERROR 默认阻断（退出码 2）；`--force` 仅显式授权后可用。

## 退出码

| 子命令 | 0 | 1 | 2 | 其它 |
|---|---|---|---|---|
| check | READY | READY（含 WARN 建议） | BLOCKED | 4 致命异常 |
| pack | PASS | — | 包内 pyc 或关键文件缺失 | 4 致命异常 |
| versions | PASS | — | 缺失 / 不一致 | 4 致命异常 |
| names | 三通道全部空闲 | 有渠道无法确认（需手动查重） | 有 TAKEN | 4 致命异常 |
| publish | dry-run 或执行成功 | — | 闸门阻断 / 渠道参数错误 | 执行中失败命令的退出码；4 致命异常 |

## 行为锚点

1. **推送闸门默认阻断**：未通过校验不得发布，`--force` 仅显式授权后可用。
2. **网络命令优雅降级**：npm / gh / clawhub 不可用时输出「需手动查重」提示，不伪造结果。
3. **只读**：不修改被测技能目录（除 npm pack 临时产物）；git init / commit 仅在 `--exec` 时执行。
4. **平台适配**：Windows 下 .cmd/.bat 子进程经 cmd.exe 执行；npm 命令使用可写 --cache 目录。

## 与工坊 / 工具链分工

- 元守（本技能）= **守**：发布前全量校验 + 发布命令封装；
- 元造 yotta-skill-creator = **造**：生成合规脚手架（元守的 `check` 对元造脚手架直接 READY）；
- 仓库 `tools/validate-skill.py` 的规则 = 元守内置校验的自包含副本来源（发布包内带实现副本，
  不依赖仓库 tools/）。
- 推荐链路：**元造 create → 人工开发 → 元守 check → pack → versions → names → publish**。

## 渐进披露

- references/check-items.md —— 校验项明细（三档模式 / 口吻黑名单 / 四方式安装 / 版本五件 / pack / names）
- references/publish-flow.md —— 三源发布流程与已踩坑清单（git 代理 / ClawHub --name / categories / gh --description / npm cache / 传播延迟）
- references/tutorial.md —— 中文教程（check → pack → versions → names → publish 全流程）
- references/faq.md —— 常见问题速查（BLOCKED / 版本不一致 / pyc / 网络降级 / 安装）

## 常见问题（速查）

check 被阻断、versions/pack 报错、网络查重降级、publish 不敢直接跑时，先看 references/faq.md。
