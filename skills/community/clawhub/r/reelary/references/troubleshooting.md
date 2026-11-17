# Troubleshooting

- `not_indexed`: nothing is indexed. Ask which folder holds their footage, then `reelary_add_folder` and poll `reelary_job_status` until `done`.
- `reindex_required`: the user switched search models. Ask them to open Reelary (`reelary_open_in_app`) and rebuild the index.
- `pro_required`: the feature or export size needs Reelary Pro. Tell the user plainly and share the `upgrade_url` once. Do not retry or work around the limit.
- `busy`: an index or export job is already running; poll the returned job id.
- "Reelary did not start": ask the user to open Reelary once by hand (macOS may ask to confirm the first launch), then retry.
- Empty or weak results: rephrase as what is visible ("a red car driving at night") rather than a story ("the chase"), try 2-3 phrasings, or check `reelary_list_folders` covers the right drive. External drives must be connected.
- Logs: Reelary > Settings > Open log folder.
