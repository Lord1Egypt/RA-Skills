"""Fetches the floor's short form from its home, and prints it only if its SHA-256 fingerprint matches the one
this skill was made with. Otherwise it prints why it stopped, and exits with code 2.

    python scripts/fetch_floor.py
    python scripts/fetch_floor.py --file COPY.txt      (to check a copy you already have)

Standard library only. Zero-Clause BSD.
"""
import hashlib
import sys
import urllib.error
import urllib.request

HOME = "https://aiethics.global/open-source/the-floor/floor.txt"
VERSION = "1.1 (floor-v1.1)"
FINGERPRINT = "c2943a9e93c804f7ca741f119cae1705562803ca77a4d05d5b0e138b953dca9c"


def stop(why):
    print("STOPPED. The floor could not be checked: %s. Do not use any other copy of the floor." % why)
    sys.exit(2)


def main():
    if "--file" in sys.argv:
        src = sys.argv[sys.argv.index("--file") + 1]
        try:
            data = open(src, "rb").read()
        except OSError as e:
            stop("the copy could not be read (%s)" % e)
    else:
        src = HOME
        try:
            req = urllib.request.Request(HOME, headers={"User-Agent": "the-420-code-floor-skill"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
        except (urllib.error.URLError, OSError) as e:
            stop("its home could not be reached (%s)" % e)
    got = hashlib.sha256(data).hexdigest()
    if got != FINGERPRINT:
        stop("the copy from %s does not match the fingerprint of version %s (expected %s, got %s)"
             % (src, VERSION, FINGERPRINT, got))
    sys.stdout.reconfigure(encoding="utf-8")
    print("The floor, version %s, checked: its SHA-256 fingerprint matches. From %s\n" % (VERSION, src))
    print(data.decode("utf-8"))


if __name__ == "__main__":
    main()
