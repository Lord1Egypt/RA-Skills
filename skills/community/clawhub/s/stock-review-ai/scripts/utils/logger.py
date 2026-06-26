"""tool for logging in stock review skill"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Union


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_to_file: bool = False,
    log_dir: Optional[Union[str, Path]] = None
) -> logging.Logger:
    """Setting up a logger with console and file handlers"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        
        # console handler
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console)
        
        # file handler
        if log_to_file:
            if log_dir is None:
                log_dir = Path(__file__).parent.parent.parent.parent / 'logs'
            else:
                log_dir = Path(log_dir)
            
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"stock_review_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(file_handler)
            logger.info(f"Log file saved: {log_file}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger by name"""
    return logging.getLogger(name)


class LoggerManager:
    """Logger manager for centralized logger management"""
    
    _instance = None
    _loggers = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_logger(self, name: str, **kwargs) -> logging.Logger:
        """Get or create a logger"""
        if name not in self._loggers:
            self._loggers[name] = setup_logger(name, **kwargs)
        return self._loggers[name]
    
    def set_level(self, name: str, level: int) -> None:
        """Set log level for a logger"""
        if name in self._loggers:
            self._loggers[name].setLevel(level)
    
    def disable_file_logging(self, name: str) -> None:
        """Disable file logging for a logger"""
        if name in self._loggers:
            logger = self._loggers[name]
            for handler in logger.handlers[:]:
                if isinstance(handler, logging.FileHandler):
                    logger.removeHandler(handler)
    
    def get_all_loggers(self) -> dict:
        """Get all managed loggers"""
        return self._loggers.copy()


# create a default logger manager instance
default_manager = LoggerManager()


def get_managed_logger(name: str, **kwargs) -> logging.Logger:
    """Get a managed logger using the default manager"""
    return default_manager.get_logger(name, **kwargs)


# export all public interfaces
__all__ = [
    'setup_logger',
    'get_logger',
    'LoggerManager',
    'default_manager',
    'get_managed_logger'
]