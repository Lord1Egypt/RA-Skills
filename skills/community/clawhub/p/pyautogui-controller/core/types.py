from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class BackendMode(str, Enum):
    BROWSER = "browser"
    DESKTOP = "desktop"
    VISION = "vision"
    HYBRID = "hybrid"


class ActionType(str, Enum):
    OPEN_APP = "open_app"
    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    HOTKEY = "hotkey"
    WAIT = "wait"
    SCROLL = "scroll"
    SCREENSHOT = "screenshot"
    FOCUS_INPUT = "focus_input"
    COMPOUND = "compound"
    UNKNOWN = "unknown"


class ElementType(str, Enum):
    BUTTON = "button"
    INPUT = "input"
    CHECKBOX = "checkbox"
    LINK = "link"
    REGION = "region"
    TEXT = "text"
    UNKNOWN = "unknown"


@dataclass
class ParsedIntent:
    action: ActionType
    raw_command: str
    target_text: Optional[str] = None
    target_type: Optional[ElementType] = None
    input_text: Optional[str] = None
    url: Optional[str] = None
    app_name: Optional[str] = None
    position_hint: Optional[str] = None
    constraints: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    children: List["ParsedIntent"] = field(default_factory=list)


@dataclass
class DetectedElement:
    element_type: ElementType
    bbox: Tuple[int, int, int, int]
    center: Tuple[int, int]
    text: str = ""
    source: str = "vision"
    score: float = 0.0
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskStep:
    id: str
    action: ActionType
    description: str
    params: Dict[str, Any] = field(default_factory=dict)
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Dict[str, Any] = field(default_factory=lambda: {"max_retries": 2})
    fallbacks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExecutionResult:
    success: bool
    action: str
    target: Optional[str] = None
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)
    evidence: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    attempts: int = 1


@dataclass
class RuntimeContext:
    active_window: Optional[str] = None
    screen_size: Tuple[int, int] = (0, 0)
    backend_mode: BackendMode = BackendMode.HYBRID
    history: List[Dict[str, Any]] = field(default_factory=list)
    last_target: Optional[DetectedElement] = None
    safety_flags: Dict[str, Any] = field(default_factory=dict)
