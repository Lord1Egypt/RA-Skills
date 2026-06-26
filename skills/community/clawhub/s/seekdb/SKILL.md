---
name: seekdb
description: Overview skill for OceanBase SeekDB. Routes to specialized skills for installing/deploying SeekDB on a target machine and for building SeekDB from source. Use as a starting point when the user mentions seekdb, pyseekdb, "install seekdb", "build seekdb", or wants a lightweight standalone OceanBase-compatible database. For obd-managed seekdb deployments and primary-standby HA, see the separate oceanbase-deploy/seekdb skill instead.
compatibility: Standalone product skill. Install and build flows have their own platform requirements — see sub-skills.
metadata:
  author: oceanbase
  version: "1.0"
---

# SeekDB

SeekDB is a lightweight OceanBase-compatible database that can run as a standalone server (Homebrew / Docker / yum / apt / Windows MSI) or as an embedded Python module (`pyseekdb`).

This is the entry point. Use the specialized skills below for specific tasks.

## Skill Index

| Skill | Use When |
|-------|----------|
| [install](install/SKILL.md) | Install / deploy SeekDB on a target machine — Homebrew, Docker, yum, apt, Windows MSI, or pip embedded. |
| [build](build/SKILL.md) | Build SeekDB binaries and packages from source — macOS, Linux, Android (cross), Windows, Python wheel. |

## When to Use Which Skill

- "Install seekdb on my Mac / Linux / Windows" → [install](install/SKILL.md)
- "I want to use seekdb from Python" → [install](install/SKILL.md), pip embedded mode
- "Build seekdb from source" / "make a release rpm/deb/tgz/apk/installer" → [build](build/SKILL.md)
- "Deploy seekdb primary-standby with obd, do switchover/failover" → use the separate **`oceanbase-deploy/seekdb`** skill (lives under [`../oceanbase-deploy/seekdb/SKILL.md`](../oceanbase-deploy/seekdb/SKILL.md)). That skill is for obd-managed clusters; this skill is for the SeekDB product itself.

## Default Ports

| Port | Purpose |
|------|---------|
| 2881 | MySQL protocol |
| 2886 | HTTP / obshell |

## References

- Product documentation: <https://www.oceanbase.ai/docs/seekdb-overview/>
- Software download center: <https://mirrors.oceanbase.com/oceanbase/community/stable/>
