from abc import ABC, abstractmethod


class BaseImageProvider(ABC):
    """Abstract base class for image generation providers."""

    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str, model: str = None, output_path: str = None, input_image: str = None) -> dict:
        """Generate or edit an image from a text prompt.

        Args:
            prompt: text prompt
            model: model identifier
            output_path: where to save the result
            input_image: path to input image for editing (optional)

        Returns dict with keys:
            status: "ok" | "error"
            image_path: absolute path to saved image
            model: model used
            provider: provider name
            metadata: any extra info
        """
        pass

    @abstractmethod
    def list_models(self) -> list:
        """Return list of available model identifiers."""
        pass

    @abstractmethod
    def validate_config(self, config: dict) -> bool:
        """Check that all required config/env vars are present."""
        pass
