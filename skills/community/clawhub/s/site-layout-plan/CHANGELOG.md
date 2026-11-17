# Changelog

## 0.7.3 · 2026-11-12 · 系列蓝标图标

### 发布物
- 新增 `icons/icon_small.png`（128×128）与 `icons/icon_large.png`（512×512），采用 Skill 系列蓝图风蓝标（深蓝底 #0A1F3C + 青蓝线 #4AD3FF + 网格底纹），图元为用地红线、建筑轮廓、塔吊与场内道路。
- `agents/openai.yaml` 增加 `interface.icon_small/icon_large` 引用，供 Codex/ClawHub 读取；SkillHub 图标经平台图标接口上传。
- 功能、规则库、契约与出图口径与 0.7.2 完全一致，无代码改动。

## 0.7.2 · 2026-11-12 · 识图链路收口

### 出图链路
- `draw_layout.py` 移除输入 DXF 解析分支（`--site-dxf` 与 `_load_site_dxf`），出图只收 `cad-site-geometry/v1` 且 `contract.contract_version=cad-contract/v1` 的 reader 契约，或 `prepare_site.py` 派生的 `base-map.json`（`source_schema` 必须回指 reader）；直读 `.dwg/.dxf/.pdf` 一律 exit 2。
- `load_site()` 读取前调用 `validate_reader_path()`；`crane_check.py` 维持只收带 `contract_id/source_sha256` 的 `site-handoff/v1`。
- 新增 `tests/test_draw.py` 直读合成 DXF 必须 exit 2 的回归；`manifest.json` 移除 `tests/fixtures/site_sample.dxf` 声明。
- 规则 26「办公区靠近主出入口」的 50 m 明确为经验提示：超距写 `manual`，不判 fail、不阻断出图（用户确认不设为硬约束）。
- `prepared_by` 改为读取包版本，`SKILL.md` 压到 8 KB 以内以过 agent-slim 闸口。

## 0.7.1 · 2026-11-12 · 发布闸口

### 识图硬链路
- 标准链路固定为 `DWG/DXF/PDF → lis-skill-bus → cad-file-reader → cad-contract/v1 → lis-skill-bus → site-layout-plan`；本技能不打开、不解析 CAD/PDF，也不自带 reader。
- `prepare_site.py`、`draw_layout.py` 读取前拒绝 `.dwg/.dxf/.pdf`，只收 `cad-site-geometry/v1 + contract.contract_version=cad-contract/v1` 的 reader 契约（出图也接受 `prepare_site.py` 派生的 `base-map.json`，但校验 `source_schema` 必须回指 reader）；`crane_check.py` 只收带 `contract_id/source_sha256` 的 `site-handoff/v1`。
- 新增 `tests/test_reader_gate.py`（6 项）：直读 DXF、非 reader JSON、旧契约版本、缺 contract 来源均拒绝，合法 reader 契约通过；无 `CAD_ALLOW_DIRECT` 逃生口。`draw_layout.py` 同步移除输入 DXF 解析分支，直读 CAD exit 2。
- 规则 26「办公区靠近主出入口」保持经验提示（`manual`），50 m 不设硬性 fail；自动布置仍可能超距，必须人工调整。
- 发布物排除 `work/`、真实图纸与项目证据；manifest 增加 `requires_skills` 与 `reader_contract` 声明。

## 0.7.0 · 2026-11-11

### 三区分类与生活区
- 办公区、员工宿舍区、工人生活区分开建模；工人生活区内置食堂、卫生间/淋浴、晾晒区三个子块，子块声明 `parent_id` 且不越出父包络。
- 规则新增生活区专项：与作业面分离、道路/消防疏散、配套完整性、办公区靠近主出入口；场地夹逼降级时写 `size_degraded/size_note`。

### 标准块与设施形象化 v2
- 7 类设施（塔吊/施工电梯/地磅/洗车台/三区）形象化 v2；DXF BLOCK 与 PNG 图例同源。
- 标准块路线定为纯 Python 自绘参数化图块（`site_layout/symbols.py`），零第三方 DWG/DXF 图块；图块只表达类型，不表达厂家真实尺寸、基础与工况。

### 三阶段与出图
- 土石方/主体/装饰三阶段分别建模、校核、出图；26 条临建规则 + 道路 R1~R4 + 周边硬/软约束 + 六视角审查。
- R12「看图版」导出；图签始终带 `DRAFT`，`final_check=false`。

### 验收（本机，未发布）
- 真实总图回归：规则 fail=0，selfcheck 12/0/0，SHA 49 项一致（s3）。
- 联合验收：本机全量测试 16 个文件全部 OK；样例代号 R09 的图签 OCR/CAD 对照在本机完成，发布包不含原图与项目字段。
- 边界：自动设施为 `candidate`；不替代审批、签字、消防/报建。
