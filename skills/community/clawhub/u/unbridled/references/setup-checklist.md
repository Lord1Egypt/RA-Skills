# Setup checklist — beeper-matrix

## What the **user** does (one-time, ~3 min on their laptop)

1. **Create a Beeper account** (beeper.com) and install **Beeper Desktop** on their machine.
2. **Bridge the networks** they care about from inside Beeper Desktop:
   - Messenger (Facebook login)
   - WhatsApp (QR scan with phone)
   - Instagram / LinkedIn / X / Signal / Telegram / Discord / Google Messages — one click each
3. **Copy the Beeper Recovery Key**:
   1. Open **Beeper Desktop**
   2. Go to **Settings** (gear icon)
   3. Click on **your name** at the top of Settings
   4. Click the **down arrow (⌄)** next to your name to expand
   5. Click **"Show Recovery Code"**
   6. Copy the key (12 groups of 4 base58 chars, e.g. `EsUC HBcy scrf uiTy DTU2 rvEB Jmgj 9Cpa D6V2 z7Vk ZrU9 9RMh`)

   If there's no existing recovery key, Beeper should offer to create one — do it and store a copy in a password manager (1Password / Bitwarden).

4. **Hand the recovery key to the agent** via a channel that won't be quoted in chat logs. Prefer:
   - SSH into the agent host and `echo '<KEY>' > ~/.secrets/beeper-recovery-key.txt && chmod 600 ~/.secrets/beeper-recovery-key.txt`
   - Or a secret manager the agent can read

   Avoid pasting it in the chat history — if it lands there, regenerate after setup (Settings → same menu → Reset recovery code).

## What the **agent** does (automated, ~2 min on the host)

1. Install `bbctl` + deps (see `SKILL.md` § Setup step 1).
2. `bbctl login` — user enters Beeper credentials interactively.
3. `bbctl whoami` — sanity check, all bridges should show `RUNNING`.
4. Save the recovery key to `~/.secrets/beeper-recovery-key.txt` with chmod 600 (step 3 user-side, or agent if it already has the key).
5. `python nio_client.py whoami` — creates the Olm store under `~/.local/share/clawd-matrix/`, uploads device keys.
6. `python bootstrap_crosssign.py` — decrypts cross-signing secrets from the recovery key and signs the device. Expected final line:
   ```
   🎉 SUCCESS — device is now cross-signed. Bridge should accept our messages.
   ```
7. `python import_key_backup.py` — downloads the Matrix key backup, decrypts all stored Megolm group sessions with the recovery key, and writes them into the nio Olm store. Required for reading historical messages. Stop the sync daemon first if it's running (it locks the sqlite store):
   ```bash
   systemctl --user stop clawd-beeper-sync 2>/dev/null || true
   python import_key_backup.py
   systemctl --user start clawd-beeper-sync 2>/dev/null || true
   ```
   Expected: `✓ Imported N sessions into ~/.local/share/clawd-matrix/`.
8. Quick smoke test on a **real chat with a real other user** (not "notes to self"):
   ```bash
   python nio_client.py list-chats --network messenger --limit 5
   python nio_client.py send --room '!xxx:beeper.local' --text "pipeline check from <agent>"
   python nio_client.py history --room '!xxx:beeper.local' --limit 10
   ```
9. User confirms message arrived on Messenger and that `history` shows real text (not `[encrypted — …]`).

## Rollback / cleanup

```bash
# Unsign the device: Beeper UI → Settings → Devices → sign out the bbctl device
# Then on the host:
rm -rf ~/.local/share/clawd-matrix     # nio store
rm -rf ~/.config/bbctl                  # bbctl access token
rm  ~/.secrets/beeper-recovery-key.txt  # recovery key
rm  ~/.secrets/beeper-desktop-token     # desktop API token, if ever created
# Keep ~/bin/bbctl if you might re-use bbctl.
```

## Things the agent should NOT touch

- The user's Beeper password.
- The "Developers → Beeper Desktop API" token on the user's laptop (different mechanism, not needed for this skill).
- Message history — only read and write through the scripts; never bypass e2ee.
