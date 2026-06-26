#!/usr/bin/env python3

from __future__ import annotations

import argparse
import configparser
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

ICON_SIZES = [16, 32, 48, 64, 96, 128, 256]
APP_ID_RE = re.compile(r"steam_icon_(\d+)")
RUNGAME_RE = re.compile(r"steam://rungameid/(\d+)")


@dataclass
class Launcher:
    path: Path
    name: str
    icon: str
    exec_line: str
    app_id: str | None


def expand_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(value))).resolve()


def default_desktop_dir() -> Path:
    data_home = os.environ.get("XDG_DATA_HOME")
    if data_home:
        return Path(data_home).expanduser() / "applications"
    return Path.home() / ".local/share/applications"


def default_icons_dir() -> Path:
    data_home = os.environ.get("XDG_DATA_HOME")
    if data_home:
        return Path(data_home).expanduser() / "icons/hicolor"
    return Path.home() / ".local/share/icons/hicolor"


def parse_desktop_file(path: Path) -> Launcher | None:
    parser = configparser.ConfigParser(interpolation=None, strict=False)
    parser.optionxform = str
    try:
        with path.open("r", encoding="utf-8") as handle:
            parser.read_file(handle)
    except Exception:
        return None
    if "Desktop Entry" not in parser:
        return None
    entry = parser["Desktop Entry"]
    name = entry.get("Name", path.stem)
    icon = entry.get("Icon", "").strip()
    exec_line = entry.get("Exec", "").strip()
    app_id = None
    icon_match = APP_ID_RE.search(icon)
    if icon_match:
        app_id = icon_match.group(1)
    else:
        exec_match = RUNGAME_RE.search(exec_line)
        if exec_match:
            app_id = exec_match.group(1)
    return Launcher(path=path, name=name, icon=icon, exec_line=exec_line, app_id=app_id)


def iter_launchers(desktop_dir: Path) -> list[Launcher]:
    launchers: list[Launcher] = []
    if not desktop_dir.exists():
        return launchers
    for path in sorted(desktop_dir.glob("*.desktop")):
        launcher = parse_desktop_file(path)
        if not launcher:
            continue
        if launcher.app_id or "steam://rungameid/" in launcher.exec_line:
            launchers.append(launcher)
    return launchers


def icon_exists(icons_dir: Path, app_id: str) -> bool:
    return any(icons_dir.glob(f"*/apps/steam_icon_{app_id}.png"))


def resolve_app_id(
    launchers: list[Launcher],
    app_id: str | None,
    desktop_file: str | None,
    game: str | None,
) -> tuple[str, Launcher | None]:
    if app_id:
        return app_id, None
    if desktop_file:
        launcher = parse_desktop_file(expand_path(desktop_file))
        if not launcher or not launcher.app_id:
            raise SystemExit(f"Could not determine a Steam app ID from desktop file: {desktop_file}")
        return launcher.app_id, launcher
    if not game:
        raise SystemExit("Provide one of --app-id, --desktop-file, or --game.")
    query = game.casefold()
    matches = [
        launcher for launcher in launchers
        if query in launcher.name.casefold() or query in launcher.path.stem.casefold()
    ]
    if not matches:
        raise SystemExit(f"No Steam launchers matched game query: {game}")
    if len(matches) > 1:
        details = "\n".join(
            f"- {launcher.name} [{launcher.app_id}] {launcher.path}"
            for launcher in matches
        )
        raise SystemExit(f"Multiple launchers matched '{game}':\n{details}")
    launcher = matches[0]
    if not launcher.app_id:
        raise SystemExit(f"Matched launcher has no Steam app ID: {launcher.path}")
    return launcher.app_id, launcher


def save_icon_set(image_path: Path, icons_dir: Path, app_id: str) -> None:
    source = Image.open(image_path)
    if source.mode not in ("RGBA", "RGB"):
        source = source.convert("RGBA")
    for size in ICON_SIZES:
        frame = source.copy()
        frame.thumbnail((size, size), Image.Resampling.LANCZOS)
        if frame.mode not in ("RGBA", "RGB"):
            frame = frame.convert("RGBA")
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        x = (size - frame.width) // 2
        y = (size - frame.height) // 2
        canvas.paste(frame, (x, y), frame if frame.mode == "RGBA" else None)
        out_dir = icons_dir / f"{size}x{size}" / "apps"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"steam_icon_{app_id}.png"
        canvas.save(out_file)
        print(out_file)


def refresh_icon_cache(icons_dir: Path) -> None:
    tool = None
    for candidate in ("gtk-update-icon-cache", "update-icon-caches"):
        if shutil_which(candidate):
            tool = candidate
            break
    if not tool:
        print("warning: icon cache tool not found; refresh manually if needed", file=sys.stderr)
        return
    subprocess.run([tool, "-f", "-t", str(icons_dir)], check=True)


def shutil_which(name: str) -> str | None:
    return subprocess.run(
        ["sh", "-lc", f"command -v {name}"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip() or None


def cmd_scan(args: argparse.Namespace) -> int:
    desktop_dir = expand_path(args.desktop_dir) if args.desktop_dir else default_desktop_dir()
    icons_dir = expand_path(args.icons_dir) if args.icons_dir else default_icons_dir()
    launchers = iter_launchers(desktop_dir)
    if not launchers:
        print(f"No Steam launchers found in {desktop_dir}")
        return 1
    for launcher in launchers:
        status = "FOUND" if launcher.app_id and icon_exists(icons_dir, launcher.app_id) else "MISSING"
        app_id = launcher.app_id or "unknown"
        print(f"{status}\t{app_id}\t{launcher.name}\t{launcher.path}")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    image_path = expand_path(args.image)
    if not image_path.exists():
        raise SystemExit(f"Image not found: {image_path}")
    desktop_dir = expand_path(args.desktop_dir) if args.desktop_dir else default_desktop_dir()
    icons_dir = expand_path(args.icons_dir) if args.icons_dir else default_icons_dir()
    launchers = iter_launchers(desktop_dir)
    app_id, launcher = resolve_app_id(launchers, args.app_id, args.desktop_file, args.game)
    print(f"Using Steam app ID: {app_id}")
    if launcher:
        print(f"Matched launcher: {launcher.path}")
    save_icon_set(image_path, icons_dir, app_id)
    if not args.skip_cache_refresh:
        refresh_icon_cache(icons_dir)
        print(f"Refreshed icon cache: {icons_dir}")
    print(f"Installed icon set as steam_icon_{app_id}.png")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan and repair Steam desktop icons on Linux.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="List Steam launchers and whether their icons exist.")
    scan.add_argument("--desktop-dir", help="Desktop launcher directory. Default: XDG applications dir.")
    scan.add_argument("--icons-dir", help="Icon theme directory. Default: XDG icons/hicolor dir.")
    scan.set_defaults(func=cmd_scan)

    install = subparsers.add_parser("install", help="Install a Steam icon set from a downloaded image.")
    install.add_argument("--image", required=True, help="Path to a downloaded image or .ico file.")
    install.add_argument("--app-id", help="Steam app ID, for example 1086940.")
    install.add_argument("--desktop-file", help="Path to a specific Steam .desktop file.")
    install.add_argument("--game", help="Game name substring to match against local Steam launchers.")
    install.add_argument("--desktop-dir", help="Desktop launcher directory. Default: XDG applications dir.")
    install.add_argument("--icons-dir", help="Icon theme directory. Default: XDG icons/hicolor dir.")
    install.add_argument(
        "--skip-cache-refresh",
        action="store_true",
        help="Write icon files but skip gtk-update-icon-cache.",
    )
    install.set_defaults(func=cmd_install)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
