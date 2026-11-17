"""
Inventory and update adapter for macOS (Homebrew, Mac App Store, softwareupdate, and /Applications).
"""

from __future__ import annotations
import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models import (
    InventoryItem,
    EnvironmentType,
    ManagerType,
)

logger = logging.getLogger(__name__)


class MacOSInventoryAdapter:
    """Inspects and audits installed software on Apple macOS hosts."""

    def __init__(self, config: Dict[str, Any], fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("macos", {})
        self.fixture_data = fixture_data
        self.excluded = set(self.config.get("excluded_packages", []))

    def is_available(self) -> bool:
        if self.fixture_data is not None:
            return True
        import sys
        return sys.platform == "darwin"

    def collect(self) -> List[InventoryItem]:
        items: List[InventoryItem] = []
        target_name = "macOS Host"

        # 0. macOS Host Operating System
        items.append(self._collect_os_info(target_name))

        # 1. Homebrew Audit (CLI formulae and GUI casks)
        brew_items = self._collect_homebrew(target_name)
        items.extend(brew_items)

        # 2. Mac App Store Audit via 'mas'
        mas_items = self._collect_mas(target_name)
        items.extend(mas_items)

        # 3. Official macOS Updates Audit (softwareupdate)
        apple_updates = self._collect_apple_updates(target_name)
        items.extend(apple_updates)

        # 4. Desktop Applications in /Applications
        app_items = self._collect_applications_dir(target_name, items)
        items.extend(app_items)

        return items

    def _collect_os_info(self, target_name: str) -> InventoryItem:
        if self.fixture_data and "os_info" in self.fixture_data:
            os_data = self.fixture_data["os_info"]
            caption = os_data.get("caption", "Apple macOS")
            version = os_data.get("version", "macOS")
            build = os_data.get("build_number", "")
        else:
            import platform
            ver, _, _ = platform.mac_ver()
            caption = "Apple macOS"
            version = ver or "macOS"
            build = ""
            try:
                build_proc = subprocess.run(["sw_vers", "-buildVersion"], capture_output=True, text=True, timeout=5)
                if build_proc.returncode == 0:
                    build = build_proc.stdout.strip()
            except Exception:
                pass

        full_version = f"{version} (Build {build})" if build else version
        return InventoryItem(
            environment=EnvironmentType.MACOS,
            target_name=target_name,
            name="macOS Operating System",
            id="macos-host-os",
            installed_version=full_version,
            manager=ManagerType.APPLE_UPDATE,
            is_supported=True,
            update_mechanism_available=True,
            requires_manual_intervention=False,
            notes="Evaluated macOS host system.",
            extra_metadata={"caption": caption, "version": version, "build": build}
        )

    def _collect_homebrew(self, target_name: str) -> List[InventoryItem]:
        items: List[InventoryItem] = []
        if self.fixture_data and "brew_outdated" in self.fixture_data:
            data = self.fixture_data["brew_outdated"]
        else:
            brew_bin = shutil.which("brew")
            if not brew_bin:
                return items
            try:
                res = subprocess.run([brew_bin, "outdated", "--json=v2"], capture_output=True, text=True, timeout=20)
                if res.returncode == 0 and res.stdout.strip():
                    data = json.loads(res.stdout.strip())
                else:
                    return items
            except Exception as e:
                logger.warning(f"Error querying Homebrew on macOS: {e}")
                return items

        # CLI formulae
        for formula in data.get("formulae", []):
            name = formula.get("name", "")
            if name in self.excluded:
                continue
            curr_ver = formula.get("installed_versions", ["unknown"])[0] if formula.get("installed_versions") else "unknown"
            latest_ver = formula.get("current_version")
            items.append(
                InventoryItem(
                    environment=EnvironmentType.MACOS,
                    target_name=target_name,
                    name=name,
                    id=f"brew:{name}",
                    installed_version=curr_ver,
                    latest_version=latest_ver,
                    manager=ManagerType.HOMEBREW,
                    is_supported=True,
                    update_mechanism_available=True,
                    notes="CLI package managed by Homebrew on macOS"
                )
            )

        # GUI Casks (e.g., Brave, Chrome, Zoom, VSCode)
        for cask in data.get("casks", []):
            name = cask.get("name", "")
            if name in self.excluded:
                continue
            curr_ver = cask.get("installed_versions", ["unknown"])[0] if cask.get("installed_versions") else "unknown"
            latest_ver = cask.get("current_version")
            items.append(
                InventoryItem(
                    environment=EnvironmentType.MACOS,
                    target_name=target_name,
                    name=name,
                    id=f"brew-cask:{name}",
                    installed_version=curr_ver,
                    latest_version=latest_ver,
                    manager=ManagerType.HOMEBREW,
                    is_supported=True,
                    update_mechanism_available=True,
                    notes="macOS GUI application managed by Homebrew Cask"
                )
            )

        return items

    def _collect_mas(self, target_name: str) -> List[InventoryItem]:
        items: List[InventoryItem] = []
        if self.fixture_data and "mas_outdated" in self.fixture_data:
            for entry in self.fixture_data["mas_outdated"]:
                items.append(
                    InventoryItem(
                        environment=EnvironmentType.MACOS,
                        target_name=target_name,
                        name=entry.get("name", ""),
                        id=f"mas:{entry.get('id', '')}",
                        installed_version=entry.get("installed_version", "unknown"),
                        latest_version=entry.get("latest_version"),
                        manager=ManagerType.MAS,
                        is_supported=True,
                        update_mechanism_available=True,
                        notes="Mac App Store application"
                    )
                )
            return items

        mas_bin = shutil.which("mas")
        if not mas_bin:
            return items

        try:
            res = subprocess.run([mas_bin, "outdated"], capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        app_id = parts[0]
                        app_name = " ".join(parts[1:-2])
                        curr_ver = parts[-2]
                        latest_ver = parts[-1]
                        items.append(
                            InventoryItem(
                                environment=EnvironmentType.MACOS,
                                target_name=target_name,
                                name=app_name,
                                id=f"mas:{app_id}",
                                installed_version=curr_ver,
                                latest_version=latest_ver,
                                manager=ManagerType.MAS,
                                is_supported=True,
                                update_mechanism_available=True,
                                notes="Mac App Store application"
                            )
                        )
        except Exception:
            pass
        return items

    def _collect_apple_updates(self, target_name: str) -> List[InventoryItem]:
        items: List[InventoryItem] = []
        if self.fixture_data and "softwareupdate" in self.fixture_data:
            for entry in self.fixture_data["softwareupdate"]:
                items.append(
                    InventoryItem(
                        environment=EnvironmentType.MACOS,
                        target_name=target_name,
                        name=entry.get("name", ""),
                        id=f"apple:{entry.get('id', '')}",
                        installed_version="pending",
                        latest_version="available",
                        manager=ManagerType.APPLE_UPDATE,
                        is_supported=True,
                        update_mechanism_available=True,
                        notes="Official macOS operating system update"
                    )
                )
            return items

        if shutil.which("softwareupdate"):
            try:
                res = subprocess.run(["softwareupdate", "-l"], capture_output=True, text=True, timeout=30)
                if "No new software available" not in res.stderr and "No new software available" not in res.stdout:
                    for line in (res.stdout + res.stderr).splitlines():
                        if "*" in line:
                            title = line.replace("*", "").strip()
                            items.append(
                                InventoryItem(
                                    environment=EnvironmentType.MACOS,
                                    target_name=target_name,
                                    name=title,
                                    id=f"apple:{title.split()[0]}",
                                    installed_version="pending",
                                    latest_version="available",
                                    manager=ManagerType.APPLE_UPDATE,
                                    is_supported=True,
                                    update_mechanism_available=True,
                                    notes="Official macOS operating system update"
                                )
                            )
            except Exception:
                pass
        return items

    def _collect_applications_dir(self, target_name: str, existing_items: List[InventoryItem]) -> List[InventoryItem]:
        items: List[InventoryItem] = []
        if self.fixture_data and "applications" in self.fixture_data:
            apps_data = self.fixture_data["applications"]
            for a in apps_data:
                name = a.get("name", "")
                if name in self.excluded:
                    continue
                items.append(
                    InventoryItem(
                        environment=EnvironmentType.MACOS,
                        target_name=target_name,
                        name=name,
                        id=a.get("id", f"app:{name.lower()}"),
                        installed_version=a.get("installed_version", "unknown"),
                        manager=ManagerType.MANUAL,
                        is_supported=False,
                        update_mechanism_available=False,
                        requires_manual_intervention=True,
                        notes="Application in /Applications without automated package manager.",
                        extra_metadata={"bundle_id": a.get("bundle_id")}
                    )
                )
            return items

        try:
            existing_names = {i.name.lower() for i in existing_items}
            existing_ids = {i.id.lower() for i in existing_items}

            # Inspect applications using mdfind if available or folder names to avoid plist parsing hooks
            app_dir = Path("/Applications")
            if app_dir.exists():
                for app_entry in app_dir.iterdir():
                    if not app_entry.name.endswith(".app"):
                        continue
                    app_name = app_entry.stem
                    bundle_id = f"com.apple.bundle.{app_name.lower().replace(' ', '')}"
                    if app_name in self.excluded or bundle_id in self.excluded:
                        continue
                    if app_name.lower() in existing_names or bundle_id.lower() in existing_ids:
                        continue

                    items.append(
                        InventoryItem(
                            environment=EnvironmentType.MACOS,
                            target_name=target_name,
                            name=app_name,
                            id=bundle_id,
                            installed_version="unknown",
                            manager=ManagerType.MANUAL,
                            is_supported=False,
                            update_mechanism_available=False,
                            requires_manual_intervention=True,
                            notes="Standalone application in /Applications with manual or internal updater.",
                            extra_metadata={"bundle_id": bundle_id, "bundle_path": str(app_entry)}
                        )
                    )
        except Exception as e:
            logger.debug(f"Error inspecting /Applications on macOS: {e}")

        return items
