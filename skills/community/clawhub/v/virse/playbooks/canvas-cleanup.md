# Canvas Cleanup

Audit and organize a messy canvas.

**Trigger keywords:** "clean up", "organize", "find orphans", "tidy up canvas"

## Steps

1. **Get state** — `get_canvas(canvas_id=..., include_group_detail=true)`
2. **Analyze** — Identify:
   - Disconnected elements (no edges)
   - Spatial clusters (close together but ungrouped)
   - Overlapping elements (similar position ranges)
   - Empty/single-member groups
   - Outlier elements far from main content
3. **Report & ask** — Present audit findings and suggested actions to the user. **Get explicit confirmation before making any changes.** Never delete without confirmation.
4. **Apply** — Based on user choices:
   - Re-layout: `update_element` to reposition into clean grid
   - Group clusters: `create_group(element_ids=[...])`
   - Remove orphans: `delete_element` (only after user confirms)
5. **Verify** — Run `get_canvas` to verify final state. Report element count before and after cleanup.

## Output

Before/after comparison: elements, edges, groups counts (before → after).
