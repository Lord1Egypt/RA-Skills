---
name: steam-icon-fixer
description: Fix missing or generic Steam game desktop icons on Linux by finding the Steam app ID from local launchers and installing replacement artwork into the user's icon theme. Use when Steam-created desktop launchers show blank or generic icons, when the app ID must be discovered from local launchers, or when a downloaded image needs to be installed in Steam's icon naming scheme.
---

# Steam Icon Fixer

Use this skill to repair Steam launcher icons on Linux desktops.

## Core workflow

1. Prefer the user's explicit inputs when available.
   - downloaded image path
   - game name
   - Steam app ID
   - specific `.desktop` file
2. Otherwise infer the common local locations.
   - launcher dir: `${XDG_DATA_HOME:-~/.local/share}/applications`
   - icon dir: `${XDG_DATA_HOME:-~/.local/share}/icons/hicolor`
3. Discover the app ID from the launcher metadata.
   - look for `Icon=steam_icon_<id>`
   - look for `Exec=...steam://rungameid/<id>`
   - if needed, search local launchers by game name
4. Run the bundled installer script.
5. Refresh the icon cache if the script does not do it automatically.

## Commands

Scan local Steam launchers for missing icons:

```bash
python3 scripts/steam_icon_fixer.py scan
```

Install an image with an explicit app ID:

```bash
python3 scripts/steam_icon_fixer.py install \
  --image /path/to/image.png \
  --app-id 1086940
```

Install an image by matching a game name:

```bash
python3 scripts/steam_icon_fixer.py install \
  --image /path/to/image.png \
  --game "Baldur's Gate 3"
```

Install using a specific desktop file:

```bash
python3 scripts/steam_icon_fixer.py install \
  --image /path/to/image.png \
  --desktop-file ~/.local/share/applications/Baldur's\ Gate\ 3.desktop
```

Use explicit directories when the machine is nonstandard:

```bash
python3 scripts/steam_icon_fixer.py install \
  --image /path/to/image.png \
  --game "DOOM: The Dark Ages" \
  --desktop-dir /custom/applications \
  --icons-dir /custom/icons/hicolor
```

## Bundled resources

- `scripts/steam_icon_fixer.py`: deterministic installer/scanner for Steam launcher icons.
- `references/`: add launcher or icon-theme notes here if the workflow needs machine-specific guidance.

## Notes

- The script should generate standard icon sizes and keep Steam's `steam_icon_<appid>.png` naming.
- For `.ico` inputs, Pillow may be required.
- If GNOME or another dock keeps the old icon, unpin and re-pin the launcher after the cache refresh.
