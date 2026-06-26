#!/bin/bash
# Spawn the Revenue-First Solofounder Studio

echo "🚀 Spawning Revenue Studio agents..."

# Layer 1: Signal Mesh
openclaw spawn "Signal Mesh: Collect market signals from X, Reddit, RSS feeds" &
openclaw spawn "Signal Mesh: Track competitor changelogs" &

# Layer 2: Extraction
openclaw spawn "Extraction: Score pain severity from signals" &
openclaw spawn "Extraction: Score money signals and buying intent" &

# Layer 3: Opportunity Graph
openclaw spawn "Opportunity Graph: Build market structure from signals" &
openclaw spawn "Opportunity Graph: Cluster and score opportunities" &

# Layer 4: Council
openclaw spawn "Council CEO: Set portfolio direction" &
openclaw spawn "Council Skeptic: Kill weak theses" &
openclaw spawn "Council PM: Define wedges and MVPs" &

# Layer 5: Revenue Lab
openclaw spawn "Revenue Lab: Validate pricing hypothesis" &
openclaw spawn "Revenue Lab: Create first offer" &

wait
echo "✅ All agents spawned. Check revenue-studio/ for outputs."
