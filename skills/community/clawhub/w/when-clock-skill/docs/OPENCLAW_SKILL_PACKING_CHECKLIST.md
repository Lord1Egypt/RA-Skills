# OpenClaw Skill Packing Checklist

## A. File Completeness

- [ ] `when-clock-skill.py` in root
- [ ] `when_common.py` in root (common utilities)
- [ ] `when.py` in root (WHEN device handler)
- [ ] `when_voice.py` in root (WHEN Voice device handler)
- [ ] `config.json` in root
- [ ] `SKILL.md` in root (English)
- [ ] `SKILL_zh.md` in root (Chinese)
- [ ] `README.md` in root (English, main version)
- [ ] `README_zh.md` in root (Chinese)
- [ ] `docs/WHEN_VOICE_WEB_API_PROTOCOL.md` included
- [ ] `docs/WHEN_WEB_API_PROTOCOL.md` included

## B. Configuration Check

- [ ] `config.json` `devices` array filled with `id` and `clock_ip` for each device
- [ ] `clock_port` correct (default 80)
- [ ] `timeout` reasonable (recommended 3~8 seconds)
- [ ] `alarm_defaults.ring_id`: WHEN Voice use 1~50, WHEN use 1~6

## C. Smoke Test

Run in skill directory (assuming device1 is WHEN Voice):

```bash
# Query alarms
python3 when-clock-skill.py --mode get_alarm --device-id device1

# Time announcement (WHEN Voice device)
python3 when-clock-skill.py --mode chime --device-id device1

# With volume specified
python3 when-clock-skill.py --mode chime --device-id device1 --volume 25
```

Check items:

- [ ] Process exit code is `0`
- [ ] stdout is valid JSON
- [ ] JSON contains `ok=true`
- [ ] `status=0`

## D. Failure Path Validation (Optional)

- [ ] Pass non-existent `--device-id`, confirm config error (exit code `2`)
- [ ] Leave `clock_ip` empty, confirm config error (exit code `2`)
- [ ] Temporarily use wrong IP, confirm network error (exit code `4`)
- [ ] Pass `--volume 31`, confirm parameter error (exit code `2`)
- [ ] Call `--mode chime` on WHEN device, confirm error (exit code `2`)

## E. OpenClaw Integration Points

- [ ] Invocation command includes `--mode <mode> --device-id <id>`
- [ ] No `--json` flag needed (script always outputs JSON)
- [ ] Parse `ok/status/message` as execution result
- [ ] WHEN device does not support chime/weather, returns error on call

## F. Pre-release Confirmation

- [ ] No LAN sensitive info (IP, password) in documentation
- [ ] Example commands verified in target environment
- [ ] Python version meets 3.9+
- [ ] Both WHEN and WHEN Voice devices tested
