#!/usr/bin/env python3
"""Attach verified, freely-licensed photographs to a plan — or attach nothing.

The page is a document you read on a phone in a city you do not know, and a photograph of the
place you are about to walk to is worth more than another paragraph about it. But the naive
version of this feature -- search the web for pretty pictures -- fails in four ways that all end
with the traveller worse off, so each one is answered here rather than hoped away:

1. **Redistribution.** Embedding an arbitrary web image into somebody's saved file is copying it.
   Only Wikimedia Commons material is used, which carries an explicit licence, and the licence and
   author are rendered next to the image because CC BY-SA requires exactly that.
2. **Accuracy.** A stock beach is not their beach. Measured while building this: searching
   "Alicante Central Market" matched the article *Bombing of Alicante*, and "Explanada de España"
   and "Postiguet Beach" both fell back to the generic *Alicante* article, which would have put
   the SAME city photo under three different anchors. Coordinate proximity proves "near the
   place", never "of the place" -- so the page title must also be about what was asked for, the
   generic-fallback case is rejected outright, and no file is used twice.
3. **Offline.** You look at this page while travelling. A hot-linked image is a broken image
   exactly then, and it also tells a third party which itinerary you are reading. Bytes are
   downloaded once, here, and embedded, so the page stays one self-contained file.
4. **Weight.** Full-resolution originals run to several megabytes. The Wikimedia API is asked for
   a thumbnail at a bounded width, so the resizing happens server-side and this script needs no
   image library -- the skill stays standard-library only.

When a slot cannot be filled to that standard it stays empty. A page with three good photographs
and two gaps is honest; a page with five photographs where two are wrong teaches the traveller
that the pictures mean nothing.

5. **Where the bytes land.** Base64 of a photograph is not a field; it is a file that happens to
   be spelled in JSON, and this script used to write it *into* the plan. Measured on a delivered
   plan: 2,047,677 of its 2,132,252 bytes were `plan["imagery"]` -- 96% of a document whose every
   sibling in the same workspace is 30-130KB. The cost is not disk. SKILL.md runs this during the
   verification stage, references/verification.md hands seven parallel agents that same plan
   path, and the gate loop after it sends the reader back to the plan after every finding: one
   read of that plan costs ~576k tokens instead of ~42k, which on a 128k-context reader is not a
   cost but an unrecoverable overflow. Nothing that reads a plan *as a document* -- no gate, no
   verifier, no human -- ever needs those bytes. So they go beside it, in a sidecar, and the plan
   keeps one small key naming it. See IMAGERY_SIDECAR_SUFFIX below for why that name is relative
   and why there is no flag to switch this on.

Usage:
    python fetch_plan_imagery.py <plan.json> [--out PATH] [--max-images N] [--dry-run]

    Photographs are written to <plan-stem>-imagery.json beside the plan; the plan itself gains
    only an `imagery_sidecar` key. render_final_trip_html.py and save_trip_deliverables.py find
    that sidecar on their own, so no other command needs a new argument.
"""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = ("travel-buddy/2.9 (https://github.com/dong845/travel-buddy) "
              "python-urllib")
WIKI_API = "https://{lang}.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# Measured, not guessed: eight concurrent requests to the Wikipedia API returned HTTP 429. Three
# with backoff completed six lookups in 0.9s, which is fast enough that the ceiling costs nothing.
MAX_CONCURRENCY = 3
# Sized to how each slot is actually displayed rather than to one number. The hero runs the full
# 1120px content width, so an 800px thumbnail was being upscaled and looked soft -- the first
# thing a reader noticed. Anchor cards sit in a ~250-350px grid, where 640 is already generous
# and anything larger is bytes nobody sees.
THUMB_WIDTH = 640
HERO_THUMB_WIDTH = 1600
# The hero is deliberately allowed more: it is one image, shown large, and the
# difference between 400KB and 900KB there is the difference between sharp and soft.
MAX_IMAGE_BYTES = 400_000
HERO_MAX_BYTES = 900_000
DEFAULT_MAX_IMAGES = 6
# Every cap above is PER IMAGE, and until this line nothing looked at the total: `--max-images 40`
# was a 20MB payload that no check refused, and the delivered 2MB plan that forced this rewrite
# passed each per-image cap individually on its way to 96% of the file. Derived rather than
# picked: the largest legitimate default run is one hero at HERO_MAX_BYTES plus
# DEFAULT_MAX_IMAGES-1 anchors at MAX_IMAGE_BYTES = 2.9MB of downloaded bytes, which base64
# inflates by 4/3 to ~3.9MB of payload. 4MB is that worst case with room for the metadata, and it
# is also roughly the point where a self-contained HTML file stops being something you open on a
# hotel wifi. Over it this refuses and prints the measured figure instead of trimming: which of
# seven verified photographs to drop is not a decision a size check is entitled to make.
MAX_IMAGERY_TOTAL_BYTES = 4_000_000
# The sidecar's name is derived from the plan's, and the key inside the plan is RELATIVE to the
# plan, both on purpose:
#
# - *Derived*, so a consumer can find the payload even when the key is gone -- a plan copied by
#   hand, or rewritten by a tool that did not know about the key, still has its photographs found
#   by name. There is deliberately no --sidecar flag on the readers either: a flag is a thing to
#   forget, and the thing a forgotten flag ships here is a silently photo-less page.
# - *Relative*, because this repo treats a plan as a portable document -- re-rendered, replanned
#   weeks later, audited from a moved workspace, restored from a backup. render_final_trip_html.py
#   gives the same reasoning for refusing to require intake_file to resolve on disk. An absolute
#   path would pin the photographs to this machine's home directory and break the first time the
#   workspace moved.
IMAGERY_SIDECAR_SUFFIX = "-imagery.json"

# A matched article must sit within this of the place it is supposed to depict. Generous because
# an article's coordinate is its centroid, not the venue door; the title rule below is what makes
# the match specific.
MAX_MATCH_KM = 25.0

# Words that carry no identifying power, so a title sharing only these has not matched anything.
STOPWORDS = {"the", "of", "de", "del", "la", "el", "les", "des", "du", "and", "in", "at",
             "city", "town", "old", "new", "square", "street", "beach", "park", "market",
             "museum", "church", "castle", "island", "port", "centre", "center"}

# A destination hero is a photograph OF a place. These name a building inside one, so a file
# whose name carries any of them depicts a rival subject however well it names the city first --
# measured, "Larnaca 01-2017 img37 LCA Airport.jpg" was selected as a Larnaca trip's cover.
# Only the hero consults this: an anchor's subject IS a facility, which is the whole point of it.
FACILITY_WORDS = {"airport", "aeropuerto", "aeroport", "aeroporto", "flughafen", "luchthaven",
                  "terminal", "station", "bahnhof", "estacion", "stadium", "arena", "hospital",
                  "university", "mall", "hotel", "museum", "cathedral", "catedral", "mosque",
                  "church", "iglesia", "castle", "castillo", "fort", "fortress", "monument",
                  "statue", "interior", "runway", "platform"}


class ImagerySidecarError(RuntimeError):
    """A plan points at a photo payload that cannot be honoured.

    Its own type because every consumer has to turn it into a non-zero exit naming the path,
    never into an empty imagery dict. The tempting shortcut -- "if the sidecar is missing, render
    without photographs; it will be obvious" -- is false here, and checkably so: `imagery` appears
    zero times in check_plan_consistency.py and validate_trip_html.py, nothing counts <img> tags,
    and the page is valid with none. A traveller would open a page that simply had no pictures and
    have no way to know that seven verified ones existed. Splitting the bytes out of the plan is
    only safe if losing them is loud.
    """


def sidecar_path_for(plan_path: str | Path) -> Path:
    """Where a plan's photo payload lives: <plan-stem>-imagery.json, beside the plan.

    Callers must not pass "-": a plan read from standard input has no directory to sit beside,
    and Path("-").stem would quietly produce "--imagery.json" in the current working directory.
    """
    path = Path(plan_path)
    if path.name in ("", "-"):
        raise ImagerySidecarError(
            "a plan read from standard input has no directory for its imagery sidecar; "
            "give the plan a real path, or pass --out to name where it should be written.")
    return path.with_name(path.stem + IMAGERY_SIDECAR_SUFFIX)


def imagery_payload_bytes(imagery: object) -> int:
    """The payload's size as it is actually written, so a refusal quotes the real figure.

    Serialized exactly the way write_json_atomic writes it -- a figure measured on a different
    encoding than the one that lands on disk is a figure the reader cannot check against `ls`.
    """
    return len(json.dumps(imagery, ensure_ascii=False, indent=2).encode("utf-8"))


FETCH_REMEDY = (f"Re-run `python scripts/fetch_plan_imagery.py <plan.json> --max-images N` with an "
                f"N below the default {DEFAULT_MAX_IMAGES}, or remove slots from the sidecar by "
                f"hand; nothing here will silently decide which verified photograph to drop.")


def aggregate_refusal(measured: int, subject: str, remedy: str = FETCH_REMEDY) -> str | None:
    """The message for a payload over MAX_IMAGERY_TOTAL_BYTES, or None when it is within it.

    Deliberately applied to the imagery payload alone -- as built here, or as read from a sidecar
    file -- and never to a merged in-memory plan. Measuring the merged plan would put a single
    legitimate hero at HERO_MAX_BYTES on the same scale as the itinerary around it, so the check
    would fire on the size of the trip rather than on the size of the pictures.

    `remedy` exists because this message is printed by three scripts and only one of them owns the
    flag it used to name. Measured on the delivery path: save_trip_deliverables.py printed "Lower
    --max-images (default 6) and re-run" for a 4.9MB payload, and `save_trip_deliverables.py
    --max-images 3` is `error: unrecognized arguments`. An instruction the operator cannot carry
    out reads as the tool not knowing what it is doing, and the next thing they try is ignoring it.
    So the default names the script that does own the flag, and a caller with a different set of
    options passes the sentence its own operator can act on.
    """
    if measured <= MAX_IMAGERY_TOTAL_BYTES:
        return None
    return (f"{subject} is {measured:,} bytes, over the {MAX_IMAGERY_TOTAL_BYTES:,}-byte ceiling "
            f"for one plan's photographs. {remedy}")


def write_json_atomic(path: Path, data: object) -> None:
    """Write JSON so a concurrent reader sees the whole old file or the whole new one.

    The version this replaces was `destination.write_text(...)`, which truncates first and writes
    after. That is a real window on this exact path and not a theoretical one: SKILL.md schedules
    this script during the verification stage, and references/verification.md hands seven parallel
    agents the same plan path -- so every one of them could read a prefix of a plan and report a
    JSONDecodeError from a file that is perfectly valid a millisecond later, which is the shape of
    a bug nobody ever reproduces. os.replace is atomic within a filesystem, and the temporary file
    is created in the destination's own directory so it is always the same filesystem.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        # A half-written temp file left behind would be picked up by nothing, but it would sit in
        # the traveller's workspace forever looking like a plan.
        try:
            tmp.unlink()
        except OSError:
            pass
        raise


def plan_slot_labels(plan: dict) -> dict[str, str]:
    """{slot key: the label THIS plan gives that slot}, in the plan's own slot order.

    The one piece of evidence a payload carries about which plan it belongs to. Every entry
    fetch() writes records the `label` of the slot it filled -- the destination for the hero, the
    anchor's name for an anchor -- so comparing a stored label against the label the plan gives
    that same key answers "is this photograph still of the thing this heading names?" without a
    network call, a checksum, or a new field in the file format.

    Built from slots() rather than from a second walk of the plan, so the question is asked with
    exactly the strings the answer was written with. A private copy of "how a slot is labelled"
    would drift the first time slots() changed, and it would drift silently: the failure is a
    photograph under the wrong heading, which renders perfectly.

    A plan too malformed for slots() to walk raises ImagerySidecarError rather than an
    AttributeError from three frames down. Every caller of this module is documented to turn that
    one type into a non-zero exit naming the path, and a traceback instead would be a lost payload
    reported as a crash in somebody else's code.
    """
    try:
        return {slot["key"]: str(slot.get("label") or "") for slot in slots(plan)}
    except (AttributeError, TypeError, KeyError) as exc:
        raise ImagerySidecarError(
            f"this plan's shape cannot be read well enough to say which photograph belongs under "
            f"which heading ({type(exc).__name__}: {exc}). 'trip' must be an object and "
            f"'destination_experience_anchors' a list. Attaching photographs to a plan nothing "
            f"can walk would put them under headings decided by an accident of the shape.") from exc


def foreign_sidecar_slots(plan: dict, payload: dict) -> list[str]:
    """Which slots of `payload` this plan does not vouch for -- empty when it vouches for all.

    Used wherever the *location* of a sidecar was guessed rather than declared. A file name is not
    provenance: measured on this repo's own working filename, a plan for Chengdu carrying no
    imagery key at all sat beside a leftover `trip-imagery.json` from a Larnaca trip and the
    delivered page opened with a photograph of Larnaca, credited to that trip's photographer, under
    the Chengdu heading. Both files were named correctly for their own plan; only the guess was
    wrong.

    A slot vouches for itself when the plan names that key AND the stored label is the label the
    plan gives it. That is positive evidence and a bare filename match is not: the filename is
    derived from a working file name that two unrelated trips routinely share ("trip.json"), while
    the label was written from this plan's own destination and anchor names.
    """
    labels = plan_slot_labels(plan)
    foreign: list[str] = []
    for key, entry in payload.items():
        expected = labels.get(key)
        stored = entry.get("label") if isinstance(entry, dict) else None
        if not expected:
            foreign.append(f"{key} is labelled {stored!r}, but this plan has no such slot")
        elif not isinstance(stored, str) or stored.strip() != expected.strip():
            foreign.append(f"{key} is labelled {stored!r}, but this plan names that slot "
                           f"{expected!r}")
    return foreign


def write_target_refusal(plan: dict, sidecar: Path, already_read: Path | None) -> str | None:
    """Why the payload already at `sidecar` must not be overwritten -- None when it may be.

    The mirror of the evidence test resolve_plan_imagery applies on the READ side, and it exists
    because the write is the more dangerous half of the same guess. A refused read costs a page:
    the operator sees the error, fixes the pointer, re-runs, and every photograph is still on
    disk. A wrong write costs the file -- another trip's verified slots, with the licences and the
    photographer credits that made them publishable, gone, and nothing left on disk to say they
    were ever there. Measured before this gate existed, with fetch() stubbed to one Chengdu slot:
    `fetch_plan_imagery.py chengdu.json --out dst/new.json` over a `dst/new-imagery.json` holding
    a two-slot Larnaca payload exited 0, printed "Imagery sidecar: ... (1 image(s))", and left the
    file at 434 bytes where 895 bytes of Larnaca had been.

    The sidecar is also the one path the operator never typed. `--out` names a PLAN; the payload's
    name is DERIVED from it (IMAGERY_SIDECAR_SUFFIX above says why), so the file this destroys is
    one nobody looked at before running the command -- which is exactly where a silent overwrite
    goes unnoticed longest.

    A payload at the write target may be overwritten only when this run can account for it:

    * it is the file this run read (`already_read`), so its slots went through the merge below and
      nothing in it is lost -- the ordinary in-place re-run, and the case that must keep working;
    * it holds no slots at all, so there is no photograph to lose.

    Anything else is refused, INCLUDING a payload whose labels prove it is this plan's own. That
    is not a second opinion about provenance but a fact about the merge: a payload this run never
    read cannot have been merged with, so writing over it replaces its slots wholesale. That is
    the "seven slots became one and the run exited 0" defect the merge in main() exists to refuse,
    relocated to a path the merge never looked at, and it deserves the same refusal.
    """
    if not sidecar.exists():
        return None
    if already_read is not None:
        try:
            if sidecar.samefile(already_read):
                return None
        except OSError:
            # `already_read` vanished between the read and here, or the two live on filesystems
            # that cannot be compared. Neither proves they are the same file, so fall through to
            # the evidence test rather than assume the safe answer.
            pass
    where = (f"this run read {already_read}" if already_read is not None
             else "this run read no existing payload")
    # The plan whose stem derives this sidecar's name -- spelled out because it is the command the
    # operator should run instead, and `.removesuffix` rather than a slice so a sidecar whose name
    # did not come from sidecar_path_for still produces a sentence rather than a mangled one.
    owner = sidecar.name.removesuffix(IMAGERY_SIDECAR_SUFFIX) + ".json"
    remedy = (f"Move or delete {sidecar.name}, or point --out at a plan whose stem does not derive "
              f"that name. If those photographs ARE this plan's, re-run against the plan that "
              f"names them -- `python scripts/fetch_plan_imagery.py {owner}` in {sidecar.parent} "
              f"-- so this run's slots are MERGED into them instead of replacing them.")
    if not sidecar.is_file():
        return (f"{sidecar} already exists and is not a regular file, so this run cannot tell what "
                f"writing over it would destroy ({where}). {remedy}")
    # Same order and same reason as the read path: measured on the file as it sits on disk, before
    # it is parsed, so an over-ceiling or concatenated payload is refused for the price of one
    # stat() instead of being loaded into memory to be rejected.
    oversize = aggregate_refusal(sidecar.stat().st_size, f"the payload already at {sidecar}")
    if oversize:
        return (f"{oversize} It is not this run's payload -- {where} -- so it cannot be read to "
                f"say what overwriting it would destroy. {remedy}")
    try:
        existing = json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return (f"{sidecar} already exists and could not be read ({exc}), so there is no way to "
                f"tell what writing over it would destroy ({where}). {remedy}")
    if not isinstance(existing, dict):
        return (f"{sidecar} already exists and holds a {type(existing).__name__}, not an object of "
                f"image slots, so there is no way to tell what writing over it would destroy "
                f"({where}). {remedy}")
    if not existing:
        return None
    foreign = foreign_sidecar_slots(plan, existing)
    if foreign:
        return (f"{sidecar} already holds {len(existing)} photograph(s) that are not this plan's, "
                f"and nothing in this plan claims them ({where}). " + "; ".join(foreign) + ". "
                f"Writing here would delete another trip's verified, licence-checked work; the "
                f"read side refuses to RENDER a payload it cannot place, and destroying one is "
                f"worse than rendering it. {remedy}")
    return (f"{sidecar} already holds {len(existing)} photograph(s) this run never read "
            f"({where}), so they were not merged with what this run verified and writing here "
            f"would replace them wholesale. Their labels do match this plan, which makes this the "
            f"dangerous case rather than the safe one: a run that reached Wikipedia for one slot "
            f"would silently leave one photograph where several verified ones had been. " + remedy)


def resolve_plan_imagery(plan: dict, plan_path: str | Path | None) -> tuple[dict, Path | None]:
    """The imagery a plan means -- inline, in its sidecar, or both -- merged in memory.

    Returns `(imagery, the sidecar actually read or None)`. The caller renders from the returned
    dict; it must NOT write it back into a plan it is about to save, which is how the 2MB got
    into the file in the first place.

    Three sources, in increasing authority:

    - `plan["imagery"]` inline. Plans delivered before the split carry it, and this keeps working
      exactly as it did: the 拉纳卡 plan in a real workspace holds 2MB of verified photographs and
      is a document a traveller may open at any time. Refusing it, or migrating it silently on
      read, would both be worse than carrying it -- a read has no business rewriting the file it
      was asked to read. It is migrated on the next *write* instead (fetch_plan_imagery.py moves
      it out, save_trip_deliverables.py externalizes it into the workspace copy).
    - A sidecar discovered by name beside the plan, even with no key naming it. This is what makes
      the split survive a plan that was copied, renamed by hand, or rewritten by a tool that
      dropped the key.
    - A sidecar named by `plan["imagery_sidecar"]`. It wins per key, because it is the payload
      written for this plan most recently and by the only script that verifies provenance.

    Every failure here raises. A missing or unreadable payload is never an empty dict.

    The declared key is AUTHORITATIVE, and the name-based discovery above it is now gated on
    evidence. The original reasoning -- "a flag is a thing to forget, so derive the name" -- was
    only half the argument, and the missing half cost a delivered page: a filename guess is a thing
    to get WRONG. Measured on this repo's own working filename, a Chengdu plan carrying no imagery
    key beside a leftover `trip-imagery.json` from a Larnaca trip rendered with Larnaca's hero
    photograph, credited to Larnaca's photographer, under Chengdu's heading -- and
    save_trip_deliverables.py then stamped `imagery_sidecar` into the saved plan, making the wrong
    file this trip's payload of record. So a guessed sidecar must prove it belongs to this plan by
    naming the same slots with the same labels (foreign_sidecar_slots above), and a guess that
    cannot prove it raises rather than being quietly used or quietly ignored. When the key IS
    declared, no proof is asked for: the plan said which file, and a plan saying so is exactly the
    provenance a filename lacks.
    """
    inline = plan.get("imagery")
    if inline is None:
        inline = {}
    elif not isinstance(inline, dict):
        # Not "ignore it and render without photographs": the renderer already tolerates a
        # non-dict by drawing nothing, which is precisely how a broken writer upstream would stay
        # invisible for as long as nobody compared the page against the plan.
        raise ImagerySidecarError(
            f"plan['imagery'] is a {type(inline).__name__}, not an object of image slots keyed "
            f"'hero' and 'anchor:N'. Something wrote a shape no renderer can read.")

    has_path = plan_path is not None and str(plan_path) not in ("", "-")
    base = Path(plan_path).parent if has_path else Path.cwd()
    declared = plan.get("imagery_sidecar")
    candidate: Path | None = None
    # Whether the DIRECTORY the candidate was found in was guessed rather than given. A declared
    # key names a file relative to the plan, so with a real plan path nothing is guessed; without
    # one -- the `-` stdin mode below -- the name is declared but the directory is a guess, and a
    # guess about where a payload lives is the same class of mistake as a guess about its name.
    guessed = False
    if declared is not None:
        if not isinstance(declared, str) or not declared.strip():
            raise ImagerySidecarError(
                f"plan['imagery_sidecar'] is {declared!r}, which names no file. Write the "
                f"sidecar's name relative to the plan, or remove the key.")
        # `base / declared` honours an absolute value too -- pathlib returns it unchanged. Nothing
        # in this repo writes one, but a hand-edited plan that does should work rather than be
        # lectured at.
        candidate = base / declared.strip()
        # SECURITY. `declared` is a string out of the plan, and the paragraph above deliberately
        # honours an absolute value for hand-edited plans. Combined with `..` that made the plan
        # able to name ANY path on the machine, and this one matters more than the same hole in
        # the intake cross-check: what is read here is decoded and embedded into the delivered
        # page as data: URIs, so a file that parses as image slots leaves the machine inside an
        # artifact the traveller then shares. A plan is a portable document -- re-rendered,
        # replanned, audited later, and therefore sometimes received from somebody else -- so a
        # path it names is a request, not an instruction.
        #
        # The sidecar's whole contract is that it lives BESIDE the plan (`<plan-stem>-imagery
        # .json`), so requiring the resolved path to stay in the plan's own directory costs no
        # legitimate case, including the absolute one: an absolute path beside the plan still
        # resolves there. What it refuses is every path that escapes it.
        try:
            resolved = candidate.expanduser().resolve()
            root = base.expanduser().resolve()
        except OSError as exc:
            raise ImagerySidecarError(
                f"plan['imagery_sidecar'] is {declared!r}, which could not be resolved "
                f"({exc}).") from exc
        if resolved.parent != root:
            raise ImagerySidecarError(
                f"plan['imagery_sidecar'] is {declared!r}, which resolves to {resolved} -- "
                f"outside the plan's own directory ({root}). The sidecar lives beside the plan by "
                f"contract, and a plan can be shared or hand-edited, so a path it names is not a "
                f"path to open. Move the sidecar beside the plan, or write its bare filename.")
        # `candidate` deliberately keeps its UNRESOLVED form: resolving it here would rewrite every
        # reported path through symlinks (/var -> /private/var on macOS), changing what callers and
        # tests see for a check that has already passed.
        # A plan on standard input has no directory of its own, so `base` is whatever directory the
        # command happened to run from. Measured, both halves of that: `cat plan.json | python
        # scripts/save_trip_deliverables.py -` exited 2 for EVERY photographed plan when run from
        # an ordinary cwd, and delivered a DIFFERENT trip's photograph, credited to a different
        # photographer, when the cwd happened to hold a file of that name. The absolute case is
        # unaffected -- an absolute value names its own directory and guesses nothing.
        guessed = not has_path and not Path(declared.strip()).is_absolute()
    elif has_path:
        guess = sidecar_path_for(plan_path)
        if guess.exists():
            candidate = guess
            guessed = True

    if candidate is None:
        return dict(inline), None
    if not candidate.is_file():
        where = ("the plan arrived on standard input, so the name was resolved against the "
                 f"current directory {base} -- pass the plan's own path instead of `-` and the "
                 f"name resolves beside the plan, the way it was written"
                 if not has_path else f"resolved against {base}")
        raise ImagerySidecarError(
            f"plan['imagery_sidecar'] names {declared!r} but {candidate} is not a file ({where}). "
            f"Re-run `python scripts/fetch_plan_imagery.py <plan.json>` to rebuild it, move the "
            f"sidecar back beside the plan, or delete the key if this plan is meant to carry no "
            f"photographs. Rendering without them silently is not an option: no gate counts "
            f"images, so nobody would notice.")

    # Measured on the file as it sits on disk, before it is parsed into memory: this is the one
    # place a hand-edited or concatenated payload can be refused while it still costs one stat().
    refusal = aggregate_refusal(candidate.stat().st_size, f"the imagery sidecar {candidate}")
    if refusal:
        raise ImagerySidecarError(refusal)
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ImagerySidecarError(f"could not read the imagery sidecar {candidate}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ImagerySidecarError(
            f"the imagery sidecar {candidate} holds a {type(payload).__name__}, not an object of "
            f"image slots keyed 'hero' and 'anchor:N'.")
    # The evidence, and only where something was guessed. An empty payload proves nothing and
    # needs to prove nothing -- there is no photograph in it to attach to the wrong trip.
    if guessed and payload:
        foreign = foreign_sidecar_slots(plan, payload)
        if foreign:
            how = ("the plan arrived on standard input, so its name was resolved against the "
                   f"current directory {base}" if not has_path
                   else "no key named it, so the name was derived from the plan's own file name")
            raise ImagerySidecarError(
                f"{candidate} does not look like this plan's photographs, and no key in the plan "
                f"says it is ({how}). " + "; ".join(foreign) + ". A file name is not provenance: "
                f"two unrelated trips share a working file name every day, and the delivered page "
                f"would carry another city's photograph under this one's heading with its licence "
                f"and photographer printed underneath. If this file really is this plan's payload, "
                f"say so by setting \"imagery_sidecar\": \"{candidate.name}\" in the plan -- a "
                f"declared key is authoritative and is not asked for proof. If it is not, move or "
                f"delete it, or re-run `python scripts/fetch_plan_imagery.py <plan.json>`.")
    return {**inline, **payload}, candidate


def _request(url: str, *, binary: bool = False, tries: int = 3):
    for attempt in range(tries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=25) as response:
                payload = response.read()
                return payload if binary else json.loads(payload)
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError):
            if attempt == tries - 1:
                return None
            time.sleep(1.5 * (attempt + 1))
    return None


def _api(base: str, params: dict):
    params = {**params, "format": "json"}
    return _request(base + "?" + urllib.parse.urlencode(params))


def _km(a: tuple[float, float], b: tuple[float, float]) -> float:
    dlat, dlon = math.radians(b[0] - a[0]), math.radians(b[1] - a[1])
    h = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(a[0])) * math.cos(math.radians(b[0])) * math.sin(dlon / 2) ** 2)
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def _tokens_raw(text: str) -> set[str]:
    """Every word, stopwords kept.

    Used only to ask "is this article the destination itself?". Stripping stopwords for that
    question is wrong: the generic half of a title is exactly what distinguishes "Larnaca Castle"
    from "Larnaca", and with `castle`, `church`, `museum`, `market` and `beach` all on the
    stopword list, every "<City> <Type>" article collapses to the bare city name and reads as a
    fall-through to it.
    """
    # Two length floors, because "how many characters is a word" is not one question.
    #
    # The single `{3,}` floor here was tuned for Latin, where three characters rules out `the`
    # and `and` and costs nothing real. Applied to CJK it deletes whole place names: measured,
    # `_tokens("香港")` and `_tokens("长洲")` both returned the empty set, and an empty specific
    # set sends _relevant() into its "the query IS the place" branch, which then compares two
    # empty sets and returns False. The consequence was silent and total -- on a Chinese-language
    # plan, EVERY two-character destination (香港, 北京, 上海, 东京, 京都, 台北, 澳门 …) failed
    # its hero lookup, the script reported "no article both near the trip and about it", exited 0,
    # and the page shipped with no photographs at all. Same family as the width bug that measured
    # CJK text with Latin metrics: a Latin constant applied to a script it was never measured on.
    #
    # CJK runs keep a floor of 2 because that is a complete name, and Latin keeps 3.
    text = str(text or "").casefold()
    latin = re.findall(r"[^\W\d_]{3,}", text, flags=re.UNICODE)
    cjk = re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]{2,}", text)
    return set(latin) | set(cjk)


def _tokens(text: str) -> set[str]:
    return {w for w in _tokens_raw(text) if w not in STOPWORDS}


def destination_forms(destination: str) -> list[set[str]]:
    """Every script the destination's own article could be titled in.

    Module-level so the rule below has a test that exercises *it* rather than a copy of it.
    """
    forms = [_tokens_raw(destination)]
    latin = latin_title(destination, "zh")
    if latin:
        forms.append(_tokens_raw(latin))
    return [form for form in forms if form]


def is_destination_article(page_title: str, forms: list[set[str]]) -> bool:
    """Did this anchor's search fall through to the destination's own article?

    Raw tokens on both sides, and both of those choices are load-bearing:

    - **Stopwords kept.** With `castle`, `church`, `museum`, `market` and `beach` all stopwords,
      `_tokens("Larnaca Castle")` is `{"larnaca"}` -- indistinguishable from the city, so the
      castle's own article reads as a fall-through and its photograph is dropped.
    - **Every script.** The plan writes the destination in the traveller's language. On a Chinese
      plan `_tokens_raw("Larnaca") <= _tokens_raw("拉纳卡")` is False for the same city, so this
      guard passed everything: measured, the anchor 拉纳卡市政市场 took the article *Larnaca* and
      was captioned with a photograph of the Finikoudes promenade.
    """
    tokens = _tokens_raw(page_title)
    return bool(tokens) and any(tokens <= form for form in forms)


def file_names_the_subject(filename: str, subject_tokens: set[str], is_hero: bool) -> bool:
    """Is this Commons file about the subject, or merely filed near it?

    A different test from the one used on article titles, and using that one here was the bug:
    it demands the title introduce no new words, which is right for "Alicante Airport" and
    wrong for "Vista de Alicante, España, 2014-07-04, DD 49.JPG" -- a file name is descriptive
    by nature, so every candidate was rejected and the destination kept its plain lead image.

    Position carries the meaning instead. Photographers name a file for its subject first:
    "Vista de Alicante, ..." is of Alicante, while "Iglesia de San Miguel Arcángel, Altea,
    Alicante, ..." is a church in a town fifty kilometres away that happens to share a province.

    Position alone, though, cannot separate "Vista de Alicante, España" from "Larnaca 01-2017
    img37 LCA Airport": both open with the place name, and the second won a real trip's cover
    photograph. The tempting repair -- "a hero's file name may introduce no other word" -- also
    rejects the España case this heuristic exists to accept, which turns the upgrade off
    everywhere and leaves every destination on its plain lead image. So only a named FACILITY
    disqualifies a hero: a country or a photographer's initials qualify the place, a terminal
    replaces it. Anchors are exempt, because a facility is exactly what they depict.
    """
    words = re.findall(r"[^\W\d_]{3,}", filename.casefold(), flags=re.UNICODE)
    if not subject_tokens & set(words[:4]):
        return False
    return not (is_hero and set(words) & FACILITY_WORDS)


# The subject classes this file has now been burned by three times, each time as an article that
# was genuinely NEAR the anchor and about something else: 阿利坎特-埃爾切機場 standing in for the
# city, *Larnaca* standing in for its municipal market, and *Vevey* -- then *Vevey railway station*
# -- standing in for the market on its lakefront. Token overlap cannot separate them: "Château de
# Chillon"/"Chillon Castle" and "Marché de Vevey"/"Vevey railway station" have the identical shape
# (one shared token, each side with its own extra), and telling them apart needs to know that
# château means castle and marché does not mean railway station.
#
# Wikipedia's own short description carries the subject class as its opening noun -- "Town in Vaud,
# Switzerland", "Railway station in Vevey, Switzerland", "Castle in Veytaux, Switzerland" -- and it
# rides along in the pageimages call, so this costs no extra request. The list is deliberately
# short and deliberately about CONTAINERS and TRANSPORT, the two things an anchor keeps falling
# through to; a general subject taxonomy would be wrong on the first trip it had not seen.
FALLTHROUGH_SUBJECTS = (
    "town", "city", "municipality", "village", "commune", "settlement", "district", "canton",
    "railway station", "train station", "metro station", "bus station", "airport", "airfield",
)

def _is_fallthrough(description: object, query: str) -> bool:
    """Is this article about a container or a transport facility the query never asked for?

    Read from the START of the description, because that is where English puts the class noun --
    "Town in Vaud, Switzerland". Checking the whole string over-fires: "Castle in the town of
    Veytaux" is a castle, and a rule that saw `town` anywhere would refuse it.

    LATIN SCRIPTS ONLY, and that is a finding rather than an omission. A Chinese list was written
    first, on the reasoning that this skill is used in Chinese most and zh.wikipedia states the
    class last (「瑞士沃州市镇」). Measured, it was worse than useless: `_tokens` treats a CJK run
    as ONE token, so 「沃韦市集」 and 「沃韦市」 share nothing and the token check one line up
    already refuses them. The only way a CJK description reaches this guard is when the query and
    the title are the SAME run -- and then the article IS what was asked for, so a class guard
    firing there would refuse the correct page. A list that cannot fire where it would help and
    misfires where it can is coverage on paper only.

    What protects CJK instead is that same whole-run tokenisation, which is strict rather than
    loose, plus the exact-title path that resolves 简体 to 繁體 without consulting this function.
    A Chinese plan whose anchors carry Latin names -- 「Marché de Vevey」 in a zh plan, which is the
    trip that exposed all of this -- searches en/fr and gets an English description, so the list
    below is the one that runs on it.
    """
    text = str(description or "").strip()
    if not text:
        return False          # no description is no evidence, and no evidence is not a refusal
    asked = query.casefold()
    lead = text.casefold().split(" in ")[0].split(",")[0]
    return any(word in lead and word not in asked for word in FALLTHROUGH_SUBJECTS)


def _relevant(query: str, page_title: str, place_name: str,
              place_vocabulary: frozenset[str] = frozenset(),
              description: object = None) -> bool:
    """Is this article about what was asked for, rather than merely near it?

    The specific part of the query is what must match -- the query minus the destination name.
    "Alicante Central Market" minus "Alicante" leaves {central, market}; the article "Bombing of
    Alicante" shares none of them and is refused, even though its coordinate is 400m away and its
    lead image really is the market. Its provenance would have been rendered under the photo.
    """
    place_tokens = _tokens(place_name)
    query_tokens = _tokens(query)
    specific = query_tokens - place_tokens
    if not specific:
        # The query IS the place -- the destination hero. Then the article must be ABOUT the
        # place, not about something located in it, so its title may introduce no new subject.
        # Without this the search for "阿利坎特" returned 阿利坎特-埃爾切機場: the airport, four
        # kilometres out, sharing the city's name, passing every coordinate rule, and about to be
        # printed as the destination's opening photograph.
        title_tokens = _tokens(page_title)
        return bool(title_tokens) and title_tokens <= place_tokens
    title_tokens = _tokens(page_title)
    if not (specific & title_tokens):
        return False

    # The article must not be a BROADER subject that merely contains the thing asked for. Sharing
    # one specific token was enough, so the anchor "Marché de Vevey" matched the article *Vevey* --
    # the town -- and a lake photograph of Vevey was about to be printed under a market's heading.
    # That is the Larnaca defect this file already guards against one level up, arriving through a
    # containing SETTLEMENT instead of through the destination, which the existing guard is the
    # only place that looks.
    #
    # A plain "title is a subset of the query" rule over-fires: the article *Lion Monument* is a
    # proper subset of the query "Lion Monument Lucerne" and is exactly right. The difference is
    # WHICH token the article dropped -- the subject ("marché") or the location ("lucerne") -- and
    # the plan already knows its own place names, so no gazetteer is needed to tell them apart.
    # Compared on RAW tokens, before stopwords are stripped, and that is not a detail. `castle`,
    # `market`, `church` and `museum` are stopwords while their non-English equivalents are not, so
    # the cooked form of "Chillon Castle" is {chillon} -- indistinguishable from the town article --
    # while "Château de Chillon" keeps {château, chillon}. Judged cooked, the guard refused the one
    # correct match this trip actually found. Raw keeps the subject word on both sides, which is
    # the only thing this comparison is trying to see.
    # Only on the anchor branch. The hero slot IS the destination, and its own article is
    # legitimately "Federal city of Switzerland" -- refusing that would delete every hero.
    # Exempt when the anchor names ONLY places this trip already knows. An anchor called 「东京」
    # on a 「日本」 trip is asking for that city's own article, and refusing it for being a
    # settlement refuses the thing that was asked for. The destination hero is handled by the
    # branch above; this covers a stop that is itself a city.
    asks_only_for_places = bool(query_tokens) and \
        query_tokens <= (place_tokens | set(place_vocabulary))
    if not asks_only_for_places and _is_fallthrough(description, query):
        return False

    raw_title, raw_query = _tokens_raw(page_title), _tokens_raw(query)
    if raw_title and raw_title < raw_query:
        dropped = raw_query - raw_title
        if dropped - _tokens_raw(place_name) - set(place_vocabulary):
            return False
    return True


def name_variants(raw: str) -> list[str]:
    """The searchable forms of a name the plan wrote for a human to read.

    Plans name places as "圣巴巴拉城堡（Castillo de Santa Bárbara）" -- the traveller's language
    first, the local name in brackets. Searching the whole string finds nothing in either
    Wikipedia, which is why the first run of this script verified zero images on a real
    Chinese-language plan while the same places resolved perfectly from their Latin names. Both
    halves are worth trying, and the bracketed one usually wins because it is the name the place
    is indexed under where it actually is.
    """
    text = str(raw or "").strip()
    if not text:
        return []
    variants: list[str] = []
    for inner in re.findall(r"[（(]([^）)]+)[）)]", text):
        inner = inner.strip()
        # A bracket holding a region rather than a name ("西班牙，瓦伦西亚自治区") is context, not
        # an alias; a comma is the reliable tell.
        if inner and "," not in inner and "，" not in inner:
            variants.append(inner)
    outer = re.sub(r"[（(][^）)]*[）)]", "", text).strip(" ·-—,，")
    if outer:
        variants.append(outer)
    seen: set[str] = set()
    return [v for v in variants if not (v in seen or seen.add(v))]


def wiki_languages(plan_language: object) -> list[str]:
    """Which Wikipedias to ask, most likely to hold the article first."""
    text = str(plan_language or "").casefold()
    # The destination's own language is unknown -- the plan records the traveller's, not the
    # place's -- so es/fr/it/de are always tried after the obvious two. They cost one request each
    # and they are where a European place name is actually indexed: every anchor of a real
    # Alicante plan is a Spanish name that en.wikipedia does not hold under that title.
    common = ["es", "fr", "it", "de"]
    if "chin" in text or text.startswith(("zh", "中")):
        return ["zh", "en", *common]
    return ["en", *common]


def resolve(query: str, near: tuple[float, float] | None, place_name: str,
            lang: str = "en", exact: bool = False,
            place_vocabulary: frozenset[str] = frozenset()) -> dict | None:
    """Find one article whose lead image can honestly be labelled as `query`.

    `exact` looks the title up directly instead of searching, and it is tried first for a reason:
    search is a ranking, so asking it for "阿利坎特" returned 阿利坎特-埃爾切機場 -- the airport --
    which sits four kilometres from the city centre, passes any coordinate rule, and shares the
    city's name. It would have appeared as the destination's hero photograph. An exact title is
    not a ranking and cannot drift like that.
    """
    lookup = ({"action": "query", "titles": query, "redirects": 1}
              if exact else
              {"action": "query", "generator": "search", "gsrsearch": query, "gsrlimit": 4})
    data = _api(WIKI_API.format(lang=lang), {
        **lookup,
        "prop": "pageimages|coordinates|description",
        "piprop": "original|name", "pilicense": "any",
    })
    pages = sorted(((data or {}).get("query") or {}).get("pages", {}).values(),
                   key=lambda p: p.get("index", 99))
    for page in pages:
        filename = page.get("pageimage")
        title = str(page.get("title") or "")
        if not filename:
            continue
        coordinates = (page.get("coordinates") or [{}])[0]
        if near and coordinates.get("lat") is not None:
            if _km(near, (coordinates["lat"], coordinates["lon"])) > MAX_MATCH_KM:
                continue
        elif near and not exact:
            # A search result with no coordinate has nothing tying it to this trip, and search is
            # a ranking that drifts. An EXACT title match is not a ranking: asking zh.wikipedia
            # for 阿利坎特 returns the city and cannot return anything else, so the title is the
            # anchor and a missing coordinate is only a gap in the article. Requiring one here
            # rejected the correct hero image of a real plan while the airport four kilometres
            # away, which does carry coordinates, had already been refused on other grounds.
            continue
        # An EXACT title lookup has already had this question answered, by the wiki rather than
        # by us: `titles=X&redirects=1` returns page X or its redirect target and can return
        # nothing else, so there is no ranking here to be sceptical of. Running the token rule on
        # it anyway rejected correct matches across writing systems -- measured,
        # `_relevant("中环街市", "中環街市", "香港")` is False, because zh.wikipedia had resolved
        # the simplified query to the traditional title and the two share no token. The article
        # was right, its image was right, and this line threw it away. The destination-fallback
        # guard below still runs, because that is a different question (is this the city's own
        # article standing in for an anchor) and it is the one the search path can actually get
        # wrong.
        if not exact and not _relevant(query, title, place_name, place_vocabulary,
                                       page.get("description")):
            continue
        return {"query": query, "page": title, "file": filename, "lang": lang,
                "page_url": f"https://{lang}.wikipedia.org/wiki/"
                            + urllib.parse.quote(title.replace(" ", "_"))}
    return None


def latin_title(title: str, lang: str) -> str | None:
    """The article's English title, for searching a file repository that names things in Latin.

    Commons file names are overwhelmingly Latin-script, so searching it for 阿利坎特 returns
    nothing and the destination silently kept the plain lead image while every Latin-named anchor
    beside it was upgraded. One langlink call fixes the asymmetry.
    """
    if lang == "en" or not title:
        return title or None
    data = _api(WIKI_API.format(lang=lang), {
        "action": "query", "titles": title, "prop": "langlinks", "lllang": "en", "redirects": 1})
    pages = list(((data or {}).get("query") or {}).get("pages", {}).values())
    links = (pages[0].get("langlinks") or []) if pages else []
    return (links[0].get("*") if links else None)


def better_candidate(subject: str, place_name: str, prefer_landscape: bool) -> str | None:
    """A Commons Quality Image of the same subject, if one exists.

    An article's lead image is chosen to be representative, which is a different thing from being
    good: the lead image for 阿利坎特 is a marina seen through a thicket of masts -- accurate,
    encyclopedic, and the first thing a reader called unattractive. Commons maintains
    peer-reviewed "Quality images" and "Featured pictures" categories, which is an editorial
    judgement about the photograph itself rather than about the subject, and searching within them
    returns professional panoramas of the same places.

    The relevance rule is unchanged and still binding: a prettier picture of the wrong thing is a
    worse defect than a plain picture of the right one, so a candidate whose own file name does
    not name the subject is discarded even when it is beautiful.
    """
    subject_tokens = _tokens(subject)

    def names_the_subject(filename: str) -> bool:
        return file_names_the_subject(filename, subject_tokens, is_hero=prefer_landscape)

    for category in ("Quality images", "Featured pictures"):
        data = _api(COMMONS_API, {
            "action": "query", "list": "search", "srnamespace": 6, "srlimit": 8,
            "srsearch": f'{subject} incategory:"{category}"',
        })
        hits = [h.get("title", "") for h in ((data or {}).get("query") or {}).get("search", [])]
        scored: list[tuple[float, str]] = []
        for title in hits:
            name = title[5:] if title.startswith("File:") else title
            if not names_the_subject(name):
                continue
            info = _api(COMMONS_API, {"action": "query", "titles": title,
                                      "prop": "imageinfo", "iiprop": "size"})
            pages = list(((info or {}).get("query") or {}).get("pages", {}).values())
            image = (pages[0].get("imageinfo") or [{}])[0] if pages else {}
            width, height = image.get("width") or 0, image.get("height") or 1
            if width < 1200:
                continue
            ratio = width / max(height, 1)
            # A hero is a wide crop; a portrait photograph loses its subject to object-fit.
            if prefer_landscape and ratio < 1.2:
                continue
            scored.append((ratio if prefer_landscape else 1.0, name))
        if scored:
            scored.sort(reverse=True)
            return scored[0][1]
    return None


def commons_details(filename: str, lang: str = "en", width: int = THUMB_WIDTH) -> dict | None:
    """Licence and author for a file, asked of the wiki that reported it.

    Asked of the wiki that reported the file rather than of Commons, because the name in
    `pageimage` is that wiki's title for it; a wiki resolves its own shared-file titles
    transparently either way, and this avoids one class of normalization mismatch.
    """
    data = _api(WIKI_API.format(lang=lang), {
        "action": "query", "titles": f"File:{filename}", "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": width,
    })
    pages = list(((data or {}).get("query") or {}).get("pages", {}).values())
    if not pages:
        return None
    info = (pages[0].get("imageinfo") or [{}])[0]
    meta = info.get("extmetadata") or {}

    def field(key: str) -> str:
        return re.sub(r"<[^>]+>", "", str((meta.get(key) or {}).get("value", ""))).strip()

    thumb = info.get("thumburl")
    if not thumb:
        return None
    return {"thumb": thumb, "descriptionurl": info.get("descriptionurl"),
            "license": field("LicenseShortName") or "see file page",
            "artist": field("Artist") or "unknown", "credit": field("Credit")}


def embed(thumb_url: str, cap: int = MAX_IMAGE_BYTES) -> tuple[str, int] | None:
    payload = _request(thumb_url, binary=True)
    if not payload or len(payload) > cap:
        return None
    # Parse the extension from the PATH, not the whole URL. Wikimedia appends analytics
    # parameters to thumbnail links, so splitting the raw string on its last dot returned
    # "org&utm_campaign=imageinfo&utm_content=thumbnail" instead of "jpg" -- every download
    # succeeded, every image was inside the size cap, and all five were then discarded as an
    # "unsupported format". The dry run reported five verified photographs and the real run wrote
    # none, which is the shape of a bug that only appears on the path that matters.
    path = urllib.parse.urlparse(thumb_url).path
    suffix = path.rsplit(".", 1)[-1].casefold() if "." in path else ""
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp"}.get(suffix)
    if not mime:
        return None
    return f"data:{mime};base64,{base64.b64encode(payload).decode('ascii')}", len(payload)


def _destination_point(plan: dict) -> tuple[float, float] | None:
    raw = (plan.get("trip") or {}).get("destination_coords")
    if isinstance(raw, list):
        raw = raw[0] if raw else None
    if isinstance(raw, dict) and isinstance(raw.get("lat"), (int, float)):
        return float(raw["lat"]), float(raw["lon"])
    return None


def place_vocabulary(plan: dict) -> frozenset[str]:
    """Every token this trip uses to NAME A PLACE, from the plan's own fields.

    Used only to tell a dropped location apart from a dropped subject in `_relevant`: an article
    that omits "Lucerne" from "Lion Monument Lucerne" is still the Lion Monument, while one that
    omits "Marché" from "Marché de Vevey" is the town. No gazetteer, because the plan already
    enumerates the places it visits and a general one would be wrong the moment a trip goes
    somewhere it has not heard of.
    """
    trip = plan.get("trip") or {}
    words: set[str] = set()
    def add(value: object) -> None:
        if isinstance(value, str) and value.strip():
            words.update(_tokens(value))
    add(trip.get("destination"))
    coords = trip.get("destination_coords")
    for entry in (coords if isinstance(coords, list) else [coords]):
        if isinstance(entry, dict):
            add(entry.get("label"))
    for option in (plan.get("booking_options") or {}).get("accommodations") or []:
        if isinstance(option, dict):
            add(option.get("stay_location"))
            add(option.get("neighborhood"))
    for day in plan.get("days") or []:
        if not isinstance(day, dict):
            continue
        add(day.get("base_location"))
        route = day.get("route") if isinstance(day.get("route"), dict) else {}
        for stop in route.get("stops_in_order") or []:
            add(stop)
    return frozenset(words)


def slots(plan: dict) -> list[dict]:
    """What the page has room for, in priority order.

    Restaurants are deliberately absent. Commons coverage of an individual restaurant is close to
    zero, so the only way to fill those slots would be a generic photograph of food, which is
    decoration pretending to be information -- and a page that does that once cannot be trusted
    when it shows a real one.
    """
    trip = plan.get("trip") or {}
    place = str(trip.get("destination") or "")
    point = _destination_point(plan)
    found = [{"key": "hero", "queries": name_variants(place) or [place], "label": place}]
    for index, anchor in enumerate(plan.get("destination_experience_anchors") or []):
        if not isinstance(anchor, dict) or not anchor.get("name"):
            continue
        name = str(anchor["name"])
        place_short = (name_variants(place) or [place])[-1]
        # Variants are tried bare first. Qualifying "Castillo de Santa Bárbara" with "阿利坎特"
        # mixes two scripts into one search string and matches nothing; the coordinate rule is
        # what disambiguates a Californian Santa Barbara, and it does that without help.
        variants = name_variants(name) or [name]
        queries = variants + [f"{variant} {place_short}".strip() for variant in variants]
        found.append({"key": f"anchor:{index}", "queries": queries, "label": name})
    vocabulary = place_vocabulary(plan)
    for slot in found:
        slot["near"] = point
        slot["place"] = place
        slot["place_vocabulary"] = vocabulary
    return found


def resolve_slot(slot: dict, languages: list[str]) -> dict | None:
    """First (variant, wikipedia) pair that passes both the coordinate and the title rule."""
    for exact in (True, False):
        for language in languages:
            for query in slot["queries"]:
                match = resolve(query, slot["near"], slot["place"], lang=language, exact=exact,
                                place_vocabulary=slot.get("place_vocabulary") or frozenset())
                if match:
                    return match
    return None


def fetch(plan: dict, limit: int, dry_run: bool = False) -> tuple[dict, list[str]]:
    wanted = slots(plan)[:max(limit, 0)]
    notes: list[str] = []
    if not wanted:
        return {}, ["plan names no destination or anchors, so there is nothing to illustrate"]

    languages = wiki_languages((plan.get("trip") or {}).get("language"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as pool:
        matches = list(pool.map(lambda slot: (slot, resolve_slot(slot, languages)), wanted))

    # The destination as the traveller's plan writes it, plus its Latin form. The fall-through
    # guard below compares an article title against the destination name, and on a Chinese plan
    # those are never the same script: `_tokens("Larnaca") <= _tokens("拉纳卡")` is False for the
    # same city, so the guard silently passed everything. Measured on a real zh plan, the anchor
    # "拉纳卡市政市场" resolved to the article "Larnaca" and was captioned with a photograph of the
    # Finikoudes promenade -- a different place, under the market's heading.
    forms = destination_forms(str((plan.get("trip") or {}).get("destination") or ""))

    imagery: dict[str, dict] = {}
    used_files: set[str] = set()
    for slot, match in matches:
        if not match:
            notes.append(f"{slot['label']}: no article both near the trip and about it — no image")
            continue
        # The generic-fallback case, seen on two of five real anchors: the search fell through to
        # the destination's own article, which would have put one city photo under three
        # different headings.
        if slot["key"] != "hero" and is_destination_article(match["page"], forms):
            notes.append(f"{slot['label']}: search fell back to the destination article — no image")
            continue
        if match["file"] in used_files:
            notes.append(f"{slot['label']}: would repeat an image already used — no image")
            continue
        is_hero = slot["key"] == "hero"
        width = HERO_THUMB_WIDTH if is_hero else THUMB_WIDTH
        subject = latin_title(match["page"], match.get("lang", "en")) or match["page"]
        # The relevance rule compares against the place name too, so it needs the same script.
        place_for_match = latin_title(slot["place"], "zh") or slot["place"] if is_hero else slot["place"]
        upgraded = better_candidate(subject, subject if is_hero else place_for_match,
                                    prefer_landscape=is_hero)
        if upgraded and upgraded not in used_files:
            details = commons_details(upgraded, match.get("lang", "en"), width)
            if details:
                match = {**match, "file": upgraded, "upgraded": True}
            else:
                details = commons_details(match["file"], match.get("lang", "en"), width)
        else:
            details = commons_details(match["file"], match.get("lang", "en"), width)
        if not details:
            notes.append(f"{slot['label']}: no licence metadata on Commons — no image")
            continue
        if dry_run:
            used_files.add(match["file"])
            imagery[slot["key"]] = {"label": slot["label"], "page": match["page"],
                                    "file": match["file"], "license": details["license"],
                                    "artist": details["artist"], "data_uri": None}
            continue
        embedded = embed(details["thumb"], HERO_MAX_BYTES if is_hero else MAX_IMAGE_BYTES)
        if not embedded:
            notes.append(f"{slot['label']}: image too large or unsupported format — no image")
            continue
        used_files.add(match["file"])
        imagery[slot["key"]] = {
            "label": slot["label"], "page": match["page"], "page_url": match["page_url"],
            "file": match["file"], "file_url": details.get("descriptionurl"),
            "license": details["license"], "artist": details["artist"],
            "bytes": embedded[1], "data_uri": embedded[0],
        }
    return imagery, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan", help="Plan JSON path")
    parser.add_argument("--out", default=None,
                        help="Where to write the enriched plan (default: in place). The "
                             "photographs go beside it as <stem>-imagery.json either way.")
    parser.add_argument("--max-images", type=int, default=DEFAULT_MAX_IMAGES)
    parser.add_argument("--dry-run", action="store_true",
                        help="Resolve and report without downloading or writing")
    args = parser.parse_args()

    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not read plan: {exc}", file=sys.stderr)
        return 2

    started = time.time()
    wanted_slots = slots(plan)[:max(args.max_images, 0)]
    imagery, notes = fetch(plan, args.max_images, args.dry_run)
    for note in notes:
        print(f"note: {note}")
    total = sum(entry.get("bytes") or 0 for entry in imagery.values())
    print(f"{len(imagery)} image(s) verified in {time.time() - started:.1f}s"
          + (f", {total / 1024:.0f} KB embedded" if total else ""))
    for key, entry in imagery.items():
        print(f"  {key}: {entry['label']} → {entry['page']} ({entry['license']}, {entry['artist']})")

    # A run that filled nothing at all used to exit 0 with a handful of `note:` lines, which is
    # indistinguishable from a run nobody needed. Measured: a delivered Chinese-language plan
    # shipped with zero photographs and the only trace was five notes that had already scrolled
    # past. Two of the three causes were ours -- a Latin token floor that erased two-character CJK
    # names, and a relevance rule that rejected the wiki's own simplified-to-traditional
    # resolution -- and neither would have been looked for, because nothing said the outcome was
    # abnormal. Zero of many is a finding; it is reported as one, and named where the author can
    # act on it.
    if not imagery and wanted_slots:
        print(f"NO IMAGERY: {len(wanted_slots)} slot(s) were offered and none could be filled. "
              f"That is a result worth reading, not a quiet default. The usual causes, in the "
              f"order they are worth checking: an anchor name written as a caption rather than as "
              f"the article's own title ('长洲（渡轮往返，海滨平路）' is a sentence; '長洲' is a "
              f"lookup key); a name written in a different form from the one that wiki titles in; "
              f"or an article that genuinely carries no lead image, which is a gap in the source "
              f"and not something to work around. A page with no photographs is a legitimate "
              f"outcome -- shipping one without knowing why is not.", file=sys.stderr)
    if args.dry_run:
        return 0

    # What the plan already carries, so this run can tell "found nothing new" from "erased what
    # was there". The previous version could not: it assigned plan["imagery"] = imagery
    # unconditionally, so a second run on a train with no signal replaced seven verified
    # photographs with {} and reported success. Nothing downstream would have noticed -- no gate
    # counts images.
    existing_broken = False
    try:
        existing, existing_source = resolve_plan_imagery(plan, args.plan)
    except ImagerySidecarError as exc:
        print(f"note: the plan's current imagery could not be read ({exc})")
        existing, existing_source, existing_broken = {}, None, True

    if not imagery:
        if existing or existing_broken:
            held = ("names an imagery payload that could not be read"
                    if existing_broken else f"carries {len(existing)} verified photograph(s)")
            print(
                f"ERROR: refusing to write. This run verified no photograph, and the plan already "
                f"{held}. Replacing them with nothing is not a result -- check the network and "
                f"re-run, or delete the 'imagery'/'imagery_sidecar' key by hand if the "
                f"photographs are genuinely meant to go.",
                file=sys.stderr)
            return 1
        print("note: no photograph met the standard, so the plan was left unchanged.")
        if args.out:
            # --out is a promise that a plan exists at that path afterwards -- a caller may be
            # feeding it to the next step. An unchanged copy keeps that promise; returning early
            # with no file would make "no photograph was good enough" look like a crash.
            try:
                write_json_atomic(Path(args.out), plan)
            except OSError as exc:
                print(f"ERROR: could not write {args.out}: {exc}", file=sys.stderr)
                return 2
            print(f"Plan JSON: {args.out}")
        return 0

    destination = Path(args.out or args.plan)
    try:
        sidecar = sidecar_path_for(destination)
    except ImagerySidecarError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # MERGED, never replaced. The guard above only fires when a re-run verifies ZERO photographs,
    # and zero is not the shape a bad network actually has: this module's own MAX_CONCURRENCY note
    # records eight of eight concurrent lookups coming back HTTP 429, and one slot resolving out of
    # seven is the ordinary result of flaky hotel wifi. Measured on a sidecar holding seven
    # verified photographs with fetch() returning one: the file went from 7 slots to 1, the run
    # printed "1 image(s) verified" and exited 0, and six photographs that had passed every
    # provenance rule were gone with no note. A run may only ADD what it verified and KEEP what it
    # did not re-verify; it may never delete a slot on the strength of having failed to reach
    # Wikipedia.
    #
    # Kept only on positive evidence, which is why this is not a blind dict merge. Slot keys are
    # positional ("anchor:2"), so if an anchor is removed from the plan every anchor after it
    # shifts up a slot and a carried-forward photograph would land under a DIFFERENT heading --
    # the exact accuracy failure this whole module exists to refuse. So a stored slot is carried
    # only when the plan still names that key with the same label it was filed under.
    #
    # Which is also how a slot is deliberately removed: delete the anchor from the plan and re-run,
    # and the orphaned slot is dropped here with a note naming it. To drop the photographs
    # altogether, delete the sidecar file and the plan's `imagery_sidecar` key -- the empty-run
    # refusal above says the same thing. To drop ONE photograph while keeping its anchor, delete
    # that key from the sidecar by hand and do not re-run this script, which re-verifies every slot
    # the plan names and would find it again.
    labels = plan_slot_labels(plan)
    carried: dict[str, dict] = {}
    dropped: list[str] = []
    ambiguous: list[str] = []
    if existing_broken:
        # Nothing to merge with, so writing is only safe where there is nothing to lose. An
        # unreadable payload is not an absent one: the over-ceiling case is a file full of real
        # photographs that this script simply refuses to parse, and clobbering it because it could
        # not be read would destroy more than a partial run ever could.
        if sidecar.exists():
            print(f"ERROR: refusing to write. This run verified {len(imagery)} photograph(s), but "
                  f"{sidecar} already exists and the plan's current imagery could not be read "
                  f"(the note above says why), so there is no way to tell what overwriting it "
                  f"would destroy. Fix or delete that file -- and the plan's 'imagery_sidecar' key "
                  f"if it names something else -- then re-run.", file=sys.stderr)
            return 1
        print(f"note: the unreadable payload the plan named is left on disk; this run writes a "
              f"fresh {sidecar.name} and points the plan at it.")
    else:
        for key, entry in existing.items():
            if key in imagery:
                continue  # re-verified by this run; the fresh entry wins
            expected = labels.get(key)
            stored = entry.get("label") if isinstance(entry, dict) else None
            if not expected:
                dropped.append(f"{key} ({stored!r}) was dropped: the plan no longer names that "
                               f"slot")
            elif isinstance(stored, str) and stored.strip() == expected.strip():
                carried[key] = entry
            else:
                ambiguous.append(f"{key} is stored under the label {stored!r}, but the plan now "
                                 f"names that slot {expected!r}")
        if ambiguous:
            # Not dropped and not kept: guessing either way puts a photograph under a heading it
            # may not depict, or throws away one that does. The operator knows which.
            print(f"ERROR: refusing to write. This run did not re-verify every slot, and for the "
                  f"slot(s) below the stored photograph cannot be shown to depict what the plan "
                  f"now names:", file=sys.stderr)
            for line in ambiguous:
                print(f"  - {line}", file=sys.stderr)
            print(f"Re-run when the network is reachable so those slots are verified afresh, or "
                  f"edit {sidecar.name} by hand. Carrying them forward would risk captioning a "
                  f"photograph with a place it is not of; dropping them would delete verified "
                  f"work this run never checked.", file=sys.stderr)
            return 1

    # Everything above protects the payload this run READ. This protects the payload it is about
    # to WRITE ON, which is not always the same file: `existing` came from wherever the SOURCE
    # plan's photographs live, while `sidecar` is derived from --out. Between them sits a file
    # nobody named on the command line and nothing above has looked at. write_target_refusal says
    # why destroying it is the worse half of the same mistake a refused read makes.
    blocked = write_target_refusal(plan, sidecar, existing_source)
    if blocked:
        print(f"ERROR: refusing to write. {blocked}", file=sys.stderr)
        return 1

    # The plan's own slot order, so two runs of this script produce a diffable file rather than
    # one whose key order depends on which slots happened to resolve.
    merged = {**carried, **imagery}
    payload = {key: merged[key] for key in labels if key in merged}
    payload.update({key: value for key, value in merged.items() if key not in payload})
    for line in dropped:
        print(f"note: {line}")
    for key in carried:
        print(f"note: {key} ({carried[key].get('label')!r}) was not re-verified by this run and "
              f"was carried forward unchanged.")

    # Measured on what is about to land on disk, not on what this run built: a carried-forward
    # slot costs exactly the same bytes as a fresh one, and the ceiling is about the file a
    # traveller opens on hotel wifi.
    refusal = aggregate_refusal(imagery_payload_bytes(payload),
                                "the imagery this run would write")
    if refusal:
        print(f"ERROR: {refusal}", file=sys.stderr)
        return 1
    # The bytes leave the plan entirely rather than being written to both places. Keeping a copy
    # inline would mean the sidecar bought nothing: the plan would still cost ~576k tokens to
    # read, which is the whole defect. They are not lost -- they are in the file named on the
    # line below, and every consumer finds it without being told.
    plan.pop("imagery", None)
    plan["imagery_sidecar"] = sidecar.name
    try:
        # Sidecar first, plan second. If the second write fails the sidecar is an orphan that the
        # next run overwrites and that consumers find by name anyway; the other order would leave
        # a plan pointing at a file that does not exist, which every reader is required to refuse.
        write_json_atomic(sidecar, payload)
        write_json_atomic(destination, plan)
    except OSError as exc:
        print(f"ERROR: could not write the plan or its imagery sidecar: {exc}", file=sys.stderr)
        return 2
    # Only when this run rewrote the plan that referenced the old sidecar. With --out the source
    # plan is untouched and still points at its own payload, so calling that file unreferenced
    # would send somebody to delete a photograph set that is still in use.
    in_place = args.out is None or Path(args.out).resolve() == Path(args.plan).resolve()
    if in_place and existing_source is not None and existing_source.resolve() != sidecar.resolve():
        print(f"note: {existing_source} is now unreferenced; this plan points at {sidecar.name}.")
    # The count of what LANDED, not of what this run verified. The two are the same number only
    # when every slot resolved, and the run that erased six photographs announced itself as
    # "1 image(s) verified" -- a true sentence about the run and a wholly misleading one about the
    # file, which is how nobody noticed.
    print(f"Imagery sidecar: {sidecar} ({len(payload)} image(s), "
          f"{imagery_payload_bytes(payload) / 1024:.0f} KB"
          + (f"; {len(imagery)} verified now, {len(carried)} carried forward" if carried else "")
          + ")")
    print(f"Plan JSON: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
