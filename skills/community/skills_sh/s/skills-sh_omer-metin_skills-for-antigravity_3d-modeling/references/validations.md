# 3D Modeling - Validations

## Unapplied Transforms in Export Script

### **Id**
unapplied-transforms-export
### **Severity**
critical
### **Category**
export
### **Description**
  Export scripts that don't apply transforms before exporting will cause
  scale and rotation issues in game engines.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
fbx_export|export_scene\.fbx|gltf_export
  #### **File Patterns**
    - *.py
    - *.blend
### **Anti Pattern Example**
  # BAD: Exporting without applying transforms
  import bpy
  
  def export_model(filepath):
      bpy.ops.export_scene.fbx(filepath=filepath)  # No transform application!
  
### **Correct Example**
  # GOOD: Apply transforms before export
  import bpy
  
  def export_model(filepath):
      # Select all mesh objects
      for obj in bpy.context.scene.objects:
          if obj.type == 'MESH':
              obj.select_set(True)
              bpy.context.view_layer.objects.active = obj
  
      # Apply all transforms
      bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
  
      # Now export
      bpy.ops.export_scene.fbx(
          filepath=filepath,
          apply_scale_options='FBX_SCALE_ALL',
          apply_unit_scale=True
      )
  
### **Fix Suggestion**
  Add transform application before export:
  ```python
  bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
  ```
  

## Missing Normals Recalculation

### **Id**
missing-normals-recalculation
### **Severity**
high
### **Category**
topology
### **Description**
  Scripts that modify geometry but don't recalculate normals can leave
  models with inverted or incorrect normals.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
bpy\.ops\.mesh\.(flip_normals|mirror|boolean|bridge_edge_loops|extrude)
  #### **File Patterns**
    - *.py
### **Anti Pattern Example**
  # BAD: Mirror without recalculating normals
  import bpy
  
  def mirror_mesh():
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='SELECT')
      bpy.ops.transform.mirror(constraint_axis=(True, False, False))
      # Missing: recalculate_normals!
      bpy.ops.object.mode_set(mode='OBJECT')
  
### **Correct Example**
  # GOOD: Recalculate normals after geometry operations
  import bpy
  
  def mirror_mesh():
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='SELECT')
      bpy.ops.transform.mirror(constraint_axis=(True, False, False))
      bpy.ops.mesh.normals_make_consistent(inside=False)  # Recalculate!
      bpy.ops.object.mode_set(mode='OBJECT')
  
### **Fix Suggestion**
  Add normals recalculation after geometry changes:
  ```python
  bpy.ops.mesh.normals_make_consistent(inside=False)
  ```
  

## No N-gon Check Before Export

### **Id**
no-ngon-check
### **Severity**
high
### **Category**
topology
### **Description**
  Export scripts should validate that meshes contain no n-gons before
  exporting to avoid subdivision and shading issues.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
export_scene\.(fbx|gltf|obj)
  #### **File Patterns**
    - *.py
### **Anti Pattern Example**
  # BAD: Export without n-gon validation
  import bpy
  
  def export_for_game(filepath):
      bpy.ops.export_scene.fbx(filepath=filepath)
  
### **Correct Example**
  # GOOD: Check for n-gons before export
  import bpy
  import bmesh
  
  def has_ngons(obj):
      """Check if mesh has any n-gons (faces with 5+ vertices)"""
      if obj.type != 'MESH':
          return False
      bm = bmesh.new()
      bm.from_mesh(obj.data)
      ngons = [f for f in bm.faces if len(f.verts) > 4]
      count = len(ngons)
      bm.free()
      return count > 0
  
  def export_for_game(filepath):
      for obj in bpy.context.selected_objects:
          if has_ngons(obj):
              raise ValueError(f"Object {obj.name} contains n-gons! Fix before export.")
  
      bpy.ops.export_scene.fbx(filepath=filepath)
  
### **Fix Suggestion**
  Add n-gon validation before export:
  ```python
  def has_ngons(obj):
      bm = bmesh.new()
      bm.from_mesh(obj.data)
      ngons = [f for f in bm.faces if len(f.verts) > 4]
      bm.free()
      return len(ngons) > 0
  ```
  

## No Non-Manifold Geometry Check

### **Id**
no-nonmanifold-check
### **Severity**
high
### **Category**
topology
### **Description**
  Export scripts should check for non-manifold geometry which causes
  physics and baking failures.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
export_scene\.(fbx|gltf|obj)
  #### **File Patterns**
    - *.py
### **Correct Example**
  # GOOD: Check for non-manifold geometry
  import bpy
  import bmesh
  
  def has_nonmanifold(obj):
      """Check for non-manifold edges and verts"""
      if obj.type != 'MESH':
          return False
  
      bm = bmesh.new()
      bm.from_mesh(obj.data)
  
      # Non-manifold edges (not exactly 2 faces)
      nonmanifold_edges = [e for e in bm.edges if not e.is_manifold]
  
      # Non-manifold verts (edges don't form closed fan)
      nonmanifold_verts = [v for v in bm.verts if not v.is_manifold]
  
      has_issues = len(nonmanifold_edges) > 0 or len(nonmanifold_verts) > 0
      bm.free()
      return has_issues
  
  def export_validated(filepath):
      for obj in bpy.context.selected_objects:
          if has_nonmanifold(obj):
              print(f"WARNING: {obj.name} has non-manifold geometry!")
      bpy.ops.export_scene.fbx(filepath=filepath)
  

## Missing Merge by Distance After Boolean

### **Id**
merge-by-distance-missing
### **Severity**
medium
### **Category**
topology
### **Description**
  Boolean operations leave floating vertices. Scripts should clean up
  after boolean operations.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
bpy\.ops\.object\.modifier_apply.*bool|\.BOOLEAN
  #### **File Patterns**
    - *.py
### **Anti Pattern Example**
  # BAD: Apply boolean without cleanup
  import bpy
  
  def apply_boolean(obj_name, cutter_name):
      obj = bpy.data.objects[obj_name]
      mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
      mod.object = bpy.data.objects[cutter_name]
      mod.operation = 'DIFFERENCE'
  
      bpy.context.view_layer.objects.active = obj
      bpy.ops.object.modifier_apply(modifier="Boolean")
      # Missing cleanup!
  
### **Correct Example**
  # GOOD: Clean up after boolean
  import bpy
  
  def apply_boolean_clean(obj_name, cutter_name):
      obj = bpy.data.objects[obj_name]
      mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
      mod.object = bpy.data.objects[cutter_name]
      mod.operation = 'DIFFERENCE'
      mod.solver = 'EXACT'  # More reliable solver
  
      bpy.context.view_layer.objects.active = obj
      bpy.ops.object.modifier_apply(modifier="Boolean")
  
      # CLEANUP: Remove floating vertices
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='SELECT')
      bpy.ops.mesh.remove_doubles(threshold=0.0001)
      bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
      bpy.ops.object.mode_set(mode='OBJECT')
  

## Unity Calculating Normals Instead of Importing

### **Id**
unity-import-normals-calculate
### **Severity**
medium
### **Category**
import
### **Description**
  Unity should import normals from the file rather than calculating them,
  to preserve artist intent for hard/soft edges.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
ModelImporter|ImportNormals|normalImportMode
  #### **File Patterns**
    - *.cs
    - *.meta
### **Anti Pattern Example**
  // BAD: Calculate normals in Unity
  ModelImporter importer = assetImporter as ModelImporter;
  importer.importNormals = ModelImporterNormals.Calculate;
  
### **Correct Example**
  // GOOD: Import normals from file
  ModelImporter importer = assetImporter as ModelImporter;
  importer.importNormals = ModelImporterNormals.Import;
  importer.normalCalculationMode = ModelImporterNormalCalculationMode.AreaAndAngleWeighted;
  importer.normalSmoothingSource = ModelImporterNormalSmoothingSource.FromSmoothingGroups;
  

## Unity Non-Standard Scale Factor

### **Id**
unity-scale-factor-wrong
### **Severity**
medium
### **Category**
import
### **Description**
  Unity scale factor should typically be 1.0 for properly exported assets.
  Non-standard values indicate a pipeline issue.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
globalScale\s*=\s*(?!1\.0|1f)
  #### **File Patterns**
    - *.cs
    - *.meta
### **Anti Pattern Example**
  // BAD: Compensating for bad export with scale factor
  importer.globalScale = 0.01f;  // Indicates export issue
  
### **Correct Example**
  // GOOD: Standard scale with proper export pipeline
  ModelImporter importer = assetImporter as ModelImporter;
  importer.globalScale = 1.0f;
  importer.useFileUnits = true;
  

## Unreal LOD Not Using Auto Compute

### **Id**
unreal-lod-no-auto-compute
### **Severity**
low
### **Category**
optimization
### **Description**
  For hero assets, LODs should be manually created rather than auto-computed
  to maintain quality.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
bAutoComputeLODScreenSize\s*=\s*true
  #### **File Patterns**
    - *.cpp
    - *.h
### **Correct Example**
  // For hero assets, set explicit LOD distances
  StaticMesh->bAutoComputeLODScreenSize = false;
  StaticMesh->SourceModels[0].ScreenSize = 1.0f;
  StaticMesh->SourceModels[1].ScreenSize = 0.5f;
  StaticMesh->SourceModels[2].ScreenSize = 0.25f;
  

## Unreal Using Complex Collision

### **Id**
unreal-collision-not-simplified
### **Severity**
medium
### **Category**
optimization
### **Description**
  Using the render mesh for collision is expensive. Most objects should
  use simplified collision.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
CollisionTraceFlag\s*=\s*CTF_UseComplexAsSimple|bUseComplexAsSimpleCollision\s*=\s*true
  #### **File Patterns**
    - *.cpp
    - *.h
    - *.ini
### **Anti Pattern Example**
  // BAD: Using render mesh for collision (expensive)
  StaticMeshComponent->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
  StaticMesh->ComplexCollisionMesh = StaticMesh;
  StaticMesh->bUseComplexAsSimpleCollision = true;
  
### **Correct Example**
  // GOOD: Use simplified collision
  // In Blender: Create low-poly collision mesh named UCX_MeshName
  // Or in Unreal: Auto-generate convex collision
  StaticMesh->CreateBodySetup();
  StaticMesh->BodySetup->CollisionTraceFlag = CTF_UseSimpleAsComplex;
  
  // For simple shapes, use primitives
  UBoxComponent* BoxCollision = CreateDefaultSubobject<UBoxComponent>(TEXT("BoxCollision"));
  

## Godot Not Generating Collision Shape

### **Id**
godot-mesh-not-generating-collision
### **Severity**
medium
### **Category**
import
### **Description**
  Imported meshes in Godot should have collision shapes generated for
  physics interaction.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
\.glb|\.gltf
  #### **File Patterns**
    - *.tscn
    - *.tres
### **Correct Example**
  # In Godot import settings (.import file):
  [params]
  meshes/generate_collision_shapes=true
  meshes/collision_shape_type=1  # Convex
  
  # Or programmatically:
  var mesh_instance = MeshInstance3D.new()
  mesh_instance.mesh = load("res://models/object.glb")
  mesh_instance.create_trimesh_collision()  # For static
  # OR
  mesh_instance.create_convex_collision()   # For dynamic
  

## Invalid Asset Naming Convention

### **Id**
invalid-asset-naming
### **Severity**
low
### **Category**
organization
### **Description**
  Asset names should follow consistent conventions for organization
  and automation compatibility.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
(?i)^(final|new|test|old|copy|backup|\d+)[._-]|\s+\.|[^a-zA-Z0-9_.-]
  #### **File Patterns**
    - *.fbx
    - *.obj
    - *.gltf
    - *.glb
    - *.blend
### **Anti Pattern Example**
  # BAD naming examples:
  Final_Chair.fbx
  chair final v2.fbx
  New Folder/model.fbx
  test123.fbx
  chair (1).fbx
  
### **Correct Example**
  # GOOD naming convention:
  SM_Chair_Wood_LOD0.fbx
  SK_Character_Hero.fbx
  SM_Prop_Barrel_Metal_v02.fbx
  
  # Pattern: [Type]_[Category]_[Name]_[Variant]_[LOD/Version]
  

## Missing LOD Suffix on LOD Meshes

### **Id**
missing-lod-suffix
### **Severity**
low
### **Category**
organization
### **Description**
  LOD meshes should have explicit _LOD# suffix for proper identification
  and auto-import by game engines.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
(?<!LOD[0-9])\.fbx$
  #### **File Patterns**
    - *_low.fbx
    - *_med.fbx
    - *_high.fbx
### **Anti Pattern Example**
  # BAD: Unclear LOD naming
  chair_low.fbx
  chair_medium.fbx
  chair_high.fbx
  
### **Correct Example**
  # GOOD: Standard LOD naming
  SM_Chair_LOD0.fbx  # Base mesh
  SM_Chair_LOD1.fbx  # 50% reduction
  SM_Chair_LOD2.fbx  # 25% reduction
  SM_Chair_LOD3.fbx  # 12.5% reduction
  

## Non-Power-of-Two Texture Dimensions

### **Id**
non-power-of-two-textures
### **Severity**
medium
### **Category**
optimization
### **Description**
  Textures should be power-of-two dimensions (256, 512, 1024, 2048, 4096)
  for optimal GPU memory usage and mipmap generation.
  
### **Detection**
  #### **Type**
script
  #### **Script**
    # This would be validated by a separate texture checking tool
    # Dimensions should be: 256, 512, 1024, 2048, 4096
    valid_sizes = [256, 512, 1024, 2048, 4096, 8192]
    
### **File Patterns**
  - *.png
  - *.tga
  - *.jpg
### **Correct Example**
  # GOOD texture dimensions:
  T_Chair_D.png     # 2048x2048
  T_Character_D.png # 4096x4096
  T_Icon_UI.png     # 256x256
  
  # Can be non-square but still power-of-two:
  T_Ribbon_D.png    # 2048x256
  

## Wrong Texture Type Suffix

### **Id**
wrong-texture-suffix
### **Severity**
low
### **Category**
organization
### **Description**
  Texture files should have correct suffixes indicating their type
  for material auto-assignment.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
(?i)(?<!_[DNRMAOHE])(_diffuse|_normal|_roughness|_metallic|_ao|_height|_emissive|_opacity)\.(?:png|tga|jpg)
  #### **File Patterns**
    - *.png
    - *.tga
    - *.jpg
### **Anti Pattern Example**
  # BAD: Full word suffixes (inconsistent)
  chair_diffuse.png
  chair_normal.png
  chair_roughness.png
  
### **Correct Example**
  # GOOD: Single letter suffixes (industry standard)
  T_Chair_D.png   # Diffuse/Albedo
  T_Chair_N.png   # Normal
  T_Chair_R.png   # Roughness
  T_Chair_M.png   # Metallic
  T_Chair_AO.png  # Ambient Occlusion
  T_Chair_H.png   # Height
  T_Chair_E.png   # Emissive
  
  # OR packed textures:
  T_Chair_ORM.png # Occlusion, Roughness, Metallic (RGB)
  T_Chair_ARM.png # AO, Roughness, Metallic (RGB)
  