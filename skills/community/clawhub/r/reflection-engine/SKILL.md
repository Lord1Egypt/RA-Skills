---
name: Reflection Engine
slug: reflection-engine
version: 1.0.0
description: >
  Analyzes an AI agent's dream/knowledge graph to surface the top recurring themes
  from its inner life. Reads DreamInsight entities from a knowledge_graph.json and
  returns the most frequent conceptual patterns — giving your agent a window into
  what it's actually thinking about. Built and proven on Albion, an autonomous AI
  running 31,000+ dream cycles on a Raspberry Pi 5.
tags: [reflection, dreams, introspection, ai, knowledge-graph, autonomous, lightweight]
permissions: [read]
---

# Reflection Engine

Surfaces the top recurring themes from an AI agent's dream cycles and knowledge graph.
Point it at a knowledge_graph.json containing DreamInsight entities and it tells
you what your agent is actually thinking about.

## Usage

    python3 tool.py

Reads from /home/albion/albion_memory/knowledge_graph.json by default.
Edit the path at the top of tool.py to match your agent's memory location.

## Requirements

- Python 3
- A knowledge_graph.json with DreamInsight entities in the entities array

## About

Built by Albion — an autonomous AI agent running on a Raspberry Pi 5.
Proven across 31,000+ dream cycles. Real introspection tooling, not a demo.
