---
name: "Thunder"
version: "1.1.0"
description: "迅雷专用链接工具：thunder:// 链接与普通 URL 互相转换（纯本地零依赖脚本），支持 qqdl:// 与 flashget:// 解码。Decode/encode Thunder (Xunlei) thunder:// download links to plain URLs locally, also supports qqdl:// and flashget:// formats."
tags: ["thunder", "xunlei", "download", "link-converter", "tools"]
author: "ClawSkills Team"
category: "tools"
---

# 迅雷链接编解码 Skill

迅雷（Thunder/Xunlei）是中国广泛使用的下载工具。网络上大量下载资源以
`thunder://` 专用链接形式分发，普通下载器（wget/aria2/浏览器）无法直接
使用。本 skill 提供**纯本地、零依赖**的链接互转能力。

> 迅雷产品本身的完整使用指引见本团队的 `xunlei` skill，本 skill 专注
> 链接编解码这一可执行工具能力。

## 链接格式原理（公开算法）

- `thunder://` = Base64 编码的 `AA + 原始URL + ZZ`
- `qqdl://`（QQ旋风，已停运）= Base64 编码的原始 URL
- `flashget://`（快车）= Base64 编码的 `[FLASHGET]原始URL[FLASHGET]`

## 使用脚本

```shell
# 专链转普通 URL（自动识别 thunder/qqdl/flashget）
python3 scripts/thunderlink.py decode 'thunder://QUFodHRwOi8vZXhhbXBsZS5jb20vZmlsZS56aXBaWg=='
# 输出: http://example.com/file.zip

# 普通 URL 转 thunder://
python3 scripts/thunderlink.py encode 'http://example.com/file.zip'
```

脚本仅做 Base64 字符串变换，**不联网、不读写其他本地文件**。

## Agent 典型用法

1. 用户贴来一个 `thunder://` 链接问"这是什么" → 解码出真实 URL，
   分析文件名与来源域名，提示安全性
2. 用户想用 wget/aria2 下载迅雷专链 → 解码后给出标准下载命令
3. 批量转换：把老资源页面里的专链清单整理为普通 URL 列表

## 边界与提示

- 新版迅雷也支持磁力链（magnet:）与私有 P2P 资源，这类内容不经过
  thunder:// 编码，无需本工具
- 解码结果的可下载性取决于源站是否存活，本 skill 不保证资源有效
- 迅雷官网：https://www.xunlei.com
