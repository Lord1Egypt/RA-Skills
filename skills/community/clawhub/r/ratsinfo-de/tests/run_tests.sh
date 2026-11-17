#!/usr/bin/env bash
# Offline test run. Touches no municipality, needs no network.
#
#   bash tests/run_tests.sh
#
# Exits non zero on the first failed expectation.

set -u
cd "$(dirname "$0")/.." || exit 1

export RATSINFO_MIN_INTERVAL=0
export RATSINFO_CACHE="$(mktemp -d)"

python3 tests/mock_ris.py &
MOCK_OK=$!
MOCK_PORT=8801 MOCK_TOWN="Stadt Beispielstadt" MOCK_AGS=05158000 \
    python3 tests/mock_ris.py &
MOCK_T2=$!
python3 tests/mock_broken.py &
MOCK_BAD=$!
trap 'kill $MOCK_OK $MOCK_T2 $MOCK_BAD 2>/dev/null; rm -rf "$RATSINFO_CACHE"' EXIT
sleep 1

PASS=0
FAIL=0

expect() { # expect <name> <expected-exit> <needle> <command...>
    local name="$1" want="$2" needle="$3"; shift 3
    local out rc
    out="$("$@" 2>&1)"; rc=$?
    if [ "$rc" != "$want" ]; then
        printf 'FAIL %s: exit %s, expected %s\n%s\n' "$name" "$rc" "$want" "$out"
        FAIL=$((FAIL + 1)); return
    fi
    if ! printf '%s' "$out" | grep -q -- "$needle"; then
        printf 'FAIL %s: output does not contain %s\n%s\n' "$name" "$needle" "$out"
        FAIL=$((FAIL + 1)); return
    fi
    printf 'ok   %s\n' "$name"
    PASS=$((PASS + 1))
}

OK=http://127.0.0.1:8799/system
BAD=http://127.0.0.1:8798

expect "check reads the System object" 0 "oparlVersion" \
    python3 scripts/ratsinfo.py check "$OK"
expect "check shows the licence" 0 "dl-de/by-2-0" \
    python3 scripts/ratsinfo.py check "$OK"
expect "papers follows links.next across pages" 0 "3 matching of 3 scanned" \
    python3 scripts/ratsinfo.py papers "$OK"
expect "papers filters on the client side" 0 "2 matching of 3 scanned" \
    python3 scripts/ratsinfo.py papers "$OK" --term Sanierung
expect "papers exposes the file URL" 0 "files/0.pdf" \
    python3 scripts/ratsinfo.py papers "$OK" --term Kaestner
expect "meetings lists sittings" 0 "Rat der Stadt Musterhausen" \
    python3 scripts/ratsinfo.py meetings "$OK"
expect "a disabled endpoint fails loudly" 2 "switched off" \
    python3 scripts/ratsinfo.py check "$BAD/dead"
expect "a bot check page is recognised" 2 "did not return JSON" \
    python3 scripts/ratsinfo.py check "$BAD/botcheck"
expect "robots.txt is honoured" 2 "robots.txt" \
    python3 scripts/ratsinfo.py check "$BAD/blocked"
expect "--ignore-robots gets past robots.txt" 2 "not an OParl System object" \
    python3 scripts/ratsinfo.py check "$BAD/blocked" --ignore-robots

expect "bodies lists the bodies" 0 "Stadt Musterhausen" \
    python3 scripts/ratsinfo.py bodies "$OK"
expect "json output is valid json" 0 '"oparlVersion"' \
    python3 scripts/ratsinfo.py check "$OK" --json
expect "papers json carries the file url" 0 '"files"' \
    python3 scripts/ratsinfo.py papers "$OK" --term Kaestner --json
expect "a body that does not exist is refused" 2 "does not exist" \
    python3 scripts/ratsinfo.py papers "$OK" --body 7

expect "track resolves the consultation chain" 0 "Bauausschuss" \
    python3 scripts/ratsinfo.py track "http://127.0.0.1:8799/paper/0"
expect "track names the decision" 0 "beschlossen" \
    python3 scripts/ratsinfo.py track "http://127.0.0.1:8799/paper/0"
expect "track marks the authoritative step" 0 "authoritative" \
    python3 scripts/ratsinfo.py track "http://127.0.0.1:8799/paper/0" --json
expect "bodies exposes the official municipality key" 0 "05124000" \
    python3 scripts/ratsinfo.py bodies "$OK"
expect "people lists memberships" 0 "Vorsitzende" \
    python3 scripts/ratsinfo.py people "$OK"
expect "watch reports new items on first run" 0 "3 new" \
    python3 scripts/ratsinfo.py watch "$OK"
expect "watch reports nothing new on second run" 0 "0 new" \
    python3 scripts/ratsinfo.py watch "$OK"
expect "watch writes an ical file" 0 "calendar written" \
    python3 scripts/ratsinfo.py watch "$OK" --kind meeting --ics "$RATSINFO_CACHE/t.ics"

# --- the guards. each of these caught a real defect during review. ---
expect "a file:// url is refused" 2 "Only http and https" \
    python3 scripts/ratsinfo.py get "file:///etc/passwd"
expect "a cross host link is not followed" 2 "not the endpoint you asked for" \
    python3 scripts/ratsinfo.py check "http://127.0.0.1:8799/evil-system"
expect "--allow-cross-host lets it through" 2 "body list is empty" \
    python3 scripts/ratsinfo.py check "http://127.0.0.1:8799/evil-system" --allow-cross-host
expect "a malformed list is refused, not misread" 2 "not a list" \
    python3 scripts/ratsinfo.py bodies "http://127.0.0.1:8799/dirty-system"
expect "--ics is refused for papers" 2 "only makes sense" \
    python3 scripts/ratsinfo.py watch "$OK" --ics "$RATSINFO_CACHE/x.ics"

grep -q "BEGIN:VCALENDAR" "$RATSINFO_CACHE/t.ics" \
    && { printf 'ok   the ical file is a valid calendar\n'; PASS=$((PASS + 1)); } \
    || { printf 'FAIL the ical file is not a calendar\n'; FAIL=$((FAIL + 1)); }

# the PDF dossier, the artefact people actually keep
expect "report writes a pdf" 0 "Beratungen" \
    python3 scripts/ratsinfo.py report "http://127.0.0.1:8799/paper/0" \
        --pdf "$RATSINFO_CACHE/v.pdf"
if head -c 5 "$RATSINFO_CACHE/v.pdf" | grep -q "%PDF-"; then
    printf 'ok   the pdf has a valid header\n'; PASS=$((PASS + 1))
else
    printf 'FAIL the pdf header is wrong\n'; FAIL=$((FAIL + 1))
fi
if python3 tests/check_pdf.py "$RATSINFO_CACHE/v.pdf"; then
    printf 'ok   the pdf carries the paper title and the timeline\n'; PASS=$((PASS + 1))
else
    printf 'FAIL the pdf content is missing\n'; FAIL=$((FAIL + 1))
fi
expect "report survives a missing logo" 0 "Beratungen" \
    python3 scripts/ratsinfo.py report "http://127.0.0.1:8799/paper/0" \
        --pdf "$RATSINFO_CACHE/v2.pdf" --logo /does/not/exist.png

# the market report across several municipalities
printf 'http://127.0.0.1:8799/system\nhttp://127.0.0.1:8801/system\nhttp://127.0.0.1:8797/tot\n' \
    > "$RATSINFO_CACHE/eps.txt"
expect "scan queries several municipalities" 0 "3 Kommunen abgefragt, 2 erreichbar" \
    python3 scripts/ratsinfo.py scan --endpoints "$RATSINFO_CACHE/eps.txt" \
        --term Sanierung
expect "scan names both towns" 0 "Beispielstadt" \
    python3 scripts/ratsinfo.py scan --endpoints "$RATSINFO_CACHE/eps.txt" \
        --term Sanierung
expect "scan reports the dead endpoint instead of hiding it" 0 "nicht auswertbar" \
    python3 scripts/ratsinfo.py scan --endpoints "$RATSINFO_CACHE/eps.txt" \
        --term Sanierung
expect "scan writes a market report" 0 "Bericht:" \
    python3 scripts/ratsinfo.py scan --endpoints "$RATSINFO_CACHE/eps.txt" \
        --term Sanierung --pdf "$RATSINFO_CACHE/markt.pdf"
if python3 tests/check_pdf.py "$RATSINFO_CACHE/markt.pdf" markt; then
    printf 'ok   the market report names towns and states its limits\n'
    PASS=$((PASS + 1))
else
    printf 'FAIL the market report is incomplete\n'; FAIL=$((FAIL + 1))
fi

# ICS escaping and time zones. Both of these were broken before review.
python3 scripts/ratsinfo.py watch "$OK" --kind meeting --ics "$RATSINFO_CACHE/n.ics" \
    >/dev/null 2>&1
python3 - "$RATSINFO_CACHE/nasty.ics" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("r", "scripts/ratsinfo.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
r.allow_host("http://127.0.0.1:8799/x")
ics = r.to_ics(list(r.iter_list("http://127.0.0.1:8799/nasty-meetings")))
open(sys.argv[1], "w").write(ics)
PY
if grep -q 'DTSTART:20260310T160000Z' "$RATSINFO_CACHE/nasty.ics"; then
    printf 'ok   ics converts +02:00 to UTC\n'; PASS=$((PASS + 1))
else
    printf 'FAIL ics time zone conversion\n'; FAIL=$((FAIL + 1))
fi
if [ "$(grep -c '^ATTENDEE' "$RATSINFO_CACHE/nasty.ics")" = "0" ]; then
    printf 'ok   ics escapes a hostile meeting title\n'; PASS=$((PASS + 1))
else
    printf 'FAIL ics injection is possible\n'; FAIL=$((FAIL + 1))
fi

# The throttle is the central promise of this skill, so it gets a test.
ELAPSED=$(RATSINFO_MIN_INTERVAL=0.7 python3 - <<'PY'
import importlib.util, time
spec = importlib.util.spec_from_file_location("r", "scripts/ratsinfo.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
r.allow_host("http://127.0.0.1:8799/system")
start = time.monotonic()
for _ in range(3):
    r.fetch_json("http://127.0.0.1:8799/system")
print(f"{time.monotonic() - start:.2f}")
PY
)
if python3 -c "import sys; sys.exit(0 if float('$ELAPSED') >= 1.2 else 1)"; then
    printf 'ok   three requests to one host take at least 1.2 s (%s)\n' "$ELAPSED"
    PASS=$((PASS + 1))
else
    printf 'FAIL the throttle did not throttle (%s s)\n' "$ELAPSED"; FAIL=$((FAIL + 1))
fi

rm -rf "$RATSINFO_CACHE"
printf '\n%s passed, %s failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
