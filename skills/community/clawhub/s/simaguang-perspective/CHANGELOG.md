# Changelog


## 0.4.7 (2026-10-28)

**隐私清除 + 断链显性化：技能包换一台别人的机器也能跑。**

- 新增 `scripts/project_paths.py`：外部项目根三级解析（`SIMAGUANG_PROJECT_DIR` → 逐级相对探测 → 友好报错），`pdftotext` 三级解析（env → PATH → codex runtime → 安装指引）。所有原先写死作者家目录的脚本改走它。
- `prepare_input.py`：PDFTOTEXT 常量删除，改 `find_pdftotext()`；缺 poppler 时打印 brew/apt/choco 安装指引并以 rc=3 退出，txt/md/docx/epub/mobi 不受影响。
- `build_handoff.py`：修 `parents[3]` 路径 Bug（原来指向 `~/.workbuddy/skills`）；输出改 `--out` → 项目根/学习记录/ → 包内 `handoff/`；无项目时三节数据标 `[no project dir]` 并给设置指引。
- `check_distillation_quality.py`、`extract_routing_feedback.py`、`audit_skill_index.py`、`build_skill_index.py`、`test_routing_coverage.py`：同上改用 `project_paths`，解析不到项目根时打印指引退出（rc=2），不再指向作者本机目录。
- `test_routing_coverage.py`：报告输出改 `--out`/项目根/包内 `handoff/`，新增 `--quiet`；报告标题日期改自动取当天，不再写死 2026-08-20。
- `fetch-celebrity.py`：状态目录从 Agent 全局配置目录改到 `~/.cache/simaguang-celebrity/`（可用 `SIMAGUANG_STATE_DIR` 覆盖）；SKILL.md 注明图片经 `images.weserv.nl` 代理。
- references 去本机路径：`名人分析卡-Elon-Musk.md`、`冰鉴分析-Elon-Musk.md` 图片路径改 `~/.cache/...`；`溯源标注协议.md` 示例改 `<项目根>` 占位符 + 解析说明；`实时数据协议.md` 的 runtime python 绝对路径改 `python3`。
- `references/技能路由索引.md`：头部加「本地扩展索引，技能包独立可用」说明块 + 包内 58 份协议清单 + 有/无外部项目的两种用法；`build_skill_index.py` 同步生成该块。
- 新增 `references/optional-本地扩展.md`：承接原 SKILL.md「自我学习闭环」中依赖外部项目目录的部分，主 SKILL 改为三行自包含说明。
- `lint_cross_platform.py`：新增 `ABS_USER_PATH` 规则（macOS/Linux 用户目录前缀、Windows 用户目录前缀，命中即 ERROR，不享受平台分支豁免）；规则表改按名字索引；修掉 `cad-file-reader` 遗留文案与指向不存在脚本（platform_paths.py / safe_timeout.py / mem_guard.py）的 fix 建议。
- 发布卫生：删除 `scripts/_archived_onetime/`（7 个一次性脚本）与 `__pycache__`；manifest 按磁盘实际文件重建（scripts 28 / references 67），`description` 从残值 `>` 修正为 SKILL.md 正文摘要，补 `project_paths.py`、`scripts/generate_work_product.cmd`、`scripts/prepare_input.cmd`。
- `self_test.py` 从 19 项扩到 38 项：新增隐私扫描（绝对路径/明文密钥 0 命中）、发布卫生（无 pycache/pyc/一次性归档）、SKILL.md→references 断链检查、manifest 文件存在性、版本单源一致、3 类模板冒烟渲染、`build_handoff --out` 降级冒烟。

## 0.4.6 (2026-10-21)
- 三平台对齐（cross-platform + i18n overseas）：README.en.md、`--lang en|zh` 主入口、i18n.py、CFI 三平台 workflow 全绿。
- 不改变业务算法/中文模板；平台专用调整只改发布副本。

# CHANGELOG

## 0.4.3（2026-10-18）

- 新增 `references/实时与历史报道素材索引.md`、`references/报道式决策案例库.md`、`references/跨源交叉核验协议.md`，登记 5 条历史 + 6 条实时脱敏公开素材，收录 7 个报道式决策案例。
- 路由测试提示词从 303 条扩到 311 条，新增 8 条报道式决策素材触发用例。
- 版本统一本机 / SkillHub / GitHub / ClawHub：0.4.3。
- 自检结果：`routing_accuracy_status=OK`（311 条 missed=0）、`INTEGRATION_OK`、发布合规扫描 0 命中。

## 0.4.2（2026-10-11）

- 新增 `references/使用边界与复核清单.md`：历史/预测/易学内容仅供结构参考，不替代专业判断。
- `SKILL.md` / `SKILL.lite.md` 版本统一 0.4.2。
- 自检：303 条路由提示词 `routing_accuracy_status=OK`。
