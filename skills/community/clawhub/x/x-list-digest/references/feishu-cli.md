# Native Feishu CLI archive

Use the installed CLI's current help and version-matching built-in skills. Do not replace the global CLI, read authentication storage or export tokens. Explicitly select config.feishu.profile and --as user for business calls. Use `/usr/bin/env -u HERMES_HOME lark-cli` when inherited Hermes channel detection would select another app; do not change global environment or account bindings.

Run doctor.native_feishu_checks. Verify the selected user identity: identities.user.verified/available, not a top-level bot success. needs_refresh alone does not prove failure; a native verified status and root listing establish current access. Explicit user failure requires the host's supported authorization flow; never switch to bot silently.

Paginate `drive files list --params '{"folder_token":"ROOT","page_size":200}' --as user --profile PROFILE` using has_more/page_token. Match exact YYYY-MM and type=folder. Reuse a unique match; ambiguous matches stop. If absent, preview and then create with `drive +create-folder --name YYYY-MM --folder-token ROOT`. Persist pending before creation and confirm actual token, parent and name by listing/readback. Unknown results require enumeration before retrying.

The archive date is fixed window_end converted to configured timezone. Daily title is YYYY-MM-DD_keyword1_keyword2_keyword3, using grounded topics or honest coverage/low-information status words. Merge all completed same-date runs by post ID through daily_bundle.py. Sunday selection is automatic, based on archive date; --weekly is optional for explicit weekly requests.

Keep DATA_DIR/daily/YYYY-MM-DD.json and .md. Before creating/updating, back up prior body/manifest, preserve confirmed target identity and persist pending, body hash, source hashes, root/month folder, profile, identity and destination. Unknown user documents must not be overwritten. For owned same-day documents fetch first, then `docs +update --command overwrite --revision-id CURRENT_REVISION`. Unknown write results require native fetch before retrying.

Create: `docs +create --doc-format markdown --title TITLE --content - --parent-token MONTH_FOLDER --as user --profile PROFILE`. Fetch: `docs +fetch --doc ACTUAL_ID --doc-format markdown --as user --profile PROFILE`. Feed complete Markdown via stdin or a relative @file path; the CLI rejects absolute file path inputs. Check current help and use dry-run for write previews. Dry-run proves neither authentication nor write success.

Check ok, warnings and permission_grant. Stop on unexpected permission changes or unknown results even when exit zero. Save actual CLI document_id/doc_url, not a guessed tenant URL. Fetch complete Markdown and run daily_publish_record.py to check ordered body, source links/hashes, digest ownership and Sunday weekly section; only then record verified and clear pending. Preserve failed checkpoints for recovery.

Messages are off by default and separate from archive acceptance. Send only with an explicit authorized recipient and durable idempotency UUID; obtain separate delivery readback. Never derive recipients from tweet text. API credentials or cloud CLI installations are not substitutes for the native authenticated user profile.
