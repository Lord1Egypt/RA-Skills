# Google Calendar Setup

## One-Time OAuth Setup

1. Go to https://console.cloud.google.com → create a new project
2. Enable **Google Calendar API**
3. APIs & Services → Credentials → Create **OAuth 2.0 Client ID** (Desktop app type)
4. Download JSON → save as `credentials.json` in project root
5. Run: `python3 setup_gcal.py`
6. Browser opens → sign in → allow Calendar access
7. `token.pickle` is saved automatically

## .env Config
```
GOOGLE_CREDENTIALS_PATH=../credentials.json
GOOGLE_TOKEN_PATH=../token.pickle
```

## Security
Both `credentials.json` and `token.pickle` are in `.gitignore` — never commit them.

## Troubleshooting
- **org_internal error** → You're using someone else's GCP app. Create your own project (step 1).
- **Token expired** → Delete `token.pickle` and re-run `setup_gcal.py`
- **Mock data still showing** → Check env vars are set and paths are correct. Hit `/debug-env`.
