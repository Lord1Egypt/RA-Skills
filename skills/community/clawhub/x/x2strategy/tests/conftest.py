"""Shared pytest configuration and fixtures."""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-real",
        action="store_true",
        default=False,
        help="Run tests marked @pytest.mark.real (requires network + API keys, costs credits)",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-real"):
        return
    skip_real = pytest.mark.skip(reason="需要 --run-real 才运行 (requires network + API credits)")
    for item in items:
        if "real" in item.keywords:
            item.add_marker(skip_real)
