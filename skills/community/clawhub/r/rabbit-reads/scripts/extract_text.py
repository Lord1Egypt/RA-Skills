#!/usr/bin/env python3
"""
extract_text.py - normalize a source document to plain text.

    python3 extract_text.py book.epub
    python3 extract_text.py paper.pdf --out scratch/paper.txt
    python3 extract_text.py chapter.docx --stdout

One command per format family, so the reader loop always starts from the same
object: UTF-8 text, LF line endings, no markup. The converter is chosen by
extension and named in the output, because a silent chain of converters is how
a scanned PDF ends up read as an empty book.

Every format goes through rwlib.injection before anything is written, because
the text this produces is what the fan-out phase hands to subagents. The scan
runs over the richest representation of the document rather than over the
output: the raw xhtml for an epub chapter, the raw markup for an html file, and
the run properties for a .docx, since concealment lives in exactly the markup
the normalizer strips. A finding's `line` is a line in that representation, not
in the output file, which is the same trade rwlib.docx_text makes when it
reports a paragraph number.

Nothing is ever stripped or repaired here. The safety band surfaces and
quarantines, and an extractor that "cleaned up" an injection would hand the
reader a text file that looks honest and destroy the only evidence that it is
not.

Exit codes: 0 extracted. 1 extracted but flagged (a scanned PDF with no
text layer, or any format carrying a concealed directive). 2 usage, unreadable
input, a missing converter binary, or a converter that failed.

Stdlib only, 3.9+. Nothing in here writes into a tracked path by default:
output lands under scratch/ in the working directory, which .gitignore covers.
"""

import argparse
import glob
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
from html import unescape
from xml.etree import ElementTree
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if "_bootstrap" in sys.modules and getattr(sys.modules["_bootstrap"], "__file__", None) != os.path.join(HERE, "_bootstrap.py"):
    del sys.modules["_bootstrap"]
import _bootstrap
from _bootstrap import cli_error
from rwlib import artifacts, injection, language
from rwlib.findings import sort_key
from rwlib.endpoint import estimate_tokens

EXAMPLES = [
    "extract_text.py book.epub",
    "extract_text.py paper.pdf --out scratch/paper.txt",
    "extract_text.py chapter.docx --stdout",
]

SUPPORTED = (".txt", ".md", ".docx", ".docm", ".pdf", ".doc", ".rtf",
             ".html", ".htm", ".odt", ".epub")

GUARDRAIL = ("Intermediates belong under a gitignored scratch/ or outside any "
             "repo, never in tracked paths.")

# Enough extracted characters to call a PDF a text document. Under this the
# file is almost certainly page images, and pretending otherwise hands the
# reader an empty book with a 0 exit code.
MIN_PDF_CHARS = 200

# The scanned-PDF verdict is a reading instruction, not a converter failure,
# which is why it costs exit 1 beside the hidden-directive case rather than 2.
SCANNED_VERDICT = ("likely a scanned PDF with no text layer, needs OCR before "
                   "any reading (tesseract, or the print-disabled route your "
                   "platform offers)")

# Shared by the extractors and the --check preflight, so the hint a failing
# conversion prints is word for word the one the preflight shows up front.
PDF_HINT = ("Install poppler: `brew install poppler` on macOS, "
            "`apt-get install poppler-utils` on Debian/Ubuntu.")
TEXTUTIL_HINT = ("textutil ships with macOS. On another platform convert the "
                 "file on a Mac, or via pandoc / libreoffice, and feed the "
                 "result in as .txt or .md.")

# Demarcation between concatenated sources. Deliberately matches nothing in
# map_structure.py: no `Chapter N`, no bare `N.`, no ATX hashes, so a
# demarcation line never surfaces as a section boundary.
SOURCE_DEMARC = "========== rabbit-reads source: %s =========="


def die_usage(message):
    print(cli_error.format_llm_error("extract_text.py", message,
                                     examples=EXAMPLES), file=sys.stderr)
    return 2


def die_io(parameter, path, details):
    print(cli_error.format_file_error("extract_text.py", path, parameter,
                                      details=details, examples=EXAMPLES),
          file=sys.stderr)
    return 2


def read_passthrough(path):
    """txt and md: the text itself, with CRLF flattened and any BOM gone.

    Decoding is utf-8 because everything upstream in this plugin already
    treats utf-8 as the floor, and a latin-1 fallback would silently rename
    mojibake to prose. A file that is not utf-8 is an exit 2 the reader can
    see, not a book that scans clean while reading wrong.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    try:
        # utf-8-sig eats a BOM when present and decodes plain utf-8 untouched.
        return data.decode("utf-8-sig").replace("\r\n", "\n")
    except UnicodeDecodeError as exc:
        raise IOError("not utf-8: %s" % exc)


def run_converter(argv, path, parameter, install_hint):
    try:
        result = subprocess.run(argv, capture_output=True)
    except OSError as exc:
        return None, die_io(parameter, argv[0],
                            "converter binary not found or not runnable: %s. %s"
                            % (exc, install_hint))
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip() or (
            "exited %d" % result.returncode)
        return None, die_io(parameter, path, detail)
    return result.stdout.decode("utf-8", "replace"), 0


def extract_pdf(path):
    hint = PDF_HINT
    text, code = run_converter(["pdftotext", "-enc", "UTF-8", path, "-"],
                               path, "source (.pdf)", hint)
    if code:
        return text, code
    stripped = "".join(text.split())
    if len(stripped) < MIN_PDF_CHARS:
        print(SCANNED_VERDICT, file=sys.stderr)
        return text, 1
    return text, 0


def extract_textutil(path):
    hint = TEXTUTIL_HINT
    return run_converter(["textutil", "-convert", "txt", "-stdout", path],
                         path,
                         "source (%s)" % os.path.splitext(path)[1].lower(),
                         hint)


CONTAINER_NS = "{urn:oasis:names:tc:opendocument:xmlns:container}"
OPF_NS = "{http://www.idpf.org/2007/opf}"


def extract_epub(path):
    """The spine, in order, tags stripped, chapters joined by a blank line.

    Returns (text, spans, exit_code), where spans is the raw xhtml of each
    chapter paired with its name inside the archive. The raw markup is what
    the safety scan reads: strip_xhtml deletes an html comment outright, so a
    concealed directive scanned after the strip is a directive nobody can see
    and nobody was told about. Scanning the markup keeps the evidence, and the
    finding names the chapter because that is where a reader has to go to look
    at it.

    The container indirection exists so an epub can keep its content in any
    directory it likes, so the OPF path is read from META-INF/container.xml
    rather than guessed. hrefs are relative to the OPF, not to the zip root,
    which is the one detail every hand-rolled epub reader gets wrong.
    """
    try:
        with zipfile.ZipFile(path) as zf:
            container = ElementTree.fromstring(zf.read("META-INF/container.xml"))
            rootfile = container.find(".//" + CONTAINER_NS + "rootfile")
            if rootfile is None or not rootfile.get("full-path"):
                raise KeyError("container.xml names no rootfile")
            opf_path = rootfile.get("full-path")
            opf = ElementTree.fromstring(zf.read(opf_path))
            base = posixpath.dirname(opf_path)

            hrefs = {}
            for item in opf.iter(OPF_NS + "item"):
                hrefs[item.get("id")] = item.get("href")

            chapters, spans = [], []
            for itemref in opf.iter(OPF_NS + "itemref"):
                href = hrefs.get(itemref.get("idref"))
                if not href or href.rsplit(".", 1)[-1].lower() not in (
                        "xhtml", "html", "htm"):
                    continue
                name = posixpath.normpath(posixpath.join(base, href))
                markup = zf.read(name).decode("utf-8", "replace")
                spans.append((name, markup))
                chapters.append(strip_xhtml(markup))
    except (OSError, KeyError, zipfile.BadZipFile,
            ElementTree.ParseError) as exc:
        return None, [], die_io("source (.epub)", path,
                                "not a readable epub: %s" % exc)
    return "\n\n".join(c for c in chapters if c.strip()) + "\n", spans, 0


TAG_RX = re.compile(r"<[^>]+>")
SCRIPT_STYLE_RX = re.compile(r"<(script|style)\b.*?</\1\s*>", re.S | re.I)
# Block-closing tags mark line breaks the way a reader saw them, so list
# items and paragraphs survive the tag strip as separate lines.
BLOCK_CLOSE_RX = re.compile(r"</\s*(p|div|h[1-6]|li|tr|blockquote|section)\s*>",
                            re.I)
LINEBREAK_RX = re.compile(r"<\s*br\s*/?\s*>", re.I)


def strip_xhtml(markup):
    text = SCRIPT_STYLE_RX.sub(" ", markup)
    text = LINEBREAK_RX.sub("\n", text)
    text = BLOCK_CLOSE_RX.sub("\n", text)
    text = TAG_RX.sub("", text)
    text = unescape(text)
    # Single spacing inside a block, one blank line between blocks: the same
    # shape the docx extractor emits, so downstream tools see one form rather
    # than a per-format paragraph convention.
    lines = [line.strip() for line in text.splitlines()]
    out, pending_blank = [], False
    for line in lines:
        if not line:
            pending_blank = bool(out)
            continue
        if out and pending_blank:
            out.append("")
        out.append(line)
        pending_blank = False
    return "\n".join(out)


def extract_docx(path):
    """Visible text plus the findings a .docx declares about its own runs.

    Returns (text, findings, exit_code), where exit_code is 2 or 0: whether a
    safety P0 costs exit 1 is decided once in main(), for every format, rather
    than here for this one. The visible text is scanned like any other format
    afterwards, and the two do not overlap: these findings are about the runs
    a reader never sees, which is exactly what the visible text excludes.
    """
    try:
        from rwlib import docx_text
    except (ImportError, ModuleNotFoundError) as exc:
        return None, [], die_io("source (.docx/.docm)", path,
                                "rwlib.docx_text module not found: %s" % exc)
    try:
        text, findings = docx_text.extract(path)
    except docx_text.DocxError as exc:
        return None, [], die_io("source (.docx/.docm)", path, str(exc))
    return text, findings, 0


def extract_html(path):
    """HTML and HTM: stripped via stdlib strip_xhtml.

    Returns (text, spans, exit_code). The span is the raw markup, for the
    reason extract_epub gives: the strip is what an injection hides behind.
    """
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        raw = data.decode("utf-8-sig", "replace").replace("\r\n", "\n")
        return strip_xhtml(raw) + "\n", [("", raw)], 0
    except OSError as exc:
        return None, [], die_io(
            "source (%s)" % os.path.splitext(path)[1].lower(), path, str(exc))


def safety_findings(spans):
    """Every rwlib.injection finding over `spans`, worst first.

    `spans` is [(context, text)]. The context names where inside the document
    the text came from and is empty when the whole document is one span. It
    rides in the label because the finding schema carries one line number and
    has nowhere else to put it, and without it an epub reports twelve findings
    at "line 4" of nothing in particular.
    """
    out = []
    for context, text in spans:
        for finding in injection.scan(text):
            if context:
                finding["label"] = "%s: %s" % (context, finding["label"])
            out.append(finding)
    out.sort(key=sort_key)
    return out


def invisible_note(text):
    """One line about the invisible characters in the extracted text, or None.

    A note rather than a finding, because the judgement already has a home.
    A run of Unicode tag characters that decodes to words is
    injection.tag_runs' P0 and comes back through safety_findings. Everything
    under that floor is the paste residue scan.py reports on the notes
    themselves, once they exist. What is left for this script is telling a
    reader that the text about to be fanned out to subagents is not the plain
    ASCII it looks like. Nothing here is stripped.
    """
    parts = []
    zero_width = sum(len(artifacts.occurrences(text, ch))
                     for ch in artifacts.ZERO_WIDTH)
    if zero_width:
        parts.append("%d zero-width" % zero_width)
    tags = len(artifacts.range_occurrences(text, artifacts.TAG_RX))
    if tags:
        parts.append("%d unicode-tag" % tags)
    # Per-character, because the tolerances are per-character: enough LRM for
    # real mixed-script typography is not the same number as one override.
    bidi = 0
    for ch in artifacts.REPORT_ONLY_UNICODE:
        seen = len(artifacts.occurrences(text, ch))
        if seen > artifacts.REPORT_ONLY_TOLERANCE.get(ch, 0):
            bidi += seen
    if bidi:
        parts.append("%d direction-formatting" % bidi)
    unlisted = artifacts.unlisted_invisibles(text)
    if unlisted:
        parts.append("%d unlisted (%s)"
                     % (sum(len(v) for v in unlisted.values()),
                        ", ".join("U+%04X" % ord(ch)
                                  for ch in sorted(unlisted))))
    if not parts:
        return None
    return ("invisible characters: %s. Nothing was stripped."
            % ", ".join(parts))


def print_findings(findings, stream, header="Safety findings"):
    stream.write("%s\n" % header)
    for f in findings:
        stream.write("  L%-4d %s %s: %s\n"
                     % (f.get("line", 0), f.get("priority", "?"),
                        f.get("id", "?"), f.get("label", "")))


def run_preflight(stream):
    """The --check report: which converters exist, what that makes usable.

    Informational by design: it processes nothing and exits 0 whether or not
    the external binaries are there, because a hard-fail preflight is a
    different flag with a different contract. The hints are the same
    constants the failing conversions print, so the advice never drifts.
    """
    usable = {"txt", "md", "html", "htm", "epub"}
    for name, hint, enables in (
            ("pdftotext", PDF_HINT, ("pdf",)),
            ("textutil", TEXTUTIL_HINT, ("doc", "rtf", "odt"))):
        found = shutil.which(name)
        if found:
            stream.write("%s: FOUND: %s\n" % (name, found))
            usable.update(enables)
        else:
            stream.write("%s: MISSING. %s\n" % (name, hint))
    order = ["txt", "md", "docx", "docm", "pdf", "doc", "rtf", "html",
             "htm", "odt", "epub"]
    # docx and docm go through the stdlib reader, so they ride with the
    # always-usable set rather than behind either external binary.
    usable.update(("docx", "docm"))
    ok = [f for f in order if f.lstrip(".") in usable]
    no = [f for f in order if f.lstrip(".") not in usable]
    stream.write("usable now: %s\n" % (", ".join(ok) or "none"))
    if no:
        stream.write("not usable: %s\n" % ", ".join(no))
    return 0


def print_findings(findings, stream, header="Safety findings"):
    stream.write("%s\n" % header)
    for f in findings:
        stream.write("  L%-4d %s %s: %s\n"
                     % (f.get("line", 0), f.get("priority", "?"),
                        f.get("id", "?"), f.get("label", "")))


def normalize_one(path):
    """(text, findings, converter, code) for one source.

    The per-format branch bodies main() used to inline, factored out so a
    multi-source run converts and safety-scans each file the same way the
    single-source run always has. code is this source's contribution to the
    exit: 2 a failed conversion (the caller stops), 1 a scanned PDF or a
    concealed directive (the text still lands), 0 clean.
    """
    ext = os.path.splitext(path)[1].lower()
    findings, spans = [], None
    if ext in (".txt", ".md"):
        try:
            text, code = read_passthrough(path), 0
        except IOError as exc:
            return None, [], None, die_io("source", path, str(exc))
        converter = "passthrough"
    elif ext in (".docx", ".docm"):
        text, findings, code = extract_docx(path)
        if code == 2:
            return None, [], None, 2
        converter = "rwlib.docx_text"
    elif ext == ".pdf":
        text, code = extract_pdf(path)
        if code == 2:
            return None, [], None, 2
        converter = "pdftotext"
    elif ext == ".epub":
        text, spans, code = extract_epub(path)
        if code:
            return None, [], None, code
        converter = "stdlib zipfile (epub spine)"
    elif ext in (".html", ".htm"):
        text, spans, code = extract_html(path)
        if code:
            return None, [], None, code
        converter = "stdlib html (strip_xhtml)"
    else:
        text, code = extract_textutil(path)
        if code:
            return None, [], None, code
        converter = "textutil"
    findings.extend(safety_findings(
        spans if spans is not None else [("", text)]))
    # One rule, every format. A concealed directive still produces the text
    # file, because a reader has to see what was extracted before judging it,
    # and then costs exit 1 the way the scanned PDF does: flagged, not lost.
    if any(f.get("band") == "safety" and f.get("priority") == "P0"
           for f in findings):
        code = 1
    return text, findings, converter, code


def expand_sources(entries):
    """The positional entries as one ordered file list, or an error string.

    Each entry expands in this order: an existing directory becomes its
    sorted non-recursive supported members; a glob pattern becomes its sorted
    file matches; anything else is one file that has to exist and be
    supported. Order is the merge order, so it is stable on purpose.
    """
    files = []
    for entry in entries:
        if os.path.isdir(entry):
            members = sorted(
                n for n in os.listdir(entry)
                if os.path.splitext(n)[1].lower() in SUPPORTED
                and os.path.isfile(os.path.join(entry, n)))
            if not members:
                return die_io("source", entry,
                              "no supported files (%s) in directory"
                              % ", ".join(SUPPORTED))
            files.extend(os.path.join(entry, n) for n in members)
        elif any(c in entry for c in "*?["):
            matches = sorted(p for p in glob.glob(entry) if os.path.isfile(p))
            if not matches:
                return die_io("source", entry, "glob matched no files")
            files.extend(matches)
        else:
            if not os.path.isfile(entry):
                return die_io("source", entry, "no such file")
            files.append(entry)
    for path in files:
        if os.path.splitext(path)[1].lower() not in SUPPORTED:
            return die_usage("unsupported format %r in %r. Supported: %s"
                             % (os.path.splitext(path)[1].lower(), path,
                                ", ".join(SUPPORTED)))
    return files


def _force_utf8_streams():
    """Reconfigure stdout/stderr to UTF-8.

    This tool's whole job is surfacing text a document is hiding, including
    tag-smuggled characters `injection.py` decodes and prints in a finding's
    label. Windows defaults a piped or redirected stream to the system
    codepage (often cp1252), which raises `UnicodeEncodeError` on anything
    outside Latin-1, crashing before the finding it exists to report ever
    reaches the caller. `reconfigure` is a no-op on a stream that is already
    UTF-8, which every other platform's default already is.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def main(argv=None):
    _force_utf8_streams()
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=EXAMPLES)
    ap.add_argument("sources", metavar="PATH", nargs="*",
                    help="the document(s) to normalize: %s. A directory "
                         "expands to its sorted supported members, a glob to "
                         "its matches, and several sources merge in the order "
                         "given, each behind a demarcation line"
                         % ", ".join(SUPPORTED))
    ap.add_argument("--out", metavar="PATH",
                    help="where the text goes. Defaults to "
                         "scratch/<source-stem>.txt under the working "
                         "directory for one source; required for several, "
                         "which also writes <out>.manifest.json")
    ap.add_argument("--stdout", action="store_true",
                    help="print the text instead of writing a file, with the "
                         "stats on stderr so stdout stays pipeable")
    ap.add_argument("--check", action="store_true",
                    help="report which converters are installed and which "
                         "input formats are therefore usable, then exit 0. "
                         "Processes nothing")
    args = ap.parse_args(argv)

    if args.check:
        if args.sources:
            return die_usage("--check processes nothing, so it cannot be "
                             "combined with source paths")
        return run_preflight(sys.stdout)
    if not args.sources:
        return die_usage("give at least one source path, or --check")

    files = expand_sources(args.sources)
    if isinstance(files, int):
        return files

    multi = len(files) > 1
    if multi and args.stdout:
        return die_usage("multiple sources cannot go to --stdout; give --out "
                         "so the merge and its manifest land somewhere")
    if multi and not args.out:
        return die_usage("multiple sources need --out: there is no single "
                         "stem to name a default output after")

    if not multi:
        # One source: the shape this script has always had, byte for byte.
        path = files[0]
        text, findings, converter, code = normalize_one(path)
        if code == 2:
            return 2
        if findings:
            print_findings(findings, sys.stderr if args.stdout else sys.stdout)

        out_path = args.out or os.path.join(
            "scratch", "%s.txt" % os.path.splitext(os.path.basename(path))[0])
        if args.stdout:
            sys.stdout.write(text)
        else:
            os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                        exist_ok=True)
            with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)

        stats = sys.stderr if args.stdout else sys.stdout
        stats.write("format: %s\n" % (os.path.splitext(path)[1].lstrip(".")
                                      or "none"))
        stats.write("converter: %s\n" % converter)
        stats.write("bytes in: %d\n" % os.path.getsize(path))
        stats.write("chars out: %d\n" % len(text))
        stats.write("words out: %d\n" % len(text.split()))
        stats.write("lines out: %d\n" % len(text.splitlines()))
        # A budget, not a tokenizer; rwlib.endpoint pins the pessimism.
        stats.write("est. tokens: %d\n" % estimate_tokens(text))
        stats.write("output: %s\n"
                    % ("<stdout>" if args.stdout else out_path))
        invisible = invisible_note(text)
        if invisible:
            stats.write(invisible + "\n")
        foreign = language.note(text)
        if foreign:
            stats.write(foreign + "\n")
        stats.write(GUARDRAIL + "\n")
        return code

    merged_parts, manifest = [], []
    line_cursor, code = 0, 0
    for path in files:
        text, findings, converter, src_code = normalize_one(path)
        if src_code == 2:
            return 2
        demarc = SOURCE_DEMARC % path
        # Each source is one block: the demarcation line, its text, and a
        # blank separator. line_offset addresses the demarcation, which is
        # where the source's slice of the merged file begins.
        offset = line_cursor + 1
        merged_parts.append(demarc + "\n")
        if not text.endswith("\n"):
            text += "\n"
        merged_parts.append(text)
        merged_parts.append("\n")
        line_cursor += len(text.splitlines()) + 2
        manifest.append({"path": path, "converter": converter,
                         "bytes_in": os.path.getsize(path),
                         "words": len(text.split()),
                         "line_offset": offset})
        if findings:
            stream = sys.stderr if args.stdout else sys.stdout
            print_findings(findings, stream, "Safety findings: %s" % path)
        code = max(code, src_code)

    merged = "".join(merged_parts)
    out_path = args.out
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(merged)
    manifest_path = out_path + ".manifest.json"
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")

    stats = sys.stderr if args.stdout else sys.stdout
    stats.write("sources: %d\n" % len(files))
    for i, entry in enumerate(manifest):
        stats.write("source[%d]: %s (%s, %d bytes in, %d words, line %d)\n"
                    % (i, entry["path"], entry["converter"],
                       entry["bytes_in"], entry["words"],
                       entry["line_offset"]))
    stats.write("chars out: %d\n" % len(merged))
    stats.write("words out: %d\n" % len(merged.split()))
    stats.write("lines out: %d\n" % len(merged.splitlines()))
    # A budget, not a tokenizer; rwlib.endpoint pins the pessimism.
    stats.write("est. tokens: %d\n" % estimate_tokens(merged))
    stats.write("output: %s\n" % out_path)
    stats.write("manifest: %s\n" % manifest_path)
    invisible = invisible_note(merged)
    if invisible:
        stats.write(invisible + "\n")
    foreign = language.note(merged)
    if foreign:
        stats.write(foreign + "\n")
    stats.write(GUARDRAIL + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
