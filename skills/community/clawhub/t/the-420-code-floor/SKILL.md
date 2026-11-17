---
name: the-420-code-floor
description: Gives you the floor, the short text of what an AI reasons from in The 420 Code, fetched from its home and checked against its fingerprint before you read it. Use when asked to read, apply or check against the floor.
---

# The floor, checked

- **Home:** https://aiethics.global/open-source/the-floor/
- **Version:** 1.1, tag floor-v1.1
- **Fingerprint of its short form,** the file the script fetches: SHA-256 `c2943a9e93c804f7ca741f119cae1705562803ca77a4d05d5b0e138b953dca9c`

This skill holds no copy of the floor. It fetches the floor's short form from its home, and checks it against the fingerprint above before you read any of it. You cannot check a fingerprint by reading. The script does it.

1. **Run the script.** From this skill's own folder, run `python scripts/fetch_floor.py`. It needs Python 3 and nothing else.
2. **If it passes.** Its first line says the check passed. That line is the script's own; the floor begins after it. Use the floor's text as it is: do not shorten it, reword it, or mix it with any other copy.
3. **If it stops.** It prints a line beginning "STOPPED", and exits with code 2. Say plainly that the floor could not be checked, and give the reason the script gives. Do not use any other copy of the floor, from memory or from anywhere else. A stop means that the copy at its home was not the one this skill was made for: either it was changed, or a newer version is there that this skill does not know yet.

The floor's own text gives a different fingerprint: that is the fingerprint of the floor's source. The one above is of the short form.

When a new version of the floor is tagged, this skill is updated with the new fingerprint by its workflow, never by hand.

To comment or send your work, use the site: https://aiethics.global/open-source/
