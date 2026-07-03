# Linux mm Source-to-HTML Hierarchy Example

Session-specific pattern for a successful `background=true + notify_on_complete=true` Super-Router job that turns a large local source tree into a durable HTML explainer.

## Scenario

User requested: analyze `~/home_B/linux/mm/` and generate a self-contained HTML file containing:

- an elaborated hierarchy picture of the Linux `mm/` implementation;
- interpretation and description of what `mm` is responsible for;
- detailed workflows, principles, and source-reading guide;
- background execution via `exec(background=true, notify_on_complete=true)`.

## Durable technique

Use the generic `source-html-background-wrapper` pattern, but for a very large source tree add a deterministic local source inventory stage before invoking the router:

1. Create a run directory under `~/.openclaw/logs/<topic>_<timestamp>/`.
2. Write `collect_context.py` that scans source files and emits `context.json` with:
   - source path, file count, total lines/bytes;
   - Makefile object samples and Kconfig option samples;
   - subsystem buckets with file lists and line counts;
   - representative function/symbol samples with file:line provenance;
   - exported symbol samples where practical.
3. Write `make_router_prompt.py` that compacts `context.json` into a grounded `ROUTER_TASK`; do not stuff full source files into the prompt.
4. Write `generate_html.py` that builds the final self-contained HTML from `context.json` plus `super_router_stream.log`.
5. Write `run_<topic>_router.sh` that performs collection -> prompt -> `zsh -lic` router stream -> HTML generation -> verification.
6. Launch the wrapper with `exec(background=true, notify_on_complete=true)` and immediately `process(action="poll")` once.

## Linux mm bucket taxonomy that worked well

For `linux/mm/`, useful source-derived buckets were:

- Boot/init + topology: `memblock`, `mm_init`, `init-mm`, `sparse`, `sparse-vmemmap`, `numa`, `memory_hotplug`, `mmzone`.
- Physical pages + zones: `page_alloc`, `page_ext`, `page_owner`, `page_isolation`, `page_reporting`, `page_idle`, `compaction`, `shuffle`, `show_mem`.
- Virtual address spaces: `memory.c`, `mmap`, `mprotect`, `mremap`, `msync`, `mlock`, `vma`, `vmalloc`, `pagewalk`, `pgtable`, `mseal`.
- Page cache + file IO: `filemap`, `readahead`, `fadvise`, `truncate`, `page-writeback`, `backing-dev`, `mapping_dirty_helpers`.
- Reclaim + working set: `vmscan`, `workingset`, `shrinker`, `list_lru`, `vmpressure`, `damon`.
- Swap + compression: `swap`, `swapfile`, `swap_state`, `page_io`, `zswap`, `zsmalloc`, `zpool`, `zpdesc`.
- Kernel allocators: `slab`, `slub`, `mempool`, `percpu`, `page_frag_cache`, `dmapool`, `kasan`, `kmsan`, `kfence`, `kmemleak`.
- Huge pages + THP: `hugetlb`, `huge_memory`, `khugepaged`.
- Cgroups + policy: `memcontrol`, `mempolicy`, `memory-tiers`, `page_counter`, `bpf_memcontrol`, `swap_cgroup`, `hugetlb_cgroup`.
- Special mappings + reliability: `gup`, `userfaultfd`, `hmm`, `migrate`, `memory-failure`, `secretmem`, `memfd`, `cma`, `balloon`, `memremap`.

## Artifact shape

The generated HTML should be self-contained and include:

- source metrics near the top;
- a clear interpretation of `mm/` as the translation layer between memory intent and physical pages;
- an inline SVG hierarchy diagram;
- workflow cards for boot/init, page fault, page allocation/free, page cache IO, reclaim/swap, SLUB, memcg, huge pages/migration/failure;
- detailed `<details>` sections for subsystem buckets;
- Makefile/Kconfig/exported-symbol evidence;
- a provenance section with run dir, context JSON, router log, router exit, and log excerpt.

## Verification thresholds

Tune thresholds to catch a half-written artifact. For the Linux mm hierarchy guide, suitable minimums were approximately:

```bash
bytes >= 25000
sections >= 7
workflow cards >= 8
details >= 10
svg >= 1
```

The wrapper may still generate a valid artifact if the router provider exits non-zero, provided the HTML explicitly records the router failure and the content is grounded in verified local source inventory. Do not claim provider analysis succeeded when only the deterministic local collector and HTML generator succeeded.
