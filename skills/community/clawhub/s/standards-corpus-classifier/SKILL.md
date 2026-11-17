---
name: standards-corpus-classifier
description: |-
  将一批标准 PDF（国家 GB / 行业 QX·JB·YY… / 地方 DB11·DB31…）按「级别 × 领域」自动归置：
  解析文件名中的标准代号，查注册表得级别与归属，按名称关键词分入编号领域子文件夹，
  并产出 CSV 编目与 HTML 可视化报告，支持按分类/年份/标准号/名称筛选打包下载。
  This skill should be used when a user has a folder of standard PDFs
  (国家标准/行业标准/地方标准/团体标准/企业标准) and wants them classified, organized
  into domain subfolders, or inventoried — e.g. "把这批标准按建筑、食品、交通等分类",
  "整理一下地方标准文件夹", "给这些 PDF 出个分类目录", "下载某分类/某年度标准".
version: 1.0.0
license: MIT-0
emoji: "🗂️"
author: "老王子建工老孟"
tags: [standards, classification, pdf, china-standards, 标准语料, 归档]
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# 标准语料库分类（级别 × 领域）

把零散的标准 PDF 沉淀为可检索的语料库：按**级别**（国家/行业/地方，来自标准代号前缀）
与**领域**（建筑/交通/农林/环境…，来自标准名称关键词）双重归类，移入 `01_领域` 编号
子文件夹，并生成 `standards_categorized.csv` 编目。

## 何时使用
- 用户有一批标准 PDF 需要**分类、整理进文件夹**或**出编目 CSV**。
- 用户提到按主题归类标准（建筑、食品、交通、环境、医疗…）。
- 用户的语料可能是国家(GB)、行业(QX/JB/YY/…)、地方(DB11 北京 / DB31 上海 / …) 任一级别。
- 支持扩展到任意省份/行业：编辑 `references/sources.json` 追加代号即可（无需联网）。

## 核心机制（关键洞察）
标准代号前缀天然编码「级别 + 归属」：
- `GB` / `GB_T` → 国家；`QX` → 气象行业；`DB11` → 北京地方；`DB31` → 上海地方……
- 领域分类（关键词）与级别**正交**，因此一套分类引擎通吃所有级别。

## 用法
脚本位于 `scripts/classify_standards.py`，从自身位置自动加载 `references/sources.json`
与 `references/domains.json`：

```bash
# 干跑（仅统计，不移动、不写文件）
python scripts/classify_standards.py CORPUS_DIR --dry

# 实际执行：递归扫描 CORPUS_DIR 下所有 PDF，
# 分类后写入 CORPUS_DIR/pdfs/01_领域/…，并生成 CORPUS_DIR/standards_categorized.csv
python scripts/classify_standards.py CORPUS_DIR
```

参数：
- `CORPUS_DIR`：含 PDF 的目录。脚本**递归扫描**，所以 PDF 放在根目录或 `pdfs/` 子目录均可；
  已正确归位的文件会被跳过，放错的文件会自动挪正（可重复运行）。
- `--dry`：仅预览，不动文件。
- `--sources PATH` / `--domains PATH`：覆盖默认注册表 / 领域表（用于 per-corpus 定制）。
- `--out SUBDIR`：PDF 输出子目录名，默认 `pdfs`。

输出 `standards_categorized.csv` 列：领域 / 级别 / 归属 / 标准类型(强制·推荐) / 年份 /
标准号 / 名称 / 子文件夹。

## 可视化 HTML 报告（自包含 / 离线可用）
分类完成后，用 `scripts/make_report.py` 把 CSV 渲染成一份可双击打开的 HTML 报告
（统计卡片 + 领域分布条形图 + 年份分布图 + 级别/归属占比 + 可展开领域明细）。
**无任何外部 CDN 依赖**，断网也能看。

```bash
# 读取 classify_standards.py 产出的 CSV，生成报告
python scripts/make_report.py CORPUS_DIR/standards_categorized.csv \
    --title "北京市地方标准(DB11)" \
    --out CORPUS_DIR/分类可视化报告.html
```
- `--title`：报告标题（默认「标准语料分类报告」）。
- `--out`：输出 HTML 路径（默认 `report.html`）。
- 报告内「领域明细」用 `<details>` 折叠，默认收起，点击展开可看该领域全部标准号+名称。
- 报告另含「按年份浏览」折叠区：每年显示总数、领域分布与可展开标准列表。

## 按年份归类与导出（下载子集）
除"按领域"分类外，支持"按发布年份"维度与"下载子集"：
- **建年度文件夹**：分类时加 `--year-folders`，在 `<CORPUS>/by_year/YYYY/` 下用**硬链接**复制出按年份组织的视图（与领域文件夹指向同一文件，不占额外磁盘）。
- **CSV 含「文件名」列**：导出时据此精确定位源文件。
- **导出/下载某一分类、某一年度，或按标准号/名称模糊查找**：`scripts/export_standards.py` 按 `--domain` / `--year` / `--stdno`(标准号) / `--name`(标准名称) 过滤 CSV，把匹配 PDF 打包成 zip（即"下载该子集"）。各条件为 **AND 组合**；`--stdno` / `--name` 为**子串模糊匹配（忽略大小写）**；`--list` 仅预览不打包。

```bash
# 下载（导出）某一分类
python scripts/export_standards.py CORPUS_DIR/standards_categorized.csv --domain 安全生产 --out 安全生产.zip
# 下载（导出）某一年度
python scripts/export_standards.py CORPUS_DIR/standards_categorized.csv --year 2024 --out 2024年度.zip
# 按标准号模糊查找下载（如含 1031 的全部标准）
python scripts/export_standards.py CORPUS_DIR/standards_categorized.csv --stdno 1031 --out 含1031.zip
# 按标准名称模糊查找下载
python scripts/export_standards.py CORPUS_DIR/standards_categorized.csv --name 大气污染物 --out 大气污染物.zip
# 组合：某分类 + 某年度 + 名称关键词
python scripts/export_standards.py CORPUS_DIR/standards_categorized.csv --domain 安全生产 --year 2024 --name 加油站 --out 安全生产_2024_加油站.zip
# 全量导出（不指定任何过滤条件时默认拒绝，需显式 --all）
python scripts/export_standards.py CORPUS_DIR/standards_categorized.csv --all --out 全部标准.zip
```

**安全约束（对抗式审查已验证）**：
- 源文件严格限制在语料目录内：恶意 CSV 行用 `子文件夹=..` 指向语料外文件会被判为缺失、**不会**装入 zip（防路径遍历读取外泄）。
- zip 内部路径用 `_` 净化并拦截 `..`，**不会**出现 `../x.pdf` 这类逃逸项（防 zip-slip 解压越界）。
- CSV 缺失给出友好报错，不会抛 traceback。
- 不指定任何过滤条件时**默认拒绝**导出整个语料（防误下载数 GB）；确需全量请加 `--all`，或加 `--list` 仅预览。

## 事实一致性核验（防幻觉机制）
本技能的产出（CSV/PDF 归类/报告数字）**全部由确定性脚本从文件名+注册表算出，不调用任何 LLM**，
因此必须可验证、可追溯。发布前或每次重跑后，用 `verify_consistency.py` 断言以下不变量，
**任意一项失败即说明产物有错（或幻觉）**，必须修复后再发布：

```bash
# 核验 CSV 行数==实际PDF数、文件名可追溯、领域无空、标准号无重复、报告数字一致
python scripts/verify_consistency.py CORPUS_DIR \
    --report CORPUS_DIR/分类可视化报告.html
```

断言项：
1. `CSV 行数 == pdfs/ 下实际 PDF 文件数`（无丢行/多行）
2. 每行「文件名」都能在 `pdfs/<子文件夹>/<文件名>` 真实找到（无虚构条目）
3. 领域列无空值（无未归类）
4. 标准号无重复（无编造/重复计数）
5. 报告 HTML 中声称的总数 == CSV 行数

> 已实测：北京 DB11（2420 份，2003–2026，24 年度）、气象 QX（767 份，2000–2026，27 年度）
> 均通过以上 5 项断言，0 缺失 / 0 空领域 / 0 重复。

## 发布前自查（引用 skill-publish-checklist）
本技能上架前，除上面的事实一致性核验外，另需跑通用发布检查清单
`skill-publish-checklist` 做元数据 / 安全 / 署名 / 打包的端到端自查（二者配合，
前者管"产物无幻觉"，后者管"能安全上架"）：

```bash
python <skill-publish-checklist>/scripts/check_publish.py \
    <本技能所在目录>
```

该清单覆盖：frontmatter 字段齐全、危险 API 静态扫描、作者署名校验、
资源完整性、打包校验，输出 ✅/⚠️/❌ 结论。

## 真实官方平台链接（已内置）
`references/sources.json` 已预置全国 31 省/自治区/直辖市 + 深圳(计划单列市) 的
**专属平台**与**统一兜底平台**（公开汇总 + 联网核验，2026-08）：
- 国家：`https://std.samr.gov.cn/`（全文 `https://openstd.samr.gov.cn/`）
- 行业备案：`https://hbba.sacinfo.org.cn`
- 地方（覆盖全部 31 省/市/区）：`https://dbba.sacinfo.org.cn`
- 各省级 `portal` 见 `sources.json` 的 `local` 条目（如河南 `hndb41.com`、
  广东 `amr.gd.gov.cn/standard/`、深圳 `amr.sz.gov.cn/.../szsdfbz/`）。
> 注：部分省级站点可能更新域名或仅提供目录（不全文），以实际访问为准；
> 兜底平台 `dbba.sacinfo.org.cn` 永远可用。

## 扩展（用户加链接，无需联网）
- **加省份/行业**：在 `references/sources.json` 的 `local` / `industry` 下追加
  `"DBxx": {"name": "归属名", "level": "地方", "portal": "https://...", "aggregator": "https://dbba.sacinfo.org.cn"}`。
  此后凡含该代号的 PDF 都会自动标上正确级别/归属。
- **子级市自动回退**：`DB4403`(深圳) 等子级市代码若未单列，脚本自动回退到省级
  `DB44`(广东) 并标注子级代号，无需手动配置。
- **改领域集**：复制 `references/domains.json` 改成自定义领域与关键词，运行时用
  `--domains 自定义.json`。领域顺序即匹配优先级（靠前的先命中）。

## 已知坑与边界（务必注意）
1. **文件名含下划线+空格**：如 `DB11_ 2567-2026_名称.pdf`（北京强制性标准），
   不是 `DB11_T`。解析器按「首个空白切分」已兼容，但若手工构造正则须保留此容错。
2. **关键词首匹的边界误分**：分类按名称关键词首次命中，跨领域标准可能落错类
   （如「印刷工业大气污染物排放标准」因含「印刷」归入文化旅游而非环境）。
   缓解：在 `domains.json` 调关键词或顺序；属已知局限，非 bug。
3. **关键词碰撞**：如「蒸压**加气**混凝土」(建材) 易被能源类裸词「加气」」误命中——
   已改为「加气站」规避。新增关键词时留意类似子串碰撞。
4. **实时搜索（Phase 2 发现机制）**：发现未知省份/行业官网并固化，流程如下
   （agent 执行，脚本只做安全写回）：
   1. 遇到 `sources.json` 未登记的代号 → 用 WebSearch 搜「XX省 地方标准 信息公开平台」
      或「XX行业 标准 备案平台」，拿到官方网址；
   2. 调用 `scripts/discover_sources.py --code DBxx --name 归属 --portal https://...`
      安全写回（先自动备份 `sources.json.bak`）；
   3. 之后该代号即纳入注册表，下次直接命中。
   ```bash
   python scripts/discover_sources.py --code DB44 --name 广东 --portal https://amr.gd.gov.cn/standard/
   ```
5. **代号未配置**：未在 `sources.json` 登记的代号，仍按领域分类，级别/归属标为「未配置」；
   发现后可走上面 Phase 2 流程补录。

## 已验证语料（真实性背书）
本技能已在真实语料上跑通并通过 `verify_consistency.py` 全部断言：
- **北京 DB11 地方标准**：2420 份（2003–2026，24 年度），0 缺失 / 0 空领域 / 0 重复。
- **气象 QX 行业标准**：767 份（2000–2026，27 年度），并配套 `references/qx_domains.json`
  （12 类专属 taxonomy，可作 per-corpus 覆盖示例）。
