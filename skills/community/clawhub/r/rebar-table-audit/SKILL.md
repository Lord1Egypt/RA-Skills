---
name: rebar-table-audit
slug: rebar-table-audit
displayName: 钢筋数量表核对 / Rebar Table Audit
description: 从结构图纸（DWG/DXF）里找出设计方自带的“钢筋/材料工程数量表”（LINE 网格 + TEXT/MTEXT），还原成结构化表格，做 R001–R006 确定性算术核对（单根长×根数=总长、总长×单位理论重量=重量、行重量之和=表内声明合计等），输出 evidence.json、钢筋数量表.xlsx、report.md，每个单元格值和每条疑点都带图元 handle。适用于隧道/地下结构等算量审图场景，用户要“钢筋量”“导出钢筋表”“核对数量表”“钢筋表有没有算错”时使用。不适用：不做配筋图几何独立算钢筋（翻样），不处理扫描件/PDF/BIM 模型，不对算术不一致下“设计错误”结论。
summary: 从 DWG/DXF 图纸还原设计方自带的钢筋数量表并做确定性算术核对，只报疑点和图元证据，不下结论。
version: 0.1.0
license: MIT
homepage: https://github.com/dongsheng123132/rebar-table-audit
tags:
  - cad
  - dwg
  - dxf
  - rebar
  - quantity-takeoff
  - construction
author: 2Origin
metadata:
  openclaw:
    requires:
      bins:
        - python
    homepage: https://github.com/dongsheng123132/rebar-table-audit
---

# 钢筋数量表核对（rebar-table-audit）

## 这个 Skill 做什么

给一份 `.dwg` 或 `.dxf` 结构图纸，在其中找到设计方自己画的「钢筋/材料工程数量表」
（表头有编号/规格/根数/总长/重量之类的列，用 LINE 画格子，TEXT/MTEXT 填内容），
把它还原成结构化数据，跑几条确定性算术核对，然后：

- `evidence.json`：每个单元格值、每条疑点，都能点回原图的图元 handle。
- `钢筋数量表.xlsx`：汇总 / 明细 / 问题清单 / 证据缺口 / 符号映射五个工作表。
- `report.md`：中文人读报告。

**只报疑点，不下结论**——算术不一致只说「期望值 vs 实际值 + 证据 handle」，
是不是设计图纸本身画错了，由设计/造价人员自己核实原图。

## 不适用

- 从配筋图几何独立算钢筋（翻样）——这是完全不同的任务，本 Skill 不做。
- 图纸里根本没有数量表——退出码 3，不会凑数据。
- 扫描件、PDF 图纸、BIM 模型——只吃 AutoCAD 实体的 DWG/DXF。

## 安装依赖

需要 Python ≥3.10、`ezdxf>=1.4`、`openpyxl>=3.1`。Skill 装好后，在 Skill 目录里二选一：

**方式一：安装成命令**（之后直接用 `rebar-audit ...`）

```bash
# Windows
python -m pip install .
# macOS / Linux
python3 -m pip install .
```

**方式二：只装依赖**（之后在 Skill 目录里用 `python -m rebar_table_audit ...`，参数和 `rebar-audit ...` 完全相同）

```bash
# Windows
python -m pip install "ezdxf>=1.4" "openpyxl>=3.1"
python -m rebar_table_audit doctor
# macOS / Linux
python3 -m pip install "ezdxf>=1.4" "openpyxl>=3.1"
python3 -m rebar_table_audit doctor
```

如果输入是 `.dwg`，还需要下面二选一（都不随本包分发，用户自行安装）：

- **ODA File Converter**（免费，需在 [ODA 官网](https://www.opendesign.com/guestfiles/oda_file_converter) 接受条款后下载）。
- **GNU LibreDWG** 的 `dwg2dxf`（GPLv3，作为外部程序调用，本 Skill 不打包也不链接其代码）。

装好后设置环境变量 `ODA_FILE_CONVERTER` / `LIBREDWG_DWG2DXF` 指向可执行文件，
或放进自动探测路径（见 README.md「转换器探测」一节）。`.dxf` 输入不需要这一步。

## 怎么用

```bash
rebar-audit run 图纸.dwg --out ./out --converter auto
rebar-audit run 图纸.dxf --out ./out --json      # stdout 只输出一个 JSON 摘要
rebar-audit doctor --json                         # 查环境：Python/ezdxf/转换器版本与路径
```

`--symbols map.json` 可以覆盖/追加钢筋牌号符号映射（同图纸可能混用多种符号编码，
默认映射见 `rebar_table_audit/data/symbols.default.json` 和 `references/symbols.md`）。

退出码：`0` 无 error 级疑点；`2` 有 error 级疑点；`3` 未找到或未能还原任何数量表
（标题匹配上了但下方没有合格网格、或网格异常，也算在内——"找到标题"不等于"还原出表"）；
`1` 运行失败（转换失败、文件读不了等）。

`--json` 摘要里的 `tables` 是匹配上标题的次数，`tables_parsed` 才是真正还原出至少
一行数据的表数，`complete` 是"本次运行有没有任何 R005 证据缺口"（`gaps` 计数是否为 0）。
**`complete=false` 时不得向用户表述为"未发现问题"**——它只说明没有 error/warning 级
疑点，可能是因为有表格/符号/单元格没能解析，根本没被规则核对到，不是"核对过了、
没问题"。

## 核对规则（ID 稳定，可在报告里按 ID 引用）

| ID | 级别 | 检查 |
|---|---|---|
| R001 | error | 重量 ≈ 总长(m) × 单位理论重量(d)（GB 名义值与 0.00617d² 任一在容差内即过） |
| R002 | error | 有单根长和根数时：总长 ≈ 单根长 × 根数 |
| R003 | error | 各牌号行重量之和 ≈ 表内声明合计 |
| R004 | warning | 同一张表内钢筋编号重复 |
| R005 | gap | 符号 / 单元格 / 表结构无法解析——行保留，进证据缺口，不静默丢弃 |
| R006 | warning | 表头声明单位与算术反推单位不一致（"多数通过"判定：某候选单位通过行数唯一最高且 ≥60%/≥2 行才改判，并列或 n=1 则不改判，详见 README） |

## 已知边界

- 表格检测靠"标题下方搜索距离内、由近到远逐个试结构判据（≥2 条竖线相接、≥2 条水平
  线）"找上边框，再按包围盒连通收集网格线，并有列数/bbox 尺寸的健全性闸门挡掉明显
  异常的聚合结果；但同一图层里如果有别的线段恰好落在合格网格的包围盒范围内，仍可能
  被误收进同一张表——这是已知的简化，遇到了要靠 evidence.json 里的 handle 定位排查。
- 判定"最后一个非表头行带 = 合计/备注区"依赖编号列内容（不匹配编号正则的行带都会被
  当成合计池扫描），不依赖固定位置；但表头本身如果被画成两个独立行带（而不是同一
  行带里的多行文字），会被误判成两行无法识别的数据，需要人工核对报告里的证据缺口。
- 符号映射里标 `observed-in-sample` 的条目（如 `Ì`→HRB400、`%%201`→HPB300）来自
  2026-09-28 客户样图的实测，**同一份图纸换字体/换设计院可能对不上**，报告里会把
  本次实际用到的每条映射和次数都列出来，交给人工确认。
- 文字先做编码归一化（`\U+XXXX`/`\M+`/孤立代理项三种转换链差异统一处理，evidence
  同时留原文和归一化后文字）；规格格子解出的直径必须落在标准公称直径表内，否则记
  gap 不猜测（绝不用 0 或不合理值去算 R001）；牌号字面量不会被误当直径，未知牌号
  原文照录记 gap；无编号列的表遇到「合计/总计/总重」视为表体结束，之后再出现的
  类似表头行判定为未识别子表，不静默混进本表明细。细节见 README.md「证据边界」。

## 相关文件

- `references/symbols.md`：符号编码说明，及如何写自定义映射 JSON。
- `README.md`：安装、命令、退出码、证据边界更完整的说明。
