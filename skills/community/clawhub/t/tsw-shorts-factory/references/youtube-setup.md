# YouTube OAuth Setup

## One-Time Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable **YouTube Data API v3**
3. Create credentials → **OAuth 2.0 Client ID** → Desktop app
4. Download JSON → rename to `yt_client_secrets.json` in working dir
5. Run: `python3 scripts/yt_setup.py` (opens browser for auth)
6. Token saved to `~/.yt_token.pickle` — valid until revoked

## Token Refresh
Tokens auto-refresh. If auth breaks after 6+ months:
```bash
rm ~/.yt_token.pickle
python3 scripts/yt_setup.py
```

## Upload Quota
YouTube API default: 10,000 units/day. Each upload ≈ 1,600 units.
→ ~6 uploads/day on free quota. Request increase at Google Cloud Console if needed.

## Draft vs Public
Videos upload as **unlisted** by default (privacy=unlisted).
To auto-publish, change `privacyStatus` in `pipeline.py`:
```python
'privacyStatus': 'public'  # Use with caution — review content first
```
