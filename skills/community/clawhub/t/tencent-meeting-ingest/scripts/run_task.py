import argparse
import sys
from pathlib import Path

from meeting_kb_writer import apply_pages, validate_page_manifest
from meeting_reader import delete_prepare_context_cache, expected_page_output, load_cached_prepare_context, prepare_context, save_prepare_context_cache
from task_io import print_json, read_payload, write_result
from utils import read_json_file, write_json_file


def main():
    parser = argparse.ArgumentParser(description="Research KB Tencent Meeting ingest helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Fetch Tencent Meeting recording/minutes materials through tencent-meeting-skill and build OpenClaw context")
    prepare.add_argument("--input", required=True, help="Backend payload JSON path")
    prepare.add_argument("--context-output", help="Where to write the generated context JSON")
    prepare.add_argument("--result-output", help="Optional result JSON path when there is nothing new to process")

    validate = subparsers.add_parser("validate-manifest", help="Validate the Tencent Meeting Markdown drafts and compact page manifest without writing Gitea")
    validate.add_argument("--input", required=True, help="Backend payload JSON path")
    validate.add_argument("--context", required=True, help="Context JSON produced by the prepare command")
    validate.add_argument("--manifest", help="Compact page manifest JSON path; defaults to context.pageOutput.manifestPath")
    validate.add_argument("--draft-dir", help="Markdown draft root; defaults to context.pageOutput.draftDir")

    apply = subparsers.add_parser("apply", help="Write OpenClaw-generated Tencent Meeting Markdown drafts to the Gitea KB")
    apply.add_argument("--input", required=True, help="Backend payload JSON path")
    source = apply.add_mutually_exclusive_group()
    source.add_argument("--manifest", help="Compact page manifest JSON path; defaults to context.pageOutput.manifestPath")
    source.add_argument("--pages", help="Legacy OpenClaw-generated pages JSON path")
    apply.add_argument("--draft-dir", help="Markdown draft root; defaults to context.pageOutput.draftDir")
    apply.add_argument("--context", required=True, help="Context JSON produced by the prepare command")
    apply.add_argument("--result-output", help="Where to write the backend result JSON")

    args = parser.parse_args()
    if args.command == "prepare":
        run_prepare(args)
    elif args.command == "validate-manifest":
        run_validate_manifest(args)
    elif args.command == "apply":
        run_apply(args)


def run_prepare(args):
    payload = read_payload(args.input)
    try:
        context = load_cached_prepare_context(payload)
        if context is None:
            context = prepare_context(payload)
            save_prepare_context_cache(payload, context)
        if args.context_output:
            write_json_file(args.context_output, context)
        if context.get("mode") == "skip":
            errors = context.get("errors") or []
            success = not errors
            skipped = context.get("skippedSources") or ([{"reason": "no_new_tencent_meeting_content"}] if success else [{"reason": "platform_fetch_failed"}])
            result = {
                "success": success,
                "processedSources": [],
                "createdPages": [],
                "updatedPages": [],
                "archivedFiles": context.get("archivedFiles") or [],
                "skippedSources": skipped,
                "incompleteItems": context.get("incompleteItems") or [],
                "errors": errors,
                "commitId": "",
                "snapshot": context.get("snapshot") or {},
            }
            result_path = args.result_output or payload.get("resultFile")
            if result_path:
                write_result(result_path, result)
            if not success:
                print_json(result)
                sys.exit(1)
        print_json(context)
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
        sys.exit(1)


def run_validate_manifest(args):
    payload = read_payload(args.input)
    try:
        context = read_json_file(args.context)
        manifest_path, draft_dir = manifest_locations(args, context, payload)
        manifest_doc = read_required_json(manifest_path, "page manifest")
        print_json(validate_page_manifest(manifest_doc, context, draft_dir=draft_dir, require_drafts=True))
    except Exception as exc:
        print_json({"success": False, "validationOnly": True, "errors": [str(exc)]})
        sys.exit(1)


def run_apply(args):
    payload = read_payload(args.input)
    try:
        context = read_json_file(args.context)
        if args.pages:
            pages_doc = read_required_json(args.pages, "legacy pages JSON")
            result = apply_pages(payload, pages_doc, context, require_drafts=False)
        else:
            manifest_path, draft_dir = manifest_locations(args, context, payload)
            manifest_doc = read_required_json(manifest_path, "page manifest")
            result = apply_pages(payload, manifest_doc, context, draft_dir=draft_dir, require_drafts=True)
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            result = write_result(result_path, result)
            delete_prepare_context_cache(payload)
        else:
            result = {"success": True, **result}
        print_json(result)
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
        sys.exit(1)


def manifest_locations(args, context, payload):
    output = context.get("pageOutput") or {}
    manifest_path = getattr(args, "manifest", None) or output.get("manifestPath")
    draft_dir = getattr(args, "draft_dir", None) or output.get("draftDir")
    if not manifest_path:
        raise ValueError("Missing page manifest path; use --manifest or context.pageOutput.manifestPath")
    if not draft_dir:
        raise ValueError("Missing Markdown draft directory; use --draft-dir or context.pageOutput.draftDir")
    expected = expected_page_output(payload)
    if Path(manifest_path).expanduser().resolve() != Path(expected["manifestPath"]).expanduser().resolve():
        raise ValueError("Page manifest path does not match the task-scoped prepare output")
    if Path(draft_dir).expanduser().resolve() != Path(expected["draftDir"]).expanduser().resolve():
        raise ValueError("Markdown draft directory does not match the task-scoped prepare output")
    return manifest_path, draft_dir


def read_required_json(path, label):
    data = read_json_file(path)
    if not data:
        raise ValueError(f"Missing or empty {label}: {path}")
    return data


if __name__ == "__main__":
    main()
