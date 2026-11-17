# Changelog

## v0.1.7 (2026-11-05)

- README 去硬编码版本；补使用范围与法律红线声明；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v0.1.6 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.1.5 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.1.4 (2026-09-18)

- JSON 输出新增 `scannedFiles`，显式列出实际读取的 package manifest / lock 文件；`files` 继续只表示产生发现的文件，消除 `files: []` 被误读成“未读取锁文件”的歧义。
- 统一 stdout / stderr UTF-8 编码，并补程序化捕获回归；补充自洽 yarn 夹具与缺失条目 high finding 回归。

## v0.1.3 (2026-09-17)

- npm 生态新增 `yarn.lock` / `pnpm-lock.yaml` / `bun.lock` 基础解析，锁文件存在时不再误报 `missing_lockfile`；`bun.lockb` 明确标记 `lockfile_parse_unsupported`，不做不可靠的二进制猜测。
- Python 生态新增 `uv.lock` 识别与基础一致性校验；`pyproject.toml` 无锁文件提示统一覆盖 `poetry.lock` / `uv.lock`。
- 新增 5 项锁文件格式回归；版本对齐到 `0.1.3`。

## v0.1.2 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-chain --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-chain.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.2。
- 无功能变更（仅文档与版本同步）。

## 0.1.1 (2026-08-27)

- 修复：README 安装方式统一为三方式（方式一 npx `-g` / `--dir` 指定目录，方式二 install.sh（`--agent` 仅示例用），方式三手动复制+目录表），删除 npx 固定 `--agent codex` 的写法；README 中英双版同步。
- 对齐：package.json / SKILL.md / CHANGELOG / README / references/rules.md 的版本锚点统一到 v0.1.1；引擎 `version` 输出与测试断言同步。
- 引擎无功能变更，测试保持 52/52。

## 0.1.0 (2026-08-27)

- 初始版本：零依赖供应链依赖校验引擎（Python 3.8+ 标准库，纯本地离线）。
- 生态：npm（package.json + package-lock v1/v2/v3 + npm-shrinkwrap + .npmrc 作用域仓库）、
  Python（requirements*.txt + pyproject.toml（PEP 621 / poetry）+ poetry.lock + Pipfile / Pipfile.lock）、
  Maven（pom.xml 基础：未固定版本 / SNAPSHOT / 可疑仓库 URL）。
- 检测：
  - 依赖混淆：scope 私有仓库配置 vs 实际解析仓库、同一包多仓库混合、可疑仓库 URL（http / IP / localhost）、
    pip extra-index 公共回退、poetry secondary 源、Pipfile 公私源混配；
  - lockfile 一致性：清单条目缺失 / 版本范围不满足（npm semver + PEP 440）/ 根信息不一致 /
    悬空引用 / 缺 integrity / 同版本多来源冲突；
  - 卫生：缺失锁文件 / 未固定版本（* / latest）/ Maven SNAPSHOT；
  - typo-squat：依赖名与知名 npm / PyPI 包编辑距离 ≤ 2 提示。
- SBOM-lite：CycloneDX 1.5 子集 JSON（components + dependencies + purl，scope / direct / resolved / integrity）。
- 输出：text / JSON / CSV；scan 退出码 0（干净）/ 1（有发现）/ 4（错误），--gate 可调 CI 闸门。
- 测试：52/52 全绿。
