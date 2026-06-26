import subprocess
import os
import json

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(MODULE_DIR, "..", "..", "scripts"))
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "agent_bridge.py")

# Default timeouts
DEFAULT_TIMEOUT_CYCLES = 1800      # 30 minutes for Cycles (production quality)
DEFAULT_TIMEOUT_EEVEE = 60          # 1 minute for EEVEE (fast testing)


def render_procedural_scene(
    blend_file: str, 
    output_path: str, 
    parameters: dict, 
    samples: int = 128,
    engine: str = "CYCLES",
    timeout: int = None,
    reference_image: str = None,
    compute_metrics: bool = False
):
    """
    OpenClaw Skill: Executes Blender in background mode to render a procedural scene.
    
    :param blend_file: Absolute path to the .blend file.
    :param output_path: Where to save the resulting image (e.g., /tmp/render.png).
    :param parameters: A dictionary of node names and float values (e.g., {"Scale": 5.0}).
    :param samples: Cycles samples for rendering (default: 128). Ignored for EEVEE.
    :param engine: Render engine - "CYCLES" (production) or "EEVEE" (fast testing).
    :param timeout: Custom timeout in seconds. Defaults based on engine.
    :return: Dict with status, output path, and log or error message.
    """
    # Validate engine choice
    engine = engine.upper()
    if engine not in ["CYCLES", "EEVEE", "BLENDER_EEVEE_NEXT"]:
        return {"status": "error", "message": f"Invalid engine '{engine}'. Use 'CYCLES' or 'EEVEE'"}
    
    # Set default timeout based on engine
    if timeout is None:
        timeout = DEFAULT_TIMEOUT_CYCLES if engine == "CYCLES" else DEFAULT_TIMEOUT_EEVEE
    
    # Validate blend file exists
    if not os.path.exists(blend_file):
        return {"status": "error", "message": f"Blend file not found: {blend_file}"}
    
    # Validate output directory exists
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            return {"status": "error", "message": f"Cannot create output directory: {e}"}
    
    # Validate parameters are numeric
    for k, v in parameters.items():
        if not isinstance(v, (int, float)):
            return {"status": "error", "message": f"Parameter '{k}' must be a number, got {type(v).__name__}"}
    
    # Format parameters for the Blender script (key=value)
    param_args = [f"{k}={v}" for k, v in parameters.items()]
    
    # Pass engine and samples to the Blender script via environment variables
    env = os.environ.copy()
    env["SYNTHCLAW_PACKAGE_PATH"] = os.path.abspath(os.path.join(MODULE_DIR, ".."))
    env["BLENDER_ENGINE"] = engine
    env["BLENDER_SAMPLES"] = str(samples)
    
    # Build the CLI command
    # -b: background, -P: run python script, -o: output, -f 1: render frame 1
    command = [
        "blender", 
        "-b", blend_file, 
        "-P", SCRIPT_PATH, 
        "-o", output_path, 
        "-f", "1", 
        "--"
    ] + param_args

    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=timeout,
            env=env
        )
        
        # Check if output_path exists, otherwise find and rename the file Blender actually wrote
        if not os.path.exists(output_path):
            base, ext = os.path.splitext(output_path)
            possible_path_1 = f"{base}{ext}0001{ext}"
            possible_path_2 = f"{base}0001{ext}"
            if os.path.exists(possible_path_1):
                os.rename(possible_path_1, output_path)
            elif os.path.exists(possible_path_2):
                os.rename(possible_path_2, output_path)

        metrics = {}
        if compute_metrics:
            try:
                import numpy as np
                from PIL import Image
                test_img = Image.open(output_path).convert('RGB')
                img_np = np.array(test_img)
                
                # GranatPy Metrics
                try:
                    import granatpy
                    # Single Image Naturalness
                    _, nfs, _, _, _ = granatpy.naturalize_rgb_image(img_np)
                    metrics["naturalness_channels"] = [float(x) for x in nfs]
                    metrics["naturalness_mean"] = float(np.mean(nfs))
                    
                    # Comparative Metrics
                    if reference_image and os.path.exists(reference_image):
                        ref_img = Image.open(reference_image).convert('RGB')
                        ref_np = np.array(ref_img)
                        comp_metrics = granatpy.compute_all_metrics(ref_np, img_np, verbose=False)
                        for k, v in comp_metrics.items():
                            metrics[f"granatpy_{k}"] = float(v)
                except ImportError:
                    metrics["granatpy_status"] = "granatpy not installed"
                except Exception as e:
                    metrics["granatpy_error"] = str(e)
                
                # LPIPS Metric
                if reference_image and os.path.exists(reference_image):
                    try:
                        import torch
                        import torchvision.transforms.functional as TF
                        import lpips
                        
                        ref_img = Image.open(reference_image).convert('RGB')
                        img_t = TF.to_tensor(test_img) * 2 - 1
                        ref_t = TF.to_tensor(ref_img) * 2 - 1
                        
                        img_t = img_t.unsqueeze(0)
                        ref_t = ref_t.unsqueeze(0)
                        
                        # Using alexnet as default
                        loss_fn_alex = lpips.LPIPS(net='alex', verbose=False)
                        lpips_val = loss_fn_alex(img_t, ref_t)
                        metrics["lpips_alex"] = float(lpips_val.item())
                    except ImportError:
                        metrics["lpips_status"] = "lpips not installed"
                    except Exception as e:
                        metrics["lpips_error"] = str(e)
                        
            except Exception as e:
                metrics["error"] = str(e)

        return {
            "status": "success", 
            "output": output_path, 
            "log": result.stdout[-500:],
            "engine": engine,
            "samples": samples if engine == "CYCLES" else None,
            "metrics": metrics
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": f"Render timed out after {timeout} seconds"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}


def render_procedural_scene_fast(
    blend_file: str, 
    output_path: str, 
    parameters: dict,
    reference_image: str = None,
    compute_metrics: bool = False
):
    """
    Convenience function for fast EEVEE rendering (testing).
    Same as render_procedural_scene with engine='EEVEE'.
    """
    return render_procedural_scene(
        blend_file=blend_file,
        output_path=output_path,
        parameters=parameters,
        engine="EEVEE",
        timeout=DEFAULT_TIMEOUT_EEVEE,
        reference_image=reference_image,
        compute_metrics=compute_metrics
    )


def render_procedural_scene_production(
    blend_file: str, 
    output_path: str, 
    parameters: dict,
    samples: int = 512,
    reference_image: str = None,
    compute_metrics: bool = False
):
    """
    Convenience function for production Cycles rendering.
    Same as render_procedural_scene with engine='CYCLES' and higher samples.
    """
    return render_procedural_scene(
        blend_file=blend_file,
        output_path=output_path,
        parameters=parameters,
        samples=samples,
        engine="CYCLES",
        timeout=DEFAULT_TIMEOUT_CYCLES,
        reference_image=reference_image,
        compute_metrics=compute_metrics
    )


def analyze_blend(blend_file: str):
    """
    Analyzes a Blender file and returns available Value Nodes.
    
    :param blend_file: Absolute path to the .blend file.
    :return: Dict with status and list of available parameters or error message.
    """
    # Validate blend file exists
    if not os.path.exists(blend_file):
        return {"status": "error", "message": f"Blend file not found: {blend_file}"}
    
    # Path to the analyze script
    ANALYZE_SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "analyze_blends.py")
    
    command = [
        "blender",
        "-b", blend_file,
        "-P", ANALYZE_SCRIPT_PATH,
        "--"
    ]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=60  # 1 minute timeout for analysis
        )
        
        output = result.stdout
        if "---ANALYSIS_START---" in output and "---ANALYSIS_END---" in output:
            start = output.find("---ANALYSIS_START---") + len("---ANALYSIS_START---\n")
            end = output.find("---ANALYSIS_END---")
            json_str = output[start:end].strip()
            return {
                "status": "success",
                "parameters": json.loads(json_str),
                "blend_file": blend_file
            }
        else:
            return {"status": "error", "message": "Failed to find analysis markers in output.", "log": output[-500:]}
            
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Analysis timed out after 60 seconds"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}


def render_procedural_dataset(
    blend_file: str,
    output_dir: str,
    num_images: int = 2,
    randomizations: list = None,
    engine: str = "CYCLES",
    samples: int = 128,
    timeout: int = None
):
    """
    OpenClaw Skill: Generates a procedural dataset from any .blend file by executing
    frame-by-frame sweeps with dynamic randomization rules.
    
    :param blend_file: Absolute path to the .blend file.
    :param output_dir: Absolute path to save the dataset.
    :param num_images: Number of images to render (default: 2).
    :param randomizations: List of randomization rules.
    :param engine: Render engine - "CYCLES" or "EEVEE".
    :param samples: Cycles samples per frame (default: 128).
    :param timeout: Custom timeout in seconds.
    :return: Dict with status and output path details.
    """
    engine = engine.upper()
    if engine not in ["CYCLES", "EEVEE"]:
        return {"status": "error", "message": f"Invalid engine '{engine}'. Use 'CYCLES' or 'EEVEE'"}
        
    # Validate blend file exists
    if not os.path.exists(blend_file):
        return {"status": "error", "message": f"Blend file not found: {blend_file}"}

    # Set default timeout based on engine and count
    if timeout is None:
        base_timeout = DEFAULT_TIMEOUT_CYCLES if engine == "CYCLES" else DEFAULT_TIMEOUT_EEVEE
        timeout = base_timeout * num_images

    # Validate output directory
    output_dir = os.path.abspath(output_dir)
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        return {"status": "error", "message": f"Cannot create output directory: {e}"}

    # Generate config data and write to a temporary file
    config_data = {
        "output_dir": output_dir,
        "num_images": num_images,
        "randomizations": randomizations or []
    }
    
    import tempfile
    config_fd, config_path = tempfile.mkstemp(suffix=".json", dir=output_dir)
    try:
        with os.fdopen(config_fd, 'w') as f:
            json.dump(config_data, f, indent=2)
            
        script_path = os.path.join(SCRIPTS_DIR, "render_dataset.py")
        
        # Pass engine and samples to the Blender script via environment variables
        env = os.environ.copy()
        env["SYNTHCLAW_PACKAGE_PATH"] = os.path.abspath(os.path.join(MODULE_DIR, ".."))
        env["BLENDER_ENGINE"] = engine
        env["BLENDER_SAMPLES"] = str(samples)
        
        command = [
            "blender", 
            "-b", blend_file, 
            "-P", script_path, 
            "--",
            config_path
        ]
        
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=timeout,
            env=env
        )
        
        return {
            "status": "success",
            "output_dir": output_dir,
            "images_generated": num_images,
            "log": result.stdout[-500:]
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": f"Render dataset timed out after {timeout} seconds"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr or e.stdout}
    finally:
        if os.path.exists(config_path):
            try:
                os.remove(config_path)
            except Exception:
                pass


# Example usage for OpenClaw registration:
# {
#   "name": "render_procedural_scene",
#   "description": "Adjusts procedural nodes and renders a frame in Blender 4.0+",
#   "parameters": { ... }
# }

