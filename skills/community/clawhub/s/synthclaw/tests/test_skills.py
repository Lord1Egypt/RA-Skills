import os
import json
import shutil
from synthclaw import (
    analyze_blend,
    render_procedural_scene_fast,
    analyze_dataset,
    render_procedural_dataset
)

def test_blender_skill():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_blend = os.path.join(repo_root, "assets", "test.blend")

    print(f"Testing against test.blend at: {test_blend}")
    if not os.path.exists(test_blend):
        print("ERROR: Could not find test.blend. Skipping tests.")
        return

    print("\n--- Analyzing Test File ---")
    res = analyze_blend(test_blend)
    print(json.dumps(res, indent=2))
    assert res["status"] == "success"
    assert "AgentControl" in res["parameters"]["value_nodes"]

def test_render_procedural_scene():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_blend = os.path.join(repo_root, "assets", "test.blend")
    output_dir = os.path.join(repo_root, "output")
    output_path = os.path.join(output_dir, "test_render.png")
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    if not os.path.exists(test_blend):
        print("ERROR: Could not find test.blend. Skipping render test.")
        return
        
    print("\n--- Testing Procedural Scene Rendering ---")
    res = render_procedural_scene_fast(
        blend_file=test_blend,
        output_path=output_path,
        parameters={"AgentControl": 0.9}
    )
    print("Render Result:", json.dumps(res, indent=2))
    
    assert res["status"] == "success"
    assert os.path.exists(output_path), f"File {output_path} does not exist! Rendered file might have different name."

def test_generate_dataset():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_blend = os.path.join(repo_root, "assets", "test.blend")
    dataset_dir = os.path.join(repo_root, "output", "dataset")
    images_dir = os.path.join(dataset_dir, "images")
    metadata_dir = os.path.join(dataset_dir, "metadata")
    
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
        
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    if not os.path.exists(test_blend):
        print("ERROR: Could not find test.blend. Skipping dataset generation test.")
        return
        
    print("\n--- Testing Procedural Dataset Generation ---")
    # 1. Analyze the blend file to discover parameters dynamically
    analysis = analyze_blend(test_blend)
    assert analysis["status"] == "success"
    value_nodes = list(analysis["parameters"]["value_nodes"].keys())
    assert len(value_nodes) > 0, "No value nodes available for sweep."
    
    target_param = value_nodes[0] # "AgentControl"
    
    # 2. Define sweep parameters
    sweep_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    # 3. Generate the images and metadata JSONs
    for idx, val in enumerate(sweep_values, 1):
        filename_base = f"image_{idx:04d}"
        img_name = f"{filename_base}.png"
        meta_name = f"{filename_base}.json"
        
        img_path = os.path.join(images_dir, img_name)
        meta_path = os.path.join(metadata_dir, meta_name)
        
        # Render the procedural scene
        render_res = render_procedural_scene_fast(
            blend_file=test_blend,
            output_path=img_path,
            parameters={target_param: val}
        )
        assert render_res["status"] == "success"
        assert os.path.exists(img_path)
        
        # Write matching metadata/ground truth JSON
        metadata = {
            "image_file": os.path.join("images", img_name),
            "parameters": {
                target_param: val
            }
        }
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)
            
        print(f"Generated sample {idx}: {img_name} and {meta_name} with {target_param}={val}")
        
    # 4. Verify outputs
    generated_images = os.listdir(images_dir)
    generated_metadata = os.listdir(metadata_dir)
    
    assert len(generated_images) == len(sweep_values)
    assert len(generated_metadata) == len(sweep_values)
    
    for meta_file in generated_metadata:
        with open(os.path.join(metadata_dir, meta_file), "r") as f:
            data = json.load(f)
            assert "image_file" in data
            assert target_param in data["parameters"]

def test_analyze_dataset():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dataset_dir = os.path.join(repo_root, "output", "dataset")
    images_dir = os.path.join(dataset_dir, "images")
    
    if not os.path.exists(images_dir):
        print("ERROR: Dataset images not found. Skipping test_analyze_dataset.")
        return
        
    image_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith(".png")]
    if not image_files:
        print("ERROR: No images found. Skipping test_analyze_dataset.")
        return
        
    print("\n--- Testing Dataset Analysis (Diversity & Naturalness) ---")
    res = analyze_dataset(image_files)
    print("Analysis Result:", json.dumps(res, indent=2))
    
    assert res["status"] == "success"
    assert "diversity" in res
    assert "naturalness_mean" in res
    assert isinstance(res["diversity"], float)
    assert isinstance(res["naturalness_mean"], float)
    assert len(res["individual_metrics"]) == len(image_files)

def test_render_procedural_dataset():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_blend = os.path.join(repo_root, "assets", "test.blend")
    output_dir = os.path.join(repo_root, "output", "procedural_dataset")
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    if not os.path.exists(test_blend):
        print("ERROR: Could not find test.blend. Skipping render dataset test.")
        return

    # Analyze blend to find material of AgentControl
    analysis = analyze_blend(test_blend)
    assert analysis["status"] == "success"
    value_nodes = analysis["parameters"]["value_nodes"]
    assert "AgentControl" in value_nodes
    mat_name = value_nodes["AgentControl"]["material"]

    print("\n--- Testing Generic Procedural Dataset Rendering ---")
    randomizations = [
        {
            "type": "value_node",
            "target": mat_name,
            "sub_target": "AgentControl",
            "distribution": "uniform",
            "range": [0.1, 0.9]
        }
    ]
    
    res = render_procedural_dataset(
        blend_file=test_blend,
        output_dir=output_dir,
        num_images=3,
        randomizations=randomizations,
        engine="EEVEE"
    )
    print("Render Dataset Result:", json.dumps(res, indent=2))
    assert res["status"] == "success"
    assert os.path.exists(output_dir)
    
    files = os.listdir(output_dir)
    rendered_images = [f for f in files if f.endswith(".png")]
    print("Generated files:", rendered_images)
    assert len(rendered_images) == 3

if __name__ == "__main__":
    test_blender_skill()
    test_render_procedural_scene()
    test_generate_dataset()
    test_analyze_dataset()
    test_render_procedural_dataset()

