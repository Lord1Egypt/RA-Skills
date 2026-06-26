import bpy
import os

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a simple cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object

# Create a new material
mat = bpy.data.materials.new(name="TestMaterial")
mat.use_nodes = True

# Clear default nodes
mat.node_tree.nodes.clear()

# Add nodes
output_node = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
output_node.location = (300, 0)

diffuse_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
diffuse_node.location = (0, 0)

# Add a Value node that can be controlled by the agent
value_node = mat.node_tree.nodes.new(type='ShaderNodeValue')
value_node.location = (-300, 0)
value_node.outputs[0].default_value = 0.5

# CRITICAL: Set the node name so the agent can find it
value_node.name = "AgentControl"

# Link nodes
mat.node_tree.links.new(value_node.outputs[0], diffuse_node.inputs['Color'])
mat.node_tree.links.new(diffuse_node.outputs[0], output_node.inputs['Surface'])

# Assign material to cube
cube.data.materials.append(mat)

# Add a light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
light = bpy.context.active_object
light.data.energy = 5

# Add a camera
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)

# Set as active camera
bpy.context.scene.camera = camera

# Configure render settings for fast testing
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.resolution_percentage = 50  # Lower res for speed

# Save the file
output_path = os.path.join(os.path.dirname(__file__), "test.blend")
bpy.ops.wm.save_as_mainfile(filepath=output_path)
print(f"Created test.blend at: {output_path}")
