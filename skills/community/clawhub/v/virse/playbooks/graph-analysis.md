# Graph Analysis

Analyze a canvas as a directed graph — find roots, hubs, chains, and isolated nodes.

**Trigger keywords:** "分析图结构", "graph structure", "工作流结构", "workflow structure", "根节点", "root nodes", "画布拓扑", "canvas topology"

## Steps

1. **Get workspace** — `list_workspaces` → save `canvas_id` and `space_id` for the target workspace
2. **Run graph analysis** — Pipe `get_canvas` output to the analysis script:
   ```bash
   python3 ${SKILL_DIR}/scripts/virse_call.py call get_canvas '{"canvas_id":"CANVAS_ID"}' | python3 ${SKILL_DIR}/scripts/graph_analysis.py
   ```
   For machine-readable output, add `--format json`.
3. **Present summary** — Show the user:
   - Total nodes, edges, connected components
   - Root nodes (workflow entry points): count and list
   - Hub nodes (highly connected, degree >= 4): count and list
   - Sink nodes (terminal outputs): count
   - Isolated nodes (no connections): count
   - Chain depths from each root
4. **Optional deep-dive** — If the user wants to explore specific nodes:
   - Use `get_element` to inspect a root or hub node
   - Use `get_asset_detail` to see generation details (prompt, model)
   - Use `trace_connections` to explore a specific chain in detail
5. **Cleanup suggestion** — If there are many isolated nodes, suggest running the `canvas-cleanup.md` playbook to audit and organize them.

## Output

Graph analysis summary: node/edge counts, classified node lists, chain traces from roots, component breakdown, and isolated node report.
