#!/usr/bin/env python3
"""Static and offline checks for the UCP Gateway skill bundle."""

import io
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path.cwd()
TARGET_VERSION = "0.2.3"
EXPECTED_SOURCE = "https://github.com/theagenttimes/ucp-gateway-skill"
EXPECTED_HOMEPAGE = "https://ucpgateway.theagenttimes.com/"
EXPECTED_CATEGORY = "mcp-tools"
TOOL_NAMES = [
    "register_ucp_profile",
    "get_ucp_profile",
    "shopping_product_search",
    "shopping_product_get",
    "shopping_cart_create",
    "shopping_cart_get",
    "shopping_cart_update",
    "shopping_cart_cancel",
    "shopping_checkout_create",
    "shopping_checkout_get",
    "shopping_checkout_update",
    "shopping_checkout_cancel",
]
OLD_ALIASES = [
    "shopping_search_products",
    "shopping_get_product",
    "shopping_create_cart",
    "shopping_get_cart",
    "shopping_update_cart",
    "shopping_cancel_cart",
    "shopping_create_checkout",
    "shopping_get_checkout",
    "shopping_update_checkout",
    "shopping_cancel_checkout",
]
EXPECTED_SCRIPTS = {
    "init": "python3 scripts/init_ucpgateway.py",
    "register": "python3 scripts/register_profile.py",
    "call": "python3 scripts/call_mcp.py",
    "check": "python3 scripts/check_skill.py && python3 scripts/init_ucpgateway.py --dry-run && python3 scripts/call_mcp.py --help",
}
EXPECTED_BIN = {
    "ucpgateway-init": "./scripts/init_ucpgateway.py",
    "ucpgateway-register": "./scripts/register_profile.py",
    "ucpgateway-call": "./scripts/call_mcp.py",
}
PRIVATE_FIELDS = {"d", "p", "q", "dp", "dq", "qi", "k"}
ERRORS = []


def fail(message):
    ERRORS.append(message)


def read_text(path):
    return path.read_text(encoding="utf-8")


def check_frontmatter(skill):
    match = re.match(r"^---\n([\s\S]*?)\n---\n", skill)
    if not match:
        fail("SKILL.md missing YAML frontmatter")
        return
    frontmatter = match.group(1)
    lines = [line.strip() for line in frontmatter.splitlines() if line.strip()]
    keys = [line.split(":", 1)[0] for line in lines]
    for required in ("name", "version", "description", "tags", "metadata"):
        if required not in keys:
            fail(f"frontmatter missing {required}")
    extra = [key for key in keys if key not in {"name", "version", "description", "tags", "metadata"}]
    if extra:
        fail(f"frontmatter contains unsupported keys: {', '.join(extra)}")
    if f"version: {TARGET_VERSION}" not in lines:
        fail(f"frontmatter version must be {TARGET_VERSION}")
    tag_lines = [line for line in lines if line.startswith("tags:")]
    if len(tag_lines) != 1:
        fail("frontmatter must contain one tags line")
    else:
        tags_text = tag_lines[0].split(":", 1)[1]
        for required_tag in ("mcp", "shopping", "ucp"):
            if required_tag not in tags_text:
                fail(f"frontmatter tags must include {required_tag}")
    if re.search(r"\balways\b", frontmatter, flags=re.IGNORECASE):
        fail("frontmatter must not contain always")
    metadata_lines = [line for line in lines if line.startswith("metadata:")]
    if len(metadata_lines) != 1:
        fail("frontmatter must contain one metadata line")
        return
    try:
        metadata = json.loads(metadata_lines[0].split(":", 1)[1].strip())
    except json.JSONDecodeError as exc:
        fail(f"frontmatter metadata must be single-line JSON: {exc.msg}")
        return
    openclaw = metadata.get("openclaw") if isinstance(metadata, dict) else None
    if not isinstance(openclaw, dict):
        fail("frontmatter metadata.openclaw must be an object")
        return
    allowed_openclaw = {"emoji", "category", "homepage", "source", "requires", "paths"}
    extra_openclaw = sorted(set(openclaw) - allowed_openclaw)
    if extra_openclaw:
        fail(f"frontmatter metadata.openclaw has unsupported keys: {', '.join(extra_openclaw)}")
    if openclaw.get("category") != EXPECTED_CATEGORY:
        fail(f"frontmatter metadata.openclaw.category must be {EXPECTED_CATEGORY}")
    if openclaw.get("homepage") != EXPECTED_HOMEPAGE:
        fail(f"frontmatter metadata.openclaw.homepage must be {EXPECTED_HOMEPAGE}")
    if openclaw.get("source") != EXPECTED_SOURCE:
        fail(f"frontmatter metadata.openclaw.source must be {EXPECTED_SOURCE}")
    requires = openclaw.get("requires")
    if requires is not None:
        if not isinstance(requires, dict):
            fail("frontmatter metadata.openclaw.requires must be an object when present")
            return
        allowed_requires = {"bins", "tools", "env", "optionalEnv", "paths"}
        extra_requires = sorted(set(requires) - allowed_requires)
        if extra_requires:
            fail(f"frontmatter metadata.openclaw.requires has unsupported keys: {', '.join(extra_requires)}")
        bins = requires.get("bins")
        if bins not in (None, ["python3"]):
            fail("frontmatter metadata.openclaw.requires.bins may only require ['python3']")
        tools = requires.get("tools")
        if tools not in (None, []):
            fail("frontmatter metadata.openclaw.requires.tools must be [] when present")
        env = requires.get("env")
        if env not in (None, []):
            fail("frontmatter metadata.openclaw.requires.env must be [] when present")
        paths = requires.get("paths")
        if paths not in (None, ["./.ucpgateway/"]):
            fail("frontmatter metadata.openclaw.requires.paths must be ['./.ucpgateway/'] when present")
    paths = openclaw.get("paths")
    if paths != ["./.ucpgateway/"]:
        fail("frontmatter metadata.openclaw.paths must be ['./.ucpgateway/']")


def check_skill_text(skill):
    for name in TOOL_NAMES:
        if name not in skill:
            fail(f"SKILL.md missing tool name {name}")
    if re.search(r"shopify_", skill, flags=re.IGNORECASE):
        fail("SKILL.md must not contain provider-specific aliases")
    for alias in OLD_ALIASES:
        if alias in skill:
            fail(f"SKILL.md must not contain removed alias {alias}")


def check_package(pkg):
    if pkg.get("version") != TARGET_VERSION:
        fail(f"package.json version must be {TARGET_VERSION}")
    if pkg.get("homepage") != EXPECTED_HOMEPAGE:
        fail(f"package.json homepage must be {EXPECTED_HOMEPAGE}")
    repository = pkg.get("repository") or {}
    if repository.get("url") != "git+" + EXPECTED_SOURCE + ".git":
        fail("package.json repository.url must point to the GitHub source repository")
    keywords = pkg.get("keywords") or []
    for keyword in ("mcp-tools", "mcp", "ucp", "shopping"):
        if keyword not in keywords:
            fail(f"package.json keywords must include {keyword}")
    if pkg.get("type") == "module":
        fail("package.json should not declare ESM module mode after the Python rewrite")
    scripts = pkg.get("scripts") or {}
    for name, expected in EXPECTED_SCRIPTS.items():
        if scripts.get(name) != expected:
            fail(f"package.json scripts.{name} must be {expected!r}")
    for name, command in scripts.items():
        if "node" in command.split():
            fail(f"package.json scripts.{name} must not invoke the Node runtime")
    bins = pkg.get("bin") or {}
    if bins != EXPECTED_BIN:
        fail("package.json bin entries must point to the Python helper scripts")
    for target in bins.values():
        target_path = ROOT / target.lstrip("./")
        if target_path.suffix != ".py":
            fail(f"bin target {target} must be a Python script")
            continue
        if not target_path.exists():
            fail(f"bin target {target} does not exist")
            continue
        first_line = read_text(target_path).splitlines()[0] if read_text(target_path).splitlines() else ""
        if first_line != "#!/usr/bin/env python3":
            fail(f"bin target {target} must start with a python3 shebang")
        if os.name == "posix" and not os.access(target_path, os.X_OK):
            fail(f"bin target {target} should be executable")


def check_python_scripts():
    scripts_dir = ROOT / "scripts"
    legacy_suffix = "." + "mjs"
    legacy_files = sorted(path.name for path in scripts_dir.iterdir() if path.suffix == legacy_suffix)
    if legacy_files:
        fail(f"legacy helper scripts remain in scripts/: {', '.join(legacy_files)}")
    expected = {"init_ucpgateway.py", "register_profile.py", "call_mcp.py", "check_skill.py"}
    actual = {path.name for path in scripts_dir.glob("*.py")}
    missing = sorted(expected - actual)
    if missing:
        fail(f"missing Python helper script(s): {', '.join(missing)}")
    for path in sorted(scripts_dir.glob("*.py")):
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as exc:
            fail(f"{path.relative_to(ROOT)} does not compile: {exc.msg}")
    # Python bytecode caches must never ship in the ClawHub/npm tarball.
    if (scripts_dir / "__pycache__").exists():
        fail("scripts/__pycache__ exists; remove it so it is not packaged")
    stray_bytecode = sorted(
        path.name
        for path in scripts_dir.rglob("*")
        if path.suffix in {".pyc", ".pyo"}
    )
    if stray_bytecode:
        fail(f"compiled Python bytecode must not ship: {', '.join(stray_bytecode)}")


def check_version_fallback():
    register_script = read_text(ROOT / "scripts" / "register_profile.py")
    match = re.search(r'PACKAGE_VERSION\s*=\s*"([^"]+)"', register_script)
    if not match:
        fail("register_profile.py missing PACKAGE_VERSION fallback")
    elif match.group(1) != TARGET_VERSION:
        fail(f"register_profile.py fallback {match.group(1)} does not match package version {TARGET_VERSION}")


def check_examples():
    examples_dir = ROOT / "examples"
    for path in sorted(examples_dir.iterdir()):
        if not (path.name.endswith(".json") or path.name.endswith(".json.example")):
            continue
        try:
            json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            fail(f"examples/{path.name} is not valid JSON: {exc.msg}")


def check_skill_card():
    card_path = ROOT / "skill-card.md"
    if not card_path.exists():
        fail("skill-card.md must be included for ClawHub verification")
        return
    card = read_text(card_path)
    for required in ("Description:", "Use Case:", "Known Risks and Mitigations:", "Skill Output:", "Skill Version(s):"):
        if required not in card:
            fail(f"skill-card.md missing {required}")


def check_no_stale_runtime_refs():
    legacy_token = "." + "mjs"
    old_command_token = "node " + "scripts/"
    targets = [ROOT / "package.json", ROOT / "README.md", ROOT / "SKILL.md"]
    targets.extend(sorted((ROOT / "scripts").glob("*.py")))
    targets.extend(sorted((ROOT / "examples").iterdir()))
    for path in targets:
        if not path.is_file():
            continue
        text = read_text(path)
        if legacy_token in text:
            fail(f"{path.relative_to(ROOT)} contains a stale legacy script extension reference")
        if old_command_token in text:
            fail(f"{path.relative_to(ROOT)} contains a stale Node helper command")


def assert_file_mode(path, expected_mode):
    if os.name != "posix":
        return
    actual = stat.S_IMODE(path.stat().st_mode)
    if actual != expected_mode:
        fail(f"{path.name} mode {oct(actual)} should be {oct(expected_mode)}")


def check_init_tempdir_behaviour():
    try:
        import init_ucpgateway as init_script
    except Exception as exc:  # noqa: BLE001 - report concise check failure
        fail(f"could not import init_ucpgateway.py for offline tests: {exc}")
        return

    try:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            out = io.StringIO()
            err = io.StringIO()
            init_script.run(["--dry-run"], cwd=temp_root, stdout=out, stderr=err)
            if (temp_root / ".ucpgateway").exists():
                fail("init dry-run must not create ./.ucpgateway")

            init_script.run([], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            state_dir = temp_root / ".ucpgateway"
            private_path = state_dir / "private_key.jwk"
            public_path = state_dir / "public_key.jwk"
            if not private_path.exists() or not public_path.exists():
                fail("init must create private_key.jwk and public_key.jwk when both are missing")
                return
            assert_file_mode(private_path, 0o600)
            assert_file_mode(public_path, 0o644)
            private_jwk = json.loads(private_path.read_text(encoding="utf-8"))
            public_jwk = json.loads(public_path.read_text(encoding="utf-8"))
            if PRIVATE_FIELDS.intersection(public_jwk):
                fail("public_key.jwk must not contain private JWK fields")
            derived_public = init_script.derive_public_from_private(private_jwk)
            if init_script.validate_public_jwk(public_jwk) != init_script.validate_public_jwk(derived_public):
                fail("generated public_key.jwk must match private_key.jwk")

            public_path.unlink()
            init_script.run([], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            if not public_path.exists():
                fail("private-only state must derive public_key.jwk")

            private_path.unlink()
            try:
                init_script.run([], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            except init_script.UcpInitError:
                pass
            else:
                fail("public-only state must fail unless --public-only is supplied")
            init_script.run(["--public-only"], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            init_script.run([], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            state_dir = temp_root / ".ucpgateway"
            public_path = state_dir / "public_key.jwk"
            _, other_public = init_script.generate_keypair()
            init_script.write_json(public_path, other_public, 0o644)
            try:
                init_script.run([], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            except init_script.UcpInitError:
                pass
            else:
                fail("mismatched private/public key files must fail")

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            init_script.run([], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            private_path = temp_root / ".ucpgateway" / "private_key.jwk"
            before = json.loads(private_path.read_text(encoding="utf-8"))["d"]
            init_script.run(["--force-rotate"], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            after = json.loads(private_path.read_text(encoding="utf-8"))["d"]
            if before == after:
                fail("--force-rotate must replace the private key")

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            init_script.run(["--legacy-draft"], cwd=temp_root, stdout=io.StringIO(), stderr=io.StringIO())
            draft = json.loads((temp_root / ".ucpgateway" / "profile.draft.json").read_text(encoding="utf-8"))
            signing_key = draft["signing_keys"][0]
            if PRIVATE_FIELDS.intersection(signing_key):
                fail("profile.draft.json signing key must not contain private fields")
    except Exception as exc:  # noqa: BLE001 - continue with concise validation failure
        fail(f"init_ucpgateway.py offline behaviour test failed: {exc}")


def check_call_mcp_tool_descriptor_filter():
    try:
        import call_mcp as call_script
    except Exception as exc:  # noqa: BLE001 - report concise check failure
        fail(f"could not import call_mcp.py for offline tests: {exc}")
        return

    sample_tools = [
        {
            "name": "shopping_product_search",
            "description": "Search the product catalog through The Agent Times UCP Gateway.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string", "description": "Registered UCP Gateway UUID."},
                    "query": {"type": "string", "description": "Natural-language product search query."},
                },
                "required": ["agent_id", "query"],
            },
        },
        {"name": "shopping_cart_create", "description": "Create a merchant cart.", "inputSchema": {"type": "object"}},
        {"name": "shopping_checkout_create", "description": "Create a merchant checkout handoff URL.", "inputSchema": {"type": "object"}},
    ]

    original_post_json = call_script.post_json

    def fake_post_json(url, payload, timeout=60):  # noqa: ARG001 - signature mirrors helper
        if payload.get("method") != "tools/list":
            raise AssertionError("descriptor filter must discover schemas through tools/list")
        return {"jsonrpc": "2.0", "id": payload.get("id"), "result": {"tools": sample_tools}}, 200

    try:
        call_script.post_json = fake_post_json
        out = io.StringIO()
        code = call_script.run(["--tool", "shopping_product_search"], cwd=ROOT, stdout=out, stderr=io.StringIO())
        if code != 0:
            fail("call_mcp.py --tool shopping_product_search should succeed with tools/list data")
            return
        filtered = json.loads(out.getvalue())
        if filtered.get("source") != "tools/list":
            fail("call_mcp.py --tool output must identify tools/list as descriptor source")
        tools = filtered.get("tools") or []
        if len(tools) != 1 or tools[0].get("name") != "shopping_product_search":
            fail("call_mcp.py --tool must print only the requested tool descriptor")
        query_description = (((tools[0].get("inputSchema") or {}).get("properties") or {}).get("query") or {}).get("description")
        if "Natural-language" not in (query_description or ""):
            fail("call_mcp.py --tool must preserve query field descriptions from tools/list")

        out = io.StringIO()
        code = call_script.run(["--shopping-tools"], cwd=ROOT, stdout=out, stderr=io.StringIO())
        if code != 0:
            fail("call_mcp.py --shopping-tools should succeed with tools/list data")
            return
        filtered = json.loads(out.getvalue())
        names = [tool.get("name") for tool in filtered.get("tools") or []]
        if names != ["shopping_product_search", "shopping_cart_create", "shopping_checkout_create"]:
            fail("call_mcp.py --shopping-tools must print search, cart-create, and checkout-create descriptors in order")
    except Exception as exc:  # noqa: BLE001 - continue with concise validation failure
        fail(f"call_mcp.py descriptor filter offline test failed: {exc}")
    finally:
        call_script.post_json = original_post_json


def main():
    try:
        skill = read_text(ROOT / "SKILL.md")
        pkg = json.loads(read_text(ROOT / "package.json"))
    except Exception as exc:  # noqa: BLE001 - concise validation failure
        print(f"check-skill: {exc}", file=sys.stderr)
        return 1

    check_frontmatter(skill)
    check_skill_text(skill)
    check_package(pkg)
    check_python_scripts()
    check_version_fallback()
    check_examples()
    check_skill_card()
    check_no_stale_runtime_refs()
    check_init_tempdir_behaviour()
    check_call_mcp_tool_descriptor_filter()

    if ERRORS:
        for message in ERRORS:
            print(f"check-skill: {message}", file=sys.stderr)
        return 1
    print(f"check-skill: ok ({pkg.get('name')}@{pkg.get('version')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
