import os

def clean_up_tifs(output_dir):
    """
    Walks the output directories and removes unnecessary .tif files.
    """
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.tif'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"[SynthClaw] CleanUp: Deleted temporary TIFF file {os.path.join(root, file)}")
                except Exception as e:
                    print(f"[SynthClaw] CleanUp: Failed to delete TIFF file {file}: {e}")
