import bpy
import json
import os
import sys

# Dynamically add synthclaw package path to Blender's Python sys.path
package_path = os.environ.get("SYNTHCLAW_PACKAGE_PATH")
if package_path and package_path not in sys.path:
    sys.path.append(package_path)

from synthclaw.blender.device import configure_render_engine
from synthclaw.blender.randomizer import apply_scene_randomizations
from synthclaw.blender.compositor import configure_compositor_outputs
from synthclaw.blender.cleanup import clean_up_tifs

def main():
    try:
        args = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        args = []

    config_path = args[0] if args else None
    if not config_path or not os.path.exists(config_path):
        print("[SynthClaw] Error: Missing or invalid configuration JSON path.")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    output_dir = config.get("output_dir", "./output")
    num_images = config.get("num_images", 2)
    randomizations = config.get("randomizations", [])

    os.makedirs(output_dir, exist_ok=True)
    configure_render_engine()
    scene = bpy.context.scene

    for i in range(num_images):
        print(f"\n--- [SynthClaw] Rendering Frame {i + 1}/{num_images} ---")
        scene.frame_set(i)
        
        # Apply randomizations with sync tracking
        sync_values = {}
        apply_scene_randomizations(randomizations, sync_values)
        
        # Route compositor nodes
        has_compositor = configure_compositor_outputs(scene, output_dir, i)
        
        # Always route default render path to the output directory as a PNG
        scene.render.filepath = os.path.join(output_dir, f"{i}.png")
        scene.render.image_settings.file_format = 'PNG'
        print(f"[SynthClaw] Direct Render: Route default filepath to '{scene.render.filepath}' (PNG)")
            
        # Trigger frame render
        bpy.ops.render.render(write_still=True)

    print("\n--- [SynthClaw] Render Loop Complete. Cleaning up files... ---")
    clean_up_tifs(output_dir)
    print("[SynthClaw] Complete!")

if __name__ == "__main__":
    main()
