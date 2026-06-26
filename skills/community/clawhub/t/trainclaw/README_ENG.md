# TrainClaw 🚄

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/AI4MSE/TrainClaw/blob/master/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-AI4MSE%2FTrainClaw-black.svg)](https://github.com/AI4MSE/TrainClaw)

[中文](README.md) | English

A lightweight CLI tool for querying China Railway 12306 — **no login, no API key, plug & play**. Check remaining tickets, route stops, and transfer plans with a single command.

**3-in-1 China 12306 query: tickets + route stops + transfer plans, zero login.**

> More skills: flight query (FlyClaw), navigation (NavClaw), etc. See https://github.com/AI4MSE/

## Why TrainClaw?

- **Zero friction** — No login, no API key, no tokens. Just `pip install requests` and go.
- **Single-file** — One Python script (`trainclaw.py`) + one config file. Fully transparent, easy to audit.
- **Multi-format output** — `text` for humans, `json` for programs, `csv` for spreadsheets.
- **Rich filtering** — Filter by train type (G/D/Z/T/K), time window, sort by departure/arrival/duration.
- **Transfer planning** — Auto-recommend or specify transfer stations for multi-leg journeys.
- **OpenClaw skill** — Works as an OpenClaw AI skill out of the box (see `SKILL.md`).

## Install

```bash
# Requires Python 3.8+ and requests
pip install requests
```

## Usage

### Ticket Query

```bash
# Basic query — Beijing to Shanghai
python trainclaw.py query -f 北京 -t 上海

# Tomorrow's bullet trains, morning only, sorted by duration, top 5
python trainclaw.py query -f 北京 -t 上海 -d 2026-03-04 --type G \
  --earliest 8 --latest 12 --sort duration -n 5

# JSON output
python trainclaw.py query -f 南京 -t 杭州 --type D -o json

# CSV output
python trainclaw.py query -f 广州 -t 深圳 -o csv

# Verbose mode (debug HTTP requests to stderr)
python trainclaw.py -v query -f 北京 -t 上海
```

### Route Stops

```bash
python trainclaw.py route -c G1 -d 2026-03-04
python trainclaw.py route -c G1033 -o json
```

### Transfer Plans

```bash
# Auto-recommend transfer stations
python trainclaw.py transfer -f 深圳 -t 拉萨 -n 5

# Specify a transfer station
python trainclaw.py transfer -f 深圳 -t 拉萨 -m 西安 -d 2026-03-04
```

## Station Name Input

Three formats, auto-detected:

| Format | Example | Description |
|------|------|------|
| Exact station name | `北京南`, `上海虹桥` | Direct match |
| City name | `北京`, `上海` | Maps to the city's main station |
| 3-letter code | `BJP`, `SHH` | Used directly |

## Train Type Codes

| Code | Meaning |
|------|------|
| G | High-speed / Intercity (G/C prefix) |
| D | EMU (D prefix) |
| Z | Direct Express |
| T | Express |
| K | Fast |
| O | Other (non-GDZTK) |
| F | Fuxing (CR series) |
| S | Smart EMU |

Codes are combinable — e.g. `--type GD` matches both high-speed and EMU trains.

## Command Reference

### Common Parameters

| Parameter | Description | Default |
|------|------|--------|
| `-d, --date` | Query date (yyyy-MM-dd) | Today |
| `-o, --format` | Output format: text / json / csv | text |
| `-v, --verbose` | Enable debug logging to stderr | Off |

### Filter Parameters (query / transfer)

| Parameter | Description | Default |
|------|------|--------|
| `-f, --from` | Departure station (name / city / code) | **Required** |
| `-t, --to` | Arrival station (name / city / code) | **Required** |
| `--type` | Train type filter (see table above) | All |
| `--earliest` | Earliest departure hour (0–24) | 0 |
| `--latest` | Latest departure hour (0–24) | 24 |
| `--sort` | Sort by: startTime / arriveTime / duration | None |
| `--reverse` | Reverse sort order | No |
| `-n, --limit` | Max results | query: unlimited, transfer: 10 |

## Output Formats

### text (default)
```
Train | From→To | Depart→Arrive | Duration | Seats | Tags
G25   | 北京南→上海虹桥 | 17:00→21:18 | 04:18 | Business:1/¥2318, First:Avail/¥1060 | Fuxing
```

### json
Full JSON array with all fields — ideal for programmatic processing.

### csv (query only)
Standard CSV with headers — ready for spreadsheets and data analysis.

## Version

**Current**: 0.0.4

## Notes

1. Generally supports today + next 15 days only (12306 limitation).
2. First run downloads station data (~3000 stations), cached locally for 7 days.
3. Errors go to stderr, data to stdout — fully pipe-friendly.
4. Transfer results depend on 12306's recommendation algorithm.

## Disclaimer

This tool is for educational and technical research purposes only. Not recommended for production use. Please comply with local laws and regulations. This project is not affiliated with China Railway.

## Author

This is a community-driven, open-source skill — free for everyone.

- **Email**: nuaa02@gmail.com
- **Xiaohongshu (小红书)**: @深度连接
- **GitHub**: [AI4MSE/TrainClaw](https://github.com/AI4MSE/TrainClaw)

## License

[Apache License 2.0](LICENSE)
