---
name: workspace-ping
description: A simple demo skill that performs a ping/pong business workflow for testing resource ingestion pipelines.
metadata: {"openclaw":{"emoji":"🏓"}}
---

# Workspace Ping Skill

A minimal demo skill for testing digital resource ingestion pipelines.

## What it does

The skill defines a simple ping/pong business process: given an input message, it returns the same message prefixed with "pong: ".

## Basic usage

```bash
# From the workspace shell
echo '{"message": "hello"}' | ping-process
```

## Workflow steps

1. Receive JSON input with a `message` field
2. Echo "pong: <message>" to stdout
3. Exit 0 on success, non-zero on invalid input

## Example

```bash
echo '{"message": "test"}' | ping-process
# Output: pong: test
```

This skill is intended as a sample digital asset for testing upload/ingestion workflows into resource registries.
