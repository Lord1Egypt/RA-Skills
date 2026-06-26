# WeChat Article Reader

An OpenClaw skill for reading WeChat official account articles.

## Features

- Auto-normalizes WeChat article URLs (appends `?scene=1` to bypass CAPTCHA)
- Extracts article body text using the built-in browser tool
- Cascading content selectors (`#js_content` → `.rich_media_content` → `body`)

## Install

```bash
# From local directory
openclaw skill install ./skills/wechat-article-reader

# From GitHub
openclaw skill install https://github.com/bernylinville/my-skills/blob/main/skills/wechat-article-reader/SKILL.md
```

## Usage

In OpenClaw, simply ask:

```
Read this WeChat article https://mp.weixin.qq.com/s/xxx
```

## File Structure

```
wechat-article-reader/
├── SKILL.md   # Skill definition
└── README.md  # This file
```
