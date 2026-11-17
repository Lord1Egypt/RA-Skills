#!/usr/bin/env python3
"""A dependency free PDF writer, just large enough for a council dossier.

Standard library only. zlib does the compression, the base fourteen fonts
do the typography, and PNG images are decoded and re-encoded by hand. That
keeps the whole skill installable with nothing but Python, which is the
point.

Not a general PDF library. It writes one kind of document: a one or two
page report with an optional logo, a heading, key value pairs and a
timeline. That is all the council dossier needs.
"""

from __future__ import annotations

import struct
import zlib

A4 = (595.28, 841.89)  # points

INK = (0.16, 0.22, 0.35)       # Alpha Quadrat navy, the default accent
GREY = (0.42, 0.45, 0.50)
LIGHT = (0.82, 0.84, 0.87)
BLACK = (0.11, 0.12, 0.14)


# --------------------------------------------------------------------------
# PNG decoding, enough for logos
# --------------------------------------------------------------------------

def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def read_png(path: str):
    """Return (width, height, rgb_bytes) for a PNG, white where transparent.

    Supports colour types 0 (grey), 2 (RGB), 4 (grey+alpha) and 6 (RGBA) at
    eight bits per channel. Palette images are refused rather than guessed.
    """
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")

    pos = 8
    width = height = depth = colour = 0
    idat = bytearray()
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, colour = struct.unpack(">IIBB", body[:10])
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break

    if depth != 8:
        raise ValueError(f"{path}: only 8 bit PNGs are supported")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(colour)
    if channels is None:
        raise ValueError(
            f"{path}: colour type {colour} is not supported. "
            "Save the logo as RGB or RGBA PNG."
        )

    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    out = bytearray()
    previous = bytearray(stride)
    pos = 0
    for _ in range(height):
        filt = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        for i in range(stride):
            left = line[i - channels] if i >= channels else 0
            up = previous[i]
            upleft = previous[i - channels] if i >= channels else 0
            if filt == 1:
                line[i] = (line[i] + left) & 0xFF
            elif filt == 2:
                line[i] = (line[i] + up) & 0xFF
            elif filt == 3:
                line[i] = (line[i] + ((left + up) >> 1)) & 0xFF
            elif filt == 4:
                line[i] = (line[i] + _paeth(left, up, upleft)) & 0xFF
        out += line
        previous = line

    # normalise to RGB, compositing any alpha onto white
    rgb = bytearray(width * height * 3)
    for i in range(width * height):
        if colour == 2:
            r, g, b, a = out[i * 3], out[i * 3 + 1], out[i * 3 + 2], 255
        elif colour == 6:
            r, g, b, a = out[i * 4:i * 4 + 4]
        elif colour == 0:
            r = g = b = out[i]
            a = 255
        else:  # grey + alpha
            r = g = b = out[i * 2]
            a = out[i * 2 + 1]
        if a != 255:
            r = (r * a + 255 * (255 - a)) // 255
            g = (g * a + 255 * (255 - a)) // 255
            b = (b * a + 255 * (255 - a)) // 255
        rgb[i * 3:i * 3 + 3] = bytes((r, g, b))
    return width, height, bytes(rgb)


# --------------------------------------------------------------------------
# the document
# --------------------------------------------------------------------------

def _esc(text: str) -> bytes:
    out = str(text).encode("latin-1", "replace")
    return out.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


class Report:
    """One dossier. Call the drawing methods, then save()."""

    LEFT = 56.0
    RIGHT = A4[0] - 56.0

    def __init__(self, logo: str | None = None, accent=INK):
        self.parts: list[bytes] = []
        self.pages: list[bytes] = []
        self.y = A4[1] - 64
        self.accent = accent
        self.running = ""
        self.logo = None
        if logo:
            try:
                self.logo = read_png(logo)
            except (OSError, ValueError):
                self.logo = None  # a missing logo must never fail a report

    # --- primitives -------------------------------------------------------

    def _text(self, x, y, size, text, font="F1", colour=BLACK):
        self.parts.append(
            b"BT /%s %.1f Tf %.3f %.3f %.3f rg %.2f %.2f Td (%s) Tj ET\n"
            % (font.encode(), size, colour[0], colour[1], colour[2], x, y,
               _esc(text))
        )

    def _rule(self, y, colour=LIGHT, width=0.8):
        self.parts.append(
            b"%.3f %.3f %.3f RG %.2f w %.2f %.2f m %.2f %.2f l S\n"
            % (colour[0], colour[1], colour[2], width, self.LEFT, y,
               self.RIGHT, y)
        )

    def _box(self, x, y, w, h, colour):
        self.parts.append(
            b"%.3f %.3f %.3f rg %.2f %.2f %.2f %.2f re f\n"
            % (colour[0], colour[1], colour[2], x, y, w, h)
        )

    @staticmethod
    def _width(text: str, size: float, bold: bool = False) -> float:
        # Helvetica averages close enough for wrapping decisions.
        return len(str(text)) * size * (0.55 if bold else 0.5)

    def wrap(self, text: str, size: float, width: float) -> list[str]:
        limit = max(8, int(width / (size * 0.5)))
        words, lines, current = [], [], ""
        for raw in str(text).split():
            while len(raw) > limit:  # long URLs have no spaces to break at
                words.append(raw[:limit])
                raw = raw[limit:]
            words.append(raw)
        for word in words:
            candidate = f"{current} {word}".strip()
            if self._width(candidate, size) > width and current:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines or [""]

    def _space(self, needed: float) -> None:
        if self.y - needed < 90:
            self._finish_page()

    # --- blocks -----------------------------------------------------------

    def header(self, org: str, title: str, subtitle: str = "") -> None:
        top = A4[1] - 46
        if self.logo:
            w, h, rgb = self.logo
            box = 30.0
            scale = box / max(w, h)
            self.parts.append(
                b"q %.2f 0 0 %.2f %.2f %.2f cm /Im1 Do Q\n"
                % (w * scale, h * scale, self.LEFT, top - h * scale + 11)
            )
            text_x = self.LEFT + box + 14
        else:
            text_x = self.LEFT
        self._text(text_x, top, 11, org, "F2", self.accent)
        self._rule(top - 14, self.accent, 1.2)
        self.running = f"{org}  \u00b7  {title}"[:110]
        self.y = top - 42
        self._text(self.LEFT, self.y, 17, title, "F2", BLACK)
        self.y -= 18
        if subtitle:
            for line in self.wrap(subtitle, 10.5, self.RIGHT - self.LEFT):
                self._text(self.LEFT, self.y, 10.5, line, "F1", GREY)
                self.y -= 13
        self.y -= 10

    def status(self, text: str) -> None:
        self._space(46)
        height = 26.0
        self._box(self.LEFT, self.y - 8, self.RIGHT - self.LEFT, height,
                  (0.95, 0.96, 0.97))
        self._box(self.LEFT, self.y - 8, 3, height, self.accent)
        self._text(self.LEFT + 12, self.y + 2, 10.5, text, "F2", BLACK)
        self.y -= height + 14

    def field(self, label: str, value: str) -> None:
        self._space(18)
        self._text(self.LEFT, self.y, 9, label.upper(), "F2", GREY)
        lines = self.wrap(value or "-", 10, self.RIGHT - self.LEFT - 130)
        for i, line in enumerate(lines):
            self._text(self.LEFT + 130, self.y - i * 12, 10, line, "F1", BLACK)
        self.y -= max(15, len(lines) * 12 + 3)

    def section(self, title: str) -> None:
        self._space(34)
        self.y -= 8
        self._text(self.LEFT, self.y, 11, title, "F2", self.accent)
        self.y -= 6
        self._rule(self.y, LIGHT)
        self.y -= 16

    def step(self, date: str, body: str, detail: str = "",
             marked: bool = False) -> None:
        self._space(40)
        if marked:
            self._box(self.LEFT - 8, self.y - 4, 3, 16, self.accent)
        self._text(self.LEFT, self.y, 10, date or "-", "F2", GREY)
        for i, line in enumerate(self.wrap(body, 10.5,
                                           self.RIGHT - self.LEFT - 90)):
            self._text(self.LEFT + 90, self.y - i * 13, 10.5, line, "F2"
                       if marked else "F1", BLACK)
            self.y -= 0 if i == 0 else 13
        self.y -= 13
        if detail:
            for line in self.wrap(detail, 9.5, self.RIGHT - self.LEFT - 90):
                self._text(self.LEFT + 90, self.y, 9.5, line, "F1", GREY)
                self.y -= 12
        self.y -= 5

    def result(self, text: str) -> None:
        """The outcome of one consultation, set apart so it is findable."""
        self._space(22)
        for i, line in enumerate(self.wrap(text, 10, self.RIGHT - self.LEFT - 90)):
            self._text(self.LEFT + 90, self.y, 10, line, "F2", self.accent)
            self.y -= 13
        self.y -= 3

    def quote(self, text: str) -> None:
        """The wording of the decision, verbatim. This is the part people
        actually came for, so it gets a rule and real space."""
        lines = self.wrap(text, 9.5, self.RIGHT - self.LEFT - 108)
        self._space(len(lines) * 12 + 14)
        top = self.y + 9
        for line in lines:
            self._text(self.LEFT + 104, self.y, 9.5, line, "F1", BLACK)
            self.y -= 12
        self.parts.append(
            b"%.3f %.3f %.3f RG 1.6 w %.2f %.2f m %.2f %.2f l S\n"
            % (LIGHT[0], LIGHT[1], LIGHT[2], self.LEFT + 94, top,
               self.LEFT + 94, self.y + 10)
        )
        self.y -= 6

    def link(self, label: str, title: str, url: str) -> None:
        """A document reference, with the URL kept so the file can be found."""
        self._space(28)
        for line in self.wrap(f"{label}: {title}", 9.5,
                              self.RIGHT - self.LEFT - 90):
            self._text(self.LEFT + 90, self.y, 9.5, line, "F1", BLACK)
            self.y -= 11
        for line in self.wrap(url, 8, self.RIGHT - self.LEFT - 90):
            self._text(self.LEFT + 90, self.y, 8, line, "F1", GREY)
            self.y -= 10
        self.y -= 3

    def note(self, text: str) -> None:
        self._space(24)
        for line in self.wrap(text, 9.5, self.RIGHT - self.LEFT):
            self._text(self.LEFT, self.y, 9.5, line, "F1", GREY)
            self.y -= 12
        self.y -= 4

    # --- output -----------------------------------------------------------

    def _footer(self, number: int, footer: str) -> None:
        self._rule(64, LIGHT)
        for i, line in enumerate(footer.split("\n")[:3]):
            self._text(self.LEFT, 52 - i * 11, 8, line, "F1", GREY)
        self._text(self.RIGHT - 40, 52, 8, f"Seite {number}", "F1", GREY)

    def _finish_page(self) -> None:
        self.pages.append(b"".join(self.parts))
        self.parts = []
        self.y = A4[1] - 64
        if self.running:  # a running head, so page two is not anonymous
            top = A4[1] - 46
            self._text(self.LEFT, top, 9, self.running, "F1", GREY)
            self._rule(top - 10, LIGHT)
            self.y = top - 34

    def save(self, path: str, footer: str = "") -> str:
        for index in range(len(self.pages) + 1):
            pass
        pending = self.parts
        self.parts = []
        self.pages.append(b"".join(pending))

        streams = []
        for i, content in enumerate(self.pages, start=1):
            self.parts = []
            self._footer(i, footer)
            streams.append(zlib.compress(content + b"".join(self.parts)))

        objects: list[bytes] = []

        def add(body: bytes) -> int:
            objects.append(body)
            return len(objects)

        font_regular = add(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>"
        )
        font_bold = add(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
            b"/Encoding /WinAnsiEncoding >>"
        )
        image_ref = None
        if self.logo:
            w, h, rgb = self.logo
            packed = zlib.compress(rgb)
            image_ref = add(
                b"<< /Type /XObject /Subtype /Image /Width %d /Height %d "
                b"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter "
                b"/FlateDecode /Length %d >>\nstream\n" % (w, h, len(packed))
                + packed
                + b"\nendstream"
            )

        resources = (
            b"<< /Font << /F1 %d 0 R /F2 %d 0 R >>" % (font_regular, font_bold)
        )
        if image_ref:
            resources += b" /XObject << /Im1 %d 0 R >>" % image_ref
        resources += b" >>"

        pages_ref = len(objects) + len(streams) * 2 + 1
        page_refs = []
        for packed in streams:
            content_ref = add(
                b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(packed)
                + packed
                + b"\nendstream"
            )
            page_refs.append(
                add(
                    b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] "
                    b"/Resources %s /Contents %d 0 R >>"
                    % (pages_ref, A4[0], A4[1], resources, content_ref)
                )
            )

        kids = b" ".join(b"%d 0 R" % ref for ref in page_refs)
        pages_obj = add(
            b"<< /Type /Pages /Count %d /Kids [%s] >>" % (len(page_refs), kids)
        )
        catalog = add(b"<< /Type /Catalog /Pages %d 0 R >>" % pages_obj)

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for number, body in enumerate(objects, start=1):
            offsets.append(len(out))
            out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
        start = len(out)
        out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
        for offset in offsets[1:]:
            out += b"%010d 00000 n \n" % offset
        out += (
            b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objects) + 1, catalog, start)
        )
        with open(path, "wb") as handle:
            handle.write(bytes(out))
        return path
