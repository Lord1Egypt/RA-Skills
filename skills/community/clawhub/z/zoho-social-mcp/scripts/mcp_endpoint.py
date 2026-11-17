#!/usr/bin/env python3
"""Portable endpoint resolution for Zoho MCP helper CLIs.

Resolution order for the MCP URL:
1. --mcp-url
2. --profile (or an app-specific/generic profile environment variable)
3. the app-specific endpoint environment variable(s)

Optional organization IDs follow the same cascade:
1. --organization-id
2. the selected profile's organization_id
3. ZOHO_<SERVICE>_ORGANIZATION_ID, then ZOHO_ORGANIZATION_ID

Profile files are local configuration and must never be committed with real URLs.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit


DEFAULT_PROFILES_FILE = "~/.config/zoho-mcp/profiles.json"
_PROFILE_ENV = "ZOHO_MCP_PROFILE"
_PROFILES_FILE_ENV = "ZOHO_MCP_PROFILES_FILE"
_ORG_ENV = "ZOHO_ORGANIZATION_ID"
_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_ORG_ID = re.compile(r"^[A-Za-z0-9_-]+$")
_SERVICE_LABELS = {"crm": "CRM", "people": "People", "books": "Books", "desk": "Desk", "workdrive": "WorkDrive", "social": "Social"}


class EndpointResolutionError(RuntimeError):
    """Raised when an MCP endpoint cannot be resolved safely."""


def add_endpoint_arguments(parser, include_organization_id=False):
    """Add shared multi-account endpoint options to an argparse parser."""
    group = parser.add_argument_group("MCP endpoint selection")
    group.add_argument(
        "--mcp-url",
        metavar="URL",
        help="use this endpoint for this invocation (highest priority; credential may be visible in process listings)",
    )
    group.add_argument(
        "--profile",
        metavar="NAME",
        help="select a named account from the Zoho MCP profiles file",
    )
    group.add_argument(
        "--profiles-file",
        metavar="PATH",
        help=f"profiles JSON path (default: {_PROFILES_FILE_ENV} or {DEFAULT_PROFILES_FILE})",
    )
    if include_organization_id:
        group.add_argument(
            "--organization-id",
            metavar="ID",
            help="Zoho organization ID for this invocation",
        )
    return parser


def _option(args, name):
    return getattr(args, name, None) if args is not None else None


def _validate_url(value, source):
    value = str(value or "").strip()
    if not value:
        raise EndpointResolutionError(f"{source} is empty")
    if any(char.isspace() for char in value):
        raise EndpointResolutionError(f"{source} contains whitespace")
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise EndpointResolutionError(f"{source} must be an absolute HTTP(S) URL")
    return value


def _validate_organization_id(value, source):
    value = str(value or "").strip()
    if not value:
        raise EndpointResolutionError(f"{source} is empty")
    if not _ORG_ID.fullmatch(value):
        raise EndpointResolutionError(f"{source} is not a valid organization ID")
    return value


def _service_label(service):
    return _SERVICE_LABELS.get(service, service.title())


def _profile_name(args, service, environ):
    explicit = _option(args, "profile")
    if explicit:
        return explicit
    app_env = f"ZOHO_{service.upper()}_MCP_PROFILE"
    return environ.get(app_env) or environ.get(_PROFILE_ENV)


def _profiles_path(args, environ):
    raw = _option(args, "profiles_file") or environ.get(_PROFILES_FILE_ENV) or DEFAULT_PROFILES_FILE
    return Path(raw).expanduser()


def _load_profiles(path):
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EndpointResolutionError(f"profiles file not found: {path}") from exc
    except OSError as exc:
        raise EndpointResolutionError(f"profiles file cannot be read: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EndpointResolutionError(
            f"profiles file is invalid JSON at line {exc.lineno}, column {exc.colno}: {path}"
        ) from exc

    if not isinstance(document, dict):
        raise EndpointResolutionError("profiles file root must be a JSON object")
    version = document.get("version", 1)
    if version != 1:
        raise EndpointResolutionError(f"unsupported profiles file version: {version}")
    profiles = document.get("profiles")
    if not isinstance(profiles, dict):
        raise EndpointResolutionError("profiles file must contain a 'profiles' object")
    return profiles


def load_profile_service(args, service, environ=None):
    """Return (profile_name, service_config, profile_file) or (None, None, None)."""
    environ = os.environ if environ is None else environ
    name = _profile_name(args, service, environ)
    if not name:
        return None, None, None

    path = _profiles_path(args, environ)
    profiles = _load_profiles(path)
    profile = profiles.get(name)
    if not isinstance(profile, dict):
        raise EndpointResolutionError(f"profile '{name}' not found in {path}")

    services = profile.get("services", profile)
    if not isinstance(services, dict):
        raise EndpointResolutionError(f"profile '{name}' has no services object")
    config = services.get(service)
    if isinstance(config, str):
        config = {"url": config}
    if not isinstance(config, dict):
        raise EndpointResolutionError(
            f"profile '{name}' has no '{service}' service in {path}"
        )
    return name, config, path


def _resolve_profile_url(profile_name, config, path, environ):
    sources = [key for key in ("url", "env", "url_file") if config.get(key)]
    if len(sources) != 1:
        raise EndpointResolutionError(
            f"profile '{profile_name}' must define exactly one of url, env, or url_file"
        )

    source = sources[0]
    if source == "url":
        value = config["url"]
        label = f"profile '{profile_name}' url"
    elif source == "env":
        env_name = str(config["env"])
        if not _ENV_NAME.fullmatch(env_name):
            raise EndpointResolutionError(
                f"profile '{profile_name}' contains an invalid environment variable name"
            )
        value = environ.get(env_name)
        if not value:
            raise EndpointResolutionError(
                f"profile '{profile_name}' requires environment variable {env_name}"
            )
        label = f"environment variable {env_name}"
    else:
        url_path = Path(str(config["url_file"])).expanduser()
        if not url_path.is_absolute():
            url_path = path.parent / url_path
        try:
            value = url_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise EndpointResolutionError(
                f"profile '{profile_name}' URL file cannot be read: {url_path}"
            ) from exc
        label = f"profile '{profile_name}' URL file"

    return _validate_url(value, label)


def resolve_mcp_url(args, service, env_vars, environ=None):
    """Resolve one MCP URL without printing or returning its source credentials."""
    environ = os.environ if environ is None else environ

    explicit = _option(args, "mcp_url")
    if explicit:
        return _validate_url(explicit, "--mcp-url")

    profile_name, profile_config, profile_path = load_profile_service(
        args, service, environ=environ
    )
    if profile_name:
        return _resolve_profile_url(
            profile_name, profile_config, profile_path, environ
        )

    for env_name in env_vars:
        value = environ.get(env_name)
        if value:
            return _validate_url(value, f"environment variable {env_name}")

    app_profile_env = f"ZOHO_{service.upper()}_MCP_PROFILE"
    env_help = " or ".join(env_vars)
    raise EndpointResolutionError(
        f"no Zoho {_service_label(service)} MCP endpoint configured; use --mcp-url, "
        f"--profile (or {app_profile_env}/{_PROFILE_ENV}), or set {env_help}"
    )


def resolve_organization_id(args, service, environ=None, required=False):
    """Resolve an optional or required Zoho organization ID."""
    environ = os.environ if environ is None else environ

    explicit = _option(args, "organization_id")
    if explicit:
        return _validate_organization_id(explicit, "--organization-id")

    profile_name, profile_config, _profile_path = load_profile_service(
        args, service, environ=environ
    )
    if profile_name and profile_config.get("organization_id"):
        return _validate_organization_id(
            profile_config["organization_id"],
            f"profile '{profile_name}' organization_id",
        )

    for env_name in (f"ZOHO_{service.upper()}_ORGANIZATION_ID", _ORG_ENV):
        value = environ.get(env_name)
        if value:
            return _validate_organization_id(value, f"environment variable {env_name}")

    if required:
        raise EndpointResolutionError(
            f"no Zoho {_service_label(service)} organization ID configured; use "
            f"--organization-id, a profile organization_id, or set "
            f"ZOHO_{service.upper()}_ORGANIZATION_ID"
        )
    return None


class EndpointSelector:
    """Holds CLI selection state and resolves lazily on the first real call."""

    def __init__(self, service, env_vars, require_organization_id=False):
        self.service = service
        self.env_vars = tuple(env_vars)
        self.require_organization_id = require_organization_id
        self.args = None
        self._cached_url = None
        self._cached_org = None
        self._org_resolved = False

    def configure(self, args):
        self.args = args
        self._cached_url = None
        self._cached_org = None
        self._org_resolved = False

    def get(self):
        if self._cached_url is None:
            self._cached_url = resolve_mcp_url(
                self.args,
                service=self.service,
                env_vars=self.env_vars,
            )
        return self._cached_url

    def organization_id(self):
        if not self._org_resolved:
            self._cached_org = resolve_organization_id(
                self.args,
                service=self.service,
                required=self.require_organization_id,
            )
            self._org_resolved = True
        return self._cached_org
