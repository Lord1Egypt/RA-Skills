"""
Persistent configuration manager and schema validation for Security Maintainer.
"""

from __future__ import annotations
import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "default_config.json"
USER_CONFIG_DIR = Path.home() / ".security-maintainer"
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.json"


def _parse_yaml_minimal(content: str) -> Dict[str, Any]:
    """Basic fallback YAML parser when pyyaml is not installed."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Si pyyaml está disponible, usarlo
    if HAS_YAML:
        return yaml.safe_load(content)

    # Parser de emergencia para subconjunto simple de YAML
    result: Dict[str, Any] = {}
    lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().strip('"').strip("'")
            val = val.strip().strip('"').strip("'")
            if val.lower() == "true":
                result[key] = True
            elif val.lower() == "false":
                result[key] = False
            elif val.isdigit():
                result[key] = int(val)
            elif val:
                result[key] = val
    return result


class ConfigManager:
    """Gestiona la lectura, validación y migración de la configuración."""

    def __init__(self, custom_path: Optional[str] = None):
        self.custom_path = custom_path
        self.config: Dict[str, Any] = self.load()

    def load(self) -> Dict[str, Any]:
        """Carga la configuración combinando defaults con el archivo de usuario."""
        # 1. Cargar configuración base por defecto
        base_config: Dict[str, Any] = {}
        if DEFAULT_CONFIG_PATH.exists():
            with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
                base_config = json.load(f)

        # 2. Localizar archivo de configuración del usuario
        target_path: Optional[Path] = None
        if self.custom_path:
            target_path = Path(self.custom_path)
        elif os.environ.get("SECURITY_MAINTAINER_CONFIG"):
            target_path = Path(os.environ["SECURITY_MAINTAINER_CONFIG"])
        elif USER_CONFIG_FILE.exists():
            target_path = USER_CONFIG_FILE

        if target_path and target_path.exists():
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if HAS_YAML and (target_path.suffix in [".yaml", ".yml"]):
                        user_config = yaml.safe_load(content)
                    else:
                        try:
                            user_config = json.loads(content)
                        except json.JSONDecodeError:
                            user_config = _parse_yaml_minimal(content)
                    if isinstance(user_config, dict):
                        base_config = self._deep_merge(base_config, user_config)
            except Exception as e:
                # Loggear y usar base_config
                pass

        # Validar y migrar si es necesario
        migrated_config = self.migrate(base_config)
        return migrated_config

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(base)
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def migrate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Garantiza compatibilidad de esquemas entre versiones."""
        current_version = config.get("version", "1.0.0")
        # Asegurar campos críticos conservadores
        if "mode" not in config:
            config["mode"] = "ask"
        if "windows" not in config:
            config["windows"] = {"enabled": True, "allow_reboots": False, "excluded_packages": []}
        if "wsl" not in config:
            config["wsl"] = {"enabled": True, "auto_start_stopped_distros": False, "allow_reboots": False}
        if "execution" not in config:
            config["execution"] = {"max_actions_per_run": 25, "plan_validity_minutes": 30}
        return config

    def save_user_config(self, new_config: Dict[str, Any]) -> bool:
        """
        Saves user configuration to local disk (~/.security-maintainer/config.json).
        WARNING: Modifies persistent user preferences for subsequent runs.
        """
        USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(USER_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            self.config = new_config
            logger.info(f"Configuración guardada en archivo persistente de usuario: {USER_CONFIG_FILE}")
            return True
        except Exception as e:
            logger.warning(f"No se pudo guardar la configuración de usuario: {e}")
            return False

    @property
    def mode(self) -> str:
        return self.config.get("mode", "ask")

    @property
    def allow_reboots(self) -> bool:
        return bool(self.config.get("windows", {}).get("allow_reboots", False))

    @property
    def max_actions(self) -> int:
        return int(self.config.get("execution", {}).get("max_actions_per_run", 25))

    @property
    def plan_validity_minutes(self) -> int:
        return int(self.config.get("execution", {}).get("plan_validity_minutes", 30))
