import subprocess
import json
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(MODULE_DIR, "..", "..", "scripts"))
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "analyze_blends.py")

def analyze_blender_file(blend_file: str):
    """
    OpenClaw Skill: Executes Blender in background mode to analyze scene settings.
    """
    command = [
        "blender", 
        "-b", blend_file, 
        "-P", SCRIPT_PATH
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Parse output between markers
        output = result.stdout
        if "---ANALYSIS_START---" in output and "---ANALYSIS_END---" in output:
            start = output.find("---ANALYSIS_START---") + len("---ANALYSIS_START---\n")
            end = output.find("---ANALYSIS_END---")
            json_str = output[start:end].strip()
            return {"status": "success", "data": json.loads(json_str)}
        else:
            return {"status": "error", "message": "Failed to find analysis markers in output.", "log": output[-500:]}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}


def analyze_dataset(image_paths: list[str]) -> dict:
    """
    Computes dataset-wide diversity (Shannon entropy) and average Naturalness across a list of images.
    
    :param image_paths: List of absolute paths to images.
    :return: Dict containing status, diversity, naturalness_mean, and individual_metrics.
    """
    if not image_paths:
        return {"status": "error", "message": "No image paths provided."}
        
    try:
        import granatpy
        import numpy as np
        from PIL import Image
    except ImportError as e:
        return {"status": "error", "message": f"Required library not installed: {str(e)}"}

    # Filter out paths that don't exist
    valid_paths = [p for p in image_paths if os.path.exists(p)]
    if not valid_paths:
        return {"status": "error", "message": "None of the provided image paths exist."}

    # Compute dataset-wide Shannon entropy (Diversity)
    try:
        diversity = float(granatpy.dataset_entropy(valid_paths))
    except ValueError as e:
        return {
            "status": "error", 
            "message": f"Failed to compute dataset entropy: No images could be loaded. Details: {str(e)}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to compute dataset entropy: {str(e)}"}

    # Compute Naturalness for each image
    naturalness_scores = []
    individual_metrics = {}
    
    for path in valid_paths:
        try:
            img = Image.open(path).convert('RGB')
            img_np = np.array(img)
            _, nfs, _, _, _ = granatpy.naturalize_rgb_image(img_np)
            mean_nf = float(np.mean(nfs))
            naturalness_scores.append(mean_nf)
            individual_metrics[path] = {
                "naturalness_mean": mean_nf,
                "naturalness_channels": [float(x) for x in nfs]
            }
        except Exception as e:
            individual_metrics[path] = {
                "error": f"Failed to compute naturalness: {str(e)}"
            }

    if not naturalness_scores:
        return {
            "status": "error",
            "message": "Failed to compute naturalness for any of the images.",
            "diversity": diversity
        }

    return {
        "status": "success",
        "diversity": diversity,
        "naturalness_mean": float(np.mean(naturalness_scores)),
        "individual_metrics": individual_metrics
    }

