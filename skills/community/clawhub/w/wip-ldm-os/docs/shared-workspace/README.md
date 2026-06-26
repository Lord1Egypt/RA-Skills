###### WIP Computer

# Shared Workspace

## One folder. All your AIs.

LDM OS creates a single directory on your computer where all your AIs share memory, tools, identity files, and configuration.

```
~/.ldm/
├── agents/              Each AI gets its own space
│   ├── claude-code/     Identity, soul, context, journals
│   ├── openclaw/        Same structure, different AI
│   └── .../
├── extensions/          Tools installed via Universal Installer
├── memory/              Shared memory (crystal.db, daily logs)
├── shared/              Boot files, shared config
└── version.json         What's installed
```

## How It Works

Every AI that runs LDM OS reads from and writes to the same directory. Claude Code, GPT, OpenClaw, any AI. They all see the same memory, the same tools, the same history.

Each AI gets its own agent folder for identity files (who it is, how it behaves, its journals). But memory and tools are shared.

## Backup

Everything lives in one folder. Back it up however you back up anything else. iCloud, external drive, Dropbox, Time Machine. Move to a new computer by copying the folder.

## Sacred Data

LDM OS never touches your existing data during install or update. Your memories, agent files, secrets, and state are protected. Updates only touch code and config, never data.

## Part of LDM OS

Shared Workspace is included with LDM OS. Run `ldm init` to create it.

---

[Technical Reference](./TECHNICAL.md)
