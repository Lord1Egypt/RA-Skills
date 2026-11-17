# Attendance write walkthrough (fpx cookie + curl)

Mirrors `setlist-mcp`'s `setlist_mark_attended` / `setlist_unmark_attended`
tools exactly (`src/tools/attendance.ts`, `src/web-client.ts`). There is no
JSON API for this — you're driving the same server-rendered Apache Wicket
page a signed-in browser would.

Prereqs: `SETLIST_API_KEY` set (Part 1) and `COOKIE`/`UA` captured per
`SKILL.md` Part 2.

## Step 0 — resolve the setlist's canonical URL

You need the setlist's public page path. Either you already have a
setlist.fm URL (skip to step 1), or resolve it via the API using the
`setlistId`:

```sh
SETLIST_ID=63de4613
META=$(curl -s "https://api.setlist.fm/rest/1.0/setlist/$SETLIST_ID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json')
URL=$(echo "$META" | jq -r '.url')          # e.g. https://www.setlist.fm/setlist/.../...-4ba8a766.html
PATH_ONLY=$(echo "$URL" | sed -E 's#https?://[^/]+##')   # /setlist/.../...-4ba8a766.html
```

## Step 1 — fetch the page, authenticated

```sh
HTML=$(curl -s "https://www.setlist.fm$PATH_ONLY" \
  -H "Cookie: $COOKIE" -H "User-Agent: $UA")
```

**Check you're actually signed in** before going further — a logged-out page
links to sign-in instead of showing the attendance control:

```sh
echo "$HTML" | grep -qE 'href="/(signin|login)\b' && echo "SESSION EXPIRED — re-capture the cookie" >&2
```

## Step 2 — find the attendance control

The control is an `<a>` tag with a `wicketAjaxGet('...')` onclick and a
`title` of either:

- `"Add this setlist to your attended shows."` → **not** currently attended
- `"Remove this setlist from your attended shows."` → **currently** attended

Extract both the per-render AJAX URL and the current state with `perl`
(installed on macOS by default). For each `<a>` tag, check for
`wicketAjaxGet(...)` and `title="..."` independently within the same
800-char window — same as `src/tools/attendance.ts`'s `parseAttendance()` —
rather than requiring `title=` to appear before `onclick=`, since real
markup doesn't guarantee that ordering. Entity-decode the URL the same way
`decodeEntities()` does: `&amp;` plus numeric character references
(`&#x..;` hex and `&#..;` decimal), which a plain grep would mangle:

```sh
read -r AJAX_URL CURRENTLY_ATTENDED < <(
  echo "$HTML" | perl -0777 -ne '
    while (/<a\b(.{0,800})/gs) {
      my $seg = $1;
      next unless $seg =~ /wicketAjaxGet\(\s*[\x27"]([^\x27"]+)[\x27"]/;
      my $url = $1;
      next unless $seg =~ /title="([^"]*attended shows[^"]*)"/;
      my $attended = $1 =~ /remove/i ? 1 : 0;
      $url =~ s/&amp;/&/g;
      $url =~ s/&#x([0-9a-fA-F]+);/chr(hex($1))/ge;
      $url =~ s/&#(\d+);/chr($1)/ge;
      print "$url $attended\n";
      last;
    }
  '
)
```

If `$AJAX_URL` is empty: the control genuinely isn't on the page (rare — a
layout change, or you hit a bot-rate-limit page) — re-check step 1's
logged-out test first, since that's the far more common cause.

## Step 3 — decide: no-op, dry-run, or toggle

```sh
DESIRED=1   # 1 = mark attended, 0 = unmark

if [ "$CURRENTLY_ATTENDED" = "$DESIRED" ]; then
  echo "already in the desired state — nothing to do"
  exit 0
fi

echo "would toggle attended: $CURRENTLY_ATTENDED -> $DESIRED (dry run — confirm before sending)"
```

The control is a toggle, so sending it from the wrong state does the
opposite of what you meant. Don't send the toggle in step 4
until you've deliberately decided to (a script arg, an explicit prompt —
whatever fits your use). Never toggle blind.

## Step 4 — replay the Wicket AJAX toggle

`$AJAX_URL` is relative to the setlist page. Resolve it, then GET it with
the Wicket AJAX headers (these are required — a plain GET without them gets
ignored or errors):

```sh
FULL_AJAX_URL=$(python3 -c "import urllib.parse,sys; print(urllib.parse.urljoin(sys.argv[1], sys.argv[2]))" "$URL" "$AJAX_URL")
AJAX_PATH=$(echo "$FULL_AJAX_URL" | sed -E 's#https?://[^/]+##')
BASE_URL_HEADER=$(echo "$PATH_ONLY" | sed -E 's#^/##')   # Wicket-Ajax-BaseURL wants no leading slash

curl -s "https://www.setlist.fm$AJAX_PATH" \
  -H "Cookie: $COOKIE" -H "User-Agent: $UA" \
  -H 'Wicket-Ajax: true' \
  -H "Wicket-Ajax-BaseURL: $BASE_URL_HEADER" \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'Accept: text/xml, text/javascript, application/xml, text/html, */*' \
  > /dev/null
```

## Step 5 — verify by re-reading (never trust the response status)

A `200` from step 4 is not proof — re-fetch the page and re-run step 2's
parse:

```sh
HTML2=$(curl -s "https://www.setlist.fm$PATH_ONLY" -H "Cookie: $COOKIE" -H "User-Agent: $UA")
read -r _ NOW_ATTENDED < <(echo "$HTML2" | perl -0777 -ne '
  while (/<a\b(.{0,800})/gs) {
    my $seg = $1;
    next unless $seg =~ /wicketAjaxGet/;
    next unless $seg =~ /title="([^"]*attended shows[^"]*)"/;
    print "x ", ($1 =~ /remove/i ? 1 : 0), "\n";
    last;
  }
')

if [ "$NOW_ATTENDED" = "$DESIRED" ]; then
  echo "verified: attended=$NOW_ATTENDED"
else
  echo "WARNING: toggle sent but re-read did not confirm the new state — check on setlist.fm" >&2
fi
```

## Notes

- **Pace writes.** Rapid-fire authenticated requests appear to get the
  session throttled/invalidated mid-batch — space multiple toggles at least
  ~600ms apart, same as the MCP's write pacer.
- **Transient 5xx**: `www.setlist.fm`'s gateway occasionally 500/502/503s —
  retry a couple times with a ~1.2s gap before concluding something's wrong.
- **This is the ONLY write surface setlist.fm has.** There's no way to edit
  setlist song content, create setlists, etc. via this path or the API —
  those are wiki edits done through the full website UI, out of scope here.
