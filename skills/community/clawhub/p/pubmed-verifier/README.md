# PubMed Citation Verifier 🔬

[![GitHub Stars](https://img.shields.io/github/stars/docsor1212/pubmed-verifier?style=social&label=Star)](https://github.com/docsor1212/pubmed-verifier/stargazers)

Batch-verify PMID citations against PubMed API. Built for researchers, medical writers, and evidence-based medicine teams.

## 简介（中文）

**PubMed 文献引用批量验证工具**——把引用列表交给它，逐条核验 PMID/DOI/arXiv ID 是否真实存在、是否指向你声称的那篇论文（AI 幻觉引用最常见的形态就是「真 PMID 指向别的论文」）。五态判定（正确/不匹配/部分匹配/无效/待确认），撤稿检测全覆盖，网络故障如实标注「未判定」、绝不误报「不存在」。零依赖、纯本地运行。

- **中文文献**：GB/T 7714 格式参考文献可解析（`……标题[J]. 刊名, 年… PMID: xxx`）；`--parse-text` 粘贴即核验整张文献表——行内 PMID/DOI 精确路由，中文条目经 OpenAlex 标题检索判定（无编号 ID 也能核）
- **参考文献格式化**：`--format-references --citation-style gbt`（另支持 Vancouver/APA/AMA/Harvard/Chicago），先验证后排版，只排已验真的条目
- **四数据源**：NCBI PubMed、Europe PMC 自动兜底、Crossref、OpenAlex（DataCite/Zenodo 等非 Crossref 注册的 DOI 也可判定）
- **投稿就绪判定 + 审计底稿**：每份报告自带证据链，`--export-audit` 输出可复放的 JSON 工作底稿

## Why?

**为什么要核验引用（中文）**：学术项目的参考文献动辄数百条，人工核对既繁琐又易漏。在我们自己一次 225 条参考文献的审计中，发现了 3 个无效 PMID 和 6 条跨领域错配——任何一条混进稿件都足以动摇整项工作。AI 生成内容的高频问题是「真 PMID 指向别的论文」，存在性检查根本查不出来。

Academic projects routinely contain hundreds of PMID citations. Manual verification is tedious and error-prone. During our own 225-reference audit, we found 3 invalid PMIDs and 6 cross-domain mismatches — errors that would have undermined the entire project.

## Features

Grouped by job. The scenario→command cheat sheet is `references/flags.md`, the full capability×limit table lives in the main `SKILL.md`, and `--help` prints the complete per-flag contract — one fact, one home.

**Verification core**

- Five-state verdicts (correct / mismatch / partial / invalid / unknown) — catches the most common AI hallucination: a REAL PMID pointing to a DIFFERENT paper
- Three ID types in one audit — PMIDs, DOIs (Crossref first, OpenAlex fallback for DataCite/Zenodo registries), arXiv preprints (published version surfaced); retraction detection on every citation plus correct-PMID replacement suggestions
- Inputs — project directories (`.docx`, `.pptx`, `.html`, JATS `.nxml`/`.xml`), pasted reference lists (`--parse-text`, numbered or prose, GB/T 7714 Chinese included), BibTeX/RIS bibliographies (format sniffed from content), structured claims JSON/CSV with offline `--lint-claims`

**Outputs & audits**

- HTML dashboard / JSON evidence chain / terminal summary, each led by a submission-readiness verdict
- `--report-bundle` one-command evidence pack; `--export-audit` replayable JSON working paper; `--diff` delta audits (a re-run sees only what changed)
- Verified-bibliography exports — BibTeX / RIS / CSL JSON (Zotero: File > Import); formatted reference lists (GB/T 7714 / Vancouver / APA / AMA / Harvard / Chicago) built from registry-verified records only

**Resilience & honesty**

- NCBI → Europe PMC automatic fallback; 429 Retry-After backoff, UA rotation, per-host circuit breaker, in-batch retry sweeps (`--retries`)
- Network failures grade `unknown` — never silently "not found", never cached; `--check-net` probes every source direct AND via proxy; `--self-check` verifies a downloaded copy offline

**Shape & docs**

- Zero dependencies, pure standard library, fully local; layered modules — one entry file plus six stdlib-only sibling modules under `scripts/`, far under static-reader ceilings; identical API via `import verify_pmids`
- Troubleshooting index (one error, one row), flags cheat sheet, operations playbook, Python API reference — routed from `references/INDEX.md`

## Quick Start

```bash
# Install
openclaw skills install docsor1212/pubmed-verifier

# Paste-and-verify a whole reference list (numbered or prose; GB/T 7714 Chinese included)
python3 scripts/verify_pmids.py --parse-text references.txt

# Verify specific PMIDs
python3 scripts/verify_pmids.py --pmids 31018962,22213727

# Network pre-flight: all four registries + arXiv, direct AND via your proxy
python3 scripts/verify_pmids.py --check-net
```

The skill's `SKILL.md` carries the ten-command quick start — the one-flag
pre-submission pass (`--quick`), claims-file verdicts, evidence bundles
(`--report-bundle`) and verified-list formatting (`--format-references`).

**China mirror (ModelScope 魔搭)**: <https://modelscope.cn/skills/Docsor/pubmed-verifier> — if you find this skill useful, a like there helps others find it.

## Use Cases

| Scenario | Example |
|----------|---------|
| **Systematic review QA** | Verify all 200+ references before submission |
| **Medical website audit** | Check evidence citations across clinical case library |
| **Paper manuscript check** | Validate every PMID in your draft |
| **Teaching material review** | Ensure lecture citations are accurate |
| **Evidence library maintenance** | Periodic batch verification of reference databases |
| **Draft reference list check & formatting** | Paste a manuscript's reference list, verify it, get a GB/T 7714 / APA list back |

## Real-World Results

Audited a 35-file pediatric rheumatology evidence library (225 PMID citations):
- **222** citations: valid and content-matched ✅
- **3** citations: invalid PMIDs found and corrected
- **6** cross-domain citations: correctly flagged, reviewed, confirmed appropriate
- Total time: ~5 minutes for full audit

## Technical Details

- **APIs**: PubMed E-utilities (esummary, esearch); Europe PMC fallback; Crossref DOI check
- **Rate limit**: 3 req/s free (0.4s batch delay), 10 req/s with `--ncbi-api-key` (0.12s)
- **Resilience**: 429 Retry-After backoff, 403/406 UA rotation, per-host circuit breaker
- **Batch size**: 50 PMIDs per request
- **File types**: `.html`, `.htm`, `.md`, `.txt`, `.json`, `.docx`, `.pptx`, `.nxml`, `.jats`, `.xml` (JATS/NLM since v6.0.0)
- **PMID patterns**: `PMID: 12345678`, `PubMed: 12345678`, `pubmed.ncbi.nlm.nih.gov/12345678/`
- **Exit codes**: 0 clean / 1 problems found (or a usage error) / 2 could-not-verify (network unreachable, or an invalid flag value — `[ERROR]` + exit 2 before any work since v5.8.0)

## License

MIT-0
