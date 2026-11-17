"""Request execution inside FreeCAD.

``execute`` is the in-process API; ``main_from_env`` is the entry point the
launcher runs inside FreeCADCmd (request/response passed through files).
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import __version__, audit, catalog, errors, validate, workspace
from .errors import SkillError


def _freecad_version() -> str:
    import FreeCAD as App

    v = App.Version()
    return ".".join(v[:3]) if len(v) >= 3 else str(v)


def _step_entry(step: Dict[str, Any], outcome: Any, warnings: List[str]) -> Dict[str, Any]:
    from . import geometry

    entry: Dict[str, Any] = {"index": step["index"], "op": step["op"]}
    obj = outcome
    data = None
    if isinstance(outcome, dict):
        obj = outcome.get("object")
        data = outcome.get("data")
    if obj is not None and hasattr(obj, "Name"):
        entry["object"] = obj.Name
        if geometry.is_part_shape(obj) and step["op"] not in ("inspect", "check"):
            s = geometry.summary(obj.Shape, validity=False)
            entry.update({k: s[k] for k in ("volume", "bbox", "solids") if k in s})
    if data is not None:
        # export details are reported once, in the top-level "exports"
        entry["data"] = {"file": data["file"]} if step["op"] == "export" else data
    if warnings:
        entry["warnings"] = list(warnings)
    return entry


def execute(request: Any, root: Path) -> Dict[str, Any]:
    """Validate and run a request; never raises."""
    base: Dict[str, Any] = {"engine": __version__}
    try:
        req = validate.validate_request(request)
    except SkillError as e:
        return errors.error_response(e, **base)

    try:
        return _run(req, Path(root), base)
    except SkillError as e:  # errors outside steps (opening, saving)
        return errors.error_response(e, **base)
    except Exception as e:
        return errors.error_response(
            SkillError(errors.INTERNAL, f"Internal error: {e}", details={"traceback": traceback.format_exc()[-2000:]}),
            **base,
        )


def _run(req: Dict[str, Any], root: Path, base: Dict[str, Any]) -> Dict[str, Any]:
    import FreeCAD as App

    from . import compat, document
    from .ops import HANDLERS

    base["freecad"] = _freecad_version()
    compat.check_version(App.Version())
    doc_path = workspace.resolve(root, req["doc"])
    base["doc"] = workspace.relative(root, doc_path)
    from . import guidata

    gui_before = guidata.capture(doc_path) if doc_path.exists() and not req["new"] else None
    doc = document.open_document(doc_path, req["new"])
    ctx = document.Context(doc, root, doc_path)
    ctx.gui_before = gui_before
    # A request that only reads (inspect, measure, export...) changes no shape: it needs neither the
    # fingerprints nor a second validity check of results that were checked when they were made.
    ctx.read_only = not req["new"] and not any(catalog.OPS_BY_NAME[st["op"]].mutates for st in req["steps"])
    shapes_before = {} if ctx.read_only else audit.fingerprints(doc)
    ctx.shapes_before = shapes_before
    if req["new"]:
        ctx.mutated = True  # an explicit reset is saved even without other changes

    done: List[Dict[str, Any]] = []
    try:
        for step in req["steps"]:
            ctx.step = step["index"]
            ctx.step_warnings = []
            try:
                mutating = catalog.OPS_BY_NAME[step["op"]].mutates
                before = _intermediates(doc) if mutating and step["op"] in ORPHAN_CHECK_OPS else None
                audit_before = audit.snapshot(doc) if step["op"] in audit.EDIT_OPS else None
                outcome = HANDLERS[step["op"]](ctx, step["params"])
                if mutating:
                    ctx.mutated = True
                if before is not None:
                    _warn_orphans(ctx, before)
                if audit_before is not None:
                    audit.compare(ctx, audit_before)
                if "expect" in step:
                    _check_step_expect(step, outcome)
            except SkillError as e:
                err = e.to_dict()
                err.update({"step": step["index"], "op": step["op"]})
                return {
                    "status": "error",
                    **base,
                    "saved": False,
                    "error": err,
                    "completed_steps": done,
                    **({"warnings": ctx.warnings} if ctx.warnings else {}),
                    "note": "Nothing was saved or exported; the document on disk is unchanged.",
                }
            except Exception as e:
                err = {
                    "code": errors.INTERNAL,
                    "message": f"{type(e).__name__}: {e}",
                    "step": step["index"],
                    "op": step["op"],
                    "details": {"traceback": traceback.format_exc()[-2000:]},
                }
                return {
                    "status": "error",
                    **base,
                    "saved": False,
                    "error": err,
                    "completed_steps": done,
                    **({"warnings": ctx.warnings} if ctx.warnings else {}),
                    "note": "Nothing was saved or exported; the document on disk is unchanged.",
                }
            done.append(_step_entry(step, outcome, ctx.step_warnings))

        try:
            audit.final_check(doc)
            if ctx.mutated:
                ctx.step = None  # a whole-document warning, not tied to one step
                audit.overlapping_results(ctx, shapes_before)
        except SkillError as e:
            return {
                "status": "error",
                **base,
                "saved": False,
                "error": e.to_dict(),
                "completed_steps": done,
                **({"warnings": ctx.warnings} if ctx.warnings else {}),
                "note": "Nothing was saved or exported; the document on disk is unchanged.",
            }

        return _finish(ctx, req, done, base)
    finally:
        for pe in ctx.pending_exports:
            if pe["tmp"].exists():
                try:
                    os.remove(pe["tmp"])
                except OSError:
                    pass
        document.close_document(doc)


# Edits that can disconnect a tool from the feature that consumed it. ('delete'
# is excluded: exposing the inputs of a deleted feature is the intended effect.)
ORPHAN_CHECK_OPS = ("set",)


def _intermediates(doc: Any) -> set:
    from . import document

    return {o.Name for o in document.visible_objects(doc) if document.role(o) == "intermediate"}


def _warn_orphans(ctx: Any, before: set) -> None:
    from . import document, geometry

    for name in sorted(before):
        o = ctx.doc.getObject(name)
        if o is not None and document.role(o) == "result" and geometry.is_part_shape(o) and not o.Shape.isNull():
            ctx.warn(
                "ORPHANED",
                f"'{name}' is no longer used by any feature and is now a result: it will be shown and "
                "exported with the model. Delete it if it was only a tool.",
            )


def _check_step_expect(step: Dict[str, Any], outcome: Any) -> None:
    from . import geometry

    obj = outcome.get("object") if isinstance(outcome, dict) else outcome
    if obj is None or not geometry.is_part_shape(obj):
        raise SkillError(errors.INVALID_PARAM, "'expect' needs a step that produces or modifies a shape")
    failures = geometry.check_expectations(obj.Shape, step["expect"])
    if failures:
        raise SkillError(
            errors.EXPECTATION_FAILED,
            f"'{obj.Name}' does not meet the step's expectations",
            hint="The operation ran, but the geometry differs from what you expected. Compare expected vs actual.",
            details={"failures": failures, "actual_bbox": geometry.bbox(obj.Shape)},
        )


def _finish(ctx: Any, req: Dict[str, Any], done: List[Dict[str, Any]], base: Dict[str, Any]) -> Dict[str, Any]:
    from . import document

    doc = ctx.doc
    objs = document.visible_objects(doc)
    result_objs = [o for o in objs if document.role(o) == "result"]
    read_only = bool(getattr(ctx, "read_only", False)) and not ctx.mutated
    results = [document.object_entry(o, validity=not read_only) for o in result_objs]
    if not read_only:
        _quality_gate(ctx, result_objs, results)
    intermediates = [o.Name for o in objs if document.role(o) == "intermediate"]

    # Final integrity pass over results.
    for r in results:
        if r.get("valid") is False:
            ctx.warnings.append(
                {"step": None, "code": "INVALID_RESULT", "message": f"{r['name']} has invalid geometry"}
            )

    files: List[str] = []
    saved = False
    exports: List[Dict[str, Any]] = []
    if not req["dry_run"]:
        if ctx.mutated:
            shown = document.apply_visibility(doc)
            document.save_document(
                doc, ctx.doc_path, {"captured": ctx.gui_before, "visibility": shown, "changed": ctx.appearance_changed}
            )
            saved = True
            files.append(base["doc"])
        for pe in ctx.pending_exports:
            os.replace(pe["tmp"], pe["dest"])
            exports.append(pe["record"])
            files.append(pe["record"]["file"])
    else:
        exports = [dict(pe["record"], dry_run=True) for pe in ctx.pending_exports]

    if req.get("brief"):  # long requests: keep what needs attention, drop the per-step geometry
        done = [{k: v for k, v in d.items() if k not in ("volume", "bbox", "solids")} for d in done]
    resp: Dict[str, Any] = {"status": "success", **base, "saved": saved, "steps": done, "results": results}
    if intermediates:
        resp["intermediates"] = intermediates
    if exports:
        resp["exports"] = exports
    if ctx.warnings:
        resp["warnings"] = ctx.warnings
    if files:
        resp["files_written"] = files
    if req["dry_run"]:
        resp["note"] = "dry_run: nothing was saved or exported"
    return resp


def _quality_gate(ctx: Any, objs: List[Any], entries: List[Dict[str, Any]]) -> None:
    """Checks that isValid() does not cover, on the results this request created or changed.

    A solid that passes through itself (a sweep thicker than its path's bends, a coil thicker than its
    pitch) is "valid" for OCC, but its volume is wrong and later booleans break on it."""
    from . import geometry

    before = getattr(ctx, "shapes_before", {})
    for obj, entry in zip(objs, entries):
        if not geometry.is_part_shape(obj) or obj.Shape.isNull() or not obj.Shape.Solids:
            continue
        if obj.Name in before and audit._same(before[obj.Name], audit._fingerprint(obj)):
            continue  # unchanged by this request: it was checked when it was made
        verdict, reason = geometry.self_check(obj.Shape)
        code = "SELF_INTERSECTION" if verdict else "SELF_INTERSECTION_UNCHECKED"
        told = any(w["code"] == code and f"'{obj.Name}'" in w["message"] for w in ctx.warnings)
        if verdict is None:
            # Not established is never reported as clean: the result says so, and so does a warning.
            entry["self_intersection_check"] = f"not checked ({reason})"
            if not told:  # else already reported by the export that wrote it
                ctx.warnings.append(
                    {
                        "step": None,
                        "code": code,
                        "message": f"'{obj.Name}' was not checked for passing through itself ({reason}), so its "
                        'volume and mass are unconfirmed. Add expect {"self_intersecting": false} to a step to '
                        "require a confirmed result.",
                    }
                )
        elif verdict and told:
            entry["self_intersecting"] = True
        elif verdict:
            entry["self_intersecting"] = True
            ctx.warnings.append(
                {
                    "step": None,
                    "code": "SELF_INTERSECTION",
                    "message": f"'{obj.Name}' passes through itself: its volume and mass are wrong, and booleans, "
                    "meshing and other CAD systems may fail on it. Typical causes: a sweep profile wider than the "
                    "path's bend radius or a helix pitch, or a shell thicker than a concave radius. Reduce the "
                    "profile, enlarge the bend radius or pitch, then check again.",
                }
            )


# ------------------------------------------------------------------ subprocess entry


def _write_json_atomic(path: Path, data: Dict[str, Any]) -> None:
    tmp = path.with_name(path.name + ".part")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    os.replace(tmp, path)


def main_from_files(request_file: str, response_file: str, workspace_root: str) -> None:
    """Entry point inside FreeCADCmd: read the request file, write the response file."""
    req_path, resp_path, root = Path(request_file), Path(response_file), Path(workspace_root)
    resp: Optional[Dict[str, Any]] = None
    try:
        with open(req_path, encoding="utf-8") as fh:
            request = json.load(fh)
        resp = execute(request, root)
    except Exception as e:
        resp = errors.error_response(
            SkillError(errors.INTERNAL, f"Engine failure: {e}", details={"traceback": traceback.format_exc()[-2000:]})
        )
    _write_json_atomic(resp_path, resp)
    sys.stdout.flush()
