from setuptools import setup, find_packages

setup(
    name="sergei-mikhailov-tg-channel-reader",
    version="0.9.4",
    description="OpenClaw skill: read Telegram channels via MTProto",
    author="Sergey Mikhailov",
    url="https://github.com/bzSega/sergei-mikhailov-tg-channel-reader",
    license="MIT",
    py_modules=["reader", "reader_telethon", "tg_reader_unified", "tg_check", "tg_state"],
    install_requires=[
        # pyrofork is a drop-in replacement for pyrogram with current TL schema.
        # The pyrogram package on PyPI is pinned at 2.0.106 (Aug 2023) and silently
        # drops `message` / `media` / `entities` content for posts encoded with TL
        # constructors introduced after that date — including many May 2026 posts.
        # pyrofork installs into the `pyrogram` import namespace, so reader.py
        # still uses `from pyrogram import Client` unchanged. Session files are
        # format-compatible — existing users do not need to re-authenticate.
        "pyrofork>=2.3.69",
        "tgcrypto>=1.2.0",
        "telethon>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "tg-reader=tg_reader_unified:main",
            "tg-reader-pyrogram=reader:main",
            "tg-reader-telethon=reader_telethon:main",
            "tg-reader-check=tg_check:main",
        ],
    },
    python_requires=">=3.9",
)
