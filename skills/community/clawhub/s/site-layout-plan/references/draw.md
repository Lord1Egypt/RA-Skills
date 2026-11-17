# 单阶段塔吊出图与设施图块

> 本文件由 SKILL.md 按需加载；内容与 0.7.2 代码同步。
> 本文件覆盖 `draw_layout.py` 的单阶段塔吊逐柱出图（8 条自检），以及 `render_facility_showcase.py` 的 7 类设施合并/分张大样。三阶段布置图的真 `DIMENSION`、坐标 CSV/图内表、指北针、统一文字排版与 12 条自检见 `references/site-plan.md` 的“出图内容（0.6.7）”。

## 1. 单阶段塔吊出图

### 出图输入

- `--site`：只收 `cad-file-reader` 的 `cad-site-geometry/v1`（`contract.contract_version=cad-contract/v1`），或 `prepare_site.py` 从该契约派生的 `base-map.json`（固定 mm，且 `source_schema` 必须回指 reader）。不直读 `.dwg/.dxf/.pdf`；直读 CAD exit 2。
- `--handoff`、`--check`、`--baseline`：同校核三件套。
- `--layout`：塔吊布置 JSON；不传时默认找与 site 同名的 `*.layout.json`。示例：

```json
{"contract_id": "CONTRACT-SYNTH-001",
 "cranes": [{"id": "P4", "model": "ZSL750", "jib_m": 70, "x_m": 0, "y_m": 0}]}
```

也接受 `x_mm/y_mm`、`jib_mm`。

- `--titleblock`：图签模板，默认 `templates/titleblock.json`。
- `--draft`：仅当契约不一致时允许出草稿图；图签打 `DRAFT-CONTRACT-MISMATCH`。

```bash
cd site-layout-plan
python3 scripts/draw_layout.py \
  --site /tmp/reader/总图.site.json \
  --handoff tests/fixtures/handoff_p4.json \
  --check /tmp/crane_check_p4/crane_check.json \
  --baseline tests/fixtures/baseline.json \
  --out-dir /tmp/layout_out --draft
```

`--out-dir` 不能等于原图目录。输出：

```text
layout_out/
├─ layout.dxf       # 模型 1:1，$INSUNITS=4（mm）
├─ layout.png       # 200 dpi，中文可读；缺字体时降级并写图签
├─ layers.csv       # 8 个固定图层的颜色/线型/用途/实体数
├─ titleblock.json  # 图签数据副本 + 原图哈希前后值
└─ selfcheck.json   # 8 条自检，每条带坐标/数值证据
```

## 2. 设施图块清单（0.7.0）

所有图块由 `site_layout/symbols.py` 内的纯 Python 图元定义，DXF BLOCK、主图 INSERT、图例和 PNG 大样共用 `primitives(category)`，不维护两套画法。图块只表达**设施类型和相对关系**，不表达厂家基础、附着、型号性能或最终尺寸。

| 展示键 | category | 块名 | 中文名 | 建议尺寸 | 阶段 | 几何要点 |
|---|---|---|---|---:|---|---|
| `crane` | `tower_crane` | `SLP_CRANE` | 塔吊 | 12.0 m | 主体 | 基础节、标准节、附着撑杆、回转总成、驾驶室、分节起重臂、小车、双倍率吊钩、平衡臂配重、塔尖拉杆、红色虚线幅度标注 |
| `elev` | `construction_elevator` | `SLP_ELEV` | 施工电梯 | 7.0 m | 主体/装饰 | 底座、双导轨、腹杆、附墙架、层门、吊笼门与开启弧、电缆滑车、地面围栏、防护棚 |
| `weighbridge` | `weighbridge` | `SLP_WEIGHBRIDGE` | 地磅 | 12.0 m | 全阶段 | 分节秤台、四角传感器、四角限位挡块、两端引坡坡度箭头、称重房、行车方向 |
| `wash` | `wheel_wash` | `SLP_WASH` | 洗车台 | 4.0 m | 全阶段 | 洗车平台、两端引坡、喷淋拱、三级沉淀池并标 `1/2/3`、排水沟、减速带、单向行驶箭头 |
| `office` | `site_office` | `SLP_OFFICE` | 办公区 | 7.0 m | 全阶段 | 两层箱房排、外走廊与栏杆、楼梯、停车位、旗杆、宣传栏 |
| `dorm` | `staff_dormitory` | `SLP_STAFFDORM` | 员工宿舍区 | 7.0 m | 全阶段 | 箱房排、空调外机、成排床位、晾晒区、两端疏散楼梯 |
| `living` | `worker_living_zone` | `SLP_LIVING` | 工人生活区 | 9.0 m | 全阶段 | 宿舍排、食堂餐桌、淋浴/厕所、晾晒区、活动场；分区用虚线短划表达 |

### 块名稳定约定

- 办公区、员工宿舍区、工人生活区的实际块名分别是 `SLP_OFFICE`、`SLP_STAFFDORM`、`SLP_LIVING`。
- `office`、`dorm`、`living` 只是大样命令的**展示选择键**，不是 DXF 块名；不要为它们另造 `SLP_OFFICE_ZONE`、`SLP_STAFF_DORM`、`SLP_WORKER_LIVING` 等重复块。
- 保持块名不变，才能让旧 DXF 的 INSERT、图例、图层统计和替换流程继续识别。需要区分“办公区组合”与“单栋办公箱房”时，应新增独立 category 和 block，不得悄悄改旧块含义。
- 块名必须唯一；`SYMBOLS` 同时写 `layer`、`stages`、`showcase`、`note`，图例与大样从同一元数据读取。

### 1000×1000 基准与原点

- 所有块以 `1000×1000` 为基准，坐标范围约 `-500..500`，原点在块中心。
- 插入时按建议尺寸缩放：`xscale = yscale = size_mm / 1000`，不得只缩一个方向。
- 大样 PNG 的中心十字只用于说明原点，不是设施实体。
- 图块内文字只做辅助识别；PNG 大样在小尺寸下不重复画块内文字，设施名称放在卡片标题和图例中。

## 3. 合并与分张大样

默认输出合并大样；给 `--out-dir` 时，每个设施另出一张 `facility-showcase-<key>.png`。合并大样第 8 格为使用说明，7 类设施各占一张卡片。

```bash
cd site-layout-plan

# 合并大样 + 7 张单图
python3 scripts/render_facility_showcase.py \
  --out work/s7/facility-showcase-v07.png \
  --only crane,elev,weighbridge,wash,office,dorm,living \
  --out-dir work/s7/showcase-v07

# 只出其中两类
python3 scripts/render_facility_showcase.py \
  --only 地磅,office \
  --out-dir /tmp/showcase-two
```

输出命名：

```text
work/s7/
├─ facility-showcase-v07.png
└─ showcase-v07/
   ├─ facility-showcase-crane.png
   ├─ facility-showcase-elev.png
   ├─ facility-showcase-weighbridge.png
   ├─ facility-showcase-wash.png
   ├─ facility-showcase-office.png
   ├─ facility-showcase-dorm.png
   └─ facility-showcase-living.png
```

- `--only` 支持展示键、category 名和少量别名（含 `地磅`）；未知键在出图前报错退出，不生成半套文件。
- 合并/单图都写“类型示意，不替代厂家标准块与专项方案”，不得当审批图或厂家基础图使用。
- 单图列出块名、中文名、建议尺寸、适用阶段、建议图层、几何要点、1000×1000 基准和原点提示。
- 大样只用于方案讨论和交底配图；正式总图仍由 `build_site_plan.py` / `draw_layout.py` 按项目坐标、图层和自检链出图。

## 4. 替换为厂家或第三方图块

当前 7 类图块全部自绘，不复制网络 CAD 图块。将来确需替换为厂家标准块或开源图块，按以下流程执行；不得直接把来源不明的图块塞进发布包。

1. **先定来源与授权**：确认是厂家公开标准块、经授权的项目资料，还是许可证兼容的开源图块；公司内部资料只在本机使用，未获明确同意不得进入发布物。
2. **记录可追溯信息**：来源 URL 或文件出处、许可证名称与版本、厂家/型号、图块版本号、原始文件 SHA-256、获取日期、适用规范/图集号。
3. **做许可证兼容检查**：本技能为 `CC-BY-NC-SA-4.0`；第三方许可证必须允许当前分发方式，禁止把“仅限内部使用”的图块放进公开仓库或三平台包。
4. **保留稳定块名**：替换几何时仍输出原 `SLP_*` 块名；如需保留厂家原名，可在说明中写“来源块名”，不要让旧 INSERT 失效。
5. **同源改造**：优先把授权图块转成 `line/poly/solid/circle/arc/text` 图元，补进 `symbols.py`，使 DXF 与 PNG 继续同源；若必须直接导入 DXF BLOCK，则增加 `ensure_symbol_blocks()` 的导入分支并写明失败回退。
6. **脱敏与回归**：去掉公司名、项目名、图签、人员、内部路径和元数据；补块名、许可证、SHA-256、图元数量、DXF 可创建、PNG 非空和 7 类可辨认回归；不通过不替换。
7. **留痕**：在 `manifest.json`、本文件和发布检查清单中记录替换项；不得只改图不记来源。

替换记录模板：

```text
设施：SLP_WEIGHBRIDGE
来源：<厂家官网/授权文件/开源仓库 URL 或内部文件编号>
许可证：<名称、版本、是否允许再分发>
厂家/型号：<...>
图块版本：<...>
原始 SHA-256：<...>
导入日期：<YYYY-MM-DD>
修改人：<...>
验证：DXF BLOCK 可创建 / PNG 非空 / 7 类回归通过
```

## 5. 固定图层

| 图层 | 内容 |
|---|---|
| `BASE-底图` | 原图几何，灰显（8 号色） |
| `CRANE-塔吊` | 符号、型号、臂长、回转中心 |
| `CRANE-覆盖` | 幅度圆，按塔吊分色 |
| `LIFT-合格` | 逐柱绿色（ok） |
| `LIFT-超载` | 逐柱红色（insufficient / out_of_range） |
| `LIFT-盲区` | 逐柱黄色（blind / review / unknown_*） |
| `TEXT-结论` | 柱号、需求/额定、利用率 |
| `META-图签` | contract_id、版本、日期、免责声明、DRAFT |

设施大样 PNG 不建立 CAD 图层；正式图中的设施 INSERT 使用 `SYMBOLS[category]["layer"]`，例如 `FAC-办公区`、`FAC-员工宿舍`、`FAC-工人生活区`、`FAC-地磅`、`FAC-洗车池`。

## 6. 出图闸门

- 每个输入（`site`、`handoff`、`crane_check`、`layout`）都必须有 `contract_id`；缺任一且未加 `--draft` → exit 5。
- 不同输入的 `contract_id` 允许不同；图签分别列出并标 `contract_ids_differ=true`。
- 是否同源以 `source_sha256` 判断：不同源且未加 `--allow-source-mismatch` → 分阶段出图 exit 5。
- `crane_check.final_check=false` → 图签必须 `DRAFT`。
- `baseline.locked_by` 为空 → 拒绝出图（exit 5），不生成文件。
- 原图 SHA-256 出图前后必须一致，写入 `titleblock.json` 的 `source_sha256_before/after`；不一致 → exit 5。

## 7. 自检 8 条（`selfcheck.json`）

1. 红线闭合（容差 50 mm），给顶点和面积。
2. 塔吊中心落在场地范围内，给中心坐标。
3. 幅度圆是否越过红线/围挡；只给 `manual` 提示，不自动判违规。
4. 盲区柱数量与 `crane_check.json` 一致，给盲区柱坐标。
5. 8 个必备图层齐全，给每层实体数与样点坐标。
6. 文字不溢出图框（粗略包围盒），给文字数与溢出项。
7. 单位一致性（输出 mm、`$INSUNITS=4`），给源单位与换算系数。
8. DRAFT 标识与输入状态匹配，给期望/实际标签。

每条状态为 `pass|fail|manual`。存在 `fail` 时仍保留已生成文件，但 CLI exit 5。

## 8. R12 看图版（CAD快速看图兼容）

主交付 `layout-*.dxf` 为 R2010，保留真 `DIMENSION`、`LWPOLYLINE`、`MTEXT`，供 CAD 编辑。国产看图软件兼容性差，需要另出 R12：

```bash
python3 scripts/dxf_view_export.py layout-structure.dxf -o layout-structure-r12.dxf
# 或批量：python3 scripts/dxf_view_export.py *.dxf --out-dir out-dir
```

实测根因（CAD快速看图 macOS，2026-11）：

| 现象 | 根因 | 看图版处理 |
|---|---|---|
| 打开全黑 | R2010/AC1024 不支持或渲染不全 | 降到 R12（AC1009） |
| 打开只看到一角/空白 | 不执行 zoom-extents，按 `VPORT *Active` 定位 | 写 `*Active` 中心=图形中心、高度=外包高度×1.06 |
| 全黑且坐标是 5e8/4e9 | float32 精度丢失 | 平移图形到原点，偏移写 `$USERR1/$USERR2` |
| 标注显示不出 | `DIMENSION` 关联对象不被识别 | 转为尺寸几何块 `INSERT` |
| 多行文字错位 | `MTEXT` 不支持 | 取 `plain_text()` 转 `TEXT` |

看图版只保证“能看能粗量”，不可当编辑源；量测结果需加回 `$USERR1/$USERR2` 偏移才是工程坐标。回归测试见 `tests/test_dxf_view_export.py`。
