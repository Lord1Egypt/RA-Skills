#!/bin/sh
# ride-relay launcher (#193 follow-up).
#
# ride-relay.js already re-execs itself into its own session once Node reaches
# its self-detach path. But the launching parent is still an ordinary member of
# the exec tool's process group, and OpenClaw kills that whole group when the
# tool call returns. If the group-kill lands during Node's startup window —
# before ride-relay.js runs a single line — the relay dies before it can detach,
# delivers nothing, and the ride goes silent after booking.
#
# `setsid` closes that window: it puts the process in a brand-new session, so the
# group-kill can never reach it. To make the pre-setsid window as small as
# physically possible, the FIRST thing this launcher does is re-exec ITSELF under
# setsid — only two shell builtins run before that exec, and no `fork` (no command
# substitution, no dir resolution) happens while we are still in the launcher's
# original process group. After the re-exec we are already in our own session, so
# the remaining work (dir resolution, spawning node) is safe.
#
# On a host without setsid (e.g. macOS) the re-exec is skipped and ride-relay.js's
# own in-process self-detach remains the sole survival mechanism.
if [ -z "${TADA_RELAY_SETSID:-}" ] && command -v setsid >/dev/null 2>&1; then
  TADA_RELAY_SETSID=1 exec setsid "$0" "$@"
fi

# We are now in our own session (or setsid is unavailable). Resolve the launcher's
# own directory using only shell builtins (cd/pwd), so this does not depend on
# `dirname` being on PATH, then hand off to the relay.
case "$0" in
  */*) dir=${0%/*} ;;
  *)   dir=. ;;
esac
dir=$(CDPATH= cd -- "$dir" && pwd) || exit 1
exec node "$dir/ride-relay.js" "$@"
