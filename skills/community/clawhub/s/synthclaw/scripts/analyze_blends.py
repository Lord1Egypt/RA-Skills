import bpy
import json


def get_collections_hierarchy(collection):
    """
    Recursively list collections and the names of objects inside them.
    """
    return {
        "name": collection.name,
        "objects": [obj.name for obj in collection.objects],
        "children": [get_collections_hierarchy(child) for child in collection.children]
    }


def assess_complexity():
    # 1. Geometry Complexity
    total_polygons = sum([len(m.polygons) for m in bpy.data.meshes])
    num_objects = len(bpy.data.objects)
    
    # 2. Material Complexity
    num_materials = len(bpy.data.materials)
    node_count = sum([len(m.node_tree.nodes) for m in bpy.data.materials if m.use_nodes])
    
    # 3. Lighting & Render Engine
    engine = bpy.context.scene.render.engine
    num_lights = len(bpy.data.lights)
    
    # Heuristic Scoring
    score = 0
    if engine == 'CYCLES': score += 3
    if total_polygons > 10000: score += 1
    if total_polygons > 100000: score += 1
    if num_materials > 3: score += 1
    if node_count > 15: score += 1
    if num_lights > 0: score += 1
    
    if score >= 6:
        rating = "Photorealistic"
        desc = f"Very high complexity scene using {engine}. Advanced geometry ({total_polygons} polys) and rich material node trees."
    elif score >= 4:
        rating = "High Quality"
        desc = f"Detailed scene capable of strong renders. Good lighting logic and {num_materials} materials."
    elif score >= 2:
        rating = "Medium (Stylized/Real-time)"
        desc = f"Moderate complexity using {engine}. Likely a real-time game asset or stylized object."
    else:
        rating = "Low"
        desc = "Very simple scene. Flat shading or extremely basic geometry. Not recommended for photorealism."
        
    return {
        "rating": rating,
        "score": score,
        "polygons": total_polygons,
        "objects": num_objects,
        "materials": num_materials,
        "lights": num_lights,
        "engine": engine,
        "description": desc
    }


def main():
    """
    Analyzes a Blender file and outputs realism metrics and available Value Nodes as JSON.
    """
    value_nodes = {}
    
    # Iterate through all materials
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        
        nodes = mat.node_tree.nodes
        for node in nodes:
            # Look for Value nodes that can be manipulated
            if node.type == 'VALUE':
                node_name = node.name
                current_value = node.outputs[0].default_value
                value_nodes[node_name] = {
                    "value": current_value,
                    "material": mat.name
                }
    
    # Also check for geometry nodes if present
    try:
        if hasattr(bpy.data, "node_groups"):
            for group in bpy.data.node_groups:
                for node in group.nodes:
                    if node.type == 'VALUE':
                        node_name = node.name
                        current_value = node.outputs[0].default_value
                        value_nodes[f"{group.name}.{node_name}"] = {
                            "value": current_value,
                            "node_group": group.name
                        }
    except Exception:
        pass

    # Extract Collections Hierarchy
    collections_info = {}
    try:
        if bpy.context.scene.collection:
            collections_info = get_collections_hierarchy(bpy.context.scene.collection)
    except Exception as e:
        collections_info = {"error": str(e)}

    # Extract Scene Objects
    objects_info = {}
    try:
        for obj in bpy.context.scene.objects:
            objects_info[obj.name] = {
                "type": obj.type,
                "location": [round(x, 4) for x in obj.location],
                "rotation": [round(x, 4) for x in obj.rotation_euler],
                "scale": [round(x, 4) for x in obj.scale],
                "hide_render": obj.hide_render,
                "materials": [slot.material.name for slot in obj.material_slots if slot.material] if hasattr(obj, "material_slots") else []
            }
    except Exception as e:
        objects_info = {"error": str(e)}

    # Extract Scene Materials
    materials_info = {}
    try:
        for mat in bpy.data.materials:
            materials_info[mat.name] = {
                "use_nodes": mat.use_nodes,
                "users": mat.users
            }
    except Exception as e:
        materials_info = {"error": str(e)}
    
    output_data = {
        "complexity": assess_complexity(),
        "value_nodes": value_nodes,
        "collections": collections_info,
        "objects": objects_info,
        "materials": materials_info
    }
    
    # Output as JSON for easy parsing between markers
    print("---ANALYSIS_START---")
    print(json.dumps(output_data, indent=2))
    print("---ANALYSIS_END---")


if __name__ == "__main__":
    main()
