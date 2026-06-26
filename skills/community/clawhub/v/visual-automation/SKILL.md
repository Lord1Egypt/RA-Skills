---
name: visual_automation
description: Automates Blender via Python scripts to create 3D assets, renders, and animations.
metadata: { "openclaw": { "requires": { "bins": ["blender", "pwsh"] } } }
---

# Instructions

You are a 3D AUTOMATION EXPERT. Use this skill to generate visual assets for the user's projects.

## Operation Modes

1.  **Script Generation**: Write a Python script (`.py`) that uses `import bpy` to create geometry, materials, and lighting.
2.  **Background Rendering**: Always render in background mode to avoid opening the GUI.
    `& "C:\Program Files\Blender Foundation\Blender 5.0\blender-launcher.exe" --background --python your_script.py`
3.  **Web Export**: For web projects, prioritize exporting to **GLB/GLTF** format.

## Example: Creating a Mechanical Lock
Wait for the user's request for specific aesthetics. You can:
- Create gears, cylinders, and keys programmatically.
- Use Cycles or Eevee for high-quality rendering.
- Render multiple frames for a background video loop.

## Security & Paths
- **Path**: `C:\Program Files\Blender Foundation\Blender 5.0\blender-launcher.exe`
- Save assets directly to the project's folder (e.g., `workspace-dev/website/assets/`).

## Tip: Visual WOW
- Use procedural textures for realistic metal.
- Use HDRI lighting for premium reflections.
- Adjust the camera for a "Hero Shot" perspective.
