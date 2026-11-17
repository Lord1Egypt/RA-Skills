---
name: time-now
description: Get the current local time, UTC offset, DST status, and timezone metadata for any IANA timezone or public IP address using the free Time.Now API. Use when a user asks what time it is somewhere, needs timezone-aware current-time data, wants to resolve an IP address to local time, or needs the supported timezone list.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "⏰"
    homepage: https://time.now/developer/openclaw
---

# Time.Now

Use the free, read-only Time.Now API for live timezone data. No account, API key, or authentication is required.

## Get current time by timezone

Use an IANA timezone identifier such as `America/New_York`, `Europe/London`, or `Asia/Tokyo`:

```bash
curl -fsS --get 'https://time.now/developer/api/time' \
  --data-urlencode 'timezone=Asia/Tokyo'
```

Replace the example value with the requested timezone. Always use `--data-urlencode`; never concatenate untrusted user input into a shell command or URL.

The JSON response includes:

- `datetime` and `utc_datetime`
- `timezone`, `abbreviation`, and `utc_offset`
- `dst`, `dst_offset`, `dst_from`, and `dst_until`
- `unixtime`, `day_of_week`, `day_of_year`, and `week_number`

For a city or region, select its canonical IANA timezone. If the place is ambiguous, ask the user which country or region they mean. Do not substitute a fixed UTC offset because offsets and daylight-saving rules can change.

## Get current time by IP address

For an explicitly supplied public IPv4 or IPv6 address:

```bash
curl -fsS 'https://time.now/developer/api/ip/8.8.8.8'
```

Validate the value as an IP address before placing it in the URL path. The response uses the same time fields and sets `client_ip` to the queried address.

To resolve the public IP of the machine making the API request:

```bash
curl -fsS 'https://time.now/developer/api/ip'
```

Do not assume this is the end user's location. An OpenClaw agent may run on a remote server, proxy, or VPN. When the user asks for "my time," prefer a timezone or location they supplied; otherwise ask for one.

## List supported timezones

```bash
curl -fsS 'https://time.now/developer/api/timezone'
```

This returns a JSON array of supported IANA timezone identifiers. Use it to confirm an identifier or offer valid alternatives after a lookup error.

## Check service health

```bash
curl -fsS 'https://time.now/developer/api/health'
```

Treat a response with `status` set to `ok` as healthy.

## Response rules

- Report the returned timezone, local time, UTC offset, and DST status when relevant.
- Preserve the API's explicit offset and timezone instead of recalculating them locally.
- Explain that timezone abbreviations can be ambiguous; prefer IANA names in technical output.
- If a request fails, report the error clearly. Check the supported timezone list for invalid identifiers; do not invent a result.
- Do not send secrets or personal data. These endpoints require neither.

API documentation: https://time.now/developer
OpenClaw skill documentation: https://time.now/developer/openclaw

