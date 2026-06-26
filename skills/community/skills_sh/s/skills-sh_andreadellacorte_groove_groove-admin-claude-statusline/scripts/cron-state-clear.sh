#!/bin/bash
# Clear loop state on session end.
echo '[]' > /tmp/claude/loops.json
exit 0
