# Packages and Containers

Use this file for package-center decisions, Synology Drive, Photos, Active Backup, and Container Manager work.

## Package Triage Order

When a Synology package looks broken:

1. Confirm DSM version and recent update history.
2. Confirm free space and volume health.
3. Confirm whether the package depends on indexing, thumbnails, database state, or another package.
4. Collect evidence before restart, reinstall, or package removal.

## Package Categories

- Core data paths: Drive, Photos, file services, backup packages
- Workload packages: Container Manager, media, office, sync
- Support packages: indexing, search, notifications, reverse proxy dependencies

Treat core data paths as higher risk than optional apps when planning downtime or reinstalls.

## Container Manager Rules

- Verify that Container Manager is actually available on this NAS and DSM build before promising compose-style workflows.
- Map host paths, volume mounts, and backup requirements before editing containers.
- Separate container problems from NAS problems: bad image, bad mount, permission mismatch, low space, and weak hardware are different failures.

## Drive and Photos

- Indexing, thumbnail generation, and library scans can dominate storage I/O long after an install or migration.
- Do not diagnose these apps from CPU alone; check free space, scan backlog, and path correctness.
- Shared folder moves or permission rewrites can break them indirectly, so map dependencies first.

## Active Backup and Other Protection Packages

- Confirm what the package protects, where it stores data, and whether restore has been tested.
- Backup software that only looks green in the dashboard is not enough. Ask what has actually been restored.
- If the package itself is failing, preserve logs and job history before changing repositories or reinstalling.

## Reinstall Decision Rule

Only propose reinstall when:
- evidence points to package corruption rather than storage, permissions, or dependency issues
- configuration and data impact are understood
- backup or export of the important state exists
- the rollback path is explicit
