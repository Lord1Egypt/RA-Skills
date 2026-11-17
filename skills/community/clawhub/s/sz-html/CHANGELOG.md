# CHANGELOG

本文件记录 sz-html 的版本轨迹与改动。

## [1.5.1] - 2026-10-17

- 修复 `szhtml_tools/style_preview.py` 的 HTML 转义漏洞：`--title`/`--tone`/`--scene`/`--purpose` 及风格资产文本字段未经转义直接写入输出，可注入标签与事件属性（XSS）
- 新增 `LICENSE.md` 专有许可具体条款（授权范围 / 禁止事项 / 免责声明 / 商用授权），README 许可证章节改为指向该文件

## [1.5.0] - 2026-10-17

- 按 REA（Reverse Engineer Anything）拆解报告的 skill 工程范式对齐（8 大范式 + 10 条可移植做法）
- 版本号单一来源：build.py 新增版本一致性校验（SKILL.md / manifest / CHANGELOG 三处不一致即打包失败）；修复 README 版本 badge 落后于 1.4.0
- 内容证据分级（观察 / 推断 / 未知）：quality_gate.md 新增内容事实溯源三级分级，硬事实禁止「推断」后写精确值
- SKILL.md 新增「按需读取路由」表（Read only the relevant guide）

## [1.4.0] - 2026-10-17

- 新增「风格可视化选型」：选型环节生成候选风格对比页（用真实色值各画一小段演示文稿小样），让客户「看脸选」而非凭编号猜
- 新增 `assets/style-system.json`（49 风格机器可读 token）+ `szhtml_tools/style_preview.py`（色系中文描述 + 候选差异 + 对比页生成）
- SKILL.md 新增「选型呈现铁律」（中文名打头、色系说人话、备选写差异、必附对比页）
- anti_patterns 新增「选型只给编号」反模式

## [1.3.0] - 2026-10-15

- 新增 `README.md`、`CHANGELOG.md`
- 新增 `rules/anti_patterns.md` 反模式清单
- SKILL.md 新增「触发契约」章节（何时调用 / 何时不要调用）
- S6 质量审核补写阻断打回迭代上限（同阻断 3 次 → 降级交付）

## [1.2.0] - 2026-10-15

- 底部新增圆点跳页：可点击圆点 + 当前页胶囊高亮 + 页数自适应
- 同步更新 SKILL.md / html_guide.md / skeleton_base.md / slide_patterns.md / quality_gate.md

## [1.1.0] - 2026-10-15

- 流程升级为「PPT 式」：新增 S2 大纲生成（先出章节结构 + 页数规划，再选型）
- 选型升级为「风格 + 页数」双定
- 新增左右翻页 + 底部页码总数与翻页进度条
- 更新 manifest 状态机、追问问题库

## [1.0.0] - 2026-10-15

- 初始版本：从「风格化待办工作台」提炼 49 种前端页面风格资产
- 三级渐进式加载（L0 选型目录 / L1 族索引 / L2 风格正文）
- S0-S6 阶段流程 + 五维质量审核 + 修订模式
- build.py 打包脚本 + manifest
