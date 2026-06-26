name: xmind-testcase
version: 0.1.0
description: >
  Generate XMind test cases from requirement descriptions.
  This Skill analyzes functional requirements and automatically
  produces structured test cases in XMind format. Supports login,
  registration, checkout, search features, and more.

entry:
  type: script
  command: python3 scripts/generate_xmind.py

inputs:
  requirement:
    type: string
    description: The functional requirement description.
    example: "用户登录功能：支持用户名密码登录，密码错误提示，三次失败锁定"

outputs:
  xmind_file:
    type: file
    description: The generated XMind test case file.
