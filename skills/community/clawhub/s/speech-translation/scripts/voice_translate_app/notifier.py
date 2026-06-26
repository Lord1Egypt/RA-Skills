from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


class BaseNotifier:
    def notify_transcript(self, text: str) -> None:
        raise NotImplementedError

    def notify_translation(self, text: str) -> None:
        raise NotImplementedError

    def notify_audio(self, audio_file: Path) -> None:
        raise NotImplementedError


class ConsoleNotifier(BaseNotifier):
    def notify_transcript(self, text: str) -> None:
        print("\n===== Transcript =====\n")
        print(text)

    def notify_translation(self, text: str) -> None:
        print("\n===== Translation =====\n")
        print(text)

    def notify_audio(self, audio_file: Path) -> None:
        print("\n===== Audio =====\n")
        print(audio_file)


@dataclass
class CommandNotifier(BaseNotifier):
    """
    用外部命令发送多条消息。

    约定：
    - transcript_command / translation_command 接收纯文本 stdin
    - audio_command 接收一个参数：音频文件路径
    """

    transcript_command: str | None = None
    translation_command: str | None = None
    audio_command: str | None = None

    def _run_text_command(self, command: str | None, text: str) -> None:
        if not command:
            return
        subprocess.run(command, input=text.encode("utf-8"), shell=True, check=True)

    def _run_audio_command(self, command: str | None, audio_file: Path) -> None:
        if not command:
            return
        if "{audio_file}" in command:
            resolved = command.format(audio_file=str(audio_file))
        else:
            resolved = f'{command} "{audio_file}"'
        subprocess.run(resolved, shell=True, check=True)

    def notify_transcript(self, text: str) -> None:
        self._run_text_command(self.transcript_command, text)

    def notify_translation(self, text: str) -> None:
        self._run_text_command(self.translation_command, text)

    def notify_audio(self, audio_file: Path) -> None:
        self._run_audio_command(self.audio_command, audio_file)
