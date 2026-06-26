# Context Frame Skill

Purpose
- Detect topic switches in conversation and create/manage Context Frames (work contexts).

Usage
- context_simulate: demo mode runs a simulated conversation and shows frame creation.

Integration
- Designed to be integrated into Consolidator or called as an isolated skill for on-demand context management.

Notes
- MVP uses lightweight heuristic topic detection; can be upgraded to embedding-based semantic similarity for production.

Packaging
- Files included: context_sim.py, preload.py, skill.json, SKILL.md
- To test locally: python3 preload.py
- To publish: upload the packaged tarball via ClawHub upload UI or use npx clawhub publish <path> (web upload recommended for first-time publish to accept license).