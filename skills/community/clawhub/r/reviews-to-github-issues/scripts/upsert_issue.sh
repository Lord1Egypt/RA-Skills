# Find or create the GitHub issue for one review topic, deduplicated by a hidden marker.
#
#   bash upsert_issue.sh find   --repo owner/name --app apple:284882215 --topic login-crash
#   bash upsert_issue.sh upsert --repo owner/name --app apple:284882215 --topic login-crash \
#        --title "Login crash after 3.2 (7 reviews)" --body-file body.md [--reopen] [--dry-run]
#
# find   prints: <number> <state> <url>, then one line "linked: <review ids>" (ids already in the
#        issue body or comments, so you can skip them), or "none" when no issue has the marker.
# upsert comments on the open issue with the marker, reopens a closed one with --reopen
#        (otherwise creates a new issue that references it), or creates a new issue
#        labelled appgoat-reviews whose body starts with the marker.
#
# Each review line in the body/comment should contain "review:<review_id>" so find can dedupe.
# Requires the GitHub CLI, authenticated (gh auth login, or GH_TOKEN in CI). GH overrides the binary.

set -euo pipefail

GH=${GH:-gh}
LABEL=appgoat-reviews

cmd=${1:-}
shift || true
repo= app= topic= title= body_file= reopen=0 dry=0
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) repo=$2; shift 2 ;;
    --app) app=$2; shift 2 ;;
    --topic) topic=$2; shift 2 ;;
    --title) title=$2; shift 2 ;;
    --body-file) body_file=$2; shift 2 ;;
    --reopen) reopen=1; shift ;;
    --dry-run) dry=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$cmd" ] || [ -z "$repo" ] || [ -z "$app" ] || [ -z "$topic" ]; then
  echo "usage: upsert_issue.sh find|upsert --repo owner/name --app store:id --topic slug [...]" >&2
  exit 2
fi
case "$topic" in
  *[!a-z0-9-]*) echo "topic must be a lowercase slug (a-z, 0-9, -): $topic" >&2; exit 2 ;;
esac

marker="<!-- appgoat:topic=$topic app=$app -->"

# Newest issue (open first) whose body contains the marker: "<number> <state> <url>"
find_issue() {
  $GH issue list --repo "$repo" --label "$LABEL" --state all --limit 500 \
    --json number,state,url,body \
    --jq "map(select(.body | contains(\"$marker\"))) | sort_by(.state != \"OPEN\", -.number) | .[0] | select(. != null) | \"\(.number) \(.state) \(.url)\""
}

linked_ids() {
  $GH issue view "$1" --repo "$repo" --json body,comments --jq '[.body, (.comments[].body)] | join("\n")' \
    | grep -oE 'review:[A-Za-z0-9._:-]+' | sed 's/^review://' | sort -u | tr '\n' ' ' || true
}

run() {
  if [ "$dry" = 1 ]; then
    echo "dry-run: $*"
  else
    "$@"
  fi
}

found=$(find_issue || true)

case "$cmd" in
  find)
    if [ -z "$found" ]; then
      echo none
    else
      echo "$found"
      echo "linked: $(linked_ids "${found%% *}")"
    fi
    ;;
  upsert)
    if [ -z "$body_file" ] || [ ! -f "$body_file" ]; then
      echo "--body-file is required" >&2
      exit 2
    fi
    number=${found%% *}
    state=$(echo "$found" | awk '{print $2}')
    if [ -n "$found" ] && [ "$state" = OPEN ]; then
      run $GH issue comment "$number" --repo "$repo" --body-file "$body_file" >/dev/null
      echo "commented #$number"
    elif [ -n "$found" ] && [ "$reopen" = 1 ]; then
      run $GH issue reopen "$number" --repo "$repo" >/dev/null
      run $GH issue comment "$number" --repo "$repo" --body-file "$body_file" >/dev/null
      echo "reopened #$number"
    else
      if [ -z "$title" ]; then
        echo "--title is required to create an issue" >&2
        exit 2
      fi
      tmp=$(mktemp)
      trap 'rm -f "$tmp"' EXIT
      {
        echo "$marker"
        cat "$body_file"
        if [ -n "$found" ]; then
          echo
          echo "Previously reported in #$number (closed)."
        fi
      } >"$tmp"
      run $GH label create "$LABEL" --repo "$repo" --color D93F0B \
        --description "Created from app store reviews by AppGoat" >/dev/null 2>&1 || true
      url=$(run $GH issue create --repo "$repo" --title "$title" --label "$LABEL" --body-file "$tmp")
      echo "created $url"
    fi
    ;;
  *)
    echo "unknown command: $cmd (find|upsert)" >&2
    exit 2
    ;;
esac
