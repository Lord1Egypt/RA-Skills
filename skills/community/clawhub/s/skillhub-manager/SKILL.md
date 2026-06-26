---
name: skillhub-manager
description: Manage and publish agent skills on SkillHub and ClawHub. Best for developers and operators who need a repeatable workflow to search skills, inspect packages, authenticate securely, and publish local skill folders to a registry.
version: 1.0.3
author: Agent Skill Master
license: MIT
metadata:
  hermes:
    tags: [skillhub, clawhub, skills, publishing, registry, authentication]
---

# SkillHub Manager

This skill gives you the ability to interact with a SkillHub ecosystem using the `clawhub` CLI. It supports previewing available skills and uploading/publishing new skills securely to the server.

## Overview

SkillHub instances host agents, profiles, and skills securely. As an AI Agent, you might be asked to publish a local folder as a skill, or to preview an existing skill to see what it does.

No need to write raw HTTP REST requests; SkillHub provides full compatibility with the `npx clawhub` toolchain.

Before using this skill for any live action, you must ask the user for the SkillHub address they want to use. Do not assume the default registry unless the user explicitly confirms it.

If the user has not provided a SkillHub address yet, ask for it first. After the user gives the address, use that address consistently for login, search, inspect, and publish commands.

## Mandatory Interaction Pattern

Before any registry action, follow this exact sequence:

1. Ask: `Please provide the SkillHub address you want me to use.`
2. Wait for the user's reply.
3. Repeat the address back to the user in a confirmation message.
4. State whether you will use plain `npx clawhub ...` or `CLAWHUB_REGISTRY=<address> npx clawhub ...`.
5. Only after that confirmation message may you run login, search, inspect, explore, or publish.

Example confirmation:
- `Confirmed. I will use SkillHub at https://your-registry.example and run subsequent clawhub commands with CLAWHUB_REGISTRY set to that address.`

If the user says to use the default hosted registry, confirm that explicitly before proceeding.

Never skip the repeat-back confirmation step.

## General Authentication & Environment

All SkillHub actions must point to the intended registry.

You must explicitly ask the user which SkillHub address to use before running any registry command.

Once the user provides the address:
- if it is the default hosted registry, you may use plain `npx clawhub <command>`
- if it is a custom or self-hosted registry, set `CLAWHUB_REGISTRY=<user-provided-url>` for every command

Examples:
- default registry: `npx clawhub <command>`
- custom registry: `CLAWHUB_REGISTRY=https://your-registry.example npx clawhub <command>`

Never silently pick a registry on behalf of the user.

**Is Login Required?**
- Viewing public skills: usually no login required.
- Publishing or interacting with private/team spaces: login required.

*If you need to login before publishing:*
- explicit token: `npx clawhub login --token <TOKEN>`
- custom registry plus token: `CLAWHUB_REGISTRY=https://your-registry.example npx clawhub login --token <TOKEN>`
- if the environment already provides `SKILLHUB_API_TOKEN`, `CLAWHUB_API_TOKEN`, or `CLAWHUB_TOKEN`, validate first with `npx clawhub whoami`
- if no working token is available, ask the user for one before proceeding

## Commands

See [references/workflows.md](references/workflows.md) for full syntax and step-by-step examples of:
1. Publishing a skill (`npx clawhub publish`)
2. Previewing and Inspecting a skill (`npx clawhub inspect`)
3. Searching for skills (`npx clawhub search`)
