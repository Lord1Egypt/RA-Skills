"""
Analizador de dependencias en proyectos de código registrados explícitamente.
NO escanea el disco indiscriminadamente ni modifica repositorios no registrados.
"""

from __future__ import annotations
import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models import (
    InventoryItem,
    EnvironmentType,
    ManagerType,
)

logger = logging.getLogger(__name__)


class RegisteredProjectsAdapter:
    """Inspecciona dependencias de proyectos Node.js y Python explícitamente autorizados."""

    def __init__(self, config: Dict[str, Any], fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("projects", {})
        self.fixture_data = fixture_data
        self.registered_paths = [Path(p) for p in self.config.get("registered_paths", [])]

    def collect(self) -> List[InventoryItem]:
        items: List[InventoryItem] = []

        if self.fixture_data and "project_items" in self.fixture_data:
            for it in self.fixture_data["project_items"]:
                items.append(
                    InventoryItem(
                        environment=EnvironmentType.PROJECT,
                        target_name=it.get("target", "Project"),
                        name=it.get("name", ""),
                        id=it.get("id", ""),
                        installed_version=it.get("version", "unknown"),
                        manager=ManagerType(it.get("manager", "node_env")),
                        is_supported=True,
                        update_mechanism_available=True,
                        notes=it.get("notes"),
                        extra_metadata=it.get("metadata", {})
                    )
                )
            return items

        for project_dir in self.registered_paths:
            if not project_dir.exists() or not project_dir.is_dir():
                continue

            target_name = f"Project:{project_dir.name}"

            # 1. Análisis de Node.js (package.json + package-lock.json)
            pkg_json = project_dir / "package.json"
            pkg_lock = project_dir / "package-lock.json"

            if pkg_json.exists():
                try:
                    with open(pkg_json, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

                    # Si existe package-lock.json, extraer versiones exactas resueltas
                    resolved_versions: Dict[str, str] = {}
                    if pkg_lock.exists():
                        try:
                            with open(pkg_lock, "r", encoding="utf-8") as lf:
                                lock_data = json.load(lf)
                                for p_name, p_info in lock_data.get("packages", {}).items():
                                    clean_name = p_name.replace("node_modules/", "")
                                    if clean_name in deps:
                                        resolved_versions[clean_name] = p_info.get("version", "")
                        except Exception:
                            pass

                    for dep_name, dep_spec in deps.items():
                        exact_ver = resolved_versions.get(dep_name, dep_spec.replace("^", "").replace("~", ""))
                        items.append(
                            InventoryItem(
                                environment=EnvironmentType.PROJECT,
                                target_name=target_name,
                                name=dep_name,
                                id=f"npm:{dep_name}",
                                installed_version=exact_ver,
                                manager=ManagerType.NODE_ENV,
                                is_supported=True,
                                update_mechanism_available=True,
                                extra_metadata={
                                    "project_path": str(project_dir),
                                    "ecosystem": "npm",
                                    "spec": dep_spec
                                }
                            )
                        )
                except Exception as e:
                    logger.warning(f"Error analizando {pkg_json}: {e}")

            # 2. Análisis de Python (requirements.txt o pyproject.toml)
            req_txt = project_dir / "requirements.txt"
            if req_txt.exists():
                try:
                    with open(req_txt, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            match = re.match(r"^([a-zA-Z0-9_\-\.]+)(?:==|>=|<=|~=)(.+)$", line)
                            if match:
                                p_name = match.group(1)
                                p_ver = match.group(2).strip()
                                items.append(
                                    InventoryItem(
                                        environment=EnvironmentType.PROJECT,
                                        target_name=target_name,
                                        name=p_name,
                                        id=f"pypi:{p_name}",
                                        installed_version=p_ver,
                                        manager=ManagerType.PYTHON_ENV,
                                        is_supported=True,
                                        update_mechanism_available=True,
                                        extra_metadata={
                                            "project_path": str(project_dir),
                                            "ecosystem": "PyPI"
                                        }
                                    )
                                )
                except Exception as e:
                    logger.warning(f"Error analizando {req_txt}: {e}")

        return items
