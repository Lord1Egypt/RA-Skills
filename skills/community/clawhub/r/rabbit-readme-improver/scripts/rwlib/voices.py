#!/usr/bin/env python3
"""
Voice rules files, with inheritance.

Blending interpolates two whole profiles, which answers the question "what does
the average of these two people sound like". The commoner real need is smaller
and sharper: my voice, plus a few things this particular repo or client does
differently. `.rabbit-voice` already pins which profile a repo uses. This is the
other half, the per-repo delta:

    {
      "voice": "whit3rabbit-acme",
      "extends": "whit3rabbit",
      "banned_words": ["synergy"],
      "mechanics": {"oxford_comma": "require"}
    }

The merge rule is deliberately lopsided.

  bans      union. A child adds to what the parent forbids and cannot quietly
            drop one, because a house style that silently unbans a word is a
            house style nobody can rely on. To soften an inherited rule, give
            the child a `banned_regex` entry with the same id: entries merge by
            id and the child's wins outright, so it can lower a priority, widen
            a `max_allowed`, or point the pattern at something narrower.
  mechanics child wins, key by key. Parent keys the child does not mention
            survive, so an override file stays two lines long.
  scalars   child wins. `voice`, `default_priority`, and anything else.

Cycles are caught rather than recursed into, and a missing parent is an error
rather than a silent fall back to no rules at all: a profile that inherits from
nothing enforces nothing, and reporting a clean voice band on a document nobody
checked is the failure mode this whole file exists to avoid.

Stdlib only, 3.9+.
"""

import json
import os
import sys

try:
    from .inflect import term_of
    from .cli_error import LLMArgumentParser, format_file_error
except ImportError:                 # run as a script: no package, but rwlib/ is
    from inflect import term_of     # on sys.path, because it holds this file
    from cli_error import LLMArgumentParser, format_file_error

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES_DIR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "voices")

# Keys merged as an ordered union of scalars.
LIST_UNION_KEYS = ("banned_words", "banned_phrases")
# Keys merged by the "id" of each entry, child wins.
LIST_BY_ID_KEYS = ("banned_regex", "required_when", "signature_moves")
# Keys merged key by key, child wins.
DICT_MERGE_KEYS = ("mechanics", "preferred_substitutions", "engine_exemptions")
# The same, one level deeper: {register: {mechanic: value}}. A shallow update
# would let a child overriding one mechanic in `chat` drop every other
# mechanic the parent scoped to `chat`, which is the silent unbanning this
# file's merge rules exist to prevent.
NESTED_DICT_MERGE_KEYS = ("mechanics_by_register",)

MAX_DEPTH = 8


class VoiceError(Exception):
    """A rules file that cannot be resolved. Never swallowed: see the module
    docstring on why an unenforced voice is worse than a missing one."""


def _union(parent, child):
    """Ordered union of two ban lists, keyed on the term.

    A ban list entry is a plain string or `{"word": ..., "inflect": true}`, so
    the key has to come out of `inflect.term_of` rather than off the value: a
    dict is unhashable, and keying on the value raised TypeError the first time a
    child profile inherited from a parent that used the object form. Keying on
    the term is also the behaviour worth having, because a child restating a
    parent's word in order to add `inflect` should replace it rather than sit
    beside it as a duplicate.
    """
    out, index = [], {}
    for entries in (parent, child):
        for value in entries:
            key = term_of(value).lower()
            if key in index:
                out[index[key]] = value      # the later spelling wins
            else:
                index[key] = len(out)
                out.append(value)
    return out


def _by_id(parent, child):
    out = [dict(e) for e in parent]
    index = {e.get("id"): i for i, e in enumerate(out) if e.get("id")}
    for entry in child:
        eid = entry.get("id")
        if eid is not None and eid in index:
            out[index[eid]] = entry
        else:
            out.append(entry)
    return out


def _contrastive_union(parent, child):
    out = list(parent)
    seen = {json.dumps(p, sort_keys=True) for p in out if isinstance(p, dict)}
    for p in child:
        if isinstance(p, dict):
            key = json.dumps(p, sort_keys=True)
            if key not in seen:
                out.append(p)
                seen.add(key)
        elif p not in out:
            out.append(p)
    return out


def merge(parent, child):
    """One level of inheritance. Order matters: parent first, then child."""
    out = dict(parent)
    for key, value in child.items():
        if key == "extends":
            continue
        if key in LIST_UNION_KEYS:
            out[key] = _union(parent.get(key, []), value)
        elif key in LIST_BY_ID_KEYS:
            out[key] = _by_id(parent.get(key, []), value)
        elif key == "contrastive_pairs":
            out[key] = _contrastive_union(parent.get(key, []), value)
        elif key in DICT_MERGE_KEYS:
            merged = dict(parent.get(key, {}))
            merged.update(value)
            out[key] = merged
        elif key in NESTED_DICT_MERGE_KEYS:
            merged = {k: dict(v) for k, v in parent.get(key, {}).items()}
            for register, overrides in value.items():
                merged.setdefault(register, {}).update(overrides)
            out[key] = merged
        else:
            out[key] = value
    return out


def _resolve_parent(name, voices_dir, source):
    """A parent named by profile name, or by a path relative to the child."""
    candidates = [os.path.join(voices_dir, name + ".rules.json")]
    if os.sep in name or name.endswith(".json"):
        candidates.insert(0, os.path.join(os.path.dirname(source), name))
    for path in candidates:
        if os.path.exists(path):
            return path
    raise VoiceError(
        "%s extends %r, which resolves to none of: %s. A profile that inherits "
        "from nothing enforces nothing."
        % (os.path.basename(source), name, ", ".join(candidates)))


def load(path, voices_dir=None, _seen=None, _depth=0):
    """The fully merged rules dict for a profile.

    Reads exactly like a flat rules file to every caller, which is the point:
    scan.py does not know or care whether a voice was written in one file or
    three.
    """
    voices_dir = voices_dir or VOICES_DIR
    path = os.path.abspath(path)
    _seen = _seen or []
    if path in _seen:
        raise VoiceError("voice inheritance loops: %s"
                         % " -> ".join(os.path.basename(p)
                                       for p in _seen + [path]))
    if _depth > MAX_DEPTH:
        raise VoiceError("voice inheritance deeper than %d files" % MAX_DEPTH)

    try:
        with open(path, encoding="utf-8") as fh:
            rules = json.load(fh)
    except (OSError, ValueError) as exc:
        raise VoiceError("could not read voice rules: %s" % exc)
    if not isinstance(rules, dict):
        raise VoiceError("%s is not a rules object" % os.path.basename(path))

    parent_name = rules.get("extends")
    if not parent_name:
        return rules
    parent_path = _resolve_parent(parent_name, voices_dir, path)
    parent = load(parent_path, voices_dir, _seen + [path], _depth + 1)
    return merge(parent, rules)


RULES_SUFFIX = ".rules.json"


def strip_rules_suffix(path):
    """`dana.rules.json` -> `dana`, and anything else back unchanged.

    Anchored on purpose. `str.replace` is not: a path carrying the suffix
    anywhere but the end had its middle rewritten, and the "read the profile
    markdown too" note that readme_check.py builds from it pointed at a file
    nobody has. One home for it, because both this module and readme_check.py
    turn a rules path into a profile name.
    """
    return path[:-len(RULES_SUFFIX)] if path.endswith(RULES_SUFFIX) else path


# --------------------------------------------------------------------------
# blending
# --------------------------------------------------------------------------
#
# references/voice.md specifies a blend as numeric interpolation of the
# dimensions, union of the Never lists, and structural defaults from the
# heavier profile. Only two of those three are about this file.
#
# The dimensions live in the profile *markdown*, in a fenced block of
# formality/confidence/warmth numbers, and nothing here reads them: they are
# instructions to a writer, not thresholds anything enforces. Interpolating them
# stays an authoring step, and the doc now says so instead of implying a
# function exists.
#
# The other two are exactly this file's business, and they are what blend()
# does. Everything mechanically enforced in a rules file can be merged, and the
# rule throughout is that the stricter side wins, because a blend that quietly
# relaxes a refusal is the failure `merge` already refuses to allow between a
# parent and a child.

# Mechanics whose values run loose to strict, so a blend can take the strict end
# without a table of pairwise answers. Ordered strict-first.
STRICTNESS = {
    "em_dash": ("forbid", "limit", "allow"),
    "double_hyphen": ("forbid", "allow"),
    "semicolon": ("forbid", "allow"),
    "emoji": ("forbid", "allow"),
    "curly_quotes": ("forbid", "allow"),
    "one_word_sentence": ("forbid", "allow"),
}
# Caps, where stricter is smaller.
NUMERIC_MECHANICS = ("max_paragraph_sentences", "max_avg_sentence_words",
                     "max_sentence_words", "max_em_dashes_per_1000w")
# Mechanics with no strictness order at all. `require` and `forbid` are opposite
# demands rather than degrees of one, and `dmy` and `mdy` are two conventions.
# The weight decides and the conflict is reported, because silently picking one
# writer's date format out of two is the kind of choice that has to be visible
# to the person whose name goes on the profile.
OPINION_MECHANICS = {"oxford_comma": "allow", "date_format": "any"}

PRIORITY_ORDER = ("P0", "P1", "P2")

# The whole mechanics vocabulary: which keys a rules file may set, and which
# values each one takes. Assembled rather than restated, because most of it is
# already here. STRICTNESS orders the forbid/allow ones, NUMERIC_MECHANICS names
# the caps, and only the two with no strictness order have to be spelled out.
#
# It lives beside the merge rules rather than in whatever checks a profile,
# because a vocabulary stated twice is a vocabulary that drifts, and scan.py
# reads these values by hand in `apply_voice_rules`. The template's
# `_options` block is the third statement of it, and a test holds the two
# together.
MECHANIC_VALUES = dict(STRICTNESS)
MECHANIC_VALUES["oxford_comma"] = ("require", "forbid", "allow")
MECHANIC_VALUES["date_format"] = ("dmy", "mdy", "iso", "any")


def mechanic_problems(mechanics):
    """[(key, message)] for every mechanic this engine will not act on.

    An unknown key and a misspelled value fail the same way at runtime, which is
    silently: `mech.get("semicolons")` is None, `== "forbid"` is False, and the
    rule the author believes they wrote never runs.
    """
    out = []
    for key, value in mechanics.items():
        if key.startswith("_"):
            continue                    # template guidance, reported elsewhere
        if key in NUMERIC_MECHANICS:
            try:
                float(value)
            except (TypeError, ValueError):
                out.append((key, "%r is not a number" % (value,)))
            continue
        allowed = MECHANIC_VALUES.get(key)
        if allowed is None:
            out.append((key, "is not a mechanic this engine reads. Known: %s"
                        % ", ".join(sorted(set(MECHANIC_VALUES) |
                                           set(NUMERIC_MECHANICS)))))
        elif value not in allowed:
            out.append((key, "is %r, which is not one of: %s"
                        % (value, ", ".join(allowed))))
    return out


def _blend_mechanic(key, left, right, weight, notes):
    """One mechanic, with the strict side winning wherever "strict" means
    anything."""
    if left is None:
        return right
    if right is None:
        return left
    if left == right:
        return left
    if key in NUMERIC_MECHANICS:
        try:
            return min(float(left), float(right))
        except (TypeError, ValueError):
            return left if weight >= 0.5 else right
    order = STRICTNESS.get(key)
    if order:
        return min((left, right), key=lambda v: order.index(v)
                   if v in order else len(order))
    loosest = OPINION_MECHANICS.get(key)
    if loosest is not None:
        # One side has no opinion: take the one that does. Two opinions that
        # disagree is a real conflict and the weight breaks it, loudly.
        if left == loosest:
            return right
        if right == loosest:
            return left
    chosen = left if weight >= 0.5 else right
    notes.append("mechanics.%s: %r and %r cannot both hold, took %r on weight"
                 % (key, left, right, chosen))
    return chosen


def blend(left, right, weight=0.5, name=None):
    """(rules, notes) for a weighted blend of two loaded profiles.

    `weight` is the share belonging to `left`, so 0.7 is "70% left, 30% right".
    It breaks ties and nothing else. Every rule that has a stricter side takes
    it whatever the weight says, which is the union-of-Nevers rule from voice.md
    applied to more than the word lists: a blend that can drop a refusal is a
    blend nobody can rely on, and the weight is a statement about emphasis
    rather than permission.

    `notes` is the half worth reading. It names every place the two profiles
    wanted incompatible things, because those are the lines the person whose
    name goes on the result has to confirm.

    The blended rules carry a `blend` key recording both sources and the weight,
    so the lineage voice.md asks for is in the file rather than in somebody's
    memory of how it was made.
    """
    if not 0.0 <= weight <= 1.0:
        raise VoiceError("blend weight %r is not between 0 and 1" % weight)
    notes = []
    heavier, lighter = ((left, right) if weight >= 0.5 else (right, left))
    out = dict(heavier)

    for key in LIST_UNION_KEYS:
        out[key] = _union(lighter.get(key, []), heavier.get(key, []))
    for key in LIST_BY_ID_KEYS:
        # By id, heavier last so it wins a collision. An id in one profile only
        # survives either way, which is the union the Never rule asks for.
        out[key] = _by_id(lighter.get(key, []), heavier.get(key, []))
        for entry in out[key]:
            eid = entry.get("id")
            in_both = (any(e.get("id") == eid for e in left.get(key, []))
                       and any(e.get("id") == eid for e in right.get(key, [])))
            if in_both:
                notes.append("%s.%s: both profiles define it, kept the heavier "
                             "one's version" % (key, eid))

    # Underscore-prefixed keys are the template's inline guidance, which it tells
    # its copier to delete. A generated file carrying another file's
    # documentation is noise, and here it would be noise attributed to a person.
    mech_keys = {k for k in (set(left.get("mechanics", {}))
                             | set(right.get("mechanics", {})))
                 if not k.startswith("_")}
    out["mechanics"] = {
        key: _blend_mechanic(key, left.get("mechanics", {}).get(key),
                             right.get("mechanics", {}).get(key), weight, notes)
        for key in sorted(mech_keys)
    }

    # Underscore keys are filtered at both levels here, the same as `mechanics`
    # above. Filtering one and not the other let the template's guidance survive
    # a blend by the back door, as a register named `_example` or an override
    # key inside a real one.
    scoped = {}
    for source in (lighter, heavier):
        for register, overrides in source.get("mechanics_by_register", {}).items():
            if register.startswith("_"):
                continue
            keep = {k: v for k, v in overrides.items() if not k.startswith("_")}
            if keep:
                scoped.setdefault(register, {}).update(keep)
    if scoped:
        out["mechanics_by_register"] = scoped
    else:
        out.pop("mechanics_by_register", None)

    subs = dict(lighter.get("preferred_substitutions", {}))
    subs.update(heavier.get("preferred_substitutions", {}))
    if subs:
        out["preferred_substitutions"] = subs

    # Intersection, not union: an exemption stands a check down, so *not*
    # exempting an id is the stricter side, unlike banned_words/banned_phrases
    # above where more bans is stricter and a union is exactly the Never rule.
    # A plain union let one side's exemption survive a blend at any weight,
    # including 0.9 toward a profile that names none at all.
    left_ex, right_ex = (lighter.get("engine_exemptions", {}),
                        heavier.get("engine_exemptions", {}))
    both = set(left_ex) & set(right_ex)
    exemptions = {eid: right_ex.get(eid) or left_ex.get(eid) for eid in both}
    dropped = (set(left_ex) | set(right_ex)) - both
    if dropped:
        notes.append("engine_exemptions: %s exempted by only one profile, "
                     "dropped from the blend (the side that still enforces "
                     "it wins)" % ", ".join(sorted(dropped)))
    if exemptions:
        out["engine_exemptions"] = exemptions

    cp = _contrastive_union(lighter.get("contrastive_pairs", []),
                            heavier.get("contrastive_pairs", []))
    if cp:
        out["contrastive_pairs"] = cp
    else:
        out.pop("contrastive_pairs", None)

    # The stricter default priority, for the same reason as everything else.
    priorities = [p for p in (left.get("default_priority"),
                              right.get("default_priority")) if p]
    if priorities:
        out["default_priority"] = min(
            priorities, key=lambda p: PRIORITY_ORDER.index(p)
            if p in PRIORITY_ORDER else len(PRIORITY_ORDER))

    # A blend is a new profile, not a child of either, so `extends` must not
    # survive: it would send load() off to re-merge a parent whose rules are
    # already folded in here, at a path relative to a file that no longer exists.
    out.pop("extends", None)
    out["voice"] = name or "%s-%s" % (left.get("voice", "left"),
                                      right.get("voice", "right"))
    out["blend"] = {"of": [left.get("voice"), right.get("voice")],
                    "weight": weight}
    notes.append("dimensions are not blended here. The formality, warmth, and "
                 "energy numbers live in the profile markdown and nothing "
                 "enforces them, so interpolating them is an authoring step: "
                 "%.2f x left + %.2f x right, written into the new .md by hand."
                 % (weight, 1 - weight))
    return out, notes


def installed(voices_dir=None):
    """Profile names in voices/, excluding the template."""
    voices_dir = voices_dir or VOICES_DIR
    if not os.path.isdir(voices_dir):
        return []
    return sorted(strip_rules_suffix(f) for f in os.listdir(voices_dir)
                  if f.endswith(RULES_SUFFIX) and not f.startswith("TEMPLATE"))


def build_voice_path(here=None):
    """Where `build_voice.py` actually is from here, or None if it is nowhere.

    The note below tells somebody with no active voice how to get one, and for
    the life of that message it named a repo-relative path. That path is right
    in a checkout and wrong everywhere else: a packaged bundle puts this file
    at `<bundle>/scripts/rwlib/voices.py`, so there is no `skills/voice-setup/`
    to find and the command a user was told to run does not exist.

    `package_skills.py` rewrites markdown paths per bundle layout and does not
    touch strings inside Python, so nothing upstream was going to catch this.

    Two candidates, matching the two layouts that ship the script:

        <bundle>/scripts/build_voice.py            vendored beside this rwlib
        <skills>/voice-setup/scripts/build_voice.py  a checkout, or loose skills

    Returning None is a real answer rather than a failure. Four of the five
    bundles vendor `rwlib` without `build_voice.py`, because only voice-setup
    builds profiles, so in those there is no path to name and the caller says
    which skill to reach for instead.
    """
    here = here or HERE
    scripts_dir = os.path.dirname(here)             # .../scripts
    skills_dir = os.path.dirname(os.path.dirname(scripts_dir))
    for candidate in (os.path.join(scripts_dir, "build_voice.py"),
                      os.path.join(skills_dir, "voice-setup", "scripts",
                                   "build_voice.py")):
        if os.path.isfile(candidate):
            return candidate
    return None


def build_voice_command(here=None):
    """The sentence telling somebody how to claim a voice, path and all.

    Printed relative to the working directory when it stays inside it, which
    is what makes it copy-pasteable from a checkout root and keeps the message
    identical to the one this repository has always printed. An absolute path
    otherwise, because a `../../..` prefix is worse than a long path and a
    wrong path is worse than both.

    `relpath` raises on Windows when the two paths are on different drives, and
    `resolve` calls this on every `--voice auto` scan, so the guard is not
    hypothetical: a plugin installed on C: and a document open on D: would have
    turned a note into a traceback.

    Shown with forward slashes even on Windows, where `relpath` returns
    backslashes: this is a command line, not a filesystem path, and `python3`
    accepts either separator, so normalizing keeps the printed command
    identical across platforms instead of leaking `os.sep` into the message.
    """
    path = build_voice_path(here)
    if path is None:
        return ("activate one through the `voice-setup` skill, which is where "
                "`build_voice.py` lives")
    try:
        shown = os.path.relpath(path, os.getcwd())
    except (ValueError, OSError):
        shown = path
    if shown.startswith(".."):
        shown = path
    else:
        shown = shown.replace(os.sep, "/")
    return "run `python3 %s --check <name> --activate` once" % shown


def _first_line(path):
    """The first non-comment line of a one-line control file, or "" if it is empty."""
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                s = line.strip()
                if s and not s.startswith("#"):
                    return s
            return ""
    except (OSError, UnicodeDecodeError):
        return ""


def _find_rabbit_voice(start_dir):
    """The nearest `.rabbit-voice` at or above `start_dir`, or None.

    Bounded on purpose. A pin sits at the root of the repository it governs,
    and a document three directories down is still that repository's. The walk
    stops at the first directory holding a `.git` (that repository's root has
    been reached and passed) and at `$HOME`, because a stray pin in a home
    directory or above it would apply a stranger's `default_priority: P0` bans
    to every unrelated checkout on the machine.
    """
    curr = os.path.abspath(start_dir)
    home = os.path.abspath(os.path.expanduser("~"))
    while True:
        pin = os.path.join(curr, ".rabbit-voice")
        if os.path.exists(pin):
            return pin
        if os.path.exists(os.path.join(curr, ".git")) or curr == home:
            break
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return None


def resolve(target_path=None, voices_dir=None):
    """(path_to_rules, voice_name, note). Which profile applies, and why.

    Whoever is active governs, and somebody has to have said so. A
    `.rabbit-voice` file pins a repo's house voice, otherwise `voices/ACTIVE`
    decides, and when neither exists this resolves nothing. Nothing here knows
    or prefers a particular person.

    **A profile nobody chose is never enforced.** This used to fall back to the
    one profile sitting in `voices/`, with a note saying so. The plugin ships
    exactly one, an example, so on a fresh install that fallback was a stranger's
    `default_priority: P0` bans applied to somebody's prose, and a note attached
    to full enforcement is close to what SKILL.md calls silent. The note now says
    which profile is there and which command claims it, and the answer is one
    command run once. Writing in the wrong person's register is worse than
    writing in none.

    `target_path` is the document being checked, if there is one: a repo's pin
    sits beside its files, so the document's own directory is searched before
    the working directory. Called with nothing, only the working directory and
    ACTIVE are consulted, which is what a scan of stdin gets.

    Each of those two directories is searched *and every directory above it*,
    up to the bound `_find_rabbit_voice` describes. A pin lives at a repo root
    and the file being scanned usually does not, so the old exact-directory
    match found the pin only when the two happened to coincide. The nearest pin
    wins, and it is named in the note, because "which profile" and "who said
    so" are one answer.

    This used to live in readme_check.py and scan.py had none of it, so the two
    checkers in one plugin disagreed about whose rules were in force. It is one
    fact about one installation, so it has one home.
    """
    voices_dir = voices_dir or VOICES_DIR
    start_dirs = []
    if target_path:
        start_dirs.append(os.path.dirname(os.path.abspath(target_path)))
    start_dirs.append(os.getcwd())

    # The first pin found decides, including when it names a profile that will
    # not load: a pin somebody wrote and got wrong is a thing to report, not a
    # reason to keep looking and silently apply a different person's rules.
    pin = next((p for p in (_find_rabbit_voice(d) for d in start_dirs) if p),
               None)
    if pin:
        name = _first_line(pin)
        if not name or os.path.basename(name) != name or ".." in name:
            return None, name, ("%s names invalid voice name %r" % (pin, name))
        rules = os.path.join(voices_dir, name + RULES_SUFFIX)
        if os.path.abspath(rules).startswith(os.path.abspath(voices_dir) + os.sep) and os.path.exists(rules):
            return rules, name, "voice pinned by %s" % pin
        return None, name, ("%s names %r but voices/%s.rules.json does not exist"
                            % (pin, name, name))

    active = os.path.join(voices_dir, "ACTIVE")
    name = _first_line(active) if os.path.exists(active) else ""
    if name:
        if not name or os.path.basename(name) != name or ".." in name:
            return None, name, ("active voice %r is an invalid voice name" % name)
        rules = os.path.join(voices_dir, name + RULES_SUFFIX)
        if os.path.abspath(rules).startswith(os.path.abspath(voices_dir) + os.sep) and os.path.exists(rules):
            return rules, name, None
        return None, name, ("active voice %r has no .rules.json, so none of its rules are "
                            "mechanically enforced" % name)

    why = ("voices/ACTIVE is missing" if not os.path.exists(active)
           else "voices/ACTIVE is empty")
    others = installed(voices_dir)
    if others:
        return None, None, (
            "%s and %d profile%s installed (%s), none of them chosen. Nothing "
            "is enforced until one is: %s, drop a `.rabbit-voice` "
            "holding the name in your repository, or pass --voice-rules <path>. "
            "The profiles that ship with this plugin are examples, not yours."
            % (why, len(others), " is" if len(others) == 1 else "s are",
               ", ".join(others), build_voice_command()))
    return None, None, ("%s and no profile is installed, prose checked against "
                        "craft rules only" % why)


def lineage(path, voices_dir=None):
    """[profile name] from this file up to the root, for reporting.

    A report that says "voice: acme" when acme inherits most of its rules from
    somebody else is telling half the truth about what just got enforced.
    """
    voices_dir = voices_dir or VOICES_DIR
    out, seen, current = [], set(), os.path.abspath(path)
    while current and current not in seen and len(out) <= MAX_DEPTH:
        seen.add(current)
        try:
            with open(current, encoding="utf-8") as fh:
                rules = json.load(fh)
        except (OSError, ValueError):
            break
        out.append(rules.get("voice")
                   or strip_rules_suffix(os.path.basename(current)))
        parent = rules.get("extends")
        if not parent:
            break
        try:
            current = _resolve_parent(parent, voices_dir, current)
        except VoiceError:
            break
    return out


def _resolve_named(name, voices_dir):
    """A profile named on the command line, by name or by path."""
    if os.path.exists(name):
        return name
    candidate = os.path.join(voices_dir, name + RULES_SUFFIX)
    if os.path.exists(candidate):
        return candidate
    raise VoiceError("no profile %r: not a path, and %s does not exist"
                     % (name, candidate))


def load_scan(caller_name="engine"):
    rwlib_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.dirname(rwlib_dir)
    scan_path = os.path.join(scripts_dir, "scan.py")
    if not os.path.exists(scan_path):
        raise SystemExit("%s: cannot find %s. This script has to run "
                         "from inside an installed plugin." % (caller_name, scan_path))
    import importlib.util
    spec = importlib.util.spec_from_file_location("rw_scan", scan_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv):
    """python3 rwlib/voices.py --blend a b [--weight 0.7] [--name ab] [--out path]

    Prints the blended rules file on stdout and the notes on stderr, so the
    result can be redirected into voices/<name>.rules.json while the conflicts
    stay in front of whoever ran it. The notes are the part worth reading: they
    name every place the two profiles wanted incompatible things.
    """
    examples = [
        "python3 rwlib/voices.py --blend profileA profileB",
        "python3 rwlib/voices.py --blend profileA profileB --weight 0.7 --name blended_profile --out voices/blended_profile.rules.json"
    ]
    ap = LLMArgumentParser(prog="voices.py", description=main.__doc__, examples=examples)
    ap.add_argument("--blend", nargs=2, metavar=("LEFT", "RIGHT"), required=True,
                    help="two profile names, or two paths to .rules.json files")
    ap.add_argument("--weight", type=float, default=0.5,
                    help="the share belonging to LEFT (default 0.5). It breaks "
                         "ties and nothing else: the stricter side wins "
                         "wherever one exists, whatever the weight says")
    ap.add_argument("--name", help="the blended profile's voice name")
    ap.add_argument("--out", help="file path to write the blended profile JSON to atomically")
    ap.add_argument("--voices-dir", default=VOICES_DIR)
    args = ap.parse_args(argv)

    try:
        left = load(_resolve_named(args.blend[0], args.voices_dir),
                    voices_dir=args.voices_dir)
        right = load(_resolve_named(args.blend[1], args.voices_dir),
                     voices_dir=args.voices_dir)
        rules, notes = blend(left, right, args.weight, args.name)
    except VoiceError as exc:
        print(format_file_error(
            "voices.py", str(args.blend), "--blend",
            expected_type="two valid voice profile names or file paths",
            details=str(exc), examples=examples
        ), file=sys.stderr)
        return 2

    content = json.dumps(rules, indent=2) + "\n"
    if args.out:
        out_path = os.path.abspath(args.out)
        out_dir = os.path.dirname(out_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        tmp_path = out_path + ".tmp.%d" % os.getpid()
        with open(tmp_path, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path, out_path)
    else:
        print(content, end="")

    for note in notes:
        print("  note: %s" % note, file=sys.stderr)
    print("\nThe rules file is the regex-checkable half. Write the blended "
          "profile markdown too, or the result enforces punctuation and "
          "describes nobody.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

