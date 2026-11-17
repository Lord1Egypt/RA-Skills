# python_api.md — Python API 参考（中文版）

> **何时读我**：在 Python 代码/流水线里直接调用 verify_pmids 模块（而非命令行）时。
> 整个工具是纯标准库 Python 模块（v6.4.0 起分为入口文件+六个 pv_* 同级模块，公共 API 逐名重导出）——`import` 即用，无需安装任何依赖。
> 可运行示例：[api_examples.md](api_examples.md)；EN 用户读同目录 `python_api.md` 历史
> 版本或直接读本页代码块（代码即接口）。
> **回** [INDEX.md](INDEX.md)

## 快速开始（30 秒）

```python
import sys
sys.path.insert(0, "/path/to/pubmed-verifier/scripts")
import verify_pmids as vp

# 1) 拉注册库元数据（NCBI，失败自动切 Europe PMC）
info = vp.fetch_summaries(["31018962"], batch_size=1)["31018962"]

# 2) 声称元数据 vs 注册元数据 → 五态判定
cross = vp.cross_check_citation(
    {"claimed_title": "Classification criteria for autoinflammatory recurrent fevers",
     "claimed_authors": "Gattorno",
     "claimed_journal": "Ann Rheum Dis",
     "claimed_year": "2019"},
    {"title": info["title"], "authors": info["authors"],
     "journal": info["journal"], "pubdate": info["pubdate"]})
print(cross["verdict"], round(cross["confidence"], 2))   # correct 0.9x
```

要点：`cross["verdict"]` ∈ correct/mismatch/partial/invalid/unknown；
`evidence` 字典逐字段给出 title/author/journal/year 比对结果；
网络故障一律 `unknown`，绝不报「不存在」。

## 1. Batch metadata for PMIDs

> 批量拉取 PMID 注册元数据（标题/作者/期刊/年份），NCBI 批 50 条，失败批次自动降级 Europe PMC。

```python
info = vp.fetch_summaries(["31018962", "22213727"])   # NCBI, EPMC fallback
r = info["31018962"]
print(r["valid"], r["title"], r["journal"], r.get("retracted"))
```

## 2. Cross-check claimed vs registered metadata (the five-state ladder)

> 五态判定阶梯：声称元数据 vs 注册元数据逐字段比对，返回 verdict/confidence/evidence。

```python
cross = vp.cross_check_citation(
    {"claimed_title": "Classification criteria for autoinflammatory recurrent fevers",
     "claimed_authors": ["Gattorno"], "claimed_journal": "Ann Rheum Dis",
     "claimed_year": "2019"},
    {"title": r["title"], "authors": r["authors"],
     "journal": r["journal"], "pubdate": r["pubdate"]})
print(cross["verdict"], cross["details"])
# verdict ∈ correct / mismatch / partial / unknown
```

`claimed` / `actual` keys are plain strings/lists — feed them from any
source (database, form, LLM extraction). Cross-language CJK↔Latin author
names (and, since v3.9.0, CJK↔Latin titles) are skipped honestly, never
counted as misses.

## 3. DOI-native verification

> DOI 原生核验：Crossref 解析，404=伪造信号（显式输入），关联 PMID 走 Europe PMC。

```python
res = vp.resolve_doi("10.1038/nature12968")     # Crossref resolve (+retraction)
entry, audit = vp.verify_doi_entry(
    "10.1038/nature12968", "cli", resolution=res,
    claimed={"claimed_title": "...", "claimed_year": "2014"})
print(entry["verdict"], entry.get("retracted"))
```

## 4. Context parsing (extract claims from free text)

> 上下文解析：从自由文本提取声称元数据（启发式；CJK 见边界表）。

```python
claimed = vp.parse_citation_context(
    "Gattorno A, Van Dijk M. Classification criteria for autoinflammatory "
    "recurrent fevers. Ann Rheum Dis. 2019. PMID: 31018962")
print(claimed)
# GB/T 7714 Chinese references are recognized since v3.9.0 (title via the
# [J]/[M] type marker; the title comparison itself is cross-language-skipped)
```

## 5. Suggestions for broken citations

> 坏引用修复建议：对 mismatch 用声称元数据搜 PubMed，给 top-3 候选。

```python
cands = vp.suggest_correct_pmid({"claimed_title": "Juvenile idiopathic arthritis",
                                 "claimed_journal": "Pediatric Rheumatology"})
for c in cands[:3]:
    print(c["pmid"], c["title"][:60])   # abbreviated journal names can return [] — use the full NLM name
```

## 6. Plain-text reference lists & formatted output (v4.0.0)

> 纯文本参考文献表解析 + 四种引文格式排版输出（GB/T/Vancouver/APA/AMA）+ BibTeX/RIS/CSL 导出。

```python
entries, issues = vp.parse_plaintext_references("refs_list.txt")
for e in entries:
    print(e["key"], e["pmid"] or e["doi"] or e["arxiv_id"] or
          "(title search)", e["claimed_title"][:50])

# One markerless entry, verified by title search (honest route label):
res, audit = vp.verify_title_entry(entries[0], "refs_list.txt")
print(res["verdict"], res.get("resolved_by"))   # correct title_search

# Render verified results as a numbered reference list:
print(vp.generate_reference_list(results, "gbt"))       # also: gbty / vancouver / apa / ama

# Bibliography exports on verified results (same inclusion rules:
# correct in, partial in with a note, retracted/mismatch/unknown out):
print(vp.generate_bibtex(results))     # @article entries
print(vp.generate_ris(results))        # RIS records
print(vp.generate_csl_json(results))   # CSL JSON array (v5.6.0) — Zotero: File > Import
```

`parse_citation_context` accepts markerless Latin references since v4.0.0
(returns `claimed_source_format: "plaintext"`); CJK entries without a
PMID marker stay with the weak-parsing boundary.

## 注意事项

- **速率礼仪**：模块内建退避/UA 轮换/断路器；长期跑批请配 `--ncbi-api-key`
  对应的 `vp._OPTS["ncbi_key"]`（或环境变量 `NCBI_API_KEY`）。
- **缓存**：`vp._cache_path()`/`_cache_init()`/`_cache_load()`/`_cache_save_fresh()`
  是命令行缓存层；直接调 `fetch_summaries` 不走缓存。
- **判定语义**：`unknown`=源不可达（可重试）；`invalid`=已核实不存在。
  自动抽取的 DOI 查无≠伪造（先 doi.org 人工复核）。
- **全旗标清单**：[flags.md](flags.md)；运维/代理/批量：[operations.md](operations.md)；
  报错速查：[troubleshooting_ZH.md](troubleshooting_ZH.md)。
