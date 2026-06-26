# Datasets API

## Purpose

Use the Datasets API for offline Semantic Scholar data ingestion, release-based downloads, and incremental diffs between releases.

## Core Workflow

- Discover the relevant release identifier.
- List or identify the dataset files available for that release.
- Download the needed files.
- If comparing releases, use the incremental diff workflow instead of re-downloading everything blindly.

## When To Use

- The user wants corpus-scale offline data.
- The user needs reproducible release snapshots.
- The user wants changes between releases rather than ad hoc online search results.

## When Not To Use

- The user only wants to search a topic or fetch a modest set of papers.
- The user needs quick interactive iteration.
- Storage or download size constraints are unclear.

## Working Rules

- Confirm local storage expectations before downloading.
- Record the exact release identifiers used.
- Treat dataset release workflows as data-engineering tasks, not standard search tasks.
