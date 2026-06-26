"""Vision via OpenAWS — uses session's configured Anthropic client."""

import base64
import os
import tempfile
from pathlib import Path


class OpenClawVisionClient:
    """Use Anthropic via OpenAWS session config."""
    
    def __init__(self, config: dict):
        self.model = config.get("vision_model") or "claude-3-5-sonnet-20241022"
    
    def analyze_frames(self, frames: list, prompt: str, max_tokens: int = 1000, json_mode: bool = False) -> tuple:
        """Analyze frames using Anthropic."""
        from anthropic import Anthropic
        
        # Get API key from environment (set by OpenAWS)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set. Run from OpenAWS session.")
        
        client = Anthropic(api_key=api_key)
        
        if len(frames) == 1:
            img_path = self._save_frame(frames[0])
        else:
            img_path = self._create_grid(frames)
        
        try:
            with open(img_path, 'rb') as f:
                img_data = base64.standard_b64encode(f.read()).decode()
            
            if json_mode:
                prompt += "\n\nOutput valid JSON only."
            
            response = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_data}},
                        {"type": "text", "text": prompt}
                    ]
                }]
            )
            
            result = response.content[0].text
            if json_mode:
                result = self._extract_json(result)
            
            return result, {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        finally:
            img_path.unlink(missing_ok=True)
    
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
