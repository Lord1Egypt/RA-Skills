# SLBrow Workflow (compact)

- **Tabs**: `tab_list` first, then pass `tab_id` to target background tabs.
- **Content**: `page_navigate` → `page_analyze`(intent_hint) → `page_extract_content`.
- **Forms**: `page_analyze`(intent_hint:"form submit") to get element IDs, then interact via element IDs.
- **VAI**: `get_page_seelink_player_list` first to get player IDs/count → `use_seelink_players_ai`(ai_function_name, player_position_list OR player_id_list, not both). Functions: reduce_fog, face_mosaic, dark_reduce, human_outline, vechicle_outline, none. Call separately per function.
- **Fallback (no MCP tools)**: `curl -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{"tool":"use_seelink_players_ai","args":{"player_position_list":[0],"ai_function_name":"face_mosaic"}}'`
