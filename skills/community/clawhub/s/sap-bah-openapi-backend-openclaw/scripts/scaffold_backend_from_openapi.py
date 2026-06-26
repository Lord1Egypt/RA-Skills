#!/usr/bin/env python3
"""Scaffold a backend module under src/ from an OpenAPI specification.

Generated module files:
- __init__.py
- tools.py      (generic HTTP wrapper + one function per operation)
- api.py        (FastAPI router exposing one POST endpoint per operation)
- prompts.py    (simple prompt helpers)

This script favors deterministic scaffolding over perfect schema typing.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

HTTP_METHODS = ("get", "post", "put", "patch", "delete")


@dataclass
class Operation:
    fn_name: str
    method: str
    path: str
    summary: str
    operation_id: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold backend module from OpenAPI")
    parser.add_argument("--spec", required=True, help="Path to OpenAPI JSON/YAML file")
    parser.add_argument("--module-id", required=True, help="Numeric module prefix, e.g. 61")
    parser.add_argument("--module-name", required=True, help="Module name, e.g. Warehouse")
    parser.add_argument("--route-prefix", help="FastAPI router prefix; default derived from module-name")
    parser.add_argument("--env-prefix", help="ENV prefix; default derived from module-name")
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]), help="Project root containing src")
    parser.add_argument("--max-operations", type=int, default=30, help="Maximum operations to scaffold")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite module folder if already exists")
    parser.add_argument("--dry-run", action="store_true", help="Print planned output without writing files")
    return parser.parse_args()


def load_spec(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Spec not found: {path}")

    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")

    if suffix == ".json":
        return json.loads(text)

    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise RuntimeError("PyYAML is required for YAML specs. Install with: pip install pyyaml") from exc
        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("YAML OpenAPI file must contain a dictionary at root")
        return loaded

    raise ValueError(f"Unsupported spec extension: {suffix}")


def to_snake(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_").lower() or "operation"


def to_pascal(text: str) -> str:
    # Split camelCase/PascalCase boundaries before normal tokenization.
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    chunks = re.split(r"[^A-Za-z0-9]+", text)
    return "".join(chunk[:1].upper() + chunk[1:] for chunk in chunks if chunk)


def build_operation_id(method: str, path: str, fallback_index: int) -> str:
    parts = [method.lower()]
    for seg in path.strip("/").split("/"):
        if not seg:
            continue
        seg = seg.strip()
        if seg.startswith("{") and seg.endswith("}"):
            parts.append(f"by_{to_snake(seg[1:-1])}")
        else:
            parts.append(to_snake(seg))
    built = "_".join(p for p in parts if p)
    return built or f"operation_{fallback_index}"


def collect_operations(spec: dict[str, Any], max_operations: int) -> list[Operation]:
    paths = spec.get("paths")
    if not isinstance(paths, dict) or not paths:
        raise ValueError("OpenAPI spec has no paths")

    ops: list[Operation] = []
    used_names: set[str] = set()
    idx = 0

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method in HTTP_METHODS:
            op_obj = path_item.get(method)
            if not isinstance(op_obj, dict):
                continue
            idx += 1
            raw_operation_id = op_obj.get("operationId") or build_operation_id(method, path, idx)
            fn_name = to_snake(str(raw_operation_id))
            if fn_name in used_names:
                suffix = 2
                while f"{fn_name}_{suffix}" in used_names:
                    suffix += 1
                fn_name = f"{fn_name}_{suffix}"

            used_names.add(fn_name)
            summary = str(op_obj.get("summary") or op_obj.get("description") or f"{method.upper()} {path}")
            ops.append(
                Operation(
                    fn_name=fn_name,
                    method=method.upper(),
                    path=path,
                    summary=summary.splitlines()[0][:140],
                    operation_id=str(raw_operation_id),
                )
            )
            if len(ops) >= max_operations:
                return ops

    return ops


def guess_api_base(spec: dict[str, Any]) -> str:
    servers = spec.get("servers")
    if not isinstance(servers, list) or not servers:
        return ""
    first = servers[0]
    if not isinstance(first, dict):
        return ""
    url = str(first.get("url") or "").strip()
    if not url:
        return ""

    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return parsed.path.rstrip("/")
    return url.rstrip("/")


def json_dump(data: Any) -> str:
    return json.dumps(data, indent=4, ensure_ascii=False)


def render_tools_py(module_name: str, env_prefix: str, api_base_hint: str, operations: list[Operation]) -> str:
    op_map = {
        op.fn_name: {
            "method": op.method,
            "path": op.path,
            "operation_id": op.operation_id,
            "summary": op.summary,
        }
        for op in operations
    }

    op_functions = []
    for op in operations:
        op_functions.append(
            f'''async def {op.fn_name}(\n'''
            f'''    path_params: Optional[Dict[str, Any]] = None,\n'''
            f'''    query: Optional[Dict[str, Any]] = None,\n'''
            f'''    body: Optional[Dict[str, Any]] = None,\n'''
            f'''    headers: Optional[Dict[str, Any]] = None,\n'''
            f''') -> Dict[str, Any]:\n'''
            f'''    """{op.summary}"""\n'''
            f'''    return await _invoke_operation("{op.fn_name}", path_params, query, body, headers)\n'''
        )

    joined_functions = "\n\n".join(op_functions)

    return f'''"""Generated tools module for {module_name}."""

import os
import json
from typing import Any, Dict, Optional
from urllib.parse import quote

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASEURL", "")
API_BASE = os.getenv("{env_prefix}_APIBase", "{api_base_hint}")
API_USERNAME = os.getenv("{env_prefix}_UserName", "")
API_PASSWORD = os.getenv("{env_prefix}_Password", "")

API_OPERATIONS: Dict[str, Dict[str, str]] = {json_dump(op_map)}


def _auth_tuple() -> Optional[tuple[str, str]]:
    if API_USERNAME and API_PASSWORD:
        return (API_USERNAME, API_PASSWORD)
    return None


def _render_path(path_template: str, path_params: Optional[Dict[str, Any]]) -> str:
    safe_params = {{}}
    for key, value in (path_params or {{}}).items():
        safe_params[key] = quote(str(value), safe="")

    try:
        return path_template.format(**safe_params)
    except KeyError as exc:
        raise ValueError(f"Missing path parameter: {{exc.args[0]}}")


def _build_url(relative_path: str) -> str:
    base = BASE_URL.rstrip("/")
    api_base = API_BASE.strip("/")
    rel = relative_path.lstrip("/")

    if not base:
        raise ValueError("BASEURL is empty. Set BASEURL in .env")

    if api_base:
        return f"{{base}}/{{api_base}}/{{rel}}"
    return f"{{base}}/{{rel}}"


async def _invoke_operation(
    operation_name: str,
    path_params: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    op = API_OPERATIONS.get(operation_name)
    if not op:
        raise ValueError(f"Unknown operation: {{operation_name}}")

    method = op["method"]
    rendered_path = _render_path(op["path"], path_params)
    url = _build_url(rendered_path)
    merged_headers = {{"Accept": "application/json"}}
    merged_headers.update(headers or {{}})

    auth = _auth_tuple()

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            kwargs: Dict[str, Any] = {{
                "params": query or {{}},
                "auth": auth,
                "headers": merged_headers,
            }}
            if body is not None and method in {{"POST", "PUT", "PATCH"}}:
                kwargs["json"] = body

            response = await client.request(method, url, **kwargs)
            response.raise_for_status()

            content_type = (response.headers.get("content-type") or "").lower()
            if "application/json" in content_type:
                data: Any = response.json()
            else:
                data = response.text

            return {{
                "status": "success",
                "operation": operation_name,
                "method": method,
                "url": url,
                "http_status": response.status_code,
                "data": data,
            }}
    except httpx.HTTPStatusError as exc:
        return {{
            "status": "error",
            "operation": operation_name,
            "method": method,
            "url": url,
            "http_status": exc.response.status_code,
            "message": exc.response.text,
        }}
    except Exception as exc:
        return {{
            "status": "error",
            "operation": operation_name,
            "method": method,
            "url": url,
            "message": str(exc),
        }}


{joined_functions}
'''


def render_api_py(route_prefix: str, module_name: str, operations: list[Operation]) -> str:
    endpoints = []
    for op in operations:
        endpoints.append(
            f'''@router.post("/{op.fn_name}", response_model=OperationResponse)\n'''
            f'''async def api_{op.fn_name}(request_data: OperationRequest):\n'''
            f'''    """{op.summary}"""\n'''
            f'''    try:\n'''
            f'''        result = await generated_tools.{op.fn_name}(\n'''
            f'''            path_params=request_data.path_params,\n'''
            f'''            query=request_data.query,\n'''
            f'''            body=request_data.body,\n'''
            f'''            headers=request_data.headers,\n'''
            f'''        )\n'''
            f'''        return OperationResponse(result=result)\n'''
            f'''    except ValueError as exc:\n'''
            f'''        raise HTTPException(status_code=400, detail=str(exc))\n'''
            f'''    except Exception as exc:\n'''
            f'''        raise HTTPException(status_code=500, detail=f"Internal server error: {{exc}}")\n'''
        )

    joined = "\n\n".join(endpoints)

    return f'''"""Generated FastAPI router for {module_name}."""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from . import tools as generated_tools


class OperationRequest(BaseModel):
    path_params: Dict[str, Any] = Field(default_factory=dict)
    query: Dict[str, Any] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    headers: Dict[str, Any] = Field(default_factory=dict)


class OperationResponse(BaseModel):
    result: Dict[str, Any]


router = APIRouter(
    prefix="/{route_prefix}",
    tags=["{module_name} Functions"],
)


{joined}
'''


def render_prompts_py(module_name: str, operations: list[Operation]) -> str:
    op_names = ", ".join(op.fn_name for op in operations[:12])
    return f'''"""Prompt helpers for {module_name}."""


def {to_snake(module_name)}_analysis(user_goal: str) -> str:
    """Create a concise analysis prompt that hints available operations."""
    return (
        f"Analyze request: {{user_goal}}\\n"
        "Use relevant API operations to gather data and summarize key findings.\\n"
        "Available generated operations include: {op_names}."
    )
'''


def render_init_py() -> str:
    return '"""Generated backend module."""\n'


def ensure_writable_target(target: Path, overwrite: bool) -> None:
    if target.exists() and any(target.iterdir()) and not overwrite:
        raise FileExistsError(f"Target module directory already exists: {target}. Use --overwrite to continue.")


def main() -> None:
    args = parse_args()

    spec_path = Path(args.spec).expanduser().resolve()
    project_root = Path(args.project_root).expanduser().resolve()
    src_root = project_root / "src"
    if not src_root.exists():
        raise FileNotFoundError(f"src directory not found under {project_root}")

    module_name_clean = to_pascal(args.module_name)
    module_folder = f"{args.module_id}_{module_name_clean}"
    target_dir = src_root / module_folder

    spec = load_spec(spec_path)
    operations = collect_operations(spec, args.max_operations)
    if not operations:
        raise ValueError("No operations were collected from spec")

    route_prefix = args.route_prefix or to_snake(args.module_name)
    env_prefix = args.env_prefix or re.sub(r"[^A-Za-z0-9]", "", module_name_clean).upper()
    api_base_hint = guess_api_base(spec)

    ensure_writable_target(target_dir, args.overwrite)

    tools_py = render_tools_py(module_name_clean, env_prefix, api_base_hint, operations)
    api_py = render_api_py(route_prefix, module_name_clean, operations)
    prompts_py = render_prompts_py(module_name_clean, operations)
    init_py = render_init_py()

    print(f"[INFO] Spec: {spec_path}")
    print(f"[INFO] Module: {module_folder}")
    print(f"[INFO] Operations scaffolded: {len(operations)}")
    print(f"[INFO] Route prefix: /{route_prefix}")
    print(f"[INFO] ENV prefix: {env_prefix}")
    if api_base_hint:
        print(f"[INFO] API base hint: {api_base_hint}")

    if args.dry_run:
        print("[DRY-RUN] No file changes were made.")
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "tools.py").write_text(tools_py, encoding="utf-8")
    (target_dir / "api.py").write_text(api_py, encoding="utf-8")
    (target_dir / "prompts.py").write_text(prompts_py, encoding="utf-8")
    (target_dir / "__init__.py").write_text(init_py, encoding="utf-8")

    print("[OK] Module scaffold generated.")
    print(f"[NEXT] Add env vars: {env_prefix}_APIBase, {env_prefix}_UserName, {env_prefix}_Password")
    print(f"[NEXT] Confirm router auto-load via src/api_server.py for {module_folder}/api.py")


if __name__ == "__main__":
    main()
