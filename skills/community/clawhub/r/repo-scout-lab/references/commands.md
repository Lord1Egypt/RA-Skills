# Repo Scout command map

Common commands:

- `repo-scout search [topic] [--topic-pack pack] [--limit 10] [--min-stars 100] [--language TypeScript] [--days 365]`
- `repo-scout ideas [topic] [--topic-pack pack] [--limit 12] [--ideas 6] [--llm]`
- `repo-scout report [topic] [--topic-pack pack] [--limit 12] [--ideas 6] [--out report.html]`
- `repo-scout brief [topic] [--topic-pack pack] [--limit 10] [--ideas 4]`
- `repo-scout trending [topic] [--limit 10] [--days 30]`
- `repo-scout history [--limit 20] [--kind ...] [--topic ...]`
- `repo-scout diff <oldRunId> <newRunId>` or `repo-scout diff --latest`
- `repo-scout dashboard [--days 60] [--preview-days 7] [--out examples/repo-scout-dashboard.html]`
- `repo-scout serve [--port 4040]`
- `repo-scout library top-repos|ideas|recurring-repos|topics|idea-families|opportunity-themes|startup-opportunities`
- `repo-scout bookmark add owner/repo [--note text]`
- `repo-scout bookmark refresh owner/repo|--all`
- `repo-scout bookmark movers [--limit 10]`
- `repo-scout spec|thesis|memo|next-actions|openclaw-prompt --latest --idea 1`

Good outputs to mention:

- `--format table` for quick inspection
- `--markdown` for shareable text
- `--json` for automation
- `--out` to save reports
