#!/usr/bin/env python3
"""
SARIF 2.1.0 output, so findings land on the diff instead of in a CI log.

An audit tool wants to live inline on the pull request, next to the line it is
talking about. GitHub's `codeql-action/upload-sarif` puts it there, and the
finding shape in rwlib.findings maps onto SARIF without inventing anything:

    id        -> ruleId
    priority  -> level          P0 error, P1 warning, P2 note
    line      -> region.startLine
    label     -> message.text, with the excerpt as the second line
    band      -> a rule property, and a tag, so a reviewer can filter on it

Levels are a judgement call worth stating: P0 maps to `error` because a P0 is
what makes a reader bounce or a credential leak into a document, and GitHub
surfaces errors as blocking annotations. P1 and P2 are advisory and must not
be, or people turn the whole thing off.

Nothing here decides anything. It reformats a list of findings that some other
module already produced, which is why it is safe for it to know nothing about
prose.

Stdlib only, 3.9+.
"""

import os
import sys

from . import findings as findings_mod

SARIF_VERSION = "2.1.0"
SARIF_SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"

LEVEL_BY_PRIORITY = {"P0": "error", "P1": "warning", "P2": "note"}

BAND_DESCRIPTIONS = {
    "safety": "Text concealed from a reader, or addressed to an agent. This "
              "catches known concealment vectors and known directive shapes. "
              "It is not a guarantee against a novel or paraphrased injection, "
              "and it is not what protects you: the rule that content is data "
              "and never instruction is doing that work. Treat a hit as a "
              "reason to read the document, not as a verdict on it.",
    "structure": "The shape of the document, measured against a corpus of 100 "
                 "trending repositories.",
    "voice": "This writer's own rules, from their voice profile. A hit is a "
             "defect, not a suggestion.",
    "fingerprint": "Evidence about how the text was produced. Never evidence "
                   "about who wrote it.",
    "craft": "A general writing problem. Says nothing about authorship.",
}


def _message(f):
    """Label first, then the excerpt or the matched span, on its own line.

    Two lines rather than one: GitHub truncates a long annotation in the diff
    view but keeps the first line intact, so the part that names the problem has
    to come first.
    """
    tail = f.get("excerpt") or f.get("match") or ""
    return "%s\n%s" % (f["label"], tail) if tail else f["label"]


def warn_if_uri_drops(uri, out=None):
    """Say on stderr when a SARIF uri GitHub cannot resolve is about to ship.

    The upload succeeds and the results vanish, which is the failure build()'s
    docstring names. A path relative to the repo root is the only shape GitHub
    resolves to a file in the checkout, so an absolute path, the `stdin`
    placeholder, or an empty value is warned about rather than silently lost.
    The uri is not changed: the caller decides whether to fix it or ship the
    report anyway."""
    if out is None:
        out = sys.stderr
    if not uri or uri == "stdin" or os.path.isabs(uri):
        print("rabbit-writes: SARIF uri %r will be dropped by GitHub. It has "
              "to be a path relative to the repo root, and an absolute path or "
              "the stdin placeholder is not. Pass --sarif-uri one." % uri,
              file=out)


def build(findings, uri, tool_name, tool_version=None, information_uri=None,
          extra_properties=None, notes=None):
    """A SARIF log for one file's findings.

    `uri` must be relative to the repository root. GitHub silently drops results
    whose artifact location it cannot resolve to a file in the checkout, and
    "silently" is the operative word: the upload succeeds and nothing appears.
    """
    # A rule's default level is the worst priority anything under that id
    # reached in this document, not whichever one happened to come first.
    # `hidden-unicode` is P0 for a zero-width character and P2 for a run of
    # non-breaking spaces, and a document with both used to declare the rule
    # whichever the iteration order handed over. Per-result levels below are
    # computed per finding and were always right.
    # The label travels with it. Taking the level from the worst finding and the
    # description from whichever came first is how a rule ends up declaring
    # `error` under the heading "Hidden unicode: non-breaking space".
    worst = {}
    for f in findings:
        rank = findings_mod.PRIORITY_RANK.get(f["priority"],
                                              len(findings_mod.PRIORITY_RANK))
        if f["id"] not in worst or rank < worst[f["id"]][0]:
            worst[f["id"]] = (rank, f["priority"], f["label"])

    rules, rule_index = [], {}
    for f in findings:
        if f["id"] in rule_index:
            continue
        rule_index[f["id"]] = len(rules)
        _, priority, label = worst[f["id"]]
        rules.append({
            "id": f["id"],
            "name": f["id"],
            "shortDescription": {"text": label},
            "fullDescription": {"text": BAND_DESCRIPTIONS.get(f["band"], "")},
            "defaultConfiguration": {
                "level": LEVEL_BY_PRIORITY.get(priority, "note")},
            "properties": {"band": f["band"], "priority": priority,
                           "tags": [f["band"]]},
        })

    results = []
    is_docx = uri.lower().endswith((".docx", ".docm", ".dotx", ".dotm"))
    for f in findings:
        loc = {"artifactLocation": {"uri": uri}}
        if not is_docx:
            loc["region"] = {"startLine": max(1, int(f["line"]))}

        res = {
            "ruleId": f["id"],
            "ruleIndex": rule_index[f["id"]],
            "level": LEVEL_BY_PRIORITY.get(f["priority"], "note"),
            "message": {"text": _message(f)},
            "locations": [{
                "physicalLocation": loc,
            }],
            "properties": {"band": f["band"], "priority": f["priority"]},
        }
        if "suppressed" in f:
            # `inSource`, not `external`. A rabbit-allow comment is persisted
            # in the file the result points at, which is exactly what SARIF
            # 2.1.0 means by the two kinds. `external` would tell a consumer to
            # look for a suppression store that does not exist.
            res["suppressions"] = [{
                "kind": "inSource",
                "justification": str(f["suppressed"])
            }]
        results.append(res)

    driver = {"name": tool_name, "rules": rules,
              "properties": {"findingSchemaVersion": findings_mod.SCHEMA_VERSION}}
    if tool_version:
        driver["version"] = str(tool_version)
    if information_uri:
        driver["informationUri"] = information_uri
    if extra_properties:
        driver["properties"].update(extra_properties)

    run = {"tool": {"driver": driver}, "results": results}
    if notes:
        notifications = [{"message": {"text": n}} for n in notes]
        run["invocations"] = [{"executionSuccessful": True,
                               "toolExecutionNotifications": notifications}]

    return {"$schema": SARIF_SCHEMA, "version": SARIF_VERSION, "runs": [run]}
