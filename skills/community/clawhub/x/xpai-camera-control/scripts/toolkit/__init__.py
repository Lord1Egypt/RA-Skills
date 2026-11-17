from .stream import (
    get_audio_video_stream,
    capture_video_screenshot,
    toggle_recording,
    start_webrtc_stream,
    stop_webrtc_stream,
    StreamResult,
    ScreenshotResult,
    RecordingResult,
    WebRTCResult,
    RecordingAction,
)

from .ptz import (
    control_ptz,
    stop_ptz,
    PTZMoveResult,
    PTZDirection,
    PTZInfo,
)

from .device_mgmt import (
    get_registered_cameras,
    register_camera,
    search_devices,
    connect_device,
    disconnect_device,
    DiscoveredDevice,
    SearchResult,
    ConnectResult,
    DisconnectResult,
    DiscoveryMethod,
    DeviceClass,
    CameraConfig,
    RegisterResult,

    AuthStatus,
    AuthOrchestrateResult,
    AuthStatusResult,
    CloudAuthRequestResult,
    request_cloud_auth,
    poll_auth_status,
    big_connect,
    resolve_target,
)

from .events import (
    manage_camera_events,
    EventAction,
    CameraEvent,
    EventMonitorResult,
    PendingEventsResult,
)

from .illumination import (
    manage_illumination,
    probe_illumination_capability,
    IlluminationAction,
    IlluminationInfo,
    FilllightQueryResult,
    FilllightSetResult,
    big_filllight_query,
    big_filllight_set,
    DAYNIGHT_MODES,
    FILLLIGHT_MODES,
)

from .image_settings import (
    manage_image_settings,
    ImageAction,
    ImageQueryResult,
    ImageSetResult,
)

from .tracking import (
    manage_tracking,
    TrackingAction,
    DetectType,
    TrackingQueryResult,
    TrackingSetResult,
)

__all__ = [

    "get_audio_video_stream",
    "capture_video_screenshot",
    "toggle_recording",
    "start_webrtc_stream",
    "stop_webrtc_stream",
    "StreamResult",
    "ScreenshotResult",
    "RecordingResult",
    "WebRTCResult",
    "RecordingAction",

    "control_ptz",
    "stop_ptz",
    "PTZMoveResult",
    "PTZDirection",
    "PTZInfo",

    "get_registered_cameras",
    "register_camera",
    "search_devices",
    "connect_device",
    "disconnect_device",
    "DiscoveredDevice",
    "SearchResult",
    "ConnectResult",
    "DisconnectResult",
    "DiscoveryMethod",
    "DeviceClass",
    "CameraConfig",
    "RegisterResult",

    "AuthStatus",
    "AuthOrchestrateResult",
    "AuthStatusResult",
    "CloudAuthRequestResult",
    "request_cloud_auth",
    "poll_auth_status",
    "big_connect",
    "resolve_target",

    "manage_camera_events",
    "EventAction",
    "CameraEvent",
    "EventMonitorResult",
    "PendingEventsResult",

    "manage_illumination",
    "probe_illumination_capability",
    "IlluminationAction",
    "IlluminationInfo",
    "FilllightQueryResult",
    "FilllightSetResult",
    "big_filllight_query",
    "big_filllight_set",
    "DAYNIGHT_MODES",
    "FILLLIGHT_MODES",

    "manage_image_settings",
    "ImageAction",
    "ImageQueryResult",
    "ImageSetResult",

    "manage_tracking",
    "TrackingAction",
    "DetectType",
    "TrackingQueryResult",
    "TrackingSetResult",
]
