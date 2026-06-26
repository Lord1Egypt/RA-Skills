---
name: ue-asset-finder
description: |
  Find Unreal Engine assets (.uasset, .umap, .uby, .udata). Use when: (1) Finding specific assets,
  (2) Locating maps/levels, (3) Finding UI widgets, (4) Finding blueprints, (5) Finding audio files,
  (6) Searching asset references, (7) Finding DataTable/CSV files
---

# UE Asset Finder

## Common Asset Types

| Extension | Type |
|----------|------|
| `.uasset` | General asset |
| `.umap` | Map/Level |
| `.uby` | Blueprint |
| `.udata` | Data table |
| `.uslot` | Slot data |
| `.uuip` | UI preview |

## Search Locations

### SilverPalace Assets
- `Project\Content\` - Main content
- `Project\Content\ArtRes\` - Art resources
- `Project\Content\LogicRes\` - Logic resources
- `Project\Content\Maps\` - Maps
- `Project\Content\Audio\` - Audio files

### Saved Game Data
- `Project\Saved\` - Saved games, logs, configs
- `Project\Saved\SaveGames\` - Save files

## Common Searches

### Find Maps
```powershell
Get-ChildItem -Path "Content" -Recurse -Filter "*.umap"
```

### Find Blueprints
```powershell
Get-ChildItem -Path "Content" -Recurse -Filter "*.uby"
```

### Find DataTables
```powershell
Get-ChildItem -Path "Content" -Recurse -Filter "*.udata"
```

### Find by Name Pattern
```powershell
Get-ChildItem -Path "Content" -Recurse | Where-Object {$_.Name -like "*Login*"}
```

### Find UI Assets
```powershell
Get-ChildItem -Path "Content\UI" -Recurse -Filter "*.uasset"
```

## SilverPalace Specific Paths

### UI Assets
- `Content\UI\` - General UI
- `Content\StartUpDev\` - Startup/loading UI

### Maps
- `Content\Maps\WP\` - World partition maps
- `Content\Maps\WC\` - World composition

### Audio
- `Content\Audio\WwiseAudio\` - Wwise audio
- `Content\Audio\GeneratedSoundBanks\` - Cooked audio

### Configuration
- `Content\TableData\` - Data tables
- `Content\Script\` - Lua scripts (not UE asset but important)

## Asset Info

When found, provide:
- Full path
- File size
- Last modified date
- Dependencies (if checking references)
