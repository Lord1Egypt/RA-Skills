#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import venv


DEFAULT_SETTINGS_TEMPLATE = """# SherpaMind staged non-secret settings
# Runtime state lives under .SherpaMind/private/ outside the skill tree.
# Secrets are stored separately under .SherpaMind/private/secrets/.
SHERPADESK_API_BASE_URL=https://api.sherpadesk.com
SHERPADESK_ORG_KEY=
SHERPADESK_INSTANCE_KEY=
SHERPAMIND_NOTIFY_CHANNEL=
"""


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def workspace_root() -> Path:
    explicit = os.getenv("SHERPAMIND_WORKSPACE_ROOT")
    if explicit:
        return Path(explicit).resolve()
    repo = repo_root().resolve()
    if repo.parent.name == "skills":
        return repo.parent.parent.resolve()
    return Path.cwd().resolve()


def sherpamind_root() -> Path:
    return workspace_root() / ".SherpaMind"


def private_root() -> Path:
    return sherpamind_root() / "private"


def config_root() -> Path:
    return private_root() / "config"


def secrets_root() -> Path:
    return private_root() / "secrets"


def data_root() -> Path:
    return private_root() / "data"


def state_root() -> Path:
    return private_root() / "state"


def logs_root() -> Path:
    return private_root() / "logs"


def runtime_root() -> Path:
    return private_root() / "runtime"


def public_root() -> Path:
    return sherpamind_root() / "public"


def settings_file() -> Path:
    return config_root() / "settings.env"


def api_key_file() -> Path:
    return secrets_root() / "sherpadesk_api_key.txt"


def api_user_file() -> Path:
    return secrets_root() / "sherpadesk_api_user.txt"


def venv_python(venv_root: Path) -> Path:
    return venv_root / "bin" / "python"


def ensure_layout() -> None:
    for path in [
        sherpamind_root(),
        private_root(),
        config_root(),
        secrets_root(),
        data_root(),
        state_root(),
        logs_root(),
        runtime_root(),
        public_root(),
        public_root() / "exports",
        public_root() / "docs",
    ]:
        path.mkdir(parents=True, exist_ok=True)
    if not settings_file().exists():
        settings_file().write_text(DEFAULT_SETTINGS_TEMPLATE, encoding="utf-8")
    for path in [api_key_file(), api_user_file()]:
        if not path.exists():
            path.write_text("", encoding="utf-8")
            try:
                path.chmod(0o600)
            except OSError:
                pass


def ensure_venv(venv_root: Path) -> None:
    if venv_python(venv_root).exists():
        return
    venv_root.parent.mkdir(parents=True, exist_ok=True)
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_root)


def pip_install(venv_root: Path) -> None:
    python = venv_python(venv_root)
    requirements = repo_root() / "requirements.txt"
    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(requirements)], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "-e", str(repo_root())], check=True)


def main() -> int:
    ensure_layout()
    venv_root = runtime_root() / "venv"
    ensure_venv(venv_root)
    pip_install(venv_root)
    print(str(venv_python(venv_root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
