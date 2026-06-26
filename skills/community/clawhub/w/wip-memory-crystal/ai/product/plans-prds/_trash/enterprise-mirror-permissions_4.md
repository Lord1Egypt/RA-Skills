# Product Idea: Enterprise/Team Mirror Permissions

**Date:** 2026-03-04
**Source:** Parker (session discussion)
**Status:** Idea (not scheduled)

## The Problem

Default mirror sync copies everything in LDM from Core to Nodes. For personal use, this is fine. For enterprise or team deployments, you don't want to sync everything. Different team members should see different data.

## The Idea

A permissions layer that controls what gets mirrored to which Nodes:
- Default (personal): sync all
- Enterprise/team: configurable scoping per Node, per agent, per data type
- Could scope by: agent ID, date range, source type, sensitivity level

## When

After the core mirror sync works reliably for personal use. Don't over-engineer before the basics are solid.
