from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="video-merger",
    version="1.0.0",
    author="machunlin",
    description="Multi-segment short video auto-merger tool, support sorting by filename, unified parameters, fade transitions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/machunlin/video-merger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "video-merger = scripts.merge:main",
        ],
    },
    keywords="video merge concatenate cli tool short-video drama production",
    project_urls={
        "Bug Reports": "https://github.com/machunlin/video-merger/issues",
        "Source": "https://github.com/machunlin/video-merger",
    },
)
