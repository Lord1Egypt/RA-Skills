# Retarus SMS4A Reference

## Servers

- `de2`: `https://sms4a.de2.retarus.com/rest/v1`
- `de1`: `https://sms4a.de1.retarus.com/rest/v1`
- `eu`: `https://sms4a.eu.retarus.com/rest/v1`

Use `eu` for sending when no fixed datacenter is required.

Do not use `eu` as the only status endpoint. It is DNS-balanced across `de1` and `de2`, so status checks must try both German datacenters.

In the helper script, `status` always checks both `de1` and `de2`. `auto` and `eu` use the order `de2 -> de1`, while `--datacenter de1` uses `de1 -> de2` and `--datacenter de2` uses `de2 -> de1`.

## Authentication

Use HTTP Basic Auth.

The helper script resolves each credential field with this precedence:

1. `--username` and `--password`
2. `RETARUS_SMS4A_USERNAME` and `RETARUS_SMS4A_PASSWORD`
3. `--secret-file`
4. `RETARUS_SMS4A_SECRET_FILE`
5. Default local secret files at `~/.openclaw/secrets/retarus-sms4a.env` and `~/.openclaw/secrets/retarus-sms4a.json`

Secret files may be JSON or `.env` style. The secret-file path can come either from
the CLI flag, from `RETARUS_SMS4A_SECRET_FILE`, or from the default local secret path.

## Main Endpoints

- `POST /jobs`
  - Send one SMS job
  - Returns `201` with `{"jobId":"..."}`
- `GET /sms?jobId=...`
  - Return recipient-level delivery reports for the job
  - Returns an array of `RecipientReport`
- `GET /jobs/{jobId}`
  - Optional job-level status lookup
- `GET /version`
  - Optional connectivity check

## Minimal Send Payload

```json
{
  "messages": [
    {
      "text": "Your access code is ABC1234",
      "recipients": [
        {
          "dst": "+4917600000000"
        }
      ]
    }
  ]
}
```

## Common Options

`options` fields that are frequently useful:

- `src`
- `encoding`: `STANDARD` or `UTF-16`
- `statusRequested`
- `flash`
- `customerRef`
- `validityMin`
- `maxParts`
- `invalidCharacters`: `REFUSE`, `REPLACE`, `TO_UTF16`, `TRANSLITERATE`
- `qos`: `EXPRESS` or `NORMAL`
- `jobPeriod`
- `duplicateDetection`

For anything more complex than the helper flags expose, create a JSON payload file and pass `--payload-file`.

## Helper Script

From the skill root:

```bash
python3 scripts/sms4a_api.py send --help
python3 scripts/sms4a_api.py status --help
python3 scripts/sms4a_api.py version --help
```

Shared flags like `--username`, `--password`, `--secret-file`, `--timeout`, and `--pretty`
work both before and after the subcommand.

Useful patterns:

```bash
python3 scripts/sms4a_api.py send \
  --datacenter eu \
  --text "Hello from Retarus" \
  --recipient +4917600000000 \
  --status-requested
```

```bash
python3 scripts/sms4a_api.py send \
  --payload-file payload.json \
  --datacenter de2
```

```bash
python3 scripts/sms4a_api.py status \
  --job-id J.20221116-102407.583-0lajfsfmoXIZJO93PQ
```

```bash
python3 scripts/sms4a_api.py status \
  --job-id J.20221116-102407.583-0lajfsfmoXIZJO93PQ \
  --datacenter de1
```
