"""Vision API client — unified interface for OpenAI, Anthropic, and OpenClaw."""

import base64
import json


def create_vision_client(config: dict):
    """Create vision client based on provider."""
    provider = config.get("provider", "openclaw")
    
    if provider == "openclaw":
        from videoarm_lib.vision_openclaw import OpenClawVisionClient
        return OpenClawVisionClient(config)
    elif provider == "anthropic":
        return AnthropicVisionClient(config)
    else:
        return OpenAIVisionClient(config)


class OpenAIVisionClient:
    """OpenAI vision API client."""
    
    def __init__(self, config: dict):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=config["openai_api_key"],
            base_url=config.get("openai_base_url"),
        )
        self.model = config["vision_model"]
    
    def analyze_frames(self, frames: list, prompt: str, max_tokens: int = 1000, json_mode: bool = False) -> tuple:
        """Analyze frames with prompt. Returns (content, usage_dict)."""
        content = [{"type": "text", "text": prompt}]
        for frame_data in frames:
            img_b64 = base64.b64encode(frame_data["image_bytes"]).decode()
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}})
        
        kwargs = {"model": self.model, "messages": [{"role": "user", "content": content}], "max_tokens": max_tokens}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        usage = response.usage
        return response.choices[0].message.content, {
            "input_tokens": usage.prompt_tokens if usage else 0,
            "output_tokens": usage.completion_tokens if usage else 0,
        }


class AnthropicVisionClient:
    """Anthropic vision API client."""
    
    def __init__(self, config: dict):
        from anthropic import Anthropic
        kwargs = {"api_key": config["anthropic_api_key"]}
        if config.get("anthropic_base_url"):
            kwargs["base_url"] = config["anthropic_base_url"]
        self.client = Anthropic(**kwargs)
        self.model = config["vision_model"]
    
    def analyze_frames(self, frames: list, prompt: str, max_tokens: int = 1000, json_mode: bool = False) -> tuple:
        """Analyze frames with prompt. Returns (content, usage_dict)."""
        content = []
        for frame_data in frames:
            img_b64 = base64.b64encode(frame_data["image_bytes"]).decode()
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}
            })
        content.append({"type": "text", "text": prompt})
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": content}]
        )
        
        result = response.content[0].text
        if json_mode:
            result = self._extract_json(result)
        
        return result, {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from Claude response."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
