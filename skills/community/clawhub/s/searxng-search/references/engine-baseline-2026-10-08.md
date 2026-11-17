# Historical local SearXNG engine spot-check

Audit date: 2026-10-08. This is a one-query availability snapshot, not a quality benchmark or a statement about current status. It tested all 261 engines listed in that local `/config`, including disabled engines via shortcuts; no engine configuration was changed. Queries were broad and sometimes poorly matched to specialty engines. Empty results are inconclusive. Some requests may have encountered cached suspensions, CAPTCHA, rate limiting, timeouts, TLS, or parser errors. Recheck live inventory and status before relying on any entry.

## Useful historical signals

| Use | Returned results | Errors / limitations |
|---|---|---|
| General web | Google CSE (`goc`), DuckDuckGo Web (`ddgw`), Bing (`bi`), Wikipedia (`wp`) | Google (`go`) was access-denied; DuckDuckGo (`ddg`) CAPTCHA; Brave (`br`) rate-limited. |
| News | DuckDuckGo News (`ddn`), Bing News (`bin`), Naver News (`nvrn`) | Reuters returned HTTP error; Google News was access-denied. |
| Biomedical/science | Europe PMC (`epmc`), arXiv (`arx`), Crossref (`cr`), OpenAlex (`oa`), Google Scholar (`gos`) | PubMed (`pub`) rate-limited; Semantic Scholar (`se`) parser error; OpenAIRE publication/dataset endpoints timed out. The Google Scholar sample was book-heavy for the generic climate query. |
| Technical | Stack Overflow (`st`), Ask Ubuntu (`ubuntu`), Super User (`su`), MDN (`mdn`), Microsoft Learn (`msl`) | GitHub search (`gh`) was access-denied. |
| Translation | MyMemory translated (`tl`) | English “hello” to German returned “hallo”; one simple phrase only, so this is not a quality assessment. |

The audit used one broad query per engine (`python`, `climate change`, `nature`, `Mozart`, or `en-de hello`) and recorded status, attributed result count, errors, and a short sample. It did not establish completeness, ranking quality, freshness, long-term reliability, or suitability for an individual research question. Full records were supplied as `searxng-engine-check.jsonl`; the original checker is not used as a routine full-inventory probe.
