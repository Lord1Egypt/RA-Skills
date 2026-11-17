# Changelog

## 0.9.36 · 2026-11-10 · S9 发布准备：版本收口

- 版本 patch bump；同步套件最低版本。s9 发布准备，未改算量逻辑。

## 0.9.35 · 2026-11-10 · 表格入口闸门 + input_channel 固化

- **`decor_qty.py` 接入入口闸门**：新增 `import entry_gate as eg`；`--input`/`--contract` 为 `.dwg/.dxf/.dwt` 直接退出 `23`；`--contract` 统一走 `eg.require_contract()`（无效 `22`、证据不足 `24`）。
- **表格链路保持可用**：不强制 reader/bus；无契约且无 `--allow-manual` 仍显式退出 `3`；`--check-deps` 改稳定码 `20/21`。
- **`input_channel=table` 固化**：JSON 输出、`provenance.json`、报告同时标注；报告写明「表格输入，不经 CAD 识图」。
- **测试修复**：`scripts/tests/test_decor_qty.py` 的运行块原来在文件中部，导致 3 个主入口用例从未执行；已移到文件末尾，并新增图纸 `23`、契约图纸 `23`、`input_channel=table` 用例。
- **文档修正**：SKILL.md 新增退出码表与固定提示，删除「强依赖底座 exit 1」的旧口径；`manifest.scripts` 登记 `scripts/entry_gate.py`。

## 0.9.34 · 2026-11-09 · 校验不再静默跳过 + 主入口闸门

- **`cad_measure_to_input.py`**：缺 reader/validator 时抛 `ValidationUnavailable`，默认 `--validate` exit 1 且不写输出 CSV；仅显式 `--no-validate` 跳过，输出 `validation=skipped` 并在行内标注。
- **`decor_qty.py` 主入口闸门**：无 `--contract` 且无 `--allow-manual` exit 3；`provenance=manual` 强制 `final_quantity=false`、`formal_ledger_eligible=false`。
- **新增**：`--check-deps`、`--contract`（仅溯源）、`provenance.json`、`run.json`、`site_handoff.json`（`specialty=finish`，缺坐标/重量如实标注）。
- **`ensure_base.sh`**：删除 `SKILL_NO_BASE=1` 静默降级（设置即报错 exit 1），默认版本 `0.34.1→0.41.0`，下载失败报错退出。
- **manifest 统一**：`requires.skills={cad-file-reader>=0.41.0, lis-skill-bus>=0.1.11}`，`entry_policy=contract-only`。

## 0.9.33 · 2026-11-09 · 常驻注入瘦身

- **description 精简**：技能目录注入的 description 压到 ≤45 字，保留原有触发词与「不做什么」边界；SKILL.md 正文与算法口径未变。

## 0.9.32 · 2026-11-08 · 技能层瘦身与发布完整性

- **SKILL.md 瘦身**：16,961 B → 10,035 B（-40.8%）。触发词、硬规则、能力边界保留在前置段；低频细则外移到 `references/`、`docs/`、`packs/`，按需加载，算法与业务口径不变。
- **发布完整性**：被引用文件随包存在、Python/bash/JSON 语法通过、技能自检 PASS；未实现的检查如实记 SKIP。
- **脱敏**：本机路径、真实项目名与公司资料引用替换为通用示例；平台专用入口只改发布副本。


## 0.9.28

- **修复（发布兼容）** SkillHub 分发包（zip）不保留文件权限，装完脚本全是 644，直接执行会 permission denied。现在 `scripts/setup.sh` 与各入口脚本（`runtime_env.sh` / `ensure_runtime.sh`）首次运行时幂等补回 `scripts/*.sh`、`scripts/*.py` 的可执行位，用户无需手动 chmod。
- **修复** `scripts/setup.sh` 里 `bash bash "$SKILL_DIR/scripts/ensure_base.sh"` 的重复 bash 会让安装第一步直接报 `bash: bash: No such file or directory`，已改为 `bash "...ensure_base.sh"`。
- **修复（自测误报）** `scripts/self_test.py` 对未随轻量包提交的开发期单测（`scripts/tests/test_*.py`）改为「存在则校验、缺失则 SKIP」，不再让 `SELF_TEST` 因缺件判失败；Windows 专属 `.cmd` 在非 Windows 平台跳过。

## 0.9.27

- **更新发布** 补 CHANGELOG 详细条目与 README.en 版本号；三端（Codex/WorkBuddy/发布仓库）同版本同内容再次校验通过。tujian-suanliang 的 manifest tests 仅保留真实存在的 `scripts/self_test.py`（完整 tests 见本机 shangwu-suanliang 商务版）。
- 算法、契约、权限、SKILL.md 正文与上一版无变化。

## 0.9.26

- **授权与保留** 新增「授权与保留」段落：作者 lis 声明本技能可商用/可再分发/可对外授权，商用前按双许可说明确认是否需联系作者申报。
- **脱敏（发布合规）** rules 中的公司内部来源字段由「公司知识库/…/规范图集」改为「公开规范与行业通用做法整理」，不再引用公司内部资料路径。
- **版本对齐** 本机 `$CODEX_SKILLS_DIR/skills`、`~/.workbuddy/skills` 与发布仓库同步同版本；算法、契约、兼容性与上一版一致，未改业务逻辑。

## 0.9.24

- **新增** `scripts/runtime_env.sh`，入口脚本统一解析解释器与底座，并自动注入底座 vendor（openpyxl 等无需全局安装）。
- **修复** 底座探测与自动安装落点原先硬编码 `$HOME/.codex`，现支持同级目录及 WorkBuddy 技能目录。
- **修复** `.sh` 缺可执行位；`scripts/tests/` 缺 `__init__.py`。
- **新增** `requirements.txt`（含可选的 `markitdown`，用于读 Word/Excel/PDF 依据）、Windows 启动器 `decor_qty.cmd` / `cad_measure_to_input.cmd` / `zhuangshi_statesync.cmd`。
- **文档** 标题版本由 v0.9.0 更正为 v0.9.24；命令统一改为 `bash scripts/*.sh`。
- **修复（发布兼容）** `cad_measure_to_input.py` 调用 `cad_validate.sh` 改为 `bash` 启动；`ensure_base.sh` / `setup.sh` 内部调用同步改 `bash`。
- **修复（跨 Agent）** `cad_measure_to_input.py` 底座探测增加同级目录与 `~/.workbuddy/skills/*`。

## 0.9.23 (2026-10-23)
- 修复 SkillHub 版 Windows 无 `.cmd` 时的接线说明：改为 `python scripts/*_statesync.py` 等价调用（bus 安装用 `python install_py.py --apply`）；GitHub 完整包保留 `.cmd`。平台发布调整，算法/契约/口径不变。


## 0.9.22 (2026-10-22)
- lis-skill-bus 可选联动（试点）：scripts/zhuangshi_statesync.py push/pull 对接 cad-contract/v1（rooms/room_schedules/practices/room_boundaries 等），新 Windows zhuangshi_statesync.cmd（未实机跑通，仅静态校验）；bus 未装自动降级。算法/口径不变。

## 0.9.21 (2026-10-21)
- 三平台对齐（cross-platform + i18n overseas）：README.en.md、`--lang en|zh` 主入口、i18n.py、CFI 三平台 workflow 全绿。
- 不改变业务算法/中文模板；平台专用调整只改发布副本。

# 更新记录
## v0.9.20 — 2026-10-19（三平台发布对齐）

- 发布对齐：以本机为规范源同步三平台；含 qto-project/v1 联动契约与 zero-config 底座默认仓库。
## P1 联动（2026-10-19，文档说明）

- 新增与 `cad-file-reader` 的目录级联动说明：识别放 `<项目目录>/识别/<slug>/`，量算输出写 `<项目目录>/算量/<slug>/`，可用底座 `scripts/qto_p1_link.py` 登记；不改算法与口径。

## 0.9.14 — 2026-10-18（第三批补齐：精装图审 27/27 全量）

- `某项目精装图审` zip 全部 27 个 DWG 回归完成：首 5 张 + 补齐 22 张 = 27/27 通过（components 主键；做法/立面/节点/平面系统图 geometry=0 属预期，记入复核）。
- 明细：`batch_results/zhuangshi-suanliang/cad-file-reader-ts-fig-1.report.json` + `cad-file-reader-ts-fig-r1..r5.report.json`。
## 0.9.13 — 2026-10-18（第三批：精装图审真图回归）

- 精装图审 zip 本机解压 27 个 DWG；本轮按每批 5 张跑 `某项目精装图审` 首 5 张（设计说明做法表、1层大厅立面、通用节点一、2层平面系统、B展厅平立面）5/5 通过（components+references 主键；geometry=0 属做法/立面/节点类预期）。
- 明细落 `work/real_regression/batch_results/zhuangshi-suanliang/cad-file-reader-ts-fig-1.report.json`。
## 0.9.12 — 2026-10-18（第二期真图回归：31 例 + PDF 节点 10 例）

- 31 例原图 30/31 通过；1 例 `会展PM（布局+精装改地下电梯厅）` 原 DWG 无法解析，在本机找到 2 张同项目可解析会展PM替代版并通过（2/2 pass）。
- 另用 `cad_pdf_ocr.sh --classify-only` 对本机 10 张钢结构节点/防水节点 PDF 做本机 OCR 分类回归，10/10 pass。
- 自检 `run_preflight.sh` 全量 5 项通过，发布合规扫描 problems=0。

## 0.9.11 — 2026-10-16（保温专篇/做法表文字证据链路）
- `scripts/cad_measure_to_input.py` 新增 `notes_text_rows()` 与 `--notes-text`（可重复）：从本地建筑说明/OCR 文本按部位关键词（保温/防水/屋面/外墙/墙面/地面/顶棚/踢脚）生成“待核对”装饰输入行，只搬运原文证据，不解析厚度/面积/材料消耗，不自动绑定做法编号，`final_quantity=false`。
- 新增单测：断言“外墙外保温…岩棉”→“待确认-保温”、“地下室顶板…防水”→“待确认-防水”。
- 真图验证：某项目建筑做法说明 PDF（字体编码损坏）改用 image-ocr 400dpi+table 本地 OCR，4 页产出可读文本（`外墙外保温…120厚岩棉 60KG/M3`、`沿外墙内侧贴 20x50 高挤塑聚苯板保温层`、`80 厚阻燃型挤塑聚苯乙烯泡沫板`、`屋面…120厚保温岩棉` 等）；用该 OCR 文本经 `--notes-text` 生成 104 条待核对证据行（防水 61/地面 20/保温 14/屋面 4/顶棚 3/墙面 2）。
- 边界：酒店建筑总说明 DWG 的做法表正文以 ACET-LAY 块/表存在，纯文字扫描读不到正文，需转 DXF 或块展开才能精确映射。
- 自测：`run_preflight.sh` 全量 5 项通过，发布合规扫描 problems=0。

## 0.9.10 — 2026-10-12（真图回归纳入发布预检，文档修正）
- 新增 `scripts/run_preflight.sh`：全量自测 → 发布合规扫描 → 真图回归（复用 cad 底座，--manifest 强制），发布前统一入口。
- README/SKILL.md 明确 `scripts/cad_measure.sh` 属于识图底座 cad-file-reader，在底座目录执行，避免发布包误判缺失脚本。
- `ensure_base.sh` 保留 SHA-256 完整性校验；默认底座版本 cad-file-reader 0.28.5。

## 更新记录

## 0.9.6 — 2026-10-12（底座自动安装加固）

- `ensure_base.sh` 增加 cad-file-reader 完整包 SHA-256 校验（从同 Release 下载 SHA256SUMS），校验失败拒绝安装与执行。
- 自动安装底座前校验包内 manifest 版本；默认底座版本升至 0.28.1。
- 平台安全扫描合规：自动下载底座改为带完整性校验、版本固定。


# 更新记录

## 0.9.0 — 2026-10-05

对接 cad-file-reader 0.25.0 底座增强：旋转标注聚合、图例匹配、契约置信度/跨专业引用字段；版本门槛升至 `cad-file-reader >= 0.25.0`。

## 0.8.0 — 2026-10-05

对接 cad-file-reader 0.19/0.20 底座的装饰识图中间数据与交接校验。

- `cad_measure_to_input.py` 新增 `--descriptive`：可导入 cad-descriptive-geometry/v7 的房间边界、墙段 clear/opening、吊顶分区、洞口归属和做法→节点索引，全部转成待核对输入行（需核对=是，做法编号只做候选，不参与本技能正式做法映射）。
- 新增 `--validate`（默认开启）：导入前用 cad-file-reader `cad_validate.sh` 校验交接 JSON，未通过行标记复核原因；缺底座时静默跳过不阻断。
- 测试扩展：新增描述几何导入与缺底座跳过校验两条合成回归。

## 0.7.0 — 2026-09-20

## 0.7.0 — 2026-09-20

对接 cad-file-reader 0.18.0 测量候选。

- 依赖从 `cad-file-reader>=0.2.0` 提升到 `>=0.18.0`。
- 新增 `cad_measure_to_input.py`：把长度/面积/体积测量候选转成装饰算量输入表草稿；面积和长度导入行保留证据，体积候选不直接转装饰输入。
- CAD 导入行做法编号留空、需核对固定为“是”；做法映射、洞口扣减、侧壁、损耗、材料台账和清单量仍由本技能计算。
- 新增合成回归覆盖面积/长度导入、缺单位复核和体积跳过。

## 0.6.0 - 2026-09-18

- 集成公开规范与造价标准资料的15项规范/清单标准元数据、算量约束和构造复核要点；不复制规范原文。
- 清单规则补充计量单位、计算规则、依据、技术规范、构造要求、复核点和“是否计入损耗”字段。
- 概算依据合并清单技术规范；Excel依据表增加知识库索引、适用部位和算量作用。
- 报告输出知识库索引、15项标准、口径边界和适用范围。
- 增强块料地面/墙面、乳胶漆、吊顶和外墙保温的构造层完整性校验。
- 外墙保温补充锚栓、网格布、抹面砂浆校验；补充GB 50411-2019和GB 50327-2001。
- 测试扩展到30项，覆盖15项标准、结构化清单规则、单位一致性和构造缺项。

## 0.5.0 - 2026-09-18

- 新增快速概算输入；按房间类型自动展开为地面、墙面、顶棚、踢脚、防水、保温等做法。
- 新增两条口径：概算量按清单/商务口径，不含损耗、搭接和附加层；物资计划量按采购口径，含损耗、搭接、附加层和块料取整。
- 新增清单工程量规则、参考综合单价和物资分类规则；均支持 CLI 项目化替换。
- Excel 台账升级为 `概算`、`物资计划`、`明细`、`汇总`、`缺项`、`依据` 六个工作表。
- 新增 `概算明细.csv`、`概算汇总.csv`、`物资计划.csv` 和装饰概算物资计划报告。
- 报告增加概算汇总、物资计划汇总、口径说明和待确认项。
- 补充 GB 50500-2013、GB 50854-2013、GB/T 50353-2013 参考约束。
- 测试扩展到 22 项，覆盖房间展开、未知房间、概算口径、防水差异、物资损耗、规则缺项和六表输出。

## 0.4.0 - 2026-09-18

- 增加 P0 输入校验：必填列、必填值、数字/单位、负数、间数和完全重复行。
- 输出 Excel 台账，固定包含明细、汇总、缺项、依据四个工作表。
- 增加项目专属规则；项目专属做法按节点编号匹配，不匹配时不回退默认做法。
- 增加国家规范参考校验，重点覆盖防水附加层、搭接、卷材幅宽、涂膜厚度、上翻高度和屋面道数。
- 增加防水涂料附加层与防水卷材搭接系数计算。
- 材料汇总增加“完成状态订货量”，区分可放心订货量和需核对量。
- 补充测试、输入模板、项目专属规则示例和规范依据表。

## 0.2.0 - 2026-09-18

- 增加建筑说明、建筑图、结构图和节点详图的交叉读取要求。
- 增加做法类型、节点编号、节点详图字段。
- 项目专属做法缺节点详图时进入缺项清单。
- 明确节点详图、房间装修做法表、建筑说明和默认规则的优先级。

## 0.1.0 - 2026-09-17

- 创建装饰算量技能。
- 支持地面、墙面、顶棚、踢脚、防水、外墙等基面量计算。
- 支持做法编号映射材料、损耗、面砖块数和缺项清单。

- 新增与 `cad-file-reader` 的目录级联动说明：识别放 `<项目目录>/识别/<slug>/`，量算输出写 `<项目目录>/算量/<slug>/`，可用底座 `scripts/qto_p1_link.py` 登记；不改算法与口径。

