# 园林算量脚本用法（完整版）

原 SKILL.md「脚本用法」章节，按需查阅。

## 脚本用法

```bash
# 1) 底座：园林识图（苗木图例/块分类/铺装闭合域候选）
scripts/cad_scan.sh 景观图.dwg --with-mtext --with-attrib --with-insert --with-blocks --with-block-geom \
  --with-geom --with-geom-layer --detail-json 景观详情.json --format json -o 景观扫描
scripts/cad_landscape_geometry.sh 景观详情.json --out-dir 园林识图

# 2) 本技能：苗木统计 + 铺装面积
bash scripts/yuanlin_qty.sh \
  --landscape 园林识图/景观详情.landscape.json \
  --scan 景观详情.json \
  --out-dir ./园林概算 \
  --project "项目名"

# 3) 可选：DXF 图块内铺装回退（仍强制 P3）
bash scripts/yuanlin_qty.sh \
  --landscape 园林识图/景观详情.landscape.json \
  --scan 景观详情.json \
  --dxf-block-paving 景观图.dxf \
  --out-dir ./园林概算-块铺装候选 \
  --project "项目名"

# 4) 可选：DXF 顶层块引用坐标去重（P2→P0；同名坐标重复不计）
bash scripts/yuanlin_qty.sh \
  --landscape 园林识图/景观详情.landscape.json \
  --scan 景观详情.json \
  --dxf-block-refs 景观图.dxf \
  --out-dir ./园林概算-块坐标 \
  --project "项目名"

# 5) 可选：叠加项目植物名称参考库（只取中文名→大类）
bash scripts/yuanlin_qty.sh \
  --landscape 园林识图/景观详情.landscape.json \
  --scan 景观详情.json \
  --plant-library 项目苗木清单.xlsx \
  --out-dir ./园林概算-项目词库 \
  --project "项目名"
```

可用参数：

- `--rules templates/项目专属规则示例.json`：项目专属图层 token、植物词库、去重半径。
- `--scale 100` / `--drawing-mm-per-unit 1`：覆盖自动比例/单位检测；显式指定后不回改单位。
- `--dedupe-tolerance 0.5`：同名块同坐标去重半径（图纸单位）。
- `--paving-all-geometry`：图层缺失时对全部几何做闭环候选；结果强制 P3、`final_quantity=false`，不计入主线。
- `--dxf-block-paving 图.dxf`：可选回退，展开块内铺装闭合环；结果强制 P3、不计入主线。
- `--dxf-block-refs 图.dxf`：可选回退，读取顶层 INSERT 坐标，同名块按坐标去重；无坐标块引用仍保持 P2，不猜株数。
- `--plant-library 参考库.{json,csv,xlsx}`：可选叠加项目植物名称参考库；**只读中文名与分类章节**，规格/密度/苗价/综合单价等列一律不读、不写进输出；可重复指定。
- `--no-default-plant-library`：不加载全部内置区域库（`rules/plant_library_*.json`，默认全部加载）；只影响分类，不影响数量口径。
- 块引用 P2：底座 `meta.block_refs` 中只有总数、没有坐标的植物块引用，只作复核线索，`final_quantity=false`。

