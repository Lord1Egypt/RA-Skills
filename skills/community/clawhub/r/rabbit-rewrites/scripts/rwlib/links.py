#!/usr/bin/env python3
"""
rwlib.links - Link conventions, vague anchor text, and claim/caveat patterns.

Shared across rabbit-readme-improver and rabbit-writes.
"""

import re

# Anchor text that tells a reader nothing out of context, which is how a screen
# reader and a skimmer both encounter it.
VAGUE_LINK_TEXT = {
    "here", "click here", "this", "this link", "link", "read more", "more",
    "learn more", "see here", "this page", "documentation here"
}

CLAIM_RX = re.compile(
    r"(?i)\b(\d+(?:\.\d+)?\s*(?:x|times)\s*(?:faster|smaller|cheaper|less|more|quicker|throughput|speedup)"
    r"|\d+(?:\.\d+)?\s*x\s+throughput"
    r"|\d+(?:\.\d+)?\s*%\s*(?:faster|smaller|cheaper|fewer|less|more|reduction|savings?|accura\w+|uptime|coverage)"
    r"|(?:uptime|coverage)[-\s:]*\d+(?:\.\d+)?\s*%"
    r"|saves?\s+(?:you\s+)?\d+(?:\.\d+)?\s*%"
    r"|cuts?\s+\w+\s+by\s+\d+(?:\.\d+)?\s*%)"
)

CAVEAT_RX = re.compile(
    r"(?i)(caveat|varies|vary|depends|depending|measured (on|with|against)|does not (cover|include)"
    r"|doesn't (cover|include)|not a guarantee|your mileage|approximat|excluding|only counts"
    r"|net.negative|worst case|in some cases|under (this|these) conditions|methodolog)"
)
