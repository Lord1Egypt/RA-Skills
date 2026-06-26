# Platform Transport Rules

These examples are transport-only snippets. They show how to write fresh payload files and pass
`--*-file` flags. They are **not** full scout-run command shapes; the authoritative run commands
live in `onboarding.md`, `search-workflow.md`, `scoring-and-trips.md`, and `delivery-and-audit.md`.

<json-file-rule>
- Use `cache_dir` from the latest successful `init-skill` output as the only transport directory for structured JSON payloads.
- Use the `cache_dir` string **verbatim** — it is emitted with forward slashes on every platform (including Windows, e.g. `C:/Weekend-Scout/.weekend_scout/cache`). Do not substitute backslashes or rebuild the path from platform-native components; bash eats unquoted backslashes and the `--*-file` argument will be silently corrupted.
- For any `python -m weekend_scout ...` command that passes structured JSON, write the payload to a fresh UTF-8 file inside that `cache_dir`, then pass the matching `--*-file` flag.
- Never pass structured JSON inline during a skill run.
- Do **not** stage payloads through `/tmp`, `%TEMP%`, or other ad hoc OS temp directories.
- Use `_tmp_*.tmp` filenames only for one-call transport payloads.
- When one command uses multiple `--*-file` flags, each flag must use its own file path.
- The CLI auto-deletes `_tmp_*.tmp` files after successful commands, so always write a fresh file immediately before the matching CLI call.
- Reuse the same cache directory, but do not assume any earlier `_tmp_*.tmp` file still exists.
- On platforms that expose both shell and `Write`, do **not** use `Write` to create brand-new transport payload files. Create them through the shell tool instead.
</json-file-rule>

<recommended-paths>
- `setup_json_path` -> `<cache_dir>/_tmp_setup.tmp`
- `detail_json_path` -> `<cache_dir>/_tmp_detail.tmp`
- `cities_json_path` -> `<cache_dir>/_tmp_cities.tmp`
- `events_json_path` -> `<cache_dir>/_tmp_events.tmp`
- `city_events_json_path` -> `<cache_dir>/_tmp_city_events.tmp`
- `trips_json_path` -> `<cache_dir>/_tmp_trips.tmp`
- `delivery_stats_json_path` -> `<cache_dir>/_tmp_delivery_stats.tmp`
- `delivery_notes_json_path` -> `<cache_dir>/_tmp_delivery_notes.tmp`
</recommended-paths>

<powershell-example>
```powershell
$cache_dir = '<cache_dir from init-skill>'
$payload_path = Join-Path $cache_dir '_tmp_detail.tmp'
'{"reason":"<skip_reason>"}' | Set-Content -LiteralPath $payload_path -Encoding utf8
python -m weekend_scout log-action --action skip --detail-file "$payload_path"
```
</powershell-example>

<setup-powershell-example>
Use this exact pattern for onboarding setup payloads:

```powershell
$cache_dir = '<cache_dir from init-skill>'
$setup_json_path = Join-Path $cache_dir '_tmp_setup.tmp'
'{"home_city":"<city>","home_country":"<country>","home_coordinates":{"lat":<lat>,"lon":<lon>},"radius_km":<radius>,"search_language":"<language>"}' | Set-Content -LiteralPath $setup_json_path -Encoding utf8
python -m weekend_scout setup --json-file "$setup_json_path"
```
</setup-powershell-example>

<posix-example>
```bash
cache_dir="<cache_dir from init-skill>"
payload_path="$cache_dir/_tmp_detail.tmp"
printf '%s' '{"reason":"<skip_reason>"}' > "$payload_path"
python -m weekend_scout log-action --action skip --detail-file "$payload_path"
```
</posix-example>

<setup-posix-example>
Use this exact pattern for onboarding setup payloads:

```bash
cache_dir="<cache_dir from init-skill>"
setup_json_path="$cache_dir/_tmp_setup.tmp"
printf '%s' '{"home_city":"<city>","home_country":"<country>","home_coordinates":{"lat":<lat>,"lon":<lon>},"radius_km":<radius>,"search_language":"<language>"}' > "$setup_json_path"
python -m weekend_scout setup --json-file "$setup_json_path"
```
</setup-posix-example>
