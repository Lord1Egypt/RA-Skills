"""Hermes external Skill directory discovery."""

import os
import re
from pathlib import Path


def read_hermes_external_dirs(home=None, env=None):
    """Read the documented YAML-list form of ``skills.external_dirs``."""
    environment = os.environ if env is None else env
    base = Path(home) if home is not None else Path(os.path.expanduser("~"))
    config = base / ".hermes" / "config.yaml"
    if not config.is_file():
        return []
    try:
        lines = config.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    output, in_skills, in_external = [], False, False
    for line in lines:
        clean = line.split("#", 1)[0]
        if re.match(r"^skills\s*:\s*$", clean):
            in_skills, in_external = True, False
            continue
        if in_skills and re.match(r"^\S", clean):
            in_skills, in_external = False, False
        if in_skills and re.match(r"^\s+external_dirs\s*:\s*$", clean):
            in_external = True
            continue
        if in_external:
            match = re.match(r"^\s*-\s*['\"]?(.+?)['\"]?\s*$", clean)
            if match:
                value = match.group(1)
                if env is None or environment is os.environ:
                    value = os.path.expandvars(value)
                else:
                    value = re.sub(
                        r"\$(\w+)|\$\{([^}]+)\}|%([^%]+)%",
                        lambda item: environment.get(
                            next(group for group in item.groups() if group is not None),
                            item.group(0)),
                        value)
                if home is None:
                    value = os.path.expanduser(value)
                elif value == "~" or value.startswith(("~/", "~\\")):
                    value = str(base) + value[1:]
                output.append(value)
            elif clean.strip():
                in_external = False
    return output
