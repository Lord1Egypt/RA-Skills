# Queue Times — doc excerpts

Source: [Theme Park Wait Times API](https://queue-times.com/pages/api) (Queue Times).

## Real Time API

Live waiting times and ride statuses; data updated about every five minutes. Free use requires displaying “Powered by Queue-Times.com” linking to `https://queue-times.com/` somewhere prominent.

## URLs (canonical)

- All parks: `https://queue-times.com/parks.json`
- One park’s queue times: `https://queue-times.com/parks/{id}/queue_times.json` (replace `{id}`; example in official docs uses Thorpe Park as `2`)

## Example snippets (from official page)

`parks.json` returns groups with nested `parks` objects including `id`, `name`, `country`, `continent`, `latitude`, `longitude`, `timezone`.

`queue_times.json` returns `lands` with `rides` containing `id`, `name`, `is_open`, `wait_time`, `last_updated` (UTC).
