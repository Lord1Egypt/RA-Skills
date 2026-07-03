from __future__ import annotations

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

from .constants import *

def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_name(value: str) -> str:
    parts: list[str] = []
    pending_separator = False
    for char in value.strip().lower():
        if (ord(char) < 128 and char.isalnum()) or is_cjk_char(char):
            if pending_separator and parts:
                parts.append("-")
            parts.append(char)
            pending_separator = False
        else:
            pending_separator = bool(parts)
    return "".join(parts).strip("-")


def normalize_pathish(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    resolved = Path(text).expanduser().resolve()
    normalized = os.path.normcase(os.path.normpath(str(resolved)))
    return normalized.replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_cjk_char(char: str) -> bool:
    code = ord(char)
    return (
        0x3400 <= code <= 0x4DBF
        or 0x3040 <= code <= 0x309F
        or 0x30A0 <= code <= 0x30FF
        or 0x31F0 <= code <= 0x31FF
        or 0x4E00 <= code <= 0x9FFF
        or 0xAC00 <= code <= 0xD7AF
        or 0x1100 <= code <= 0x11FF
        or 0x3130 <= code <= 0x318F
        or 0xA960 <= code <= 0xA97F
        or 0xD7B0 <= code <= 0xD7FF
        or 0xF900 <= code <= 0xFAFF
        or 0x20000 <= code <= 0x2A6DF
        or 0x2A700 <= code <= 0x2B73F
        or 0x2B740 <= code <= 0x2B81F
        or 0x2B820 <= code <= 0x2CEAF
    )


def estimate_context_units(text: str) -> int:
    if not text:
        return 0
    ascii_chars = 0
    cjk_chars = 0
    other_chars = 0
    for char in text:
        if ord(char) < 128:
            ascii_chars += 1
        elif is_cjk_char(char):
            cjk_chars += 1
        else:
            other_chars += 1
    return math.ceil(
        ascii_chars / TEXT_BYTES_PER_CONTEXT_UNIT
        + cjk_chars * CJK_CONTEXT_UNITS_PER_CHAR
        + other_chars * NON_ASCII_CONTEXT_UNITS_PER_CHAR
    )


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def sorted_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix())


def strip_yaml_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_inline_sequence(value: str) -> list[object] | None:
    inner = value[1:-1].strip()
    if not inner:
        return []
    items: list[str] = []
    current: list[str] = []
    quote: str | None = None
    bracket_depth = 0
    for char in inner:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            current.append(char)
            continue
        if char == "[":
            bracket_depth += 1
            current.append(char)
            continue
        if char == "]":
            if bracket_depth == 0:
                return None
            bracket_depth -= 1
            current.append(char)
            continue
        if char == "," and bracket_depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
            continue
        current.append(char)
    if quote or bracket_depth:
        return None
    item = "".join(current).strip()
    if item:
        items.append(item)
    return [
        parse_frontmatter_scalar(item) if item.startswith("[") and item.endswith("]") else strip_yaml_quotes(item)
        for item in items
    ]


def parse_frontmatter_scalar(value: str) -> object:
    value = strip_yaml_quotes(value)
    stripped = value.strip()
    if stripped[:1] in {"{", "["} and stripped[-1:] in {"}", "]"}:
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            if stripped.startswith("["):
                parsed_sequence = parse_inline_sequence(stripped)
                if parsed_sequence is not None:
                    return parsed_sequence
            return value
    return value


def safe_frontmatter_mapping(raw_yaml: str) -> dict[str, object] | None:
    if yaml is None:
        return None
    try:
        data = yaml.safe_load(raw_yaml) or {}
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return {str(key): json_safe_value(value) for key, value in data.items()}


def fallback_frontmatter_mapping(raw_yaml: str) -> dict[str, object]:
    yaml_lines = raw_yaml.splitlines()

    def line_indent(value: str) -> int:
        return len(value) - len(value.lstrip(" "))

    def next_content_index(index: int) -> int | None:
        while index < len(yaml_lines):
            stripped = yaml_lines[index].strip()
            if stripped and not stripped.startswith("#"):
                return index
            index += 1
        return None

    def parse_block(index: int, indent: int) -> tuple[object, int]:
        mapping: dict[str, object] = {}
        sequence: list[object] = []
        mode: str | None = None
        while index < len(yaml_lines):
            line = yaml_lines[index]
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                index += 1
                continue
            current_indent = line_indent(line)
            if current_indent < indent:
                break
            if current_indent > indent:
                break
            if stripped.startswith("- "):
                mode = mode or "sequence"
                if mode != "sequence":
                    break
                raw_item = stripped[2:].strip()
                index += 1
                if raw_item:
                    sequence.append(parse_frontmatter_scalar(raw_item))
                else:
                    nested, index = parse_block(index, indent + 2)
                    sequence.append(nested)
                continue
            if ":" not in stripped:
                break
            mode = mode or "mapping"
            if mode != "mapping":
                break
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            index += 1
            if raw_value in {">", "|"}:
                parts: list[str] = []
                while index < len(yaml_lines):
                    part_line = yaml_lines[index]
                    part_stripped = part_line.strip()
                    if part_stripped and line_indent(part_line) <= current_indent:
                        break
                    if part_stripped:
                        parts.append(part_stripped)
                    index += 1
                mapping[key] = (" " if raw_value == ">" else "\n").join(parts)
                continue
            if raw_value:
                mapping[key] = parse_frontmatter_scalar(raw_value)
                continue
            content_index = next_content_index(index)
            if content_index is None or line_indent(yaml_lines[content_index]) <= current_indent:
                mapping[key] = {}
                continue
            nested, index = parse_block(index, line_indent(yaml_lines[content_index]))
            mapping[key] = nested
        if mode == "sequence":
            return sequence, index
        return mapping, index

    parsed, _index = parse_block(0, 0)
    return parsed if isinstance(parsed, dict) else {}


def json_safe_value(value):
    if isinstance(value, dict):
        return {str(key): json_safe_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Parse frontmatter fields needed for skill discovery."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, text

    raw_yaml = "".join(lines[1:end_index])
    body = "".join(lines[end_index + 1 :]).lstrip("\r\n")
    parsed = safe_frontmatter_mapping(raw_yaml)
    if parsed is not None:
        return parsed, body

    return fallback_frontmatter_mapping(raw_yaml), body


def mapping_from_value(value) -> dict[str, object]:
    if isinstance(value, dict):
        return {str(key): json_safe_value(item) for key, item in value.items()}
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return {}
            if isinstance(parsed, dict):
                return {str(key): json_safe_value(item) for key, item in parsed.items()}
    return {}


def first_metadata_value(mapping: dict[str, object], keys: tuple[str, ...]) -> object | None:
    lowered = {str(key).lower(): value for key, value in mapping.items()}
    for key in keys:
        if key in mapping:
            return mapping[key]
        lowered_key = key.lower()
        if lowered_key in lowered:
            return lowered[lowered_key]
    return None


def looks_like_env_name(value: str, *, allow_camel_case: bool = False) -> bool:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        return False
    lowered = value.lower()
    if value.upper() == value or lowered.endswith(("_key", "_token", "_secret")):
        return True
    return allow_camel_case and lowered.endswith(("key", "token", "secret"))


def append_required_env(target: list[str], value: object) -> None:
    if value is None or value is False:
        return
    if isinstance(value, str):
        parts = re.split(r"[,;\s]+", value.strip())
        for part in parts:
            name = part.strip()
            if name and looks_like_env_name(name, allow_camel_case=True) and name not in target:
                target.append(name)
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            append_required_env(target, item)
        return
    if isinstance(value, dict):
        for explicit_key in ("env", "env_var", "envVar", "key", "variable", "name"):
            explicit = first_metadata_value(value, (explicit_key,))
            if explicit is None:
                continue
            before = len(target)
            append_required_env(target, explicit)
            if len(target) > before:
                return
        for key, item in value.items():
            key_text = str(key)
            if looks_like_env_name(key_text) and item is not False:
                append_required_env(target, key_text)


def required_env_from_requires(value: object) -> list[str]:
    env_names: list[str] = []
    if isinstance(value, dict):
        for key in (
            "env",
            "envs",
            "env_vars",
            "envVars",
            "environment",
            "environment_variables",
            "environmentVariables",
            "secrets",
            "apiKeys",
            "api_keys",
        ):
            append_required_env(env_names, first_metadata_value(value, (key,)))
    else:
        append_required_env(env_names, value)
    return env_names


def skill_required_env(frontmatter: dict[str, object], registry_metadata: dict[str, object]) -> list[str]:
    env_names: list[str] = []

    def extend(value: object) -> None:
        for name in required_env_from_requires(value):
            if name not in env_names:
                env_names.append(name)

    metadata = frontmatter_metadata(frontmatter)
    openclaw = openclaw_metadata(frontmatter)
    for source in (openclaw, metadata, registry_metadata):
        if not isinstance(source, dict):
            continue
        extend(first_metadata_value(source, ("requires",)))
        extend(source)
    extend(first_metadata_value(frontmatter, ("requires",)))
    return env_names


def env_value_is_configured(name: str) -> bool:
    return bool(os.getenv(name))


def missing_required_env(required_env: list[str]) -> list[str]:
    return [name for name in required_env if not env_value_is_configured(name)]


def load_skill_registry_metadata(root: Path) -> dict[str, object]:
    meta_path = root / "_meta.json"
    if not meta_path.exists():
        return {}
    try:
        payload = json.loads(read_text(meta_path))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(payload, dict):
        return {}
    return {str(key): json_safe_value(value) for key, value in payload.items()}


def frontmatter_metadata(frontmatter: dict[str, object]) -> dict[str, object]:
    return mapping_from_value(frontmatter.get("metadata"))


def openclaw_metadata(frontmatter: dict[str, object]) -> dict[str, object]:
    metadata = frontmatter_metadata(frontmatter)
    return mapping_from_value(first_metadata_value(metadata, ("openclaw",)))


def skill_install_identity(
    root: Path,
    frontmatter: dict[str, object],
    registry_metadata: dict[str, object] | None = None,
) -> str | None:
    identities = skill_install_identities(root, frontmatter, registry_metadata)
    return identities[0] if identities else None


def skill_install_identities(
    root: Path,
    frontmatter: dict[str, object],
    registry_metadata: dict[str, object] | None = None,
) -> list[str]:
    identities: list[str] = []

    def append_identity(value: str) -> None:
        if value and value not in identities:
            identities.append(value)

    registry = registry_metadata if registry_metadata is not None else load_skill_registry_metadata(root)
    if registry:
        slug = normalize_name(str(first_metadata_value(registry, ("slug", "skillKey", "skill_key", "name")) or ""))
        owner = normalize_name(str(first_metadata_value(registry, ("ownerId", "owner_id", "owner")) or ""))
        if slug:
            append_identity(f"clawhub:{owner}:{slug}" if owner else f"skill:{slug}")

    openclaw = openclaw_metadata(frontmatter)
    skill_key = normalize_name(str(first_metadata_value(openclaw, ("skillKey", "skill_key")) or ""))
    if skill_key:
        append_identity(f"skill:{skill_key}")

    return identities


def skill_install_identity_from_file(skill_md: Path) -> str | None:
    identities = skill_install_identities_from_file(skill_md)
    return identities[0] if identities else None


def skill_install_identities_from_file(skill_md: Path) -> list[str]:
    try:
        text = read_text(skill_md)
    except OSError:
        return []
    frontmatter, _body = parse_frontmatter(text)
    return skill_install_identities(skill_md.parent, frontmatter)


def extract_terms(text: str) -> set[str]:
    raw_terms = re.findall(r"[a-z0-9][a-z0-9+.]*|[\u4e00-\u9fff]{1,}", text.lower().replace("-", " "))
    terms = set()
    for term in raw_terms:
        if term in STOPWORDS:
            continue
        if term.isascii() and len(term) == 1:
            continue
        terms.add(term)
    return terms


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def guess_source(path: Path) -> str:
    joined = "/".join(part.lower() for part in path.parts)
    if "/.system/" in joined:
        return "system"
    if "/plugins/cache/" in joined:
        return "plugin"
    if "/skills/" in joined:
        return "user"
    return "other"


def guess_namespace(path: Path) -> str:
    lowered = [part.lower() for part in path.parts]
    if "plugins" in lowered and "cache" in lowered:
        cache_index = lowered.index("cache")
        if cache_index + 2 < len(path.parts):
            return normalize_name(path.parts[cache_index + 2])
    for host_marker, namespace in (
        (".openclaw", "openclaw"),
        (".agents", "agents"),
    ):
        if host_marker in lowered:
            return namespace
    source = guess_source(path)
    if source in {"system", "user"}:
        return source
    return "other"

def parse_dateish(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        stamp = float(value)
        if stamp > 1_000_000_000_000:
            stamp = stamp / 1000.0
        try:
            return datetime.fromtimestamp(stamp, tz=timezone.utc).date()
        except (OverflowError, OSError, ValueError):
            return None
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None

    normalized = text.replace("Z", "+00:00").replace("z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def normalize_dateish(value) -> str | None:
    parsed = parse_dateish(value)
    if parsed is None:
        return None
    return parsed.isoformat()


def days_since(value) -> int | None:
    parsed = parse_dateish(value)
    if parsed is None:
        return None
    return (date.today() - parsed).days


def load_json_or_jsonl(path: Path):
    text = read_text(path)
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return json.loads(text)


def coerce_int(value) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return None
    return None


def coerce_float(value) -> float | None:
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def current_script_relative_to(root: Path) -> Path | None:
    try:
        return Path(__file__).resolve().relative_to(root.resolve())
    except ValueError:
        return None


def coerce_bool(value) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1", "pass", "passed", "success", "succeeded", "ok", "成功", "通过"}:
            return True
        if lowered in {"false", "no", "0", "fail", "failed", "error", "errored", "失败", "未通过"}:
            return False
    return None


def lowered_mapping(mapping: dict) -> dict[str, object]:
    return {str(key).lower(): value for key, value in mapping.items()}


def first_present(
    mapping: dict,
    keys: tuple[str, ...] | list[str],
    lowered: dict[str, object] | None = None,
) -> object | None:
    if lowered is None:
        lowered = lowered_mapping(mapping)
    for key in keys:
        if key in mapping:
            return mapping[key]
        if key.lower() in lowered:
            return lowered[key.lower()]
    return None


def extract_record_identity(mapping: dict, hint_name: str | None = None) -> dict[str, str]:
    lowered = lowered_mapping(mapping)
    explicit_name = normalize_name(str(first_present(mapping, NAME_KEYS, lowered) or ""))
    slug = normalize_name(str(first_present(mapping, SLUG_KEYS, lowered) or ""))
    identifier = normalize_name(str(first_present(mapping, IDENTIFIER_KEYS, lowered) or ""))
    source = normalize_name(str(first_present(mapping, SOURCE_KEYS, lowered) or ""))
    namespace = normalize_name(str(first_present(mapping, NAMESPACE_KEYS, lowered) or ""))
    path = normalize_pathish(first_present(mapping, PATH_KEYS, lowered)) or ""
    name = explicit_name or slug or identifier or normalize_name(str(hint_name or ""))
    return {
        "name": name,
        "slug": slug,
        "identifier": identifier,
        "source": source,
        "namespace": namespace,
        "path": path,
    }


def record_lookup_key(identity: dict[str, str]) -> str | None:
    if identity["path"]:
        return f"path:{identity['path']}"
    if identity["namespace"] and identity["slug"]:
        return f"namespace:{identity['namespace']}:{identity['slug']}"
    if identity["namespace"] and identity["name"]:
        return f"namespace:{identity['namespace']}:{identity['name']}"
    if identity["source"] and identity["slug"]:
        return f"source:{identity['source']}:{identity['slug']}"
    if identity["source"] and identity["name"]:
        return f"source:{identity['source']}:{identity['name']}"
    if identity["slug"]:
        return f"slug:{identity['slug']}"
    if identity["identifier"]:
        return f"id:{identity['identifier']}"
    if identity["name"]:
        return f"name:{identity['name']}"
    return None


def skill_lookup_keys(skill: dict[str, object]) -> list[str]:
    keys = [f"path:{normalize_pathish(skill['path'])}"]
    namespace = str(skill.get("namespace") or "")
    source = str(skill.get("source") or "")
    slug = str(skill.get("slug") or "")
    name = str(skill.get("name") or "")
    if namespace and slug:
        keys.append(f"namespace:{namespace}:{slug}")
    if namespace and name:
        keys.append(f"namespace:{namespace}:{name}")
    if source and slug:
        keys.append(f"source:{source}:{slug}")
    if source and name:
        keys.append(f"source:{source}:{name}")
    if slug:
        keys.append(f"slug:{slug}")
    if name:
        keys.append(f"name:{name}")
    return [key for key in keys if key]


def resolve_record(
    store: dict[str, dict[str, object]],
    skill: dict[str, object],
    alias_counts: Counter[str],
) -> tuple[dict[str, object] | None, str | None]:
    collision_scopes: list[str] = []
    for key in skill_lookup_keys(skill):
        if alias_counts.get(key, 0) > 1:
            if key in store:
                collision_scopes.append(key.split(":", 1)[0])
            continue
        record = store.get(key)
        if record is not None:
            return record, None
    if collision_scopes:
        ordered_scopes = ", ".join(sorted(set(collision_scopes)))
        return None, f"ambiguous {ordered_scopes} evidence; provide path, namespace, or source"
    return None, None


def skill_display_name(skill: dict[str, object], alias_counts: Counter[str]) -> str:
    name = str(skill["name"])
    if alias_counts.get(f"name:{name}", 0) <= 1:
        return name
    namespace = str(skill.get("namespace") or "")
    if namespace and namespace not in {"system", "user", "other"}:
        return f"{name}@{namespace}"
    parent_hint = normalize_name(Path(str(skill["path"])).parent.name)
    if parent_hint and parent_hint not in {"skills", ".system"}:
        return f"{name}@{parent_hint}"
    return f"{name}@{skill['source']}"
