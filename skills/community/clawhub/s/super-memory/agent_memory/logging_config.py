from __future__ import annotations

import json as json_module
import logging
import logging.config
import os
import sys
import threading


class JsonFormatter(logging.Formatter):
    """JSON structured log formatter for log aggregation systems."""

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Add extra fields if present
        if hasattr(record, 'event'):
            log_entry["event"] = record.event
        if hasattr(record, 'duration_ms'):
            log_entry["duration_ms"] = record.duration_ms
        if hasattr(record, 'tenant_id'):
            log_entry["tenant_id"] = record.tenant_id
        if hasattr(record, 'memory_id'):
            log_entry["memory_id"] = record.memory_id
        if hasattr(record, 'results_count'):
            log_entry["results_count"] = record.results_count

        # Add exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json_module.dumps(log_entry, ensure_ascii=False)

_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            "datefmt": "%H:%M:%S",
        },
        "minimal": {
            "format": "%(message)s",
        },
        "cli": {
            "format": "[%(name)s] %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "standard",
            "level": "DEBUG",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "agent_memory": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        "uvicorn": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["console"],
        },
        "huggingface_hub": {
            "level": "WARNING",
            "propagate": False,
        },
        "urllib3": {
            "level": "WARNING",
            "propagate": False,
        },
        "sentence_transformers": {
            "level": "WARNING",
            "propagate": False,
        },
        "chromadb": {
            "level": "WARNING",
            "propagate": False,
        },
    },
}

_CLI_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_safe": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "json_safe",
            "level": "CRITICAL",
        },
    },
    "root": {"level": "CRITICAL", "handlers": ["console"]},
    "loggers": {
        "agent_memory": {"level": "CRITICAL", "propagate": False},
        "huggingface_hub": {"level": "CRITICAL", "propagate": False},
        "urllib3": {"level": "CRITICAL", "propagate": False},
        "sentence_transformers": {"level": "CRITICAL", "propagate": False},
        "chromadb": {"level": "CRITICAL", "propagate": False},
    },
}

_configured = False
_lock = threading.Lock()


def configure_logging(level: str = "INFO", fmt: str = "standard", style: str = "server") -> None:
    global _configured
    with _lock:
        if _configured:
            return
        _configured = True

    if style == "cli":
        logging.config.dictConfig(_CLI_CONFIG)
        return

    import copy
    cfg = copy.deepcopy(_DEFAULT_CONFIG)

    level_value = getattr(logging, level.upper(), logging.INFO)
    cfg["root"]["level"] = level_value
    cfg["loggers"]["agent_memory"]["level"] = level_value

    # JSON structured logging via environment variable
    log_format = os.environ.get("AGENT_MEMORY_LOG_FORMAT", "standard")
    if log_format == "json":
        formatter = JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S")
        # Register custom formatter class so dictConfig can reference it
        logging._acquireLock()
        try:
            logging._formatter_classes = getattr(logging, '_formatter_classes', {})
            logging._formatter_classes['agent_memory.JsonFormatter'] = JsonFormatter
        finally:
            logging._releaseLock()
        cfg["formatters"]["json"] = {
            "()": "agent_memory.logging_config.JsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        }
        cfg["handlers"]["console"]["formatter"] = "json"
    elif fmt not in cfg["formatters"]:
        cfg["formatters"][fmt] = {"format": fmt, "datefmt": "%Y-%m-%d %H:%M:%S"}
        cfg["handlers"]["console"]["formatter"] = fmt
    else:
        cfg["handlers"]["console"]["formatter"] = fmt

    if "LOG_FILE" in os.environ:
        cfg["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.environ["LOG_FILE"],
            "maxBytes": 10_485_760,
            "backupCount": 5,
            "formatter": fmt,
            "level": "DEBUG",
        }
        cfg["root"]["handlers"].append("file")
        cfg["loggers"]["agent_memory"]["handlers"].append("file")

    logging.config.dictConfig(cfg)

    logger = logging.getLogger("agent_memory")
    logger.info(f"日志系统已启动 level={level} fmt={fmt} style={style}")


def configure_cli_logging() -> None:
    configure_logging(style="cli")


def get_logger(name: str = None) -> logging.Logger:
    if name is None or name == "__main__":
        return logging.getLogger("agent_memory")
    return logging.getLogger(name)


try:
    _LOG_LEVEL = os.environ.get("AGENT_MEMORY_LOG_LEVEL", "INFO")
except Exception:
    _LOG_LEVEL = "INFO"

logger = get_logger("agent_memory.logging_config")