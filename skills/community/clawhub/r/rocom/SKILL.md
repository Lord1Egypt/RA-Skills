---
name: rocom
description: Roco Kingdom World offline data tool. Local JSON queries for pets, skills, and items.
metadata: { "openclaw": { "emoji": "castle", "requires": { "bins": ["node"] } } }
---

# Roco Kingdom:World Data Tool

A professional, offline-first data assistant for Roco Kingdom:World.

## Features
- **Pet Encyclopedia**: 490+ pets with full stats, attributes, and skill lists.
- **Skill Database**: 490+ skills with power, energy cost, and effect details.
- **Item Catalog**: 1700+ items, materials, and furniture with source info.
- **Dungeon Guide**: Challenge limits, reward drops, and攻略 recommendations.
- **Regional Data**: Pet distribution maps and zone descriptions.

## Usage Guide

| Command | Description | Example |
| --- | --- | --- |
| `pet search (name)` | Fuzzy search for pets | `node rocom.mjs pet search dimo` |
| `pet detail (name)` | View full stats and evolution | `node rocom.mjs pet detail dimo` |
| `skill list` | Browse all available skills | `node rocom.mjs skill list` |
| `dungeon detail (name)` | Check rewards and limits | `node rocom.mjs dungeon detail ocean` |
| `region detail (area)` | See local pet spawns | `node rocom.mjs region detail shop` |

## Data Integrity
- **Source**: Bilibili WIKI (CC BY-NC-SA 4.0).
- **Format**: Pure static JSON in the `data/` folder.
- **Safety**: No network calls, no credentials, no external links.

## Technical Notes
- **Runtime**: Requires Node.js.
- **Performance**: Millisecond-level local queries.
- **Privacy**: All processing happens on your machine.
