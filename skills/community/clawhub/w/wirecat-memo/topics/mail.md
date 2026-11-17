# memo — Mail: mailboxes are the mail CLI's; memo reads and stages what is stored

**memo never reads a mailbox; the `mail` CLI does.** The owner adds and syncs a mailbox themselves
(`mail <profile> session start`, then `mail <profile> sync`); `mail <profile> status` shows how far it is, and
`memo sync` only prepares stored mail for search by meaning. Never ask for a mail or app password in the chat.

**Look at a mailbox before a first large sync with `mail <profile> account inspect --json`**: it groups mail by
sender and list from headers only; its `suggest` is a hint, not a decision, and a high `score` is a reason to
show the owner, not to add a rule. Pass `--domain-age` only when the owner agrees: it tells domain registries the
sender domains. Old Gmail years come from a Google Takeout file: `mail <profile> messages import <file.mbox>`.

**Mail rules, Gmail cleanup and restore are commands of the `mail` CLI, not memo.** Use
`mail <profile> rules list|add|remove|apply|export|import …`, `mail <profile> messages delete --rules`,
`mail <profile> messages restore --run <id>` and `mail doctor`; `mail session list` lists the profiles and their
addresses. memo's old `memo mail add|check|inspect|rules|delete|restore|runs` commands only answer with that
command. Rules stay the owner's decision: never add a skip or envelope rule unasked, and never run a cleanup's
`--yes` without the owner's yes.

**`memo: memo sync no longer imports mail` on stderr means the config still has memo's old `mail` settings.**
Tell the owner: `memo doctor` names the mailboxes to sync with `mail`, and `memo config unset mail` removes them.

**A stderr line `memo: scheduled sync failing since …` means the owner's timer is broken** and their
notes or mail are going stale. Tell the owner, quote its reason (an error code and reason id); the full
message is in the journal `memo jobs status` names.

For new mail, `memo mail review --holder <name> --source email:<account> --json` reads what is stored past that
holder's mark, filtered, each email with the `fingerprint` to cite. `memo mail findings add <file|->` stages one
mailbox's cited tasks, task updates, facts, memories, links and new contacts (`--help` has the JSON) under the
`--key` the review's `mail-findings.add` step gave; then
`memo messages acknowledge --holder <name> --cursor <cursor>` moves the mark. Never acknowledge before staging.
Under `MEMO_READ_ONLY` these two are the only writes allowed. Mail findings are owner only. `memo messages reset`
moves a mark back so that mail is read again; it is the owner's alone, so never run it. A scheduled agent
follows `memo skill show mail-triage`. `memo messages show <ref>` gives an email's `fingerprint` too.
