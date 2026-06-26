"""Gemini image generation client."""

from pathlib import Path
from io import BytesIO
import base64

from PIL import Image as PILImage

from image_client import ImageClient, ImageGenerationError


# Gemini image size mapping (use "1K", "2K", "4K" format per API docs)
GEMINI_SIZES = {
    "1K": "1K",
    "2K": "2K",
    "4K": "4K",
}


class GeminiImageClient(ImageClient):
    """Gemini image generation client."""

    def __init__(self, model: str = "gemini-3-pro-image-preview") -> None:
        self.model = model

    def _resolve_resolution(self, resolution: str) -> str:
        """Map resolution tier to Gemini image size."""
        return GEMINI_SIZES.get(resolution, "2048x2048")

    def generate(
        self,
        prompt: str,
        filename: str,
        resolution: str,
        api_key: str,
    ) -> Path:
        """
        Generate image using Gemini.

        Raises:
            ImageGenerationError: On any failure
        """
        from google import genai
        from google.genai import types

        # Input validation
        if not prompt or not prompt.strip():
            raise ImageGenerationError("Prompt cannot be empty")
        if not api_key or not api_key.strip():
            raise ImageGenerationError("API key cannot be empty")

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        size = self._resolve_resolution(resolution)

        client = genai.Client(api_key=api_key)

        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(
                        image_size=size
                    )
                )
            )
        except Exception as e:
            # Broad exception catch is intentional: Gemini SDK raises various
            # errors that all indicate API failure. We consolidate them here.
            raise ImageGenerationError(f"Gemini API error: {e}") from e

        image_saved = False
        for part in response.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure RGB mode for PNG
                if image.mode == "RGBA":
                    rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), "PNG")
                elif image.mode == "RGB":
                    image.save(str(output_path), "PNG")
                else:
                    image.convert("RGB").save(str(output_path), "PNG")

                image_saved = True

        if not image_saved:
            raise ImageGenerationError("No image was generated in the response")

        return output_path.resolve()
