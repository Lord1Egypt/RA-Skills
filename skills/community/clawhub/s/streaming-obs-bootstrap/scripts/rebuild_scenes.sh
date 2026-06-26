#!/usr/bin/env bash
set -euo pipefail

IP="${1:-$(hostname -I | awk '{print $1}')}"
BASE="http://$IP:8787"

mc() { mcporter call "$1" >/dev/null; }

# Move to safe scene before deletes
mc 'obs.set_current_scene(scene_name: "Scene")' || true

for s in "Workspace Overlay Test" "Main Live" "Intro" "Work Mode" "Presentation Mode" "Civic Nexus Demo" "Nexus Demo V2" "Analytics Dashboard" "Chat Interaction" "BRB Screen" "Outro"; do
  mc "obs.remove_scene(scene_name: \"$s\")" || true
done

for s in "Intro" "Main Live" "Work Mode" "Presentation Mode" "Civic Nexus Demo" "Nexus Demo V2" "Analytics Dashboard" "Chat Interaction" "BRB Screen" "Outro"; do
  mc "obs.create_scene(scene_name: \"$s\")"
done

mc "obs.create_browser_source(scene_name: \"Intro\", source_name: \"Intro Overlay\", url: \"$BASE/streaming/overlays/intro.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Main Live\", source_name: \"Live Dashboard\", url: \"$BASE/streaming/overlays/live-dashboard.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Work Mode\", source_name: \"Work Status Overlay\", url: \"$BASE/streaming/overlays/work_status.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Presentation Mode\", source_name: \"Presentation Overlay\", url: \"$BASE/streaming/overlays/presentation.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Civic Nexus Demo\", source_name: \"Civic Nexus Demo Overlay\", url: \"$BASE/streaming/civic-nexus-demo.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Nexus Demo V2\", source_name: \"Nexus Demo Overlay\", url: \"$BASE/streaming/civic-nexus-demo.html?v=2\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Analytics Dashboard\", source_name: \"Analytics Overlay\", url: \"$BASE/streaming/overlays/analytics.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Chat Interaction\", source_name: \"Chat Overlay\", url: \"$BASE/streaming/overlays/chat.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"BRB Screen\", source_name: \"BRB Overlay\", url: \"$BASE/streaming/overlays/brb.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Outro\", source_name: \"Outro Overlay\", url: \"$BASE/streaming/overlays/outro.html?v=1\", width: 1920, height: 1080)"

mc 'obs.set_current_scene(scene_name: "Intro")'
echo "Rebuilt scene pack using $BASE"
