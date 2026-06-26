# Garmin Health Report

A standalone implementation of Garmin Connect health reporting using `garth` library.

## What's This?

This is a refactored version of `garmin-health-report` that simplifies dependencies by using the official Garmin Connect authentication library (`garth`) directly instead of the more complex `garmer` package.

## Why?

The original version required `garmer` which has installation issues. This version:

- ✅ **Uses only one dependency**: `garth` (official Garmin Connect library)
- ✅ **Simpler installation**: `pip3 install garth`
- ✅ **Same features**: All original functionality preserved
- ✅ **Better error handling**: Direct use of garth's stable authentication
- ✅ **Easier to debug**: Fewer layers of abstraction

## Installation

### 1. Install Dependencies

```bash
# Install garth (Garmin Connect authentication library)
pip3 install garth

# Verify Python version (requires 3.8+)
python3 --version
```

### 2. Authentication

First time setup requires authentication with Garmin Connect:

```bash
# Navigate to skill directory
cd ~/.agents/skills/garmin-health-report

# Run authentication script
python3 authenticate.py
```

Follow the prompts to enter your Garmin Connect username and password. Tokens will be securely stored in `~/.garmin-health-report/tokens.json`.

**For China Region Users (garmin.cn):**

Create a config file before authenticating:

```bash
mkdir -p ~/.garmin-health-report
cat > ~/.garmin-health-report/config.json << 'EOF'
{
  "is_cn": true,
  "log_level": "INFO"
}
EOF
```

Then run `python3 authenticate.py`.

### 3. Generate Health Report

```bash
# Today's report
python3 health_daily_report.py

# Specific date
python3 health_daily_report.py 2026-03-01

# Save to file
python3 health_daily_report.py > ~/health_report_$(date +%Y-%m-%d).txt
```

## Files

- `authenticate.py` - Garmin Connect OAuth2 authentication (using garth)
- `garmin_client.py` - Garmin Connect API client (using garth)
- `health_daily_report.py` - Main report generator
- `SKILL.md` - Skill documentation and usage guide
- `README.md` - This file
- `LICENSE` - MIT License

## Usage

```bash
# Test authentication
python3 authenticate.py

# Generate report
python3 health_daily_report.py

# Generate report for specific date
python3 health_daily_report.py 2026-03-01
```

## Features

All original features are preserved:

- **Sleep Analysis**: Duration, stages (deep/light/REM), scores, HRV
- **Heart Rate Monitoring**: Resting HR with recovery status
- **Activity Tracking**: Steps, distance, floors, goal completion
- **Professional Running Metrics**:
  - Heart Rate Zones (Zone 1-5 distribution)
  - TRIMP (Training Impulse) load calculation
  - Jack Daniels VDOT estimation with training paces
  - Personalized recovery and training advice
- **7-Day Trend Analysis**: Activity patterns and consistency tracking
- **Personalized Recommendations**: Sleep tips, step goals, training insights

## Differences from garmer-based Version

| Aspect | Original (garmer) | This Version |
|---------|----------------------|---------------|
| Dependencies | garmer (complex) | garth (single lib) |
| Installation | pip install garmer (may fail) | pip3 install garth (simple) |
| Auth module | garmer.auth.GarminAuth | authenticate.py (wraps garth) |
| API client | garmer.client.GarminClient | garmin_client.py (wraps garth) |
| Features | ✅ Same | ✅ Same |

## Troubleshooting

### Error: garth not installed

```
ModuleNotFoundError: No module named 'garth'
```

**Solution:**
```bash
pip3 install garth
```

### Error: Not authenticated

```
Error: Not authenticated.
Run 'python3 authenticate.py' first.
```

**Solution:** Run `python3 authenticate.py` to authenticate with Garmin Connect.

### China Region Issues

```bash
# Verify config
cat ~/.garmin-health-report/config.json
# Should show: {"is_cn": true, ...}

# Clear tokens and re-authenticate
rm ~/.garmin-health-report/tokens.json
python3 authenticate.py
```

## Development

The code is structured for easy modification:

1. **authenticate.py** - Wraps garth library for authentication
2. **garmin_client.py** - Implements data containers and API methods using garth
3. **health_daily_report.py** - Report generation logic (independent of authentication layer)

To add new data types or metrics:

1. Add data container class to `garmin_client.py`
2. Add API method to `GarminClient` class
3. Use in `health_daily_report.py`

## License

MIT License - See LICENSE file for details.

## Credits

- Uses [garth](https://github.com/matin/garth) library for Garmin Connect API access
- Original garmer skill for report generation logic
- Jack Daniels VDOT formulas based on "Daniels' Running Formula"
- TRIMP calculation using Banister's equation
