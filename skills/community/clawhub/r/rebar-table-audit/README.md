# rebar-table-audit

仓库：https://github.com/dongsheng123132/rebar-table-audit

从结构图纸（DWG/DXF）里找出设计方自带的「钢筋/材料工程数量表」，还原成结构化表格，
做确定性算术核对，输出 `evidence.json` + `钢筋数量表.xlsx` + `report.md`。
每个单元格值、每条疑点都带图元 handle，可以点回原图核实。

**不做什么**：不从配筋图几何独立算钢筋（翻样）；不处理扫描件/PDF/BIM 模型；
算术不一致只报「疑点 + 证据」，不下"设计错误"结论。

## 安装

从 GitHub 直接安装（需要 git）：

```bash
python -m pip install git+https://github.com/dongsheng123132/rebar-table-audit@v0.1.0
```

装好后命令是 `rebar-audit`；也可以不装命令、只装依赖后在仓库目录里用
`python -m rebar_table_audit ...`（参数相同）。

本地开发安装（克隆仓库后）：

```bash
python -m venv .venv
# Windows
./.venv/Scripts/python.exe -m pip install -e .
# macOS/Linux
./.venv/bin/python -m pip install -e .
```

依赖：Python ≥3.10、`ezdxf>=1.4`、`openpyxl>=3.1`（跑测试再加 `pytest`：
`pip install -e ".[dev]"`）。

### DWG 转换器（自行安装，二选一）

本包**不打包、不分发**任何转换器，只在运行时探测本机是否装了下面之一：

| 工具 | 许可证 | 获取方式 | 探测顺序 |
|---|---|---|---|
| ODA File Converter | 免费（需接受官网条款） | [opendesign.com](https://www.opendesign.com/guestfiles/oda_file_converter) 下载安装 | 环境变量 `ODA_FILE_CONVERTER` → `C:\Program Files\ODA\*\ODAFileConverter.exe`（及 x86 目录） |
| GNU LibreDWG `dwg2dxf` | GPLv3，作为外部程序调用 | 各平台包管理器或源码编译 | 环境变量 `LIBREDWG_DWG2DXF` → `~/.uking/tools/libredwg-*/dwg2dxf.exe` → PATH 上的 `dwg2dxf` |

`--converter auto`（默认）按上表顺序先试 ODA 再试 LibreDWG；也可以用
`--converter oda` / `--converter libredwg` 强制指定。转换器的可执行文件路径
只通过环境变量或上述自动探测拿到，代码里不写死任何具体机器上的安装路径。

ODA File Converter 只接受"目录"做输入输出，本包会把源文件拷进一个临时目录再调用；
它转换失败时也可能返回退出码 0，所以判定成败一律看"目标 DXF 文件是否真的生成"，
不看退出码。

输入本身就是 `.dxf` 时不需要装任何转换器。

## 命令

```bash
rebar-audit run <图纸.dwg|.dxf> --out <输出目录> [--symbols map.json] [--converter auto|oda|libredwg] [--json]
rebar-audit doctor [--json]
```

- `run`：抽取 + 核对，写出 `evidence.json` / `钢筋数量表.xlsx` / `report.md` 到 `--out` 目录。
  `--json` 时 **stdout 只输出一个 JSON 摘要**（`tables`/`tables_parsed`/`complete`/疑点按
  级别计数/输出文件路径），所有过程日志（转换进度、跳过的图元、抽取到的数量）都走
  stderr，不会混进 stdout。
- `doctor`：报告 Python / ezdxf / openpyxl 版本，以及探测到的转换器路径与版本
  （能取到版本就取，取不到留 `null`，不是失败）。

### 退出码

`run` 子命令：

| 码 | 含义 |
|---|---|
| 0 | 运行成功，没有 error 级疑点 |
| 2 | 运行成功，但存在 error 级疑点（R001/R002/R003） |
| 3 | 未找到或未能还原任何数量表——包括标题匹配上了、但下方没有合格网格（可能只是标题下划线）或网格连通聚合结果异常（列数过多/bbox 离题过大）这两种"看起来找到了标题，其实没还原出表"的情况；仍会写出 evidence.json 等文件，方便排查 |
| 1 | 运行失败（DWG 转换失败、DXF 读取失败、输入文件不存在等） |

`--json` 摘要字段：`tables` 是匹配上标题的次数；`tables_parsed` 是其中真正还原出
至少一行数据的表数（决定退出码是否为 3 看的是这个字段，不是 `tables`）；`complete`
表示这次运行是否**没有任何** R005 证据缺口（`gaps` 计数是否为 0）。
**`complete=false` 时不得向用户表述为"未发现问题"**：没有 error/warning 疑点，
可能只是因为有表格/符号/单元格没能解析、规则根本没跑到，不等于"核对过了、没问题"。

## 证据边界

- `evidence.json` 的 `schema` 字段是 `"rebar-table-audit/1"`；`source` 记录原始文件的
  basename/sha256/字节数/DXF 版本；`conversion` 记录用了哪个转换器、版本、生成 DXF 的
  sha256（如果输入本身是 dxf，`tool` 为 `null`）；`tables[].rows[].cells[].handles` 和
  `findings[].handles` / `gaps[].handles` 是图元 handle 路径，格式
  `INSERT:<handle>>INSERT:<handle>>...>TEXT:<handle>`——每一段的 handle 都是"定义处"
  的真实 handle（块参照内部的虚拟实体用 `source_of_copy` 找回块定义里的真实 handle），
  同一份输入重复跑，`evidence.json` 除 `generated_at` 外内容完全一致。
- DXF 读取：`ezdxf.readfile` 优先，失败则 `ezdxf.recover.readfile` 兜底，
  `conversion.recover_used` / `conversion.recover_error_count` 记录是否走了兜底以及
  auditor 报出的结构错误数。
- 找表：标题文字匹配「(钢筋|材料|工程)?...(数量|材料|明细)表」，在标题下方、搜索距离
  内（标题字高 ×8）的水平线里由近到远逐个试结构判据——收集网格后要求 ≥2 条竖线与
  候选线相接、且总共 ≥2 条水平线才接受，否则试下一条——标题下划线、分隔短线因为没
  有竖线相接会被自然跳过，不会被误判成表格上边框。候选线的横向匹配容差 ≤1×标题
  字高（不是全图统一的固定值，也不是网格收集用的 0.35×标题字高那档更紧的容差），
  避免隔壁表的顶线被误收进候选池；同一水平位置有多条候选线时优先试线中心离标题
  x 最近的那条，已经被别的标题占用的候选线跳过继续试下一条（不直接放弃整张表）——
  这样多张同版式表左右并排、顶线恰好同一个 y 时，各自能认领自己下方的网格。网格
  收集阶段的容差按每张表自己的标题字高算（0.35×标题字高，缺失才回退到整图文字
  高度中位数），避免同一张图混排不同比例尺时一个全局容差顾不上所有表。找到合格
  上边框后按包围盒连通收集网格线，竖线 x 聚类得列边界，横线 y 聚类得行带；如果聚
  合结果列数超过 20、或 bbox 宽/高超过"标题字高×300"
  （`rebar_table_audit/tables.py` 里的 `MAX_TABLE_COLUMNS` / `MAX_TABLE_SPAN_TITLE_HEIGHT_MULTIPLE`），
  判定为吸入了不相关线段的异常网格，记 R005 gap，不吐出垃圾表。首行带是表头，按关键
  词映射成列键（mark/position/spec/single_length/count/total_length/weight/unit_weight）。
  其余行带里，编号列文本匹配编号正则（或圆圈数字①-⑳）的算数据行，其余划入"合计/
  备注池"：池内文字按 y 聚类成行，同一行内文字按 x 拼接后再用正则抓 `牌号:数值kg/t`
  声明合计。
- 标题匹配上了、但搜索范围内找不到任何满足结构判据的网格（也不会被静默跳过：产出
  一条空表 + R005 gap（`tables_parsed` 不计入这种表，退出码按 3 处理）。
- 找不到编号列的表（结构不是常规钢筋表）不会被静默跳过：所有非表头行带按行抽取
  明细（mark 留空），记一条 R005 gap 说明抽取方式，规则该不适用就不适用，不强行凑数。
  这类表遇到命中「合计/总计/总重」关键词的行带（`BODY_END_KEYWORDS`）即视为表体
  结束——这一行本身留给合计/备注池抓声明合计，不算数据行；结束之后如果又出现一段
  形似表头的行带（疑似另起了一张子表），连同其下面的行都不当作本表数据行、不静默
  混进本表明细，只记一条"未识别子表"的 R005 gap。
- 文本规范化：从 DWG/DXF 抽出的文字先做一次编码归一化才参与后续匹配/解析
  （`rebar_table_audit/extract.py::normalize_text`）——LibreDWG 常把控制字符写成
  `\U+XXXX` 这种 DXF unicode 转义、`\M+` 这种 MIF 编码，ODA 转换链则可能直接给出
  已解码字符或让 ezdxf 用 surrogateescape 语义兜底产出孤立代理项（U+DC80~U+DCFF，
  按其 latin-1 恒等映射还原回原字节对应字符）；三种情况都会被归一化成同一种表示。
  `TextItem.text` 是归一化后的文字，`TextItem.raw` 保留归一化前的原始文字，两者都
  写进 `evidence.json`，方便对比审核同一符号在不同转换链下的原始写法。
- 规格单元格解析：直径必须落在 GB/T 1499 标准公称直径表内
  （`rebar_table_audit/tables.py::_VALID_DIAMETERS_MM`），否则视为解析错误——置空
  `diameter_mm` + 记 R005 gap，绝不会拿 0 或其它不合理数值当直径去算 R001 期望重量。
  牌号字面量（如"HRB400"）里的数字不会被误当直径：先从文本里把命中的牌号 token
  挖掉，再在剩余文本里找直径数字。形似牌号（`H[PR]B`+三位数字）但不在已知牌号列表
  里的（如 HRB300），原文照录记一条"未知牌号"的 R005 gap，不猜测归入已知牌号。
- R006（总长单位反推）改为"多数通过"判定，不再要求某个替代单位让全部适用行都
  通过才改判：对声明单位与每个候选单位分别统计通过行数 k(u)（n 为适用行数），
  某候选单位 u 同时满足 k(u) ≥ max(2, ⌈0.6·n⌉)、k(u) > k(声明单位)、且 u 是所有
  候选里 k 值唯一最大的（并列则谁都不采纳，保持声明单位）才会被采纳为推断单位；
  n=1 时样本不足，不做反推。采纳后 R001 用推断单位重新核对所有行，原来被"单位算
  错但自身也真错"的行不会再被单位反推连带放过，会继续以推断单位报 R001。
- 符号解码在 `rebar_table_audit/data/symbols.default.json` + `--symbols` 追加/覆盖，
  未识别的符号记 R005 gap，行仍保留在明细里；报告里列出本次实际用到的每条映射及次数。

## 测试

```bash
./.venv/Scripts/python.exe -m pytest -q
```

`tests/make_fixtures.py` 用 `ezdxf` 现造 DXF 夹具（LINE 网格 + 居中对齐 TEXT），
不含任何真实客户图纸数据。真实样图只用来本地冒烟（"跑起来不崩"），不进仓、
不用来反调规则或容差。

## 许可证

MIT，见 [LICENSE](LICENSE)。ODA File Converter 与 GNU LibreDWG
是用户自行安装的外部程序，各自遵循其自身许可证（ODA 使用条款 / GPLv3），
本包不分发也不链接它们的代码。
