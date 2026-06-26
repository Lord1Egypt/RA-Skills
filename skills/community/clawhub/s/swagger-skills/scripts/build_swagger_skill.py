"""Build API calling skill files from Swagger UI or OpenAPI/Swagger specs.

The script is self-contained inside ``swagger-skills`` and does not depend
on Skill_Seekers internals. It accepts Swagger UI pages or direct spec URLs,
normalizes endpoints, and writes Python clients plus OpenAPI reference files.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from swagger_client import (
    DEFAULT_DOC_AUTH,
    ensure_requirements_installed,
    fetch_text,
    save_json,
)

ensure_requirements_installed({"requests": "requests", "yaml": "PyYAML"})

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options", "trace"}
SUCCESS_RESPONSE_STATUSES = {"200", "201", "202", "203", "204", "205", "206", "207", "208", "226"}
JSON_MEDIA_TYPES = {"application/json", "application/*+json", "*/*"}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(description="Build ysb swagger skills from documentation")
    parser.add_argument(
        "--sources",
        default=str(SCRIPT_DIR.parent / "config" / "sources.json"),
        help="Path to sources.json",
    )
    parser.add_argument(
        "--output",
        default=str(SCRIPT_DIR.parent.parent),
        help="Base output directory. Generated skill directories are written directly under it.",
    )
    parser.add_argument(
        "--output-mode",
        choices=["auto", "combined", "separate"],
        default="auto",
        help=(
            "Skill output mode: auto asks when multiple sources exist, combined writes one skill, "
            "separate writes one skill per source"
        ),
    )
    parser.add_argument(
        "--combined-name",
        default="combined-swagger-skills",
        help="Directory and SKILL.md name for combined output mode",
    )
    parser.add_argument(
        "--clean-generated",
        action="store_true",
        help="Remove <output>/generated before building",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON config as a dictionary."""

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"配置文件必须是 JSON 对象：{path}")
    return data


def safe_name(value: str, fallback: str = "item") -> str:
    """Return a stable English-only snake_case file or directory name."""

    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value or "")
    value = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return value or fallback


def english_name(value: str) -> str:
    """Return an English-only name or an empty string when none can be derived."""

    return safe_name(value, "")


def operation_name(endpoint: dict[str, Any]) -> str:
    """Choose a readable operation name for generated files."""

    operation_id = endpoint.get("operation_id")
    if operation_id:
        return safe_name(operation_id, "operation")
    raw = f"{endpoint.get('method', 'GET')}_{endpoint.get('path', '/')}"
    raw = raw.replace("{", "by_").replace("}", "")
    return safe_name(raw, "operation")


def python_identifier(value: str) -> str:
    """Convert a generated operation name into a valid Python identifier."""

    identifier = re.sub(r"\W+", "_", value, flags=re.UNICODE).strip("_")
    if not identifier:
        identifier = "operation"
    if identifier[0].isdigit():
        identifier = f"op_{identifier}"
    return identifier


def controller_name(endpoint: dict[str, Any]) -> str:
    """Infer controller name from tag, path, or operation id."""

    tags = endpoint.get("tags") or []
    if tags:
        tag_name = english_name(str(tags[0]))
        if tag_name:
            return tag_name

    operation_id = endpoint.get("operation_id", "")
    if operation_id:
        if "_" in operation_id:
            op_prefix = english_name(operation_id.split("_", 1)[0])
            if op_prefix:
                return op_prefix
        controller_match = re.search(r"([A-Za-z][A-Za-z0-9]*Controller)", operation_id)
        if controller_match:
            return safe_name(controller_match.group(1), "default_controller")

    path = endpoint.get("path", "/")
    segments = [item for item in path.split("/") if item and not item.startswith("{")]
    generic_segments = {"api", "openapi", "swagger", "v1", "v2", "v3", "admin"}
    for segment in segments:
        segment_name = english_name(segment)
        if segment_name and segment_name not in generic_segments:
            return segment_name
    if segments:
        segment_name = english_name(segments[0])
        if segment_name:
            return segment_name

    if operation_id:
        op_name = english_name(operation_id)
        if op_name:
            return op_name
    return "default_controller"


def parse_json_any(text: str) -> Any:
    """Parse any JSON payload, returning None when it is not JSON."""

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def parse_spec_text(text: str, source_url: str) -> dict[str, Any] | None:
    """Parse JSON or YAML spec text."""

    stripped = text.lstrip()
    if stripped.startswith("{"):
        data = parse_json_any(text)
        return data if isinstance(data, dict) else None

    try:
        import yaml
    except ImportError:
        return None

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise RuntimeError(f"无法解析 Swagger/OpenAPI 内容：{source_url}: {exc}") from exc
    return data if isinstance(data, dict) else None


def looks_like_spec(data: dict[str, Any] | None) -> bool:
    """Return whether a parsed document looks like OpenAPI/Swagger."""

    return bool(data and ("openapi" in data or "swagger" in data) and "paths" in data)


def candidate_urls(page_url: str, html: str) -> list[str]:
    """Extract possible spec URLs from a Swagger UI page."""

    candidates: list[str] = []
    patterns = [
        r"\burl\s*:\s*['\"]([^'\"]+)['\"]",
        r"\burl\s*=\s*['\"]([^'\"]+)['\"]",
        r"['\"]url['\"]\s*:\s*['\"]([^'\"]+)['\"]",
        r"['\"]([^'\"]*(?:v2|v3)/api-docs[^'\"]*)['\"]",
        r"['\"]([^'\"]*swagger[^'\"]*\.(?:json|yaml|yml))['\"]",
        r"['\"]([^'\"]*openapi[^'\"]*\.(?:json|yaml|yml))['\"]",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, html, flags=re.IGNORECASE):
            candidates.append(urljoin(page_url, match))

    parsed = urlparse(page_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path or "/"
    prefixes = {origin}
    for marker in ("/swagger-ui", "/doc.html", "/swagger/"):
        if marker in path:
            prefixes.add(origin + path.split(marker, 1)[0])
    if path.endswith("/"):
        prefixes.add(origin + path.rstrip("/"))

    common_paths = [
        "/v3/api-docs",
        "/v2/api-docs",
        "/api-docs",
        "/swagger/v1/swagger.json",
        "/swagger.json",
        "/openapi.json",
    ]
    for prefix in prefixes:
        for suffix in common_paths:
            candidates.append(prefix.rstrip("/") + suffix)

    seen: set[str] = set()
    unique: list[str] = []
    for item in candidates:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return unique


def expand_swagger_resources(
    resources: Any,
    page_url: str,
) -> list[str]:
    """Convert /swagger-resources payload into candidate spec URLs."""

    if not isinstance(resources, list):
        return []
    urls: list[str] = []
    for item in resources:
        if isinstance(item, dict) and item.get("url"):
            urls.append(urljoin(page_url, str(item["url"])))
    return urls


def discover_spec(source: dict[str, Any], defaults: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Discover and parse the spec for one source entry."""

    url = source.get("spec_url") or source.get("swagger_url") or source.get("url")
    if not url:
        raise ValueError(f"source 缺少 swagger_url/spec_url/url：{source}")

    auth = source.get("doc_auth") or defaults.get("doc_auth") or DEFAULT_DOC_AUTH
    timeout = int(source.get("timeout") or defaults.get("timeout") or 30)

    text, final_url = fetch_text(str(url), auth, timeout)
    parsed = parse_spec_text(text, final_url)
    if looks_like_spec(parsed):
        return parsed, final_url

    candidates = candidate_urls(final_url, text)
    for candidate in candidates:
        try:
            candidate_text, candidate_final_url = fetch_text(candidate, auth, timeout)
        except Exception:
            continue
        candidate_data = parse_spec_text(candidate_text, candidate_final_url)
        if looks_like_spec(candidate_data):
            return candidate_data, candidate_final_url
        resource_urls = expand_swagger_resources(
            parse_json_any(candidate_text),
            candidate_final_url,
        )
        for resource_url in resource_urls:
            try:
                resource_text, resource_final_url = fetch_text(resource_url, auth, timeout)
            except Exception:
                continue
            resource_data = parse_spec_text(resource_text, resource_final_url)
            if looks_like_spec(resource_data):
                return resource_data, resource_final_url

    raise RuntimeError(f"未能从 Swagger UI 页面发现 OpenAPI/Swagger spec：{url}")


def resolve_ref(obj: Any, spec: dict[str, Any]) -> Any:
    """Resolve local JSON pointer references."""

    if not isinstance(obj, dict) or "$ref" not in obj:
        return obj
    ref = obj.get("$ref", "")
    if not ref.startswith("#/"):
        return obj
    current: Any = spec
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            return obj
        current = current[part]
    return current


def flatten_schema(schema: Any, spec: dict[str, Any], depth: int = 0) -> Any:
    """Resolve common schema references without expanding forever."""

    if not isinstance(schema, dict) or depth > 8:
        return schema
    schema = dict(resolve_ref(schema, spec))
    if "$ref" in schema:
        schema = dict(resolve_ref(schema, spec))
    for key in ("properties",):
        if isinstance(schema.get(key), dict):
            schema[key] = {
                name: flatten_schema(value, spec, depth + 1)
                for name, value in schema[key].items()
            }
    if isinstance(schema.get("items"), dict):
        schema["items"] = flatten_schema(schema["items"], spec, depth + 1)
    for key in ("allOf", "oneOf", "anyOf"):
        if isinstance(schema.get(key), list):
            schema[key] = [flatten_schema(item, spec, depth + 1) for item in schema[key]]
    return schema


def normalize_parameter(param: dict[str, Any], spec: dict[str, Any], version: int) -> dict[str, Any]:
    """Normalize one OpenAPI/Swagger parameter."""

    param = dict(resolve_ref(param, spec))
    location = param.get("in", "query")
    schema = param.get("schema") or {}
    if version == 2 and not schema and location != "body":
        schema = {
            "type": param.get("type", "string"),
            "format": param.get("format"),
            "items": param.get("items"),
            "enum": param.get("enum"),
        }
        schema = {key: value for key, value in schema.items() if value not in (None, "", [])}
    if location == "body":
        schema = flatten_schema(param.get("schema", {}), spec)
    else:
        schema = flatten_schema(schema, spec)
    return {
        "name": param.get("name", ""),
        "location": location,
        "description": param.get("description", ""),
        "required": bool(param.get("required", location == "path")),
        "schema": schema,
        "example": param.get("example") or param.get("x-example"),
    }


def normalize_request_body(body: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    """Normalize OpenAPI 3 request body."""

    body = dict(resolve_ref(body, spec))
    content: dict[str, Any] = {}
    for media_type, media_obj in body.get("content", {}).items():
        schema = flatten_schema(media_obj.get("schema", {}), spec)
        content[media_type] = {
            "schema": schema,
            "example": media_obj.get("example"),
            "examples": media_obj.get("examples", {}),
        }
    return {
        "description": body.get("description", ""),
        "required": bool(body.get("required", False)),
        "content": content,
    }


def normalize_response(response: dict[str, Any], spec: dict[str, Any], version: int) -> dict[str, Any]:
    """Normalize one response object."""

    response = dict(resolve_ref(response, spec))
    content: dict[str, Any] = {}
    if version >= 3:
        for media_type, media_obj in response.get("content", {}).items():
            content[media_type] = {
                "schema": flatten_schema(media_obj.get("schema", {}), spec),
            }
    elif response.get("schema"):
        content["application/json"] = {
            "schema": flatten_schema(response.get("schema", {}), spec),
        }
    return {
        "description": response.get("description", ""),
        "content": content,
        "headers": response.get("headers", {}),
    }


def normalize_spec(spec: dict[str, Any], source: dict[str, Any], spec_url: str) -> dict[str, Any]:
    """Extract servers, endpoints, schemas, and security schemes from a spec."""

    version = 3 if "openapi" in spec else 2
    info = spec.get("info", {})
    servers: list[dict[str, Any]] = []
    if version >= 3:
        servers = [
            {
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            }
            for item in spec.get("servers", [])
            if isinstance(item, dict)
        ]
    else:
        host = spec.get("host", "")
        base_path = spec.get("basePath", "/")
        for scheme in spec.get("schemes", ["https"]):
            if host:
                servers.append(
                    {
                        "url": f"{scheme}://{host}{base_path}",
                        "description": f"Swagger 2.0 server ({scheme})",
                    }
                )

    if source.get("base_url"):
        servers.insert(0, {"url": source["base_url"], "description": "Configured base URL"})

    endpoints: list[dict[str, Any]] = []
    for path, path_item in spec.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        path_params = path_item.get("parameters", [])
        for method in sorted(HTTP_METHODS):
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            endpoint = {
                "path": path,
                "method": method.upper(),
                "operation_id": operation.get("operationId", ""),
                "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "tags": operation.get("tags", []),
                "deprecated": bool(operation.get("deprecated", False)),
                "parameters": [],
                "request_body": {},
                "responses": {},
                "security": operation.get("security", []),
            }
            params = list(path_params) + list(operation.get("parameters", []))
            endpoint["parameters"] = [
                normalize_parameter(param, spec, version)
                for param in params
                if isinstance(param, dict)
            ]
            if version >= 3 and isinstance(operation.get("requestBody"), dict):
                endpoint["request_body"] = normalize_request_body(operation["requestBody"], spec)
            elif version == 2:
                body_params = [
                    param for param in endpoint["parameters"] if param.get("location") == "body"
                ]
                if body_params:
                    endpoint["request_body"] = {
                        "description": body_params[0].get("description", ""),
                        "required": body_params[0].get("required", False),
                        "content": {
                            "application/json": {
                                "schema": body_params[0].get("schema", {}),
                            }
                        },
                    }
            for status, response in operation.get("responses", {}).items():
                if isinstance(response, dict):
                    endpoint["responses"][str(status)] = normalize_response(response, spec, version)
            endpoints.append(endpoint)

    schemas_root = (
        spec.get("components", {}).get("schemas", {})
        if version >= 3
        else spec.get("definitions", {})
    )
    schemas = {
        name: flatten_schema(schema, spec)
        for name, schema in schemas_root.items()
        if isinstance(schema, dict)
    }
    security_schemes = (
        spec.get("components", {}).get("securitySchemes", {})
        if version >= 3
        else spec.get("securityDefinitions", {})
    )
    return {
        "document_id": source["id"],
        "document_name": source.get("name") or source["id"],
        "description": source.get("description", ""),
        "spec_url": spec_url,
        "version": spec.get("openapi") or spec.get("swagger"),
        "info": info,
        "servers": servers,
        "endpoints": endpoints,
        "schemas": schemas,
        "security_schemes": security_schemes,
    }


def schema_type(schema: Any) -> str:
    """Render a compact schema type label."""

    if not isinstance(schema, dict):
        return "any"
    if "$ref" in schema:
        return str(schema["$ref"]).split("/")[-1]
    if schema.get("type") == "array":
        return f"array[{schema_type(schema.get('items', {}))}]"
    return str(schema.get("type") or schema.get("format") or "object")


def render_schema(schema: Any, indent: int = 0) -> list[str]:
    """Render schema fields as markdown bullets."""

    prefix = "  " * indent
    if not isinstance(schema, dict):
        return [f"{prefix}- `{schema}`"]
    lines: list[str] = []
    if schema.get("description"):
        lines.append(f"{prefix}- 描述：{schema['description']}")

    if schema.get("type") == "array":
        items = schema.get("items", {})
        lines.append(f"{prefix}- 类型：`{schema_type(schema)}`")
        if isinstance(items, dict):
            item_description = items.get("description")
            if item_description:
                lines.append(f"{prefix}  - 数组元素描述：{item_description}")
            if _schema_has_nested_fields(items):
                lines.append(f"{prefix}  - 数组元素字段：")
                lines.extend(render_schema(items, indent + 2))
        return lines

    properties = schema.get("properties")
    if isinstance(properties, dict) and properties:
        required = set(schema.get("required", []))
        for name, prop in properties.items():
            mark = "必填" if name in required else "可选"
            desc = prop.get("description", "") if isinstance(prop, dict) else ""
            line = f"{prefix}- `{name}` ({schema_type(prop)}, {mark})"
            if desc:
                line += f"：{desc}"
            lines.append(line)
            if isinstance(prop, dict) and _schema_has_nested_fields(prop):
                lines.extend(render_schema(prop, indent + 1))
    elif _schema_has_composition(schema):
        for key in ("allOf", "oneOf", "anyOf"):
            variants = schema.get(key)
            if not isinstance(variants, list):
                continue
            lines.append(f"{prefix}- `{key}` 组合字段：")
            for index, variant in enumerate(variants, start=1):
                lines.append(f"{prefix}  - 方案 {index}：")
                lines.extend(render_schema(variant, indent + 2))
    else:
        lines.append(f"{prefix}- 类型：`{schema_type(schema)}`")
    return lines


def _schema_has_composition(schema: dict[str, Any]) -> bool:
    """Return whether schema contains allOf/oneOf/anyOf fields."""

    return any(isinstance(schema.get(key), list) and schema.get(key) for key in ("allOf", "oneOf", "anyOf"))


def _schema_has_nested_fields(schema: dict[str, Any]) -> bool:
    """Return whether schema has nested fields worth rendering."""

    if isinstance(schema.get("properties"), dict) and schema["properties"]:
        return True
    if schema.get("type") == "array" and isinstance(schema.get("items"), dict):
        return _schema_has_nested_fields(schema["items"]) or bool(schema["items"].get("description"))
    return _schema_has_composition(schema)


def document_env_key(document_id: str) -> str:
    """Build default environment variable name for one document base URL override."""

    return f"{document_id.upper().replace('-', '_')}_ORIGIN"


def resolve_field_mapping_enabled(source: dict[str, Any], defaults: dict[str, Any]) -> bool:
    """Resolve whether response field mapping is enabled for one source."""

    field_mapping = source.get("field_mapping")
    if isinstance(field_mapping, dict) and "enabled" in field_mapping:
        return bool(field_mapping["enabled"])
    default_mapping = defaults.get("field_mapping")
    if isinstance(default_mapping, dict) and "enabled" in default_mapping:
        return bool(default_mapping["enabled"])
    return True


def _field_description(schema: dict[str, Any], field_name: str) -> str:
    """Return a human-readable description for one schema field."""

    for key in ("description", "title"):
        value = schema.get(key)
        if isinstance(value, str) and value.strip():
            return re.sub(r"\s+", " ", value.strip())
    return field_name


def _iter_schema_field_paths(schema: Any, prefix: str = "") -> list[tuple[str, str]]:
    """Yield JSON path and description pairs from a flattened response schema."""

    if not isinstance(schema, dict):
        return []

    entries: list[tuple[str, str]] = []
    if schema.get("type") == "array":
        items = schema.get("items", {})
        array_prefix = f"{prefix}[]" if prefix else "[]"
        if isinstance(items, dict):
            item_desc = items.get("description")
            if isinstance(item_desc, str) and item_desc.strip() and prefix:
                entries.append((array_prefix, re.sub(r"\s+", " ", item_desc.strip())))
            entries.extend(_iter_schema_field_paths(items, array_prefix))
        return entries

    for key in ("allOf", "oneOf", "anyOf"):
        variants = schema.get(key)
        if isinstance(variants, list):
            for variant in variants:
                entries.extend(_iter_schema_field_paths(variant, prefix))
            return entries

    properties = schema.get("properties")
    if isinstance(properties, dict):
        for name, prop in properties.items():
            if not isinstance(prop, dict):
                continue
            field_path = f"{prefix}.{name}" if prefix else name
            desc = _field_description(prop, name)
            entries.append((field_path, desc))
            entries.extend(_iter_schema_field_paths(prop, field_path))
        return entries

    description = schema.get("description")
    if isinstance(description, str) and description.strip() and prefix:
        entries.append((prefix, re.sub(r"\s+", " ", description.strip())))
    return entries


def _response_schemas(endpoint: dict[str, Any]) -> list[dict[str, Any]]:
    """Return JSON response schemas for success status codes."""

    schemas: list[dict[str, Any]] = []
    for status, response in (endpoint.get("responses") or {}).items():
        if str(status) not in SUCCESS_RESPONSE_STATUSES:
            continue
        if not isinstance(response, dict):
            continue
        for media_type, media_obj in response.get("content", {}).items():
            if media_type not in JSON_MEDIA_TYPES and "json" not in media_type.lower():
                continue
            schema = media_obj.get("schema", {}) if isinstance(media_obj, dict) else {}
            if isinstance(schema, dict) and schema:
                schemas.append(schema)
    return schemas


def collect_field_index_entries(
    documents: list[dict[str, Any]],
    output_root: Path,
) -> list[dict[str, Any]]:
    """Build openapi_field_index.json entries from normalized endpoint schemas."""

    entries: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    namespace = len(documents) > 1

    for document in documents:
        document_id = document["document_id"]
        for endpoint in document.get("endpoints", []):
            controller = controller_name(endpoint)
            output_controller = f"{document_id}/{controller}" if namespace else controller
            op_name = endpoint.get("_ysb_operation_name") or operation_name(endpoint)
            source_file = f"references/{output_controller}/{op_name}_OPENAPI.md"
            http_method = str(endpoint.get("method", ""))
            path = str(endpoint.get("path", ""))
            operation_id = str(endpoint.get("operation_id", "") or "")

            for schema in _response_schemas(endpoint):
                for field_path, description in _iter_schema_field_paths(schema):
                    dedupe_key = (http_method, path, field_path, description)
                    if dedupe_key in seen:
                        continue
                    seen.add(dedupe_key)
                    entries.append(
                        {
                            "key": field_path,
                            "description": description,
                            "source_file": source_file,
                            "line": 0,
                            "http_method": http_method,
                            "path": path,
                            "operation_id": operation_id or None,
                        }
                    )
    entries.sort(key=lambda item: (item.get("path") or "", item.get("key") or ""))
    return entries


def write_field_index(output_root: Path, documents: list[dict[str, Any]]) -> None:
    """Write openapi_field_index.json at skill root."""

    payload = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entries": collect_field_index_entries(documents, output_root),
    }
    save_json(output_root / "openapi_field_index.json", payload)


def write_skill_common(output_root: Path, documents: list[dict[str, Any]]) -> None:
    """Generate skill_common.py with document-specific constants and shared runtime helpers."""

    template_path = SCRIPT_DIR / "skill_common.py"
    runtime_body = template_path.read_text(encoding="utf-8")
    if runtime_body.startswith('"""'):
        end = runtime_body.find('"""', 3)
        if end != -1:
            runtime_body = runtime_body[end + 3 :].lstrip("\n")
    runtime_body = re.sub(
        r"^from __future__ import annotations\s*\n",
        "",
        runtime_body,
        count=1,
    )
    document_ids = tuple(document["document_id"] for document in documents)
    env_lines = [
        f'    "{document["document_id"]}": "{document_env_key(document["document_id"])}",'
        for document in documents
    ]
    env_doc_lines = [
        f"- `{document['document_id']}` → 环境变量 `{document_env_key(document['document_id'])}`"
        for document in documents
    ]
    header = f'''"""本 skill 各接口文档的调用域名与公共配置。

修改 `config/domains.json` 后无需重生成即可生效。
也可通过环境变量临时覆盖 base_url：

{chr(10).join(env_doc_lines)}
"""

from __future__ import annotations

DOCUMENT_IDS = {document_ids!r}

ENV_OVERRIDES = {{
{chr(10).join(env_lines)}
}}

'''
    scripts_dir = output_root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    (scripts_dir / "skill_common.py").write_text(header + runtime_body, encoding="utf-8")


def write_client_file(
    output_root: Path,
    document_id: str,
    controller: str,
    op_name: str,
    endpoint: dict[str, Any],
) -> Path:
    """Write one generated Python client file."""

    function_name = python_identifier(op_name)
    path_params = [
        param["name"]
        for param in endpoint.get("parameters", [])
        if param.get("location") == "path" and param.get("name")
    ]
    client_path = output_root / "api_clients" / controller / f"{op_name}.py"
    client_path.parent.mkdir(parents=True, exist_ok=True)
    operation_id = endpoint.get("operation_id", "")
    code = f'''"""Generated API caller for {endpoint.get("method")} {endpoint.get("path")}."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

def _find_skill_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "config" / "domains.json").exists():
            return parent
    raise RuntimeError("未找到 config/domains.json，请确认当前文件位于生成的 skill 目录内。")


ROOT_DIR = _find_skill_root(Path(__file__).resolve())
SCRIPTS_DIR = ROOT_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skill_http import call_api_json

DOCUMENT_ID = {document_id!r}
METHOD = {endpoint.get("method", "GET")!r}
PATH_TEMPLATE = {endpoint.get("path", "/")!r}
OPERATION_ID = {operation_id!r}


def call_{function_name}(
    *,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    json_body: Any | None = None,
    data: Any | None = None,
    timeout: int | None = None,
    apply_field_mapping: bool | None = None,
    domain_config_path: str | Path | None = None,
):
    """Call `{endpoint.get("method")} {endpoint.get("path")}` and return parsed JSON.

    Required path params: {", ".join(path_params) if path_params else "none"}

    Use this function when the user asks to query, fetch, list, create, update,
    delete, or otherwise operate on real backend data. The companion OPENAPI.md
    file explains fields; this file performs the actual request.
    Response keys may be mapped to Chinese descriptions when field mapping is enabled.
    Set SWAGGER_RAW_JSON=1 or apply_field_mapping=False to keep original keys.
    """

    return call_api_json(
        DOCUMENT_ID,
        METHOD,
        PATH_TEMPLATE,
        path_params=path_params,
        http_method=METHOD,
        path=PATH_TEMPLATE,
        operation_id=OPERATION_ID,
        apply_field_mapping=apply_field_mapping,
        params=query,
        headers=headers,
        json_body=json_body,
        data=data,
        timeout=timeout,
        config_path=domain_config_path,
    )
'''
    client_path.write_text(code, encoding="utf-8")
    return client_path


def write_reference_file(
    output_root: Path,
    document_name: str,
    controller: str,
    op_name: str,
    endpoint: dict[str, Any],
    client_rel: str,
) -> Path:
    """Write one OpenAPI markdown reference file."""

    reference_path = output_root / "references" / controller / f"{op_name}_OPENAPI.md"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {endpoint.get('summary') or endpoint.get('operation_id') or op_name}",
        "",
        f"- 文档：{document_name}",
        f"- Controller：`{controller}`",
        f"- 方法：`{endpoint.get('method')}`",
        f"- 路径：`{endpoint.get('path')}`",
        f"- 调用文件：`{client_rel}`",
        "",
    ]
    if endpoint.get("description"):
        lines.extend(["## 接口描述", "", str(endpoint["description"]), ""])

    params = [param for param in endpoint.get("parameters", []) if param.get("location") != "body"]
    if params:
        lines.extend(["## 参数", "", "| 名称 | 位置 | 类型 | 必填 | 描述 |", "|---|---|---|---|---|"])
        for param in params:
            lines.append(
                "| `{name}` | {location} | `{type}` | {required} | {description} |".format(
                    name=param.get("name", ""),
                    location=param.get("location", ""),
                    type=schema_type(param.get("schema", {})),
                    required="是" if param.get("required") else "否",
                    description=str(param.get("description", "")).replace("\n", " "),
                )
            )
        lines.append("")

    request_body = endpoint.get("request_body") or {}
    if request_body.get("content"):
        lines.extend(["## 请求体", ""])
        if request_body.get("description"):
            lines.extend([str(request_body["description"]), ""])
        for media_type, media_obj in request_body["content"].items():
            lines.extend([f"### `{media_type}`", ""])
            lines.extend(render_schema(media_obj.get("schema", {})))
            lines.append("")

    responses = endpoint.get("responses") or {}
    if responses:
        lines.extend(["## 响应", ""])
        for status, response in sorted(responses.items()):
            lines.extend([f"### `{status}`", "", str(response.get("description", "")), ""])
            for media_type, media_obj in response.get("content", {}).items():
                lines.extend([f"Content-Type：`{media_type}`", ""])
                lines.extend(render_schema(media_obj.get("schema", {})))
                lines.append("")

    reference_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return reference_path


def rel(path: Path, root: Path) -> str:
    """Return a POSIX-style relative path for markdown."""

    return path.relative_to(root).as_posix()


def clean_generated(base_output_root: Path) -> None:
    """Remove previously generated business skills."""

    marker = "Generated by swagger-skills"
    if not base_output_root.exists():
        return
    for child in base_output_root.iterdir():
        skill_file = child / "SKILL.md"
        if not child.is_dir() or not skill_file.exists():
            continue
        try:
            content = skill_file.read_text(encoding="utf-8")
        except OSError:
            continue
        if marker in content:
            shutil.rmtree(child)


def clean_text(value: Any, max_length: int = 120) -> str:
    """Normalize text from OpenAPI fields for generated summaries."""

    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = re.sub(r"<[^>]+>", "", text)
    if len(text) > max_length:
        return text[: max_length - 3].rstrip() + "..."
    return text


def endpoint_title(endpoint: dict[str, Any]) -> str:
    """Return the most useful business-facing title for an endpoint."""

    return clean_text(
        endpoint.get("summary")
        or endpoint.get("description")
        or endpoint.get("operation_id")
        or f"{endpoint.get('method')} {endpoint.get('path')}",
        100,
    )


def collect_capability_groups(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collect business capability summaries from endpoint documentation."""

    groups: list[dict[str, Any]] = []
    for document in documents:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for endpoint in document.get("endpoints", []):
            grouped[controller_name(endpoint)].append(endpoint)

        for controller, endpoints in sorted(grouped.items()):
            titles: list[str] = []
            seen: set[str] = set()
            for endpoint in endpoints:
                title = endpoint_title(endpoint)
                if title and title not in seen:
                    titles.append(title)
                    seen.add(title)
                if len(titles) >= 5:
                    break
            if not titles:
                continue
            groups.append(
                {
                    "document": document["document_name"],
                    "controller": controller,
                    "count": len(endpoints),
                    "titles": titles,
                }
            )
    return groups


def build_skill_description(
    skill_name: str,
    documents: list[dict[str, Any]],
    capability_groups: list[dict[str, Any]],
) -> str:
    """Build frontmatter description focused on concrete API capabilities."""

    capability_phrases: list[str] = []
    for group in capability_groups[:4]:
        capability_phrases.extend(group["titles"][:2])
        if len(capability_phrases) >= 6:
            break

    if capability_phrases:
        base = "Use this skill to work with APIs for " + "; ".join(capability_phrases[:6])
    else:
        doc_names = ", ".join(document["document_name"] for document in documents[:3])
        base = f"Use this skill to work with APIs from {doc_names or skill_name}"

    suffix = (
        " Use the generated Python callers to fetch live data when the user asks for actual results; "
        "use references for parameters and field meanings."
    )
    description = base + "." + suffix
    if len(description) > 1000:
        description = description[:997].rstrip() + "..."
    return description


def write_static_skill_files(skill_root: Path, skill_name: str, documents: list[dict[str, Any]]) -> None:
    """Write SKILL.md and README.md for one generated business skill."""

    skill_root.mkdir(parents=True, exist_ok=True)
    doc_names = [document["document_name"] for document in documents]
    total_endpoints = sum(len(document.get("endpoints", [])) for document in documents)
    total_controllers = len(
        {
            controller_name(endpoint)
            for document in documents
            for endpoint in document.get("endpoints", [])
        }
    )
    capability_groups = collect_capability_groups(documents)
    description = build_skill_description(skill_name, documents, capability_groups)

    skill_lines = [
        "---",
        f"name: {safe_name(skill_name)[:64]}",
        f"description: {description}",
        "---",
        "",
        "<!-- Generated by swagger-skills -->",
        "",
        f"# {skill_name}",
        "",
        "这是一个面向具体业务接口的 API skill，提供接口功能索引、Python 调用逻辑和 OpenAPI 字段说明。",
        "",
        "## When to Use This Skill",
        "",
        "当你需要处理以下接口能力时使用本 skill：",
        "",
    ]
    if capability_groups:
        for group in capability_groups[:8]:
            title_text = "；".join(group["titles"][:4])
            skill_lines.append(
                f"- **{group['controller']}**（{group['document']}）：{title_text}"
            )
    else:
        skill_lines.extend(
            [
                "- 查找某个业务功能对应的接口。",
                "- 根据接口文档构造 Python 调用请求。",
                "- 查看接口参数、请求体、响应体和字段含义。",
            ]
        )

    skill_lines.extend(
        [
            "",
            "## How to Use This Skill",
            "",
            "- 当用户要求获取真实数据、查询列表、查看详情、创建/更新/删除数据时，优先定位并调用 `api_clients/` 中对应的 Python 函数。",
            "- 当用户只询问接口含义、字段说明、请求参数或响应结构时，读取 `references/` 中对应的 `*_OPENAPI.md`。",
            "- `FEATURES.md` 用于从业务功能快速定位到具体 Python 调用文件和字段说明文件。",
            "- 调用前先根据 `*_OPENAPI.md` 准备 path/query/header/body 参数；调用后向用户返回接口响应中的关键数据或错误信息。",
            "",
            "本 skill 还适用于：",
            "",
            "- 根据接口文档构造 Python 调用请求并执行。",
            "- 查看接口参数、请求体、响应体和字段含义。",
            "- 确认接口所属服务域名和 Swagger/OpenAPI 来源。",
        "",
        "## API Coverage",
        "",
        ]
    )
    for document in documents:
        info = document.get("info", {})
        version = document.get("version") or info.get("version") or ""
        version_text = f"，版本 `{version}`" if version else ""
        skill_lines.append(
            f"- **{document['document_name']}**：{len(document.get('endpoints', []))} 个接口{version_text}"
        )
        if document.get("description"):
            skill_lines.append(f"  - {document['description']}")
        elif info.get("description"):
            short_desc = str(info["description"]).replace("\n", " ")
            if len(short_desc) > 160:
                short_desc = short_desc[:157] + "..."
            skill_lines.append(f"  - {short_desc}")

    skill_lines.extend(
        [
            "",
            "## Capability Overview",
            "",
            f"- 接口文档数：{len(documents)}",
            f"- Controller 数：{total_controllers}",
            f"- 接口总数：{total_endpoints}",
            "",
        ]
    )

    for document in documents:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for endpoint in document.get("endpoints", []):
            grouped[controller_name(endpoint)].append(endpoint)
        if not grouped:
            continue
        skill_lines.extend([f"### {document['document_name']}", ""])
        for controller, endpoints in sorted(grouped.items()):
            examples = []
            for endpoint in endpoints[:3]:
                title = endpoint_title(endpoint)
                examples.append(f"`{endpoint.get('method')} {endpoint.get('path')}` {title}")
            example_text = "；".join(examples)
            more_text = f"，另有 {len(endpoints) - 3} 个接口" if len(endpoints) > 3 else ""
            skill_lines.append(f"- **{controller}**：{len(endpoints)} 个接口。{example_text}{more_text}")

    skill_lines.extend(
        [
            "",
            "## Navigation",
            "",
            "- 从 `FEATURES.md` 按功能、controller 或接口摘要定位接口。",
            "- 用户要求真实数据或执行操作时，调用 `api_clients/` 中的 Python 函数。",
            "- 用户询问字段、参数、响应结构时，读取 `references/` 中的说明。",
            "- 在 `config/domains.json` 中查看或修改接口调用域名；也可设置 `{DOCUMENT_ID}_ORIGIN` 环境变量临时覆盖。",
            "- 所有接口调用经 `scripts/skill_common.py` 解析域名，经 `scripts/skill_http.py` 执行请求。",
            "- 响应 JSON 默认将字段 key 映射为中文描述；设置 `SWAGGER_RAW_JSON=1` 或关闭 `field_mapping.enabled` 可保留原 key。",
            "",
            "## Output Files",
            "",
            "- `openapi_field_index.json`：字段索引，供 lookup 与响应 key 映射。",
            "- `api_clients/`：接口调用 Python 文件。",
            "- `references/`：接口字段说明与 controller 聚合说明。",
            "- `FEATURES.md`：功能集成索引。",
            "- `config/domains.json`：域名、字段映射开关、spec 和认证配置。",
            "- `scripts/skill_common.py`：各文档调用域名统一管理。",
            "- `scripts/skill_http.py`：统一 HTTP 调用与响应字段映射入口。",
            "- `scripts/openapi_fields.py`：字段索引 lookup 脚本。",
            "- `scripts/swagger_client.py`：构建期拉取 spec 的工具（运行时备用）。",
            "- `requirements.txt`：独立运行本 skill 调用文件所需的 Python 依赖。",
        ]
    )
    (skill_root / "SKILL.md").write_text("\n".join(skill_lines) + "\n", encoding="utf-8")

    readme_lines = [
        f"# {skill_name}",
        "",
        "这是一个根据 Swagger/OpenAPI 接口文档生成的业务 API skill，包含可复用的 Python 调用文件、接口字段说明和功能导航索引。",
        "",
        "## 覆盖范围",
        "",
        f"- 接口文档数：{len(documents)}",
        f"- Controller 数：{total_controllers}",
        f"- 接口总数：{total_endpoints}",
        f"- 生成来源：{', '.join(doc_names)}",
        "",
        "## 快速开始",
        "",
        "1. 用户要求获取真实数据或执行业务操作时，先打开 `FEATURES.md` 定位对应接口。",
        "2. 查看对应的 `references/<controller>/<operation>_OPENAPI.md`，确认请求参数、请求体和响应字段。",
        "3. 调用对应的 `api_clients/<controller>/<operation>.py` 中的 `call_*` 函数执行真实请求。",
        "4. 如需调整调用域名，修改 `config/domains.json`，或设置 `<DOCUMENT_ID>_ORIGIN` 环境变量。",
        "5. 字段释义可执行 `python scripts/openapi_fields.py lookup <字段名>`。",
        "6. 如果只询问接口字段或含义，可以只阅读 `references/`；如果要数据结果，应调用 `api_clients/`。",
        "7. 如果要单独运行本 skill 中的 Python 调用文件，请先执行 `python -m pip install -r requirements.txt`。",
        "",
        "## 目录结构",
        "",
        "```text",
        ".",
        "|-- SKILL.md",
        "|-- FEATURES.md",
        "|-- README.md",
        "|-- openapi_field_index.json",
        "|-- requirements.txt",
        "|-- config/",
        "|   `-- domains.json",
        "|-- scripts/",
        "|   |-- skill_common.py",
        "|   |-- skill_http.py",
        "|   |-- field_mapper.py",
        "|   |-- openapi_fields.py",
        "|   `-- swagger_client.py",
        "|-- api_clients/",
        "|   `-- <controller>/<operation>.py",
        "`-- references/",
        "    |-- <controller>/<operation>_OPENAPI.md",
        "    `-- controllers/<controller>.md",
        "```",
        "",
        "## 文档来源",
        "",
    ]
    for document in documents:
        info = document.get("info", {})
        version = document.get("version") or info.get("version") or ""
        version_text = f"（版本 `{version}`）" if version else ""
        readme_lines.append(
            f"- **{document['document_name']}**{version_text}：{len(document.get('endpoints', []))} 个接口"
        )
        servers = document.get("servers") or []
        if servers:
            readme_lines.append(f"  - 默认域名：`{servers[0].get('url', '')}`")
        if document.get("spec_url"):
            readme_lines.append(f"  - Spec：`{document['spec_url']}`")

    readme_lines.extend(
        [
            "",
            "## 命名规则",
            "",
            "产出物的文件夹和文件名只使用英文、数字和下划线。生成器会优先使用英文 tag、operationId、path 片段或 source_id；中文名称不会转换为拼音，也不会直接进入路径。",
            "",
            "## 备注",
            "",
            "本目录是可直接使用的业务接口 skill；生成器位于上层 `swagger-skills` 目录。",
        ]
    )
    (skill_root / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")


def write_generated_readmes(skill_root: Path) -> None:
    """Write README files for generated output folders."""

    api_readme = skill_root / "api_clients" / "README.md"
    api_readme.parent.mkdir(parents=True, exist_ok=True)
    api_readme.write_text(
        "# API Clients\n\n这里保存由接口文档生成的 Python 调用文件。\n",
        encoding="utf-8",
    )

    reference_readme = skill_root / "references" / "README.md"
    reference_readme.parent.mkdir(parents=True, exist_ok=True)
    reference_readme.write_text(
        "# References\n\n这里保存由接口文档生成的 OpenAPI 字段说明和 controller 聚合说明。\n",
        encoding="utf-8",
    )


def copy_runtime_files(skill_root: Path) -> None:
    """Copy runtime helpers required by generated API clients."""

    scripts_dir = skill_root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    for filename in (
        "swagger_client.py",
        "skill_http.py",
        "field_mapper.py",
        "openapi_fields.py",
    ):
        shutil.copy2(SCRIPT_DIR / filename, scripts_dir / filename)

    requirements_path = SCRIPT_DIR.parent / "requirements.txt"
    if requirements_path.exists():
        shutil.copy2(requirements_path, skill_root / "requirements.txt")


def generate_files(output_root: Path, documents: list[dict[str, Any]], config: dict[str, Any]) -> None:
    """Generate clients, references, domains, and feature index."""

    capability_groups = collect_capability_groups(documents)
    write_static_skill_files(
        output_root,
        config.get("skill_name", output_root.name),
        documents,
    )
    write_generated_readmes(output_root)
    copy_runtime_files(output_root)

    defaults = config.get("defaults", {})
    if len(documents) == 1:
        source = config["source_by_id"].get(documents[0]["document_id"], {})
        mapping_enabled = resolve_field_mapping_enabled(source, defaults)
    else:
        mapping_enabled = resolve_field_mapping_enabled({}, defaults)
    domains: dict[str, Any] = {
        "generated_by": "swagger-skills",
        "field_mapping": {
            "enabled": mapping_enabled,
        },
        "defaults": {
            "timeout": int(defaults.get("timeout") or 30),
        },
        "documents": {},
    }
    feature_lines = [
        f"# {config.get('skill_name', output_root.name)} 功能集成索引",
        "",
        "以下内容由 `swagger-skills` 根据接口文档生成。",
        "",
    ]
    if capability_groups:
        feature_lines.extend(["## 支持的主要能力", ""])
        for group in capability_groups[:12]:
            feature_lines.append(
                f"- **{group['controller']}**（{group['document']}）："
                + "；".join(group["titles"][:4])
            )
        feature_lines.append("")

    feature_lines.extend(
        [
            "## 使用规则",
            "",
            "- 用户要求获取真实数据、查询列表、查看详情、创建、更新或删除时，使用 `Python 调用` 文件执行接口请求。",
            "- 用户只询问字段含义、请求参数或响应结构时，查看 `字段说明` 文件。",
            "- 调用前先参考字段说明准备参数，调用后返回响应中的关键数据或错误信息。",
            "",
        ]
    )

    for document in documents:
        document_id = document["document_id"]
        document_name = document["document_name"]
        servers = document.get("servers") or []
        base_url = servers[0]["url"] if servers else ""
        source = config["source_by_id"].get(document_id, {})
        auth = source.get("doc_auth") or config.get("defaults", {}).get("doc_auth") or DEFAULT_DOC_AUTH
        domains["documents"][document_id] = {
            "name": document_name,
            "description": document.get("description", ""),
            "spec_url": document.get("spec_url", ""),
            "base_url": base_url,
            "servers": servers,
            "env_key": document_env_key(document_id),
            "doc_auth": {
                "type": auth.get("type", "basic"),
                "username": auth.get("username", ""),
                "password": auth.get("password", ""),
            },
        }

        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        generated: dict[tuple[str, str], dict[str, str]] = {}
        name_counts: dict[tuple[str, str], int] = {}
        namespace = len(documents) > 1
        for endpoint in document.get("endpoints", []):
            controller = controller_name(endpoint)
            output_controller = f"{document_id}/{controller}" if namespace else controller
            base_op_name = operation_name(endpoint)
            count_key = (output_controller, base_op_name)
            count = name_counts.get(count_key, 0) + 1
            name_counts[count_key] = count
            op_name = base_op_name if count == 1 else f"{base_op_name}_{count}"
            endpoint["_ysb_operation_name"] = op_name
            endpoint["_ysb_output_controller"] = output_controller
            grouped[output_controller].append(endpoint)
            client_path = write_client_file(output_root, document_id, output_controller, op_name, endpoint)
            client_rel = rel(client_path, output_root)
            reference_path = write_reference_file(
                output_root,
                document_name,
                output_controller,
                op_name,
                endpoint,
                client_rel,
            )
            generated[(output_controller, op_name)] = {
                "client": client_rel,
                "reference": rel(reference_path, output_root),
            }

        feature_lines.extend([f"## {document_name}", ""])
        if document.get("description"):
            feature_lines.extend([document["description"], ""])

        for controller, endpoints in sorted(grouped.items()):
            if namespace and "/" in controller:
                document_part, controller_part = controller.split("/", 1)
                controller_path = (
                    output_root
                    / "references"
                    / document_part
                    / "controllers"
                    / f"{controller_part}.md"
                )
            else:
                controller_path = output_root / "references" / "controllers" / f"{controller}.md"
            controller_path.parent.mkdir(parents=True, exist_ok=True)
            controller_lines = [
                f"# {controller}",
                "",
                f"- 文档：{document_name}",
                f"- 接口数量：{len(endpoints)}",
                "",
                "| 功能 | 方法 | 路径 | Python 调用 | 字段说明 |",
                "|---|---|---|---|---|",
            ]
            feature_lines.extend([f"### {controller}", ""])
            for endpoint in endpoints:
                op_name = endpoint.get("_ysb_operation_name") or operation_name(endpoint)
                files = generated[(controller, op_name)]
                title = endpoint.get("summary") or endpoint.get("operation_id") or op_name
                method = endpoint.get("method", "")
                path = endpoint.get("path", "")
                controller_lines.append(
                    f"| {title} | `{method}` | `{path}` | `{files['client']}` | `{files['reference']}` |"
                )
                feature_lines.append(
                    f"- **{title}**：`{method} {path}`，调用 `{files['client']}`，字段 `{files['reference']}`"
                )
            controller_lines.append("")
            controller_path.write_text("\n".join(controller_lines), encoding="utf-8")
            feature_lines.extend(
                [
                    "",
                    f"Controller 汇总：`{rel(controller_path, output_root)}`",
                    "",
                ]
            )

    save_json(output_root / "config" / "domains.json", domains)
    write_skill_common(output_root, documents)
    write_field_index(output_root, documents)
    (output_root / "FEATURES.md").write_text("\n".join(feature_lines).rstrip() + "\n", encoding="utf-8")


def validate_sources(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate and normalize sources config."""

    sources = config.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources.json 必须包含非空 sources 数组")
    normalized: list[dict[str, Any]] = []
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            raise ValueError(f"sources[{index}] 必须是对象")
        item = dict(source)
        item["id"] = safe_name(str(item.get("id") or item.get("name") or f"source_{index}"))
        normalized.append(item)
    return normalized


def choose_output_mode(requested_mode: str, source_count: int) -> str:
    """Choose output mode, asking the user when multiple links need a decision."""

    if requested_mode in {"combined", "separate"}:
        return requested_mode
    if source_count <= 1:
        return "separate"
    if not sys.stdin.isatty():
        raise ValueError(
            "检测到多个接口文档链接，请显式指定 --output-mode combined 或 --output-mode separate"
        )

    print("检测到多个接口文档链接，请选择产出方式：")
    print("1. combined：合并产出 1 个 skill")
    print("2. separate：按每个链接分别产出多个 skills")
    while True:
        choice = input("请输入 1 或 2：").strip()
        if choice == "1":
            return "combined"
        if choice == "2":
            return "separate"
        print("输入无效，请输入 1 或 2。")


def generated_skill_dir(base_output_root: Path, skill_name: str) -> Path:
    """Return the directory for one generated business skill."""

    return base_output_root / safe_name(skill_name, "swagger_skills")


def main() -> int:
    """CLI entry point."""

    args = parse_args()
    output_root = Path(args.output).resolve()
    sources_path = Path(args.sources).resolve()
    if not sources_path.exists():
        example = output_root / "config" / "sources.example.json"
        raise FileNotFoundError(
            f"未找到 {sources_path}。请先复制 {example} 为 sources.json 并填写 Swagger 链接。"
        )

    config = load_json(sources_path)
    sources = validate_sources(config)
    config["source_by_id"] = {source["id"]: source for source in sources}
    output_mode = choose_output_mode(args.output_mode, len(sources))

    if args.clean_generated:
        clean_generated(output_root)

    documents: list[dict[str, Any]] = []
    defaults = config.get("defaults", {})
    for source in sources:
        print(f"Discovering spec: {source.get('name') or source['id']}")
        spec, spec_url = discover_spec(source, defaults)
        documents.append(normalize_spec(spec, source, spec_url))

    generated_roots: list[Path] = []
    if output_mode == "combined":
        skill_name = safe_name(args.combined_name, "combined_swagger_skills")
        skill_root = generated_skill_dir(output_root, skill_name)
        combined_config = dict(config)
        combined_config["skill_name"] = skill_name
        generate_files(skill_root, documents, combined_config)
        generated_roots.append(skill_root)
    else:
        for document in documents:
            skill_name = f"{document['document_id']}-swagger-skills"
            skill_root = generated_skill_dir(output_root, skill_name)
            separate_config = dict(config)
            separate_config["skill_name"] = skill_name
            generate_files(skill_root, [document], separate_config)
            generated_roots.append(skill_root)

    print("Generated skill(s):")
    for root in generated_roots:
        print(f"- {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
