#!/usr/bin/env python3
from app.config import AppConfig
from core.orchestrator import Orchestrator


class SmartController:
    def __init__(self):
        self.runner = Orchestrator(AppConfig())

    def execute(self, command: str):
        return self.runner.execute(command)


if __name__ == '__main__':
    controller = SmartController()
    print(controller.execute("打开记事本"))
