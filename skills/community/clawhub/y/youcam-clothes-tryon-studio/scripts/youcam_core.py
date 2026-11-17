#!/usr/bin/env python3
"""youcam_core.py is the shared CLI that every YouCam (Perfect Corp) skill uses to call the API.

Setup:
    Run the "setup" command first. It creates a local virtual environment and installs
    everything the skill needs.

Auth:
    Set the YOUCAM_API_KEY environment variable, or create a credentials.json file (in the
    skill's root, next to SKILL.md) containing {"api_key": "..."}. The env var is used first
    if both are present. If neither is set, the command & API call fails.

Example:
    python youcam_core.py setup
    python youcam_core.py validate-key
    python youcam_core.py credits
    python youcam_core.py cost --feature skin-analysis
    python youcam_core.py templates --feature look-vto
    python youcam_core.py run --feature skin-analysis --src_file a.jpg \
        --param format=json --param dst_actions='["hd_pore","hd_skin_type"]'
    python youcam_core.py status --feature skin-analysis --task_id <task_id>
"""

import argparse
import json
import sys
from collections.abc import Container
from typing import Any, NoReturn, Optional

from constants import DEFAULT_MAX_POLLS, DEFAULT_POLL_INTERVAL
from youcam_init import exit_with_error, check_dependencies, setup_env

# Flags whose API-issued values can start with "-", which argparse would otherwise read as another option.
_DASH_VALUE_FLAGS = ("--task_id", "--starting_token")


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        exit_with_error(
            "Invalid command-line arguments.",
            hint=f"Run `{self.prog} -h` for the valid flags; API body fields (e.g. dst_actions) "
            "go through --param key=value.",
            details=message,
        )


def _bind_dash_values(argv: list[str]) -> list[str]:
    """Rewrite `--task_id <value>` as `--task_id=<value>` so values like "-9xarr..." still parse."""
    out, i = [], 0
    while i < len(argv):
        if argv[i] in _DASH_VALUE_FLAGS and i + 1 < len(argv):
            out.append(f"{argv[i]}={argv[i + 1]}")
            i += 2
        else:
            out.append(argv[i])
            i += 1
    return out


def _string_fields(body_schema: dict[str, Any]) -> set[str]:
    """Names of the body fields the feature's body_schema declares as type string."""
    props = dict(body_schema.get("properties") or {})
    for variant in body_schema.get("anyOf") or []:
        props.update(variant.get("properties") or {})
    return {k for k, v in props.items() if isinstance(v, dict) and v.get("type") == "string"}


def _parse_params(pairs: Optional[list[str]], string_fields: Container[str] = ()) -> dict[str, Any]:
    """Parse the --param "key=value" strings into a dict.

    Each value is JSON-decoded when possible, so numbers, booleans, and lists (e.g.
    'count=3' or 'tags=["a","b"]') come through as real Python types; anything that
    doesn't parse as JSON is kept as the raw string, unless it starts with "[" or "{",
    which is treated as malformed JSON.

    Fields in string_fields always stay strings, so 'resolution=720' or 'template_id=123'
    is sent as "720"/"123" rather than a number. A JSON-quoted value ('resolution="720"')
    is unquoted.

    Args:
        pairs: A list of "key=value" strings, or None.
        string_fields: Field names the feature's body_schema declares as type string.

    Returns:
        dict[str, Any]: The parsed key/value pairs.
    """
    out = {}
    for p in pairs or []:
        if "=" not in p:
            raise ValueError(f'--param expects "key=value", got "{p}"')
        k, v = p.split("=", 1)
        if k in string_fields:
            try:
                decoded = json.loads(v)
            except json.JSONDecodeError:
                decoded = None
            out[k] = decoded if isinstance(decoded, str) else v
            continue
        try:
            out[k] = json.loads(v)
        except json.JSONDecodeError as exc:
            if v.lstrip().startswith(("[", "{")):
                raise ValueError(f'--param "{k}" looks like JSON but does not parse ({exc}): {v}') from exc
            out[k] = v
    return out


def main() -> None:
    """Parse CLI arguments and dispatch to the matching command.

    Every failure path exits from where it's detected, with a structured {error, hint, details} message.
    """
    parser = _ArgumentParser(description="Run and check YouCam AI features from the command line")
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    subparsers.add_parser(
        "setup",
        help="Create a local .venv and install requirements.txt. "
        "Run this first or whenever a dependency is missing",
    )
    subparsers.add_parser("validate-key", help="Check that the configured API key works")
    subparsers.add_parser("credits", help="Show the remaining API credit units")
    cost_parser = subparsers.add_parser("cost", help="List the credit cost of each feature's pricing tiers")
    cost_parser.add_argument("--feature", help="Only list this feature's tiers; omit to list every feature")

    templates_parser = subparsers.add_parser(
        "templates", help="List a feature's predefined templates; pass a template's id as template_id"
    )
    templates_parser.add_argument("--feature", required=True)
    templates_parser.add_argument(
        "--version", help="Override the version, once the LLM learns of a newer one from the live doc"
    )
    templates_parser.add_argument("--page_size", type=int, default=20, help="Templates per page, 1-20")
    templates_parser.add_argument("--starting_token", help="next_token from the previous page")

    run_parser = subparsers.add_parser("run", help="Run a feature on an image and wait for its result")
    run_parser.add_argument("--feature", required=True)
    run_parser.add_argument("--src_file", help="Local path or URL")
    run_parser.add_argument(
        "--src_files", nargs="+", help="Multiple local paths and/or URLs, e.g. 3 angle photos"
    )
    run_parser.add_argument(
        "--ref_file", help="Local path or URL, e.g. hair-transfer/cloth-v4's reference image"
    )
    run_parser.add_argument("--ref_files", nargs="+", help="Multiple local paths and/or URLs")
    run_parser.add_argument(
        "--param",
        action="append",
        help="An API body field as key=value, repeatable, e.g. --param format=json "
        '--param \'dst_actions=["wrinkle","pore"]\'. Values are JSON-decoded when possible',
    )
    run_parser.add_argument(
        "--version", help="Override the version, once the LLM learns of a newer one from the live doc"
    )
    run_parser.add_argument("--interval", type=float, default=DEFAULT_POLL_INTERVAL)
    run_parser.add_argument("--max_polls", type=int, default=DEFAULT_MAX_POLLS)
    status_parser = subparsers.add_parser(
        "status", help="Check a previously created task's status/result by its task_id"
    )

    status_parser.add_argument("--feature", required=True)
    status_parser.add_argument("--task_id", required=True)
    status_parser.add_argument(
        "--version",
        help="Override the version, once the LLM learns of a newer one from the live doc. \
                          This is only needed if the task was created with a non-default version, \
                          use the same version to check its status.",
    )
    status_parser.add_argument("--interval", type=float, default=DEFAULT_POLL_INTERVAL)
    status_parser.add_argument(
        "--max_polls",
        type=int,
        default=1,
        help="Number of status checks; defaults to 1 (check once instead of blocking until done)",
    )
    args, extras = parser.parse_known_args(_bind_dash_values(sys.argv[1:]))
    if extras:
        # Report leftover flags from the subcommand's parser, so the hint points to e.g. `run -h`.
        subparsers.choices[args.cmd].error(f"unrecognized arguments: {' '.join(extras)}")

    if args.cmd == "setup":
        setup_env()
        return

    check_dependencies()
    # Imported only after the check: these modules need requests/PyYAML, and `setup` must run without them.
    import requests
    from youcam_api import get_credits, get_feature_cost, get_key, list_templates, load_contract
    from youcam_tasks import UploadBatchError, poll, run

    key = get_key()
    try:
        if args.cmd == "validate-key":
            print(json.dumps({"key": "valid", **get_credits(key)}, ensure_ascii=False, indent=2))
        elif args.cmd == "credits":
            print(json.dumps(get_credits(key), ensure_ascii=False, indent=2))
        elif args.cmd == "cost":
            print(json.dumps(get_feature_cost(key, args.feature), ensure_ascii=False, indent=2))

        elif args.cmd == "templates":
            templates = list_templates(key, args.feature, args.version, args.page_size, args.starting_token)
            print(json.dumps(templates, ensure_ascii=False, indent=2))

        elif args.cmd == "run":
            contract = load_contract(args.feature)
            body_schema = contract["features"][args.feature].get("body_schema") or {}
            result = run(
                args.feature,
                src_file=args.src_files or args.src_file,
                ref_file=args.ref_files or args.ref_file,
                params=_parse_params(args.param, _string_fields(body_schema)),
                key=key,
                version=args.version,
                interval=args.interval,
                max_polls=args.max_polls,
                contract=contract,
            )
            _print_task_result(result)

        elif args.cmd == "status":
            contract = load_contract(args.feature)
            result = poll(
                contract, args.feature, args.task_id, key, args.version, args.interval, args.max_polls
            )
            _print_task_result(result)

    except requests.HTTPError as exc:
        exit_with_error(
            f"HTTP error {exc.response.status_code} from the YouCam API.",
            hint="Check the request parameters, feature name, and version against "
            "the guides and documents; see `details` for the raw response body.",
            details=exc.response.text,
        )

    except UploadBatchError as exc:
        exit_with_error(
            "Some uploads failed while resolving src_file/ref_file.",
            hint="Retry with just the failed sources; see `uploaded` for what already succeeded and `failed`"
            " for what needs fixing.",
            uploaded=exc.uploaded,
            failed=exc.failed,
        )

    except Exception as exc:
        exit_with_error(
            type(exc).__name__, hint="See `details` for the underlying error message.", details=str(exc)
        )


def _print_task_result(result: dict) -> None:
    if result.get("task_status") == "error":
        exit_with_error(
            "Task failed.",
            hint="Check the request parameters against the feature's API doc, "
            "see `details` for the API's raw error payload, and visit the YouCam API documentation "
            "(https://docs.perfectcorp.com/develop/error_codes.md) for more info.",
            details=result,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
