# Skill Graph for Analogical Reasoning

This is the ClawHub/OpenClaw skill bundle for the `Skill Graph for Analogical Reasoning` project.

It exposes the `grap-skill` capability as a skill-oriented interface around three main commands:

- `/grap-skill build`
- `/grap-skill query`
- `/grap-skill look`

## What this version is

This skill version is for users who want to use the graph capability through a skill workflow.

The full source code, Python package, and CLI live in the GitHub repository for this project.

## What this skill can do

- build a graph over local `SKILL.md` folders
- select one primary skill for a task
- retrieve complementary support instead of simply taking the top similar skills
- render the skill network as a visual graph

## Skill usage

- Use `/grap-skill build` to scan local skill folders and create a `graph.json`
- Use `/grap-skill query` to select one primary skill plus complementary support from an existing graph
- Use `/grap-skill look` to render the current graph as an HTML visualization

## Cross discovery

The GitHub repository is the main development version and the official Python
package source.

Use the GitHub version when you want:

- a full source checkout
- editable installs
- direct Python package development

Use this ClawHub/OpenClaw skill version when you want:

- `openclaw skills install skill-graph-for-analogical-reasoning`
- a skill-style wrapper around the packaged graph commands
- a bundle that can be installed into an OpenClaw workspace
