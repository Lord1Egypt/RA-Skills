from dataclasses import dataclass, field
from pathlib import Path
import os


@dataclass
class VisionConfig:
    screenshot_dir: Path = Path("runtime/screenshots")
    ocr_lang: str = "chi_sim+eng"
    use_ocr: bool = True
    use_vlm: bool = False
    default_confidence: float = 0.55
    max_candidates: int = 10


@dataclass
class InputConfig:
    move_duration_fast: float = 0.12
    move_duration_safe: float = 0.25
    click_pause: float = 0.12
    type_interval: float = 0.012
    use_clipboard_for_non_ascii: bool = True
    post_action_delay: float = 0.2


@dataclass
class RuntimeConfig:
    mode: str = "adaptive"
    verify_after_action: bool = True
    max_retries: int = 3
    debug: bool = True
    browser_address_bar_y: int = 50
    browser_address_bar_x: int = 500
    preferred_window_titles: tuple = ("Chrome", "Google Chrome", "Edge", "浏览器")
    use_dom_backend: bool = os.environ.get("PYAUTOGUI_CONTROLLER_USE_DOM", "1") != "0"


@dataclass
class AppConfig:
    vision: VisionConfig = field(default_factory=VisionConfig)
    input: InputConfig = field(default_factory=InputConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
