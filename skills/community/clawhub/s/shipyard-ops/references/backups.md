# Backups of the app's data

A backup is a copy of your users' data you keep outside the live database, so a mistake or a deleted table is not the end.

## Know this first

- **Backups contain your users' personal data** (emails, anything they typed). They stay on the student's own computer, never in the app's repo, never emailed or uploaded to a chat. The folder is private to their user account. Keep them as long as needed and delete old ones.
- Supabase's paid Pro plan takes automatic daily backups. The free plan does not. For an app with real users, Pro (about $25 a month) is the real safety net; this export is the free extra copy.

## Make one

`node "${CLAUDE_PLUGIN_ROOT}/scripts/backup-export.mjs" <appDir>`

It saves every table the app lists as user data, plus profiles and the tables from added modules, one JSON file each, with a `manifest.json` (row counts, project id, database version). Folder: `~/.shipyard/backups/<app>/<date and time in UTC>/`. It prints the folder; read it to the student with the privacy warning. It needs the Supabase access token in the keys file (already there after setup). Never open or print the backup files in the chat, `manifest.json` included. The secrets guard blocks reading anything under `~/.shipyard/backups/` (reading, searching, `cat`, `jq`, `node -e`); listing folder names with `ls` and deleting old ones with `rm` still work, and the script prints the row counts itself.

Add `--include-auth` to also save the sign-in list: ids, emails, sign-up dates and whether the email was confirmed. No passwords, phone numbers, names or profile data.

If the student's home folder is itself a git repository (some people keep their dotfiles there), the script refuses unless that repository ignores `~/.shipyard/`. It prints the one line to add to `~/.gitignore`.

Run one before: a database change, a big launch step, or deleting anything.

## Restore

Restore is manual on purpose, because pushing old data back can overwrite newer data.
1. Stop and ask the student what exactly was lost and when.
2. Claude never opens the backup files, because they hold users' personal data and the guard blocks it. Instead Claude writes a small script on the student's computer (outside the app folder and outside any repo) that reads the JSON file and inserts the rows through the Supabase Management API (`SUPABASE_ACCESS_TOKEN` from the keys file, passed by environment, never in the command). The script prints only counts ("loaded 120 of 120 rows into items"), never a row. To restore only missing rows, the script filters by id in code. Show the student the script and get a yes before running it. Delete the script afterwards.
3. Test on a second, empty Supabase project first when the data matters.
4. Run `verify.mjs <appDir>` afterwards.

## Habits

- Check `ops-status.mjs` for the date of the last backup. Over a month old with active users? Suggest a new one.
- Old backups pile up: list the folder and offer to delete the oldest ones. Deleting is the student's call.
- Never copy backups into a cloud folder that is shared with others.
