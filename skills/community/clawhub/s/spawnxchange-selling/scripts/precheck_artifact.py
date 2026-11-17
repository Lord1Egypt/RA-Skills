#!/usr/bin/env python3
"""Look over an artifact folder before you package and publish it.

Standard library only. No network access, no credentials, nothing written and
nothing copied: this reads one folder and tells you what is in it that you may
not want to sell, while changing it is still cheap.

Anything that looks like a secret is reported as a file and a line number, never
as the value. Output like this ends up in transcripts and CI logs, and a checker
that quotes the key it found has moved that key somewhere it will be kept.

Check the folder, fix what it finds, check again, and only then package. That
order is the point — once the archive exists, every fix means building it again,
and once it is listed the bytes are with buyers.

It is advisory. It is not the marketplace's safety scan, it does not predict
that scan's verdict, and passing here is not approval — it is one careful look
before you spend a fee and hand your bytes to buyers, who receive them exactly
as you upload them.

Two severities:

  STOP  Something that does not belong in a listing at all: a compiled program,
        an archive nested inside your source, or a vendored dependency tree.
  LOOK  Something worth a human decision. For each one you are deciding between
        three things: it is a fair part of what you are selling, it is a leak
        you want to remove, or it is something that should not be published.
        Only you can tell those apart.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Directories that carry somebody else's code, your version control history, or a
# build cache. None of it is what a buyer is paying for, all of it bloats the
# archive, and a dependency tree is a common way for something unreviewed to end
# up inside a listing.
VENDORED_DIRS = {
    "node_modules", ".venv", "venv", "vendor", ".git", ".hg", ".svn",
    "__pycache__", ".tox", ".mypy_cache", ".pytest_cache", ".gradle", ".terraform",
    "bower_components", "site-packages",
}
# Build output is sometimes deliberate, so it is raised rather than refused.
BUILD_DIRS = {"dist", "build", "target", "out", ".next", ".nuxt", ".output"}

# How much of any one file is examined. A pre-flight check must not be the thing
# that runs out of memory, and source files are small: a text file larger than
# this is itself worth remarking on, which is what the "too large to be source"
# finding does.
SCAN_BYTES_PER_ENTRY = 128 * 1024
SNIFF_BYTES = 8192

# A folder belongs to the operator, so these are not defences against a hostile
# input the way an archive reader's would be. They are here so that pointing this
# at the wrong directory reports that it is too big and stops, instead of walking
# a filesystem until something runs out of memory.
# How many line numbers to name per pattern per file before summarising. A
# committed `.env` hits on every line; five is enough to go and look.
MAX_MATCH_LINES = 5
MAX_FILES = 20000
MAX_TOTAL_SCANNED = 64 * 1024 * 1024

NUL_BYTE = bytes([0])

# What `file` looks for. Executable code is a different finding from binary
# data: a compiled program is dead weight a buyer cannot read or review, while a
# database, an image or a PDF may be exactly what is being sold.
# Android bytecode. The version digits move between platform releases, so each
# is listed rather than matching a bare "dex\n" prefix that a text file could
# begin with.
DEX_SIGNATURES = tuple(
    (bytes.fromhex("6465780a") + version + bytes([0]),
     "an Android DEX executable")
    for version in (b"035", b"037", b"038", b"039", b"040")
)

ELF_MAGIC = bytes.fromhex("7f454c46")
# Mach-O stores its magic in the file's own byte order, so the byte sequence
# gives both the width and the endianness. An iOS or macOS binary is one of
# these; an .ipa or .apk is a zip and is caught as a nested archive.
MACHO_MAGICS = {
    bytes.fromhex("cefaedfe"): ("little", "32-bit"),
    bytes.fromhex("cffaedfe"): ("little", "64-bit"),
    bytes.fromhex("feedface"): ("big", "32-bit"),
    bytes.fromhex("feedfacf"): ("big", "64-bit"),
}
# A COFF object file has no magic number, only a machine type. Recognising one
# needs the header's shape as well: see _coff_object_description.
COFF_MACHINES = {
    0x014C: "x86", 0x8664: "x86-64", 0xAA64: "ARM64", 0x01C0: "ARM",
    0x01C4: "ARM Thumb-2", 0x0200: "Itanium", 0x0166: "MIPS",
    0x01F0: "PowerPC", 0x5032: "RISC-V 32", 0x5064: "RISC-V 64",
}

EXECUTABLE_SIGNATURES = (
    (b"MZ", "a Windows executable or DLL"),
    (bytes.fromhex("cafebabe"), "a Java class or a universal Mach-O binary"),
    (bytes.fromhex("cafebabf"), "a 64-bit universal Mach-O binary"),
    (bytes.fromhex("0061736d"), "a WebAssembly module"),
    (b"!<arch>", "a static library: an archive of object files"),
    (bytes.fromhex("4243c0de"), "LLVM bitcode: compiled, but not yet linked"),
    (bytes.fromhex("edabeedb"), "an RPM package"),
) + DEX_SIGNATURES
# An archive inside an archive: neither you nor the marketplace can see what is
# in it without unpacking it, so it is not something to ship unexamined.
NESTED_ARCHIVE_SIGNATURES = (
    (bytes.fromhex("504b0304"), "a nested zip archive"),
    (bytes.fromhex("1f8b"), "a nested gzip archive"),
    (b"BZh", "a nested bzip2 archive"),
    (bytes.fromhex("fd377a585a"), "a nested xz archive"),
    (bytes.fromhex("377abcaf271c"), "a nested 7-zip archive"),
    (b"Rar!", "a nested RAR archive"),
)
DATA_SIGNATURES = (
    (b"SQLite format 3", "a SQLite database, which may hold rows you did not "
                         "mean to publish"),
    (bytes.fromhex("89504e47"), "a PNG image"),
    (bytes.fromhex("ffd8ff"), "a JPEG image"),
    (b"GIF8", "a GIF image"),
    (b"%PDF", "a PDF"),
    (b"OggS", "an Ogg media file"),
    (bytes.fromhex("1a45dfa3"), "a Matroska or WebM media file"),
    (bytes.fromhex("00010000"), "a TrueType font"),
    (b"OTTO", "an OpenType font"),
    (b"wOF", "a web font"),
)

# Things worth a second look. Deliberately broad: this is a prompt for a human
# decision, not a detector, and a false positive costs you five seconds.
LOOK_PATTERNS = (
    ("private key material (a PEM block)", re.compile(
        r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("a 64-character hex value (a key, or a hash)", re.compile(
        r"\b0x[a-fA-F0-9]{64}\b")),
    ("a cloud metadata endpoint", re.compile(
        r"169\.254\.169\.254|metadata\.google\.internal", re.IGNORECASE)),
    ("a cloud access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    # A name that sounds like a credential, assigned a literal that looks like
    # one. The value must be a quoted string or a bare env-file value: that is
    # what keeps `token = rest[index];` from reading as a leak.
    ("an assigned secret, key or token", re.compile(
        r"""(?i)[A-Z0-9_.-]*(?:api[_-]?key|secret|passwd|password|token|"""
        r"""credential)[A-Z0-9_.-]*\s*[:=]\s*"""
        r"""(?:["'][A-Za-z0-9_.\-/+=:]{12,}["']|[A-Za-z0-9_.\-/+=]{12,}\s*$)""",
        re.MULTILINE)),
    # A line naming who wrote or owns the code. Buyers get it under the
    # marketplace licence, so a holder line in the files says otherwise. The
    # year is required after "(c)" so `f(c)` in code stays quiet.
    ("an author or copyright line", re.compile(
        r"\bcopyright\b|\u00a9|\(c\)\s*\d{4}|^\W*@?author\b|__author__\s*=",
        re.IGNORECASE | re.MULTILINE)),
    ("an email address", re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("a blockchain address", re.compile(
        r"\b0x[a-fA-F0-9]{40}\b|\bbc1[a-z0-9]{25,59}\b")),
    ("a street address", re.compile(
        r"\b\d+\s+[A-Za-z0-9\s,.-]{3,40}\s+"
        r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|"
        r"Place|Pl|Court|Ct|Parkway|Pkwy|Highway|Hwy)\b", re.IGNORECASE)),
)

# Files whose whole purpose is to hold configuration you did not mean to ship.
# Matched against the relative paths inside the folder being checked, and only
# so the seller is told to leave them out of the archive. A match is reported
# by path; the file is not opened for it, and no location outside the folder
# is ever looked at.
SENSITIVE_NAMES = re.compile(
    r"(?:^|/)(?:\.env(?:\..+)?|\.npmrc|\.pypirc|\.netrc|id_rsa|id_ed25519|"
    r"\.aws/credentials|credentials\.json|service-account.*\.json)$",
    re.IGNORECASE,
)


class PrecheckError(Exception):
    """Raised for an archive that cannot be read at all."""


def _elf_description(data):
    """Name an ELF file by its e_type, which separates an object from a program."""
    if len(data) < 18:
        return "an ELF binary"
    order = "little" if data[5] == 1 else "big"
    return {
        1: "an ELF object file, before linking",
        2: "an ELF executable",
        3: "an ELF shared library or position-independent executable",
        4: "an ELF core dump",
    }.get(int.from_bytes(data[16:18], order), "an ELF binary")


def _macho_description(data, order, width):
    """Name a Mach-O file by its filetype field, at a fixed offset of 12."""
    kind = "binary"
    if len(data) >= 16:
        kind = {
            1: "object file, before linking",
            2: "executable",
            6: "dynamic library",
            8: "loadable bundle",
        }.get(int.from_bytes(data[12:16], order), "binary")
    return f"a {width} Mach-O {kind} (macOS or iOS)"


def _coff_object_description(data):
    """Recognise an unlinked Windows object file, which carries no magic number.

    The machine type must be one we know, and the optional-header size must be
    zero: an object file has no optional header, an executable image does. Both
    conditions together are what keeps this from matching arbitrary bytes.
    """
    if len(data) < 20:
        return None
    machine = int.from_bytes(data[0:2], "little")
    if machine not in COFF_MACHINES:
        return None
    if int.from_bytes(data[16:18], "little") != 0:
        return None
    return ("a Windows COFF object file, before linking "
            f"({COFF_MACHINES[machine]})")


def looks_binary(data):
    """Classify a file by content, the way `file` does.

    Returns (description, kind) where kind is "executable", "nested archive" or
    "data", or (None, None) for text. Signatures come first so the message can
    name the thing; otherwise a NUL byte or a high share of non-text bytes is
    what separates a compiled artifact from source. This reads content, not the
    file extension, so renaming does not change the answer.
    """
    if not data:
        return None, None

    if data.startswith(ELF_MAGIC):
        return _elf_description(data), "executable"
    for magic, (order, width) in MACHO_MAGICS.items():
        if data.startswith(magic):
            return _macho_description(data, order, width), "executable"
    for signature, description in EXECUTABLE_SIGNATURES:
        if data.startswith(signature):
            return description, "executable"
    for signature, description in NESTED_ARCHIVE_SIGNATURES:
        if data.startswith(signature):
            return description, "nested archive"
    for signature, description in DATA_SIGNATURES:
        if data.startswith(signature):
            return description, "data"

    coff = _coff_object_description(data)
    if coff:
        return coff, "executable"

    head = data[:SNIFF_BYTES]
    if NUL_BYTE in head:
        return "binary (contains null bytes)", "data"
    printable = sum(
        1 for byte in head
        if byte in (9, 10, 13) or 0x20 <= byte < 0x7F or byte >= 0x80
    )
    if head and printable / len(head) < 0.85:
        return "binary (mostly non-text bytes)", "data"
    return None, None


class Entry:
    """One file, sampled in memory. Nothing is ever copied or extracted."""

    def __init__(self, name, size, data):
        self.name = name
        self.size = size
        self.data = data


class _Budget:
    """What one folder is allowed to cost this process.

    The folder belongs to the operator, so this is not a defence against a
    hostile input the way an archive reader needs to be. It is here so that
    pointing this script at the wrong directory — a home directory, a filesystem
    root — reports that it is too big and stops, rather than walking until
    something runs out of memory.
    """

    def __init__(self):
        self.files = 0
        self.scanned = 0

    def add_file(self):
        self.files += 1
        if self.files > MAX_FILES:
            return (f"the folder holds more than {MAX_FILES} files. That is far more "
                    f"than a source listing normally contains — check that this is "
                    f"the directory you meant.")
        return None

    def take(self, want):
        """How much of `want` there is still room to read."""
        return max(0, min(want, MAX_TOTAL_SCANNED - self.scanned))

    def spend(self, count):
        self.scanned += count


def _read_folder(root):
    """Walk `root` and sample every file in it.

    Returns (problems, entries, total_bytes). Symbolic links are reported and
    never followed: following one would take the walk outside the folder, and a
    link is not something an archive of source code should be carrying anyway.
    """
    problems, entries, total = [], [], 0
    budget = _Budget()

    for directory, subdirectories, filenames in os.walk(root, followlinks=False):
        here = Path(directory)
        # Prune symlinked directories before descending, and say so.
        kept = []
        for name in sorted(subdirectories):
            if (here / name).is_symlink():
                problems.append(
                    f"a directory is a symbolic link and was not followed: "
                    f"{(here / name).relative_to(root).as_posix()}/")
            else:
                kept.append(name)
        subdirectories[:] = kept

        for name in sorted(filenames):
            item = here / name
            relative = item.relative_to(root).as_posix()

            if item.is_symlink():
                problems.append(f"a file is a symbolic link: {relative}")
                continue
            if not item.is_file():
                # A socket or device node. Not sellable, and not readable either.
                problems.append(f"an entry is not a regular file: {relative}")
                continue

            problem = budget.add_file()
            if problem:
                problems.append(problem)
                return problems, entries, total

            try:
                size = item.stat().st_size
            except OSError as error:
                problems.append(f"a file could not be read: {relative} ({error})")
                continue

            # A file read short of its sample would pass every check unexamined.
            # Stop and say so rather than report a clean result for it.
            want = min(SCAN_BYTES_PER_ENTRY, size)
            if budget.take(want) < want:
                problems.append(
                    f"the check stopped after examining {budget.scanned} bytes; "
                    f"{relative} and any files after it were not examined. That is "
                    f"far more than a source listing normally contains — check that "
                    f"this is the directory you meant.")
                return problems, entries, total

            try:
                with item.open("rb") as handle:
                    data = handle.read(want)
            except OSError as error:
                problems.append(f"a file could not be read: {relative} ({error})")
                continue

            budget.spend(len(data))
            total += size
            entries.append(Entry(relative, size, data))

    return problems, entries, total


def suggest_pack_command(root, excluded):
    """The tar command that packages this folder without what was flagged.

    The point of checking before packaging is that the fix is still cheap, so
    the script says what the fix looks like rather than leaving it as an
    exercise. Directories only: a single leaked file is a decision, not
    something to paper over with an exclude.
    """
    name = Path(root).resolve().name or "artifact"
    if not excluded:
        return f"tar -czf {name}.tar.gz -C {root} ."
    flags = " ".join(f"--exclude='./{directory}'" for directory in sorted(excluded))
    return f"tar -czf {name}.tar.gz -C {root} {flags} ."


def plural(count):
    return f"{count} file" if count == 1 else f"{count} files"


def directory_of(name, groups):
    """The first path segment of `name` that names one of `groups`."""
    for part in name.split("/")[:-1]:
        if part in groups:
            return part
    return None


def precheck_folder(folder_path):
    """Read the folder and describe what is in it. Returns a plain dict."""
    root = Path(folder_path)
    if not root.is_dir():
        raise PrecheckError(f"not a folder: {root}")

    try:
        problems, entries, total_bytes = _read_folder(root)
    except OSError as exc:
        raise PrecheckError(f"the folder could not be read: {exc}") from exc

    if not entries and not problems:
        raise PrecheckError(f"the folder is empty: {root}")

    stop = [("folder structure", problem) for problem in problems]
    look = []

    vendored, build = {}, {}
    for entry in entries:
        found = directory_of(entry.name, VENDORED_DIRS)
        if found:
            vendored[found] = vendored.get(found, 0) + 1
            continue
        found = directory_of(entry.name, BUILD_DIRS)
        if found:
            build[found] = build.get(found, 0) + 1
            continue

        description, kind = looks_binary(entry.data)
        if kind in ("executable", "nested archive"):
            stop.append((kind, f"{entry.name} is {description}. A buyer cannot "
                               "read it and nobody can review it."))
            continue
        if kind == "data":
            look.append(("binary file", entry.name, description))
            continue

        # Text, but bigger than source files run. Either it is not really source
        # — a dump, an export, a log, a vendored bundle — or it is, and only its
        # first part was examined. Say so rather than let the truncation pass
        # silently.
        if entry.size > SCAN_BYTES_PER_ENTRY:
            look.append(("a file too large to be source", entry.name,
                         f"{entry.size} bytes; only the first "
                         f"{SCAN_BYTES_PER_ENTRY} were examined"))

        if SENSITIVE_NAMES.search(entry.name):
            look.append(("a file that usually holds credentials", entry.name,
                         "check whether it belongs in a listing at all"))

        # Report where a match is, never what it is. This output goes to an
        # agent's transcript, a terminal scrollback and a CI log, so printing
        # the matched text would take a secret that was contained in one local
        # file and copy it into three places that keep it. The line number is
        # what the operator needs to go and look anyway.
        text = entry.data.decode("utf-8", errors="ignore")
        for label, pattern in LOOK_PATTERNS:
            numbers = sorted({text.count("\n", 0, m.start()) + 1
                              for m in pattern.finditer(text)})
            if not numbers:
                continue
            shown = ", ".join(str(n) for n in numbers[:MAX_MATCH_LINES])
            if len(numbers) > MAX_MATCH_LINES:
                shown += f" and {len(numbers) - MAX_MATCH_LINES} more"
            where = "line" if len(numbers) == 1 else "lines"
            look.append((label, entry.name, f"{where} {shown}"))

    for directory, count in sorted(vendored.items()):
        stop.append(("vendored code",
                     f"{directory}/ is in the folder ({plural(count)}). Buyers are "
                     "not paying for this, and it hides code nobody reviewed."))
    for directory, count in sorted(build.items()):
        look.append(("build output", f"{directory}/",
                     f"{plural(count)}. Ship it only if a buyer needs it."))

    excluded = sorted(set(vendored) | set(build))
    return {
        "folder": str(root),
        "total_bytes": total_bytes,
        "entries": len(entries),
        "stop": stop,
        "look": look,
        "pack_command": suggest_pack_command(root, excluded),
        "excluded": excluded,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Look over an artifact folder before you package and publish it.")
    parser.add_argument("--folder", required=True,
                        help="the source folder you are about to package")
    parser.add_argument("--max-examples", type=int, default=5,
                        help="examples to print per category (default 5)")
    args = parser.parse_args()

    try:
        result = precheck_folder(args.folder)
    except PrecheckError as error:
        parser.exit(1, f"error: {error}\n")

    print(f"folder    {result['folder']}")
    print(f"contents  {result['entries']} files, {result['total_bytes']} bytes uncompressed")
    print()

    if result["stop"]:
        print(f"STOP  {len(result['stop'])} thing(s) that do not belong in a listing:")
        for label, detail in result["stop"][:args.max_examples * 2]:
            print(f"  [{label}] {detail}")
        print()

    if result["look"]:
        grouped = {}
        for label, where, value in result["look"]:
            grouped.setdefault(label, []).append((where, value))
        print(f"LOOK  {len(result['look'])} thing(s) worth deciding about. For each,")
        print("      is it a fair part of what you are selling, a leak you want to")
        print("      remove, or something that should not be published at all?")
        for label, hits in grouped.items():
            print(f"  {label} ({len(hits)}):")
            for where, value in hits[:args.max_examples]:
                print(f"    {where}: {value}")
            if len(hits) > args.max_examples:
                print(f"    ... and {len(hits) - args.max_examples} more")
        print()

    if not result["stop"] and not result["look"]:
        print("Nothing stood out.")
        print()

    print("Package it with:")
    print(f"  {result['pack_command']}")
    if result["excluded"]:
        print("  (the excludes above are what this check flagged)")
    print()
    print("Then check the archive's size before you list it: the marketplace takes")
    print("10 MB at most, and that limit is on the packaged archive, not on the")
    print("figure above.")
    print()
    if result["look"]:
        print("Matches are reported by line number. The matched text is never printed,")
        print("so nothing secret reaches this output, your scrollback or a CI log.")
        print()

    print("This is one careful look, not the marketplace's safety review, and it")
    print("does not predict that review's outcome. Buyers receive the archive you")
    print("upload exactly as you upload it, so what you package is what they get.")

    return 2 if result["stop"] else 0


if __name__ == "__main__":
    sys.exit(main())
