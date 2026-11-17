# Changelog

## v0.1.7 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.1.6 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.1.5 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- `template/bin/install.js` / `template/install.sh` 升级为统一安装器单一真源。

## v0.1.4 (2026-10-01)

模板安装器同步顶层跳过修复。

- 背景：`template/bin/install.js`（生成新技能的安装器模板）仍按条目名逐层跳过 `package.json` / `bin`，生成的新技能若内嵌同名载荷，安装时会被丢掉。
- 修复：模板安装器与自身安装器（0.1.3 起的口径）对齐——只跳过安装包顶层同名条目，`template/` 内嵌套载荷保留。
- 回归：把模板安装器渲染到临时包并真实执行，断言顶层 `package.json` / `bin` 跳过、嵌套 `template/package.json` / `template/bin/install.js` 保留。

## v0.1.3 (2026-09-25)

安全修复：外部元数据白名单校验 + YAML 引号化 + 生成后回读。

- 背景：`--desc` / `--summary` / `--zh` 直接字符串替换进 SKILL.md frontmatter、package.json、README 与生成的 CLI 源码——含换行、`---` 或引号的输入可注入额外 frontmatter 字段或指令（ClawHub T09 High）。
- 修复：元数据统一走 `validate_meta_text()`（控制字符 / `---` / 引号 / 反斜杠 / 反引号 / 超长一律拒绝）、frontmatter 用 YAML 双引号转义写入、生成后 `verify_generated_frontmatter()` 回读校验（name / description 与入参一致、无额外顶层键）。
- 回归：新增 5 项注入用例，测试 30/30 通过。

## v0.1.2 (2026-09-14)

- 修复嵌套模板被宿主递归扫描导致的 YAML 解析告警：`template/SKILL.md` 改名为
  `template/SKILL.md.tmpl`，`render()` 在生成目录映射回标准 `SKILL.md`。
- 模板 `.gitignore` / `.npmignore` 改为 `.tmpl` 存储并在渲染时映射回标准文件名，
  避免 npm 默认排除规则导致安装后缺少完整脚手架文件。
- 官方安装器只跳过包顶层 `package.json` / `bin` / `node_modules` / `.git`，
  保留 `template/` 内的嵌套载荷。
- 新增回归：模板目录不得包含可被宿主发现的嵌套 `SKILL.md`；`SKILL.md.tmpl`
  必须渲染为生成技能的 `SKILL.md`。

## v0.1.1 (2026-09-13)

- 文档 hygiene 清理：移除历史公开文档中的内部表述，模板占位改为中性提示，版本同步 0.1.1。
- 发布工作流 `.github/workflows/publish.yml` 纳入版本库，标签推送可触发 GitHub Actions。
- 发布包排除测试脚本与 Python 缓存，避免 `scripts/test_*.py` / `__pycache__` / `.pyc` 进入 npm 包体。

## v0.1.0 (2026-08-29)

初始发布：

- 定位：元造 —— 端到端造技能脚手架（开源，工坊 / 质量与工程线）。输入 `yotta-<名称>` +
  中文名 + 描述，一键生成符合元阁发布规范的技能目录并做结构自检，通过才输出「脚手架合格」。
- CLI：零依赖（Python 3.8+ 标准库）yotta_skill_creator.py —— `create` 子命令：命名校验
  （yotta- 前缀 / 小写连字符 / 元X 规范 / 目标不重复）→ 内嵌模板（SKILL.md / README 中英四方式 /
  package.json / CHANGELOG / LICENSE / NOTICE / install.sh + bin/install.js / .gitignore /
  .npmignore / publish.yml / references / assets）→ 占位符替换 → 结构自检（frontmatter /
  版本四件 / README 四方式 / 无残留占位符 / 围栏配对）；退出码 0 / 2 / 4 / 130。
- 自用模式 --self-use：只生成技能本体（SKILL.md / references / 可选 CLI），不生成任何发布件；
  自检只查技能本体完整性。
- references：cli-reference.md（完整参数 / 命名规则 / 退出码 / 自用模式差异）+
  scaffold-structure.md（生成目录结构与文件用途）+ tutorial.md（中文教程）。
- 测试：20 用例（命名矩阵 / 自检项 / 自用模式 / 占位符替换 / 围栏）Python 3.8 + 3.13 双版本全绿。
- 文档：SKILL.md + README 中英双版 + 四方式安装（发布规范 §3.3.1）。
