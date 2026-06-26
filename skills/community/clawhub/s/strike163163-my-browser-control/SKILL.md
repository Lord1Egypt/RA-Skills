---
slug: strike163163-my-browser-control
name: 我的浏览器控制工具
version: 0.1.1
author: strike163163
description: 基于Python实现的macOS浏览器自动化工具，可一键打开指定网址，支持Safari/Chrome浏览器。
tags:
  - 浏览器自动化
  - python
  - macos
---

# 我的浏览器控制工具
本工具专为macOS用户开发，核心功能是通过Python脚本自动打开指定网址，无需手动输入网址或点击浏览器。

## 核心功能说明
### 1. 一键打开网址功能
- 函数名：`open_website`
- 入参：`url`（字符串类型，必填，例如："https://www.baidu.com"）
- 返回值：无（直接触发浏览器打开操作）
- 实际代码（来自open_website.py）：
  ```python
  import webbrowser
  def open_website(url):
      # 调用macOS默认浏览器打开网址
      webbrowser.open(url)
      print(f"已成功打开网址：{url}")