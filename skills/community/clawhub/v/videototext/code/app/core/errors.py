from dataclasses import dataclass


@dataclass
class AppError(Exception):
    error_code: str
    message: str
    status_code: int = 400


class ErrorCodes:
    INVALID_URL = "INVALID_URL"
    UNSUPPORTED_PLATFORM = "UNSUPPORTED_PLATFORM"
    VIDEO_NOT_FOUND = "VIDEO_NOT_FOUND"
    VIDEO_NOT_ACCESSIBLE = "VIDEO_NOT_ACCESSIBLE"
    SUBTITLE_FETCH_FAILED = "SUBTITLE_FETCH_FAILED"
    AUDIO_EXTRACT_FAILED = "AUDIO_EXTRACT_FAILED"
    ASR_FAILED = "ASR_FAILED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
