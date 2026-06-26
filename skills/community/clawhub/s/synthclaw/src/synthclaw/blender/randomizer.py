import math
import random
import bpy

def apply_scene_randomizations(rules, sync_values):
    """
    Evaluates and applies randomized properties dynamically.
    """
    for rule in rules:
        rtype = rule.get("type")
        dist = rule.get("distribution")
        sync_group = rule.get("sync_group")
        
        # Determine value
        if sync_group and sync_group in sync_values:
            val = sync_values[sync_group]
        else:
            if dist == "boolean":
                val = random.choice([True, False])
            elif dist == "int_range":
                r = rule.get("range", [0, 100])
                val = random.randint(int(r[0]), int(r[1]))
            elif dist == "uniform":
                r = rule.get("range", [0.0, 1.0])
                val = random.uniform(r[0], r[1])
            elif dist == "choice":
                val = random.choice(rule.get("range", []))
            else:
                continue
            
            if sync_group:
                sync_values[sync_group] = val
                
        # Apply the value based on the type
        try:
            if rtype == "value_node":
                mat = bpy.data.materials.get(rule["target"])
                if mat and mat.use_nodes:
                    node = mat.node_tree.nodes.get(rule["sub_target"])
                    if node and node.type == 'VALUE':
                        node.outputs[0].default_value = val
                        print(f"[SynthClaw] Randomizer: Set material '{rule['target']}' node '{rule['sub_target']}' value to {val}")
                        
            elif rtype == "modifier_input":
                obj = bpy.data.objects.get(rule["target"])
                if obj:
                    mod = obj.modifiers.get(rule["sub_target"])
                    if mod:
                        mod[rule["property"]] = val
                        print(f"[SynthClaw] Randomizer: Set object '{rule['target']}' modifier '{rule['sub_target']}' property '{rule['property']}' to {val}")
                        
            elif rtype == "camera_location":
                camera = bpy.context.scene.camera
                if camera:
                    axis = rule.get("property", "x").lower()
                    if axis == "x":
                        camera.location.x = val
                    elif axis == "y":
                        camera.location.y = val
                    elif axis == "z":
                        camera.location.z = val
                    print(f"[SynthClaw] Randomizer: Set camera location {axis} to {val}")
                        
            elif rtype == "camera_rotation":
                camera = bpy.context.scene.camera
                if camera:
                    axis = rule.get("property", "x").lower()
                    rad_val = math.radians(val)
                    if axis == "x":
                        camera.rotation_euler.x = rad_val
                    elif axis == "y":
                        camera.rotation_euler.y = rad_val
                    elif axis == "z":
                        camera.rotation_euler.z = rad_val
                    print(f"[SynthClaw] Randomizer: Set camera rotation {axis} to {val} degrees")
                        
            elif rtype == "light_visibility":
                obj = bpy.data.objects.get(rule["target"])
                if obj:
                    obj.hide_render = val
                    print(f"[SynthClaw] Randomizer: Set light visibility of '{rule['target']}' to hide_render={val}")
                    
            elif rtype == "node_property":
                mat = bpy.data.materials.get(rule["target"])
                if mat and mat.use_nodes:
                    node = mat.node_tree.nodes.get(rule["sub_target"])
                    if node:
                        setattr(node, rule["property"], val)
                        print(f"[SynthClaw] Randomizer: Set material '{rule['target']}' node '{rule['sub_target']}' property '{rule['property']}' to {val}")
        except Exception as e:
            print(f"[SynthClaw] Error applying rule {rule}: {e}")
