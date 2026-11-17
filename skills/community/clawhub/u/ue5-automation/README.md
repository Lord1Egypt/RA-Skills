# UE5 蓝图自动化（SkillHub 包）

这是 `ue5-automation` 的 SkillHub 轻量技能包，只包含**操作规范与参考文档**；
运行包（UE 插件 + bridge）单独分发。

## 包内容

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 技能入口：定位、工作流、硬规则、安全边界 |
| `references/INSTALL-WINDOWS.md` | 安装、连接、客户端配置、自检 |
| `references/COMMANDS.md` | 按任务分组的命令目录 |
| `references/EXAMPLES.md` | 读图 / 写图 / 修编译 / 场景验证 / 撤销 / 多 Agent 示例 |
| `references/PITFALLS.md` | 已知陷阱 Top 20+（症状 → 根因 → 修复） |
| `references/TROUBLESHOOTING.md` | 常见故障排查 |
| `references/SECURITY.md` | 安全模型与授权边界 |
| `references/VERIFICATION.md` | 验证记录与已知边界 |

## 版本对应

| 项 | 版本 |
|---|---|
| Skill 包 | **6.5.10** |
| 运行包（插件 + bridge） | **6.5.4** |
| 适用引擎 | UE 5.1.x 开箱；5.8.x 预编译；5.2–5.7 需重编译 |

> 6.5.10 是 **ClawHub 发布用的元数据/曝光修订**，不改变运行时行为。安装、命令、
> 安全模型与 6.5.4 完全一致；正文沿用 6.5.9 的实机冒烟修正。

## 6.5.10 改了什么

- 英文优先摘要：`summary` / `description` 改为英文开头、中文补充，便于 ClawHub
  英文搜索和结果卡片阅读。
- 新增英文 `English summary` 段，说明适用/不适用场景。
- 总览图更新为 `SKILL v6.5.x · RUNTIME v6.5.4`，不再随小版本漂移。
- ClawHub 分类：**Development + Automation**（替代默认 Other）。
- topics 扩充：`unreal-engine-5`、`game-development`、`editor-automation`、
  `ai-agents`、`mcp-server`、`pie`、`windows`。
- frontmatter 增加 `icon`，指向已有的 UE5 图标。
- 6.5.9 的实机修正保留：搜索限制、L2 结构、bool 大小写、task_begin 时机、
  10048 双自启、pydantic 安装、`tools\install.bat` 路径。
- 6.5.8 的档位与参数修正保留：gateway **12** / core **18** / full **34**、
  gateway 补 `ue5_verify_behavior`、pin 示例补 `bp_path`、disconnect/delete 命名。
- 6.5.7/6.5.6/6.5.5 的曝光与结构改动保留。

## 安装

见 `references/INSTALL-WINDOWS.md`。最短路径：

1. 下载与运行包版本匹配的 portable 包：
   `https://github.com/miracle1814/ue5-automation/releases/tag/v6.5.4`
2. 解压后运行 `install.bat`，把项目 `.uproject` 拖进窗口。
3. 重启 UE 编辑器，Output Log 出现 `[ue5_bridge] [OK] 服务已在后台启动`。
4. MCP 连接 `http://127.0.0.1:8889/mcp`，请求头带 `X-Skill-Token`。
5. 调 `health`，确认 `bridge_loaded=true`。

## 企业合作 / Commercial

- **企业集成**：把 UE 蓝图自动化接进团队现有 Agent / CI / 资产管线。
- **版本适配**：UE 5.2–5.7 的 bridge 重编译与回归。
- **定制开发**：领域模板、批量迁移、审计/审批、私有工具链。
- **培训/支持**：团队上手、故障排查、交付验收。

联系方式：GitHub Issue 标题注明 `[Commercial]`，或通过
https://github.com/miracle1814 联系作者。

## 授权与商标

- 本项目原创代码：Apache-2.0；第三方组件与完整声明见仓库
  `THIRD_PARTY_NOTICES.md`。
- 截图/PIE 部分实现参考 UEBox / UnrealAgentLink（MIT），完整 MIT 文本随仓库与
  移植包分发。
- Unreal、Unreal Engine、UE 是 Epic Games, Inc. 的商标；本 Skill 与 Epic Games
  无隶属或背书关系。引擎头文件/二进制仍受 Epic EULA 约束。
- 本 Skill 不包含 Epic 美术资源、Logo、示例资产或市场内容。

## 相关链接

- 项目主页：https://github.com/miracle1814/ue5-automation
- 运行包发布：https://github.com/miracle1814/ue5-automation/releases
- 问题反馈：https://github.com/miracle1814/ue5-automation/issues
