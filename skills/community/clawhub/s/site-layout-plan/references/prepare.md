# reader 契约与单位适配

> 本文件由 SKILL.md 按需加载；内容与 0.7.2 代码同步。

reader 只出**证据**：单位可能在 `scale_unit_audit[].units`，也可能在逐条几何的 `unit`；顶层不一定有 `coord_unit`。图纸没写单位时 reader 如实标 `missing_unit`，不会替项目拍板。出图必须按 mm 落笔，所以中间必须有一层把「候选单位」变成「施工口径」并留痕——这就是 `prepare_site.py`。它不重新识图、不判定合规，只做：

- 单位优先级：顶层 `coord_unit` → `scale_unit_audit[].units` → 逐条几何声明 → 人工 `--unit`。
- reader 顶层没有 `coord_unit`、但 `scale_unit_audit[]` 有唯一单位时，`prepare_site.py` 会自动回退读取，不需要给 JSON 手工补行。
- 临时给 JSON 补 `"coord_unit": "mm"` 只能作为一次性适配；长期应在 reader 的 `_json_declared_unit()` 增加 `scale_unit_audit[].units` 回退。
- 多来源单位冲突 → **exit 4**，不挑一个「看起来对」的。
- reader 无任何单位 → 必须 `--unit mm|m|cm|ft` + `--confirmed-by`，否则 **exit 4**，不猜 10/1000 倍。
- 红线线段按 50 mm 容差串接闭合，输出顶点、面积与缺口。
- 主体轮廓优先从 `建筑-屋顶-外轮廓` 图层提取，其次 `建筑-平面/轮廓`、`BUILDING/FOOTPRINT`；排除高差、分隔、屋脊、阳台、填充、标注等噪声层。
- 建筑候选先用红线外扩 30 m 窗口过滤，再逐层走闭合环；默认最小面积 200 m²，滤掉门房、雨棚等碎环。多栋/多环按“图层等级 + 面积降序”选最大主体，并保留 `buildings` 与 `building_selection` 供人工核对。
- 底图线段只保留红线外扩 50 m 窗口内的部分，避免原点详图或 1 km 长线把图框撑大；裁剪留痕写入 `geometry_selection`。
- 输入只读；输出 `base-map.json` + `base-map.md`，绝不回写 reader 契约。
- **契约闸门**：读取前拒绝 `.dwg/.dxf/.pdf`；只收 `schema=cad-site-geometry/v1` 且 `contract.contract_version=cad-contract/v1` 的 reader 契约，否则 exit 2。`crane_check.py` 同理只收 `site-handoff/v1` 且带 `contract_id/source_sha256` 的 handoff。
- 硬链路：`DWG/DXF/PDF → lis-skill-bus → cad-file-reader → cad-contract/v1 → lis-skill-bus → site-layout-plan`。本技能不 import `ezdwg`/`ezdxf`/`read_cad` 解图，也没有 `CAD_ALLOW_DIRECT` 逃生口；bus/reader 缺失时标 `unavailable` 并停止。

```bash
cd site-layout-plan

# reader 已识别唯一单位：直接适配
python3 scripts/prepare_site.py \
  --site out/场地识图/总图.site.json \
  --out-dir out/prepared \
  --building-layer "0-建筑-屋顶-外轮廓"   # 可选：多栋/多环时显式指定

# reader 标 missing_unit：人工确认并留痕
python3 scripts/prepare_site.py \
  --site out/场地识图/总图.site.json \
  --out-dir out/prepared \
  --unit mm --confirmed-by lis
```

输出 `out/prepared/base-map.json`（`site-layout-base-map/v1`，`coord_unit=mm`）与 `base-map.md`（单位依据、证据、红线闭合/面积、主体提取、50 m 裁剪、范围、警告）。后续校核与出图都优先消费这份 `base-map.json`。

`prepare_site.py` 只提取候选主体，不替项目确认楼栋。提取不到主体时仍会输出底图并在警告中说明；`generate_site_layout.py` 默认拒绝按假定矩形出 A/B/C。多栋/多环必须核对 `buildings`，必要时用 `--building-layer` 或需求 JSON 的 `building.footprint` 锁定。

| 退出码 | 含义 | 处理 |
|---:|---|---|
| 0 | 适配成功 | 读 `base-map.md` 核对单位依据 |
| 2 | 输入不是 reader 契约 / JSON 错误 | 修输入，不绕过 |
| 4 | 单位缺失、单位冲突、人工单位与 reader 冲突 | 先统一图纸单位或补 `--unit`，禁止猜 |

