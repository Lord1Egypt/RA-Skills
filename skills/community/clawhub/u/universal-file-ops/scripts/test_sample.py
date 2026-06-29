"""测试文件：用于 py_tools.py 各子命令"""
import os
import sys

def hello():
    print("Hello World")

class Foo:
    def __init__(self):
        self.x = 1
    def bar(self):
        return self.x

if __name__ == "__main__":
    hello()
    f = Foo()
    print(f.bar())
