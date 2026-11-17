# 强依赖底座契约（cad-file-reader）

原 SKILL.md 内嵌说明，完整保留于此，供按需查阅。

本技能采用**识图与算量分离**的固定架构，`cad-file-reader` 是**强依赖底座**，不是可选增强：

- **为什么必须强依赖**：DWG/DXF/DWT/PDF 的解析、图层/文字/块/图框/几何提取、识图候选和测量候选全部集中在底座完成，一次解图、全项目复用，保证证据坐标与契约一致。本技能只做本专业口径的量算、扣减、损耗、分账和台账，不重复解析图纸。
- **分工**：底座输出 `final_quantity=false` 的识图/测量候选；本技能输出本专业概算底稿/物资计划草稿（`final_quantity=true` 仅本专业口径）。
- **版本约束**：底座最低版本以各技能 `SKILL.md`「前置/依赖」写的 `>=x.y.z` 为准；缺底座或版本不够时明确报错，不静默用错误数据。
- **安装**：先装底座（`cad-file-reader/scripts/setup.sh`），再装本技能；运行时底座可在 `SKILL_NO_BASE=1` 下退化为只读已有扫描/候选/表格输入，但精度受限并必须在结果标注。
- **联动**：装有 lis-skill-bus 时，底座与各算量技能通过 `cad-contract/v1` 共享契约，同一张图只解一次；不装 bus 时各技能自动降级为各自 `state/`，功能不丢失。

## 强依赖底座（cad-file-reader，不做弱化）

`cad-file-reader` 是强依赖底座，不是可选增强：DWG/DXF/DWT/PDF 解析、图层/文字/块/图框/几何与测量候选全部由底座完成，一次解图、全项目复用，保证证据坐标与契约一致；本技能只做本专业口径的量算、扣减、损耗、分账和台账，不重复解析图纸。底座输出 `final_quantity=false` 的候选，本技能输出概算底稿/物资计划草稿（`final_quantity=true` 仅本专业口径）。缺底座或版本不足必须明确报错，不静默用错数据。装 `lis-skill-bus` 时按 `cad-contract/v1` 共享契约，否则降级到各自 `state/`。完整说明与安装/降级细节见 `references/base-contract.md`。



- 底座 `cad-file-reader >= 0.28.1` 的 `landscape-geometry` 包是**显式依赖**；不自行解析大 DWG。
- 苗木统计输入：底座 `cad_landscape_geometry` 输出 JSON（`plant_block_legends` / `plant_legends` / `plant_schedule_links` / `systems`）与 `cad_scan` 文字/块引用详情。
- 苗木表解析：从图纸文字中识别“苗木表/苗木配置表”的表头、名称、数量、单位列；数量单位必须来自数量表头括号或单位列，缺失时不默认为株并降 P1。
- 铺装面积输入：`cad_scan --with-geom --with-geom-layer --detail-json` 详情 JSON；应有可用的铺装图层名。
- DXF 块内铺装回退：可选 `--dxf-block-paving`，使用底座 `vendor/ezdxf` 展开 INSERT 变换；只提取命中铺装 token 的闭合 `LWPOLYLINE/POLYLINE/HATCH/ARC`，展开 LWPOLYLINE bulge 圆弧，结果强制 P3。
- DXF 块引用坐标回退：可选 `--dxf-block-refs`，读取模型空间顶层 INSERT 坐标，同名块按坐标去重；只有坐标命中的块引用才升级 P0，无坐标仍保持 P2。
- 扫描件/图片型 PDF 只出苗木文字候选，不给铺装面积。

