#!/bin/bash

# Open a search for follow-back / growth tweets on X
# User can then comment using browser automation or manually

QUERY=${1:-"follow back AI builders"}

URL="https://x.com/search?q=$(python3 - <<EOF
import urllib.parse
print(urllib.parse.quote('''$QUERY'''))
EOF
)&src=typed_query&f=live"

open "$URL"

echo "Opened growth tweet search. Look for posts asking for follow backs and comment with templates like:"
echo "Followed ✅ Let's connect in the AI space."