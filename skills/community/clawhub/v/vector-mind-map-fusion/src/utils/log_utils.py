#!/usr/bin/env python3
"""
日志工具
"""
import logging
import logging.config
import yaml
from pathlib import Path


def setup_logger(name: str, config_path: str = None) -> logging.Logger:
    """
    设置日志器

    Args:
        name: logger 名称（通常是 l1/l2/l3/recall）
        config_path: logger.yaml 路径

    Returns:
        配置好的 logger
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "logger.yaml"

    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    else:
        # fallback：简单配置
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)-8s %(name)-15s %(message)s"
        )

    return logging.getLogger(name)


def get_logger(name: str) -> logging.Logger:
    """获取 logger（不使用配置文件）"""
    return logging.getLogger(name)