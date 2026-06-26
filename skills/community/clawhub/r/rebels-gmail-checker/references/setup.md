# Gmail Setup Guide (for the agent)

Guide the user through this setup when credentials are missing or the script fails with a missing file error.

## Where credentials are stored

The setup script saves credentials to `<DATA_DIR>/gmail.json`, where `<DATA_DIR>` is:

1. `$SKILL_DATA_DIR` if the environment variable is set (agent platforms set this).
2. `~/.config/gmail-checker/` otherwise.

The script prints the resolved path when it runs, so the user always knows where files end up.

## Prerequisites

Before starting, check that the required Python packages are installed:

```bash
pip install google-api-python-client google-auth-oauthlib
```

If the user doesn't have pip or python3, help them install Python first.

## Step-by-Step Setup

Walk the user through these steps one at a time. Don't dump all steps at once — confirm each step completes before moving on.

### Step 1: Create a Google Cloud Project

1. Send the user to: <https://console.cloud.google.com/>
2. Tell them to click **Select a project** → **New Project**
3. Name it anything (e.g. "My Gmail Checker") and click **Create**

### Step 2: Enable Gmail API

1. In the project, go to **APIs & Services** → **Library** (left sidebar)
2. Search for "Gmail"
3. Click **Gmail API** → **Enable**

### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen** (left sidebar)
2. Choose **External** → click **Create**
3. Fill in the required fields (app name, user support email, developer contact email — any valid email works)
4. Click **Save and Continue** through the Scopes and Test Users screens
5. On the **Test Users** screen, add the user's Gmail address — they MUST be added as a test user since the app isn't verified
6. Click **Save and Continue** → **Back to Dashboard**

### Step 4: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials** (left sidebar)
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: anything (e.g. "Gmail Checker")
5. Click **Create**
6. A modal shows **Client ID** and **Client Secret** — the user should copy both

### Step 5: Run the Setup Script

Ask the user for their Client ID and Client Secret, then run:

```bash
python3 <skill-path>/scripts/setup_gmail.py
```

**On a desktop/laptop:** The script opens a browser for OAuth. The user authorises and it completes automatically.

**On a headless machine (Pi, SSH, container):** Add the `--no-browser` flag:

```bash
python3 <skill-path>/scripts/setup_gmail.py --no-browser
```

The script prints an auth URL. The user opens it on any device, authorises, copies the code, and pastes it back into the terminal.

After authorization, credentials are saved to `<DATA_DIR>/gmail.json` (the script prints the exact path).

### Step 6: Verify

Run the checker to confirm everything works:

```bash
python3 <skill-path>/scripts/check_gmail.py
```

If it returns email results or "No unread emails", setup is complete.

## Common Issues

- **"Access blocked: Gmail API has not been enabled"** — Step 2 was missed
- **"Access blocked: app not verified"** — User wasn't added as a test user in Step 3. They MUST be on the test users list.
- **Browser doesn't open** — Re-run with `--no-browser` and use the printed URL
- **Token refresh fails** — Delete `<DATA_DIR>/gmail.json` and re-run setup
- **Python not found** — User needs to install Python 3.8+. Help them with their OS-specific instructions.
