#!/usr/bin/env python3
"""Verify that a generated dossier really contains what it should.

Reads the PDF back, decompresses its content streams and looks for the
paper title and the timeline heading. Cheap, and it would have caught an
empty or broken document.
"""
import re
import sys
import zlib

raw = open(sys.argv[1], "rb").read()
if not raw.startswith(b"%PDF-"):
    sys.exit("no PDF header")

text = b""
for block in re.findall(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
    try:
        text += zlib.decompress(block)
    except zlib.error:
        continue  # the logo image stream, not text

if len(sys.argv) > 2 and sys.argv[2] == "markt":
    wanted = [b"Marktbericht", b"Musterhausen", b"Beispielstadt",
              b"Bausumme", b"Kontaktdaten"]
else:
    wanted = [b"Erich-Kaestner", b"Weg durch die Gremien", b"Bauausschuss",
              b"Entschieden am"]
missing = [w.decode() for w in wanted if w not in text]
if missing:
    sys.exit("missing from the PDF: " + ", ".join(missing))
print("pdf content verified")
