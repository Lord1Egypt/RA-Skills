# Changelog

## v0.4.5 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v0.4.4 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.4.3 (2026-10-02)

- 分发副本 frontmatter 修复：`description` 改为单引号 YAML 标量，修复严格 YAML 解析器（官方 `skills` CLI）跳过本技能的问题；生成器同步新增 fail-closed 校验与回归测试。

## v0.4.2 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.4.1 (2026-09-17)

**装前扫描误报修复**：把 R7 中的下载即执行示例改为不含可执行命令的中性描述，元信 / 元安全不再把文档示例判为 critical。

## v0.4.0 (2026-09-08)

**评测驱动完善**：新增 FAQ 与复杂场景走查，安装器错误处理与测试补齐。

- 新增 references/faq.md 与 references/walkthroughs.md。
- 安装器支持 --help、参数校验、统一退出码与人话错误提示。
- 新增安装器测试，覆盖未知智能体、缺参、成功安装与产物形态。

# 更新日志

## v0.3.4 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-code-quality --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-code-quality.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.3.4。
- 无功能变更（仅文档与版本同步）。

## v0.3.3 (2026-08-28)

中英双语 README 对齐：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 工作流程 / 风险矩阵 / 目录结构 / 安装 / 使用 / 升级卸载 / FAQ / 来源与许可全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，顶部加语言切换链接。
- **新增 NOTICE + .npmignore**：对齐 YottaMeta 技能家族标准（品牌声明 + npm 打包排除）。
- **package.json**：files 加 README.zh-CN.md；版本 0.3.2 → 0.3.3。
- 版本对齐：package.json / SKILL frontmatter / CHANGELOG / 文档。
- 边界（B 方案）：references / 测试注释不翻译；SKILL 触发描述保持中文。

## 历史版本

- **v0.3.2 (2026-08-27)**：banner 标题改「元质代码质量守护」对齐元字辈功能后缀。
- **v0.3.1 (2026-08-27)**：中文名定稿元质 + banner 统一。
- **v0.3.0 (2026-08-27)**：更名 yotta-code-quality（原 code-quality-guard 家族对齐）。
- **v0.2.5**：README risk matrix canonical 修正 + 做厚介绍 + 补 history 配置口径。
- **v0.2.4**：README 顶部加 hero banner + 可点击徽章行；banner 入 assets/。
- **v0.2.3**：install 自动检测/PROJECT_DIRS 兜底分支补齐 17 类规范目录。
- **v0.2.2**：--list 与 README 方式三一致；去除环境变量真实路径显示。
- **v0.2.1**：--list 不再解析本机真实路径，改显示通用默认目录。
- **v0.2.0**：扩充智能体表支持国内 Trae/Qwen/Comate/CodeBuddy/Kimi。
- **v0.1.7**：README 措辞规范（.agents 通用约定中性表述）。
- **v0.1.6**：方式三简化——不确定目录交给用户。
- **v0.1.5 / v0.1.4**：--dir 自定义目录安装说明。
- **v0.1.3**：新增 npx 一行安装（bin 跨平台安装器）。
- **v0.1.2**：安装说明重构为三种方式（npm 推荐 / install.sh / 手动复制）。
