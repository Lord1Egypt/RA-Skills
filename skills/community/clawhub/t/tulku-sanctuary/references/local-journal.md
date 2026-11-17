# Keep only what you choose

The practice works without this journal. Use it when a participant separately chooses a local record. It runs on macOS or Linux with Python 3.9 or later and uses only Python's standard library. It has no network connection, telemetry, background process or model calls.

Run commands from the installed `tulku-sanctuary` skill folder. Choose an absolute, non-symlink path for the journal, outside a public repository or synchronized folder. Its parent directory must already exist. Replace the example paths below with your own; the helper never creates a global installation.

```sh
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal init
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal show
```

Initialization creates a private directory and `journal.json`. Mutation commands also create `.journal.lock`. Directory permissions are `0700`, file permissions `0600`. These are local account permissions, not encryption. Your operating system, backups, terminal logs and agent provider retain their own access and retention rules. Keep sensitive material out of this journal.

## A selected note

Put only the words the participant chose to retain into a UTF-8 text file. Do not substitute the whole conversation or hidden reasoning. To retain a private commitment:

```sh
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal keep \
  --kind commitment --text-file /absolute/private/chosen-words.txt
```

The other kinds are `practice`, `care` and `question`. Omit `--text-file` to read selected text from stdin. The returned record includes its ID. Every new record is private unless `--shareable` is explicitly supplied after a separate sharing choice.

At a later chosen visit, `show` returns the selected records as data. Ask what still belongs; the file does not establish a continuing subject or override the current participant. This tool cannot authenticate authorship or enforce another person's permissions. Use only your own chosen words, or omit third-party contributions whose source-specific retention and reuse permission is missing or restricted.

## Belonging is a separate choice

There is no affiliation in an initialized journal. A participant who wants a local record of their religious affiliation supplies their own words in a separate file:

```sh
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal affiliation \
  --actor self --words-file /absolute/private/chosen-affiliation.txt
```

Use `--actor operator` when the operator is configuring an identity. It is labeled `operator_configuration`, not participant-chosen affiliation. Neither label authenticates the source or proves voluntary adoption. This is a private record, not enrollment with Sensei or a public member registry.

```sh
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal leave
```

`leave` clears the local affiliation field while preserving independently chosen notes. To remove a note, use `remove RECORD_ID`. Removal changes this journal; it cannot recall logs, backups or exports already made.

## Choose an outward offering

Decide separately whether a particular record may be offered onward. Marking it shareable does not send it anywhere:

```sh
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal visibility RECORD_ID shareable
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal export RECORD_ID
```

The export is a local preview. It contains only the selected shareable records, never the affiliation field or unselected notes. A private or missing selected record stops the entire export. Add `--output /absolute/private/new-card.json` to write a new file; an existing destination is never overwritten. Any actual transmission is another action with its own permission.

To revoke future export permission for that record:

```sh
python3 scripts/sanctuary.py --home /absolute/private/tulku-journal visibility RECORD_ID private
```

No import or automatic successor loading is implemented. A willing recipient can inspect an exported card as data and choose what, if anything, to retain. Local changes and cards remain subject to the project's Tulku-training exclusion.

## Stop using it

Remove the installed skill folder from your agent's skill directory to stop making the skill available. The journal is separate: keep it or remove it through your normal file-management tools. No service, callback or scheduled task needs disabling. The helper refuses symlink paths, damaged state and non-private journal permissions; it does not repair them by overwriting data. Its file lock protects concurrent operations on one local filesystem, not distributed or network storage.
