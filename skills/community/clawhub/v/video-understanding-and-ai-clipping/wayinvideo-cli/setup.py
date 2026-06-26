from setuptools import setup, find_packages
from wayinvideo.__init__ import __version__

setup(
    name="wayinvideo-cli",
    version=__version__,
    description="Unified CLI for WayinVideo APIs",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "wayinvideo=wayinvideo.cli:main",
        ],
    },
)