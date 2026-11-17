"""argparse 中文错误说明。"""

from __future__ import annotations

import argparse
import sys


class ZhArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(f"参数错误：{message}\n请执行：python main.py -h 查看帮助", file=sys.stderr)
        self.exit(2)
