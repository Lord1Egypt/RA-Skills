-- Session token ledger query templates

-- Overall
SELECT * FROM overall_summary;

-- Daily
SELECT * FROM daily_summary ORDER BY date DESC;
SELECT * FROM daily_efficiency ORDER BY date DESC;

-- Largest / fattest
SELECT * FROM largest_sessions LIMIT 20;
SELECT * FROM bloated_sessions LIMIT 20;
SELECT * FROM top_context_hogs LIMIT 20;

-- Efficiency / waste hunting for subscription users
SELECT * FROM usage_efficiency LIMIT 20;
SELECT * FROM channel_efficiency;

-- By model / provider / channel
SELECT * FROM model_summary;
SELECT * FROM provider_summary;
SELECT * FROM channel_summary;

-- Cost estimate only where applicable
SELECT * FROM cost_estimate LIMIT 20;

-- Suspicious sessions
SELECT session_id, transcript_file, bad_lines, usage_entries, total_tokens
FROM sessions
WHERE bad_lines > 0 OR usage_entries = 0 OR total_tokens = 0
ORDER BY bad_lines DESC, total_tokens ASC;

-- Telegram only
SELECT date, COUNT(*) AS sessions, SUM(total_tokens) AS total_tokens
FROM sessions
WHERE channel = 'telegram'
GROUP BY date
ORDER BY date DESC;
