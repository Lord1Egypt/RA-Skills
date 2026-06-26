import os
import sys
import bpy

def configure_render_engine():
    """
    Configure Cycles or EEVEE engine, sample counts, and configure GPU devices.
    """
    engine = os.environ.get("BLENDER_ENGINE", "CYCLES").upper()
    samples = int(os.environ.get("BLENDER_SAMPLES", "128"))
    
    if engine in ["EEVEE", "BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"]:
        # EEVEE in Blender 4.0+ is BLENDER_EEVEE or BLENDER_EEVEE_NEXT
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        print(f"[SynthClaw] Using EEVEE engine (fast mode)")
    else:
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = samples
        print(f"[SynthClaw] Using CYCLES engine with {samples} samples (production mode)")
        
        # Configure GPU devices if possible, otherwise fallback to CPU
        try:
            cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
            if sys.platform == 'darwin':
                cycles_prefs.compute_device_type = "METAL"
                print("[SynthClaw] Set compute_device_type to METAL")
            else:
                cycles_prefs.compute_device_type = "CUDA"
                print("[SynthClaw] Set compute_device_type to CUDA")
                
            cycles_prefs.get_devices()
            
            gpu_enabled = False
            for device in cycles_prefs.devices:
                device.use = True
                if device.type in ['METAL', 'CUDA', 'OPTIX']:
                    gpu_enabled = True
                print(f" - {device.name} ({device.type}) - {'ENABLED' if device.use else 'DISABLED'}")
                
            if gpu_enabled:
                bpy.context.scene.cycles.device = 'GPU'
                print(f"[SynthClaw] Render device set to GPU ({cycles_prefs.compute_device_type})")
            else:
                bpy.context.scene.cycles.device = 'CPU'
                print("[SynthClaw] No GPU devices found. Set device to CPU (fallback)")
        except Exception as e:
            print(f"[SynthClaw] Could not set Cycles device preferences: {e}")
            bpy.context.scene.cycles.device = 'CPU'
            print("[SynthClaw] Falling back to CPU rendering")
