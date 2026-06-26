# 微信公众号文章读取技能

## 概述

使用 `wechat2md.py` 脚本抓取微信公众号文章内容并转换为 Markdown 格式。抓取后可对内容进行总结或直接输出原文。

## 前置条件

依赖已安装在 `/tmp/pylibs`：
- `html2text`
- `beautifulsoup4`
- `requests`

如遇 `ModuleNotFoundError`，运行：
```bash
pip3 install html2text beautifulsoup4 --target=/tmp/pylibs -q
```

## 标准流程

### Step 1：抓取文章

```bash
cd /home/node/.openclaw/workspace-research/skills/WeChat-mp
PYTHONPATH=/tmp/pylibs python3 wechat2md.py "<文章链接>"
```

文章会保存为同名 `.md` 文件在当前目录下。

### Step 2：读取内容

读取生成的 `.md` 文件，提取正文内容。

### Step 3：总结或输出

按用户需求执行：
- **总结**（默认）：提炼核心观点、主要话题、关键结论
- **完整内容**：直接输出 `.md` 原文内容，不做删减

### Step 4：清理文件

**重要！总结完成后必须删除生成的 `.md` 文件。**

```bash
rm -f "/home/node/.openclaw/workspace-research/skills/WeChat-mp/<文件名>.md"
```

除非用户**明确要求保留**，否则一律删除。

## 注意事项

- 脚本会自动处理懒加载图片（`data-src` → `src`）
- 如需下载图片到本地，可加 `--save-images` 参数
- 网络错误或文章被删时，脚本会输出明确错误信息
- 微信 JS 验证（"环境异常"）目前无法绕过，如脚本失败说明文章需要真人验证，只能告知用户无法提取

## 总结模板

```markdown
## 文章核心观点总结

### 一、核心结论
[一句话概括]

### 二、主要观点
**1. [主题]**
- 要点1
- 要点2

### 三、关键结论
| 结论 | 说明 |
|------|------|
| ... | ... |

### 四、延伸思考
[可选]
```
