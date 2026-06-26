import bpy
import sys
import os

# Dynamically add synthclaw package path to Blender's Python sys.path
package_path = os.environ.get("SYNTHCLAW_PACKAGE_PATH")
if package_path and package_path not in sys.path:
    sys.path.append(package_path)

from synthclaw.blender.device import configure_render_engine

def update_value_nodes(params):
    """
    Update Value Nodes in materials based on parameter dictionary.
    """
    updated_nodes = []
    missing_nodes = []
    
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        
        nodes = mat.node_tree.nodes
        for key, val in params.items():
            if key in nodes and nodes[key].type == 'VALUE':
                try:
                    nodes[key].outputs[0].default_value = val
                    updated_nodes.append((key, val))
                    print(f"[SynthClaw] Updated Node '{key}' to {val}")
                except Exception as e:
                    print(f"[SynthClaw] Error updating node '{key}': {e}")
            elif key not in nodes:
                missing_nodes.append(key)
    
    if missing_nodes:
        print(f"[SynthClaw] Warning: Nodes not found: {', '.join(missing_nodes)}")
    
    return updated_nodes


def main():
    """
    Agent Bridge: Reads parameters from CLI, updates Value Nodes, sets engine, and renders.
    """
    # Parse CLI arguments
    try:
        args = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        print("[SynthClaw] No parameters provided via CLI.")
        args = []
    
    # Parse key=value pairs
    params = {}
    for a in args:
        if '=' in a:
            try:
                k, v = a.split('=', 1)
                params[k] = float(v)
            except ValueError:
                print(f"[SynthClaw] Warning: Could not parse value for '{a}', skipping")
                continue
    
    # STEP 1: Set render engine FIRST (before any modifications)
    configure_render_engine()
    
    # STEP 2: Update Value Nodes
    updated_nodes = update_value_nodes(params)
    
    # Print summary
    print(f"[SynthClaw] Updated {len(updated_nodes)} nodes:")
    for name, val in updated_nodes:
        print(f"  - {name}: {val}")
    
    print(f"[SynthClaw] Ready to render with {bpy.context.scene.render.engine}...")


if __name__ == "__main__":
    main()
