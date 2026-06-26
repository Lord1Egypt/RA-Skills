"""Vision via OpenAWS Sub-Agent — spawn isolated agent for image analysis."""

import json
import os
import tempfile
from pathlib import Path


class SubAgentVisionClient:
    """Use OpenAWS sub-agent for vision analysis."""
    
    def __init__(self, config: dict):
        self.model = config.get("vision_model") or "relay/claude-opus-4-6"
    
    def analyze_frames(self, frames: list, prompt: str, max_tokens: int = 1000, json_mode: bool = False) -> tuple:
        """Analyze frames using sub-agent with image tool."""
        
        # Save frames to temp files
        if len(frames) == 1:
            img_path = self._save_frame(frames[0])
        else:
            img_path = self._create_grid(frames)
        
        try:
            # Build sub-agent task
            task = f"""{prompt}

Image: {img_path}

{"Output valid JSON only." if json_mode else ""}"""
            
            # Spawn sub-agent (this will be called from OpenAWS context)
            result = self._call_subagent(task, str(img_path))
            
            if json_mode:
                result = self._extract_json(result)
            
            # Return with dummy usage (sub-agent handles tokens internally)
            return result, {"input_tokens": 0, "output_tokens": 0}
        
        finally:
            img_path.unlink(missing_ok=True)
    
    def _call_subagent(self, task: str, image_path: str) -> str:
        """Call OpenAWS sessions_spawn with image analysis task."""
        # This will be injected by the CLI wrapper
        # For now, return placeholder
        raise NotImplementedError("Sub-agent call must be handled by CLI wrapper")
    
    def _save_frame(self, frame_data: dict) -> Path:
        """Save single frame to temp file."""
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.write(frame_data["image_bytes"])
        tmp.close()
        return Path(tmp.name)
    
    def _create_grid(self, frames: list) -> Path:
        """Create grid image from multiple frames."""
        import cv2
        import numpy as np
        
        images = []
        for frame_data in frames:
            arr = np.frombuffer(frame_data["image_bytes"], dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            images.append(img)
        
        n = len(images)
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
        
        target_w, target_h = 320, 240
        resized = [cv2.resize(img, (target_w, target_h)) for img in images]
        
        while len(resized) < rows * cols:
            resized.append(np.zeros((target_h, target_w, 3), dtype=np.uint8))
        
        grid_rows = []
        for r in range(rows):
            row_imgs = resized[r * cols:(r + 1) * cols]
            grid_rows.append(np.hstack(row_imgs))
        grid = np.vstack(grid_rows)
        
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        cv2.imwrite(tmp.name, grid)
        tmp.close()
        return Path(tmp.name)
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from response."""
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return text.strip()
