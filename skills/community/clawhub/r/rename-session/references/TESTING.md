# rename-session - test plan

Manual smoke tests for the open-source edition.

## Setup (one-time)

```bash
mkdir -p /tmp/rs-test-root/testagent/sessions
cat > /tmp/rs-test-root/testagent/sessions/sessions.json << 'EOF'
{
  "agent:testagent:main": { "label": "original label" },
  "agent:testagent:thread-1": { "label": "Side thread" }
}
EOF
export RENAME_SESSION_ROOT=/tmp/rs-test-root
```

## T1 - help

```bash
python3 scripts/rename_session.py --help
```

Expect: usage block listing all flags, exit 0.

## T2 - list (single agent auto-detect)

```bash
python3 scripts/rename_session.py --list
```

Expect: shows `agent:testagent:main` and `agent:testagent:thread-1` with
labels, exit 0.

## T3 - rename literal

```bash
python3 scripts/rename_session.py agent:testagent:main "Project X kickoff"
python3 scripts/rename_session.py --list
```

Expect: label updated, list shows new label.

## T4 - random zh

```bash
python3 scripts/rename_session.py agent:testagent:main --random --agent-name Ashley
```

Expect: line starts with `Generated label: ` containing Chinese chars + emoji.

## T5 - random en

```bash
python3 scripts/rename_session.py agent:testagent:main --random --lang en
```

Expect: ASCII-only label with emoji.

## T5b - random auto-detect language from $LANG

```bash
# Force English locale → English label
LANG=en_US.UTF-8 python3 scripts/rename_session.py agent:testagent:main --random

# Force Chinese locale → Chinese label
LANG=zh_CN.UTF-8 python3 scripts/rename_session.py agent:testagent:main --random

# No locale set → fallback to English
LANG= LC_ALL= LC_MESSAGES= python3 scripts/rename_session.py agent:testagent:main --random
```

Expect: language auto-switched based on locale env vars, exit 0.

## T6 - multi-agent must specify

```bash
mkdir -p /tmp/rs-test-root/secondagent/sessions
echo '{"agent:secondagent:main":{"label":"two"}}' > /tmp/rs-test-root/secondagent/sessions/sessions.json
python3 scripts/rename_session.py --list
```

Expect: exits with `ERROR: multiple agents detected: secondagent, testagent`
and exit 1.

```bash
python3 scripts/rename_session.py --list --agent testagent
```

Expect: works again.

## T7 - missing session key

```bash
python3 scripts/rename_session.py --agent testagent agent:testagent:nope "x"
```

Expect: `ERROR: session key 'agent:testagent:nope' not found.` and exit 1.

## T8 - bad args

```bash
python3 scripts/rename_session.py
```

Expect: argparse error and exit 2.

## T9 - history file (XDG)

```bash
ls -la ~/.local/share/rename-session/history.json
cat ~/.local/share/rename-session/history.json
```

Expect: file exists, contains last N (<=10) labels as JSON array.

## Cleanup

```bash
rm -rf /tmp/rs-test-root ~/.local/share/rename-session
unset RENAME_SESSION_ROOT
```
