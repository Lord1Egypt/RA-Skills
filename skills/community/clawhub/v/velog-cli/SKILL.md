---
name: Velog CLI
slug: velog-cli
version: 0.1.0
summary: Fetch latest posts for any Velog user via public RSS (no API key).
labels: ["latest", "korea", "blog", "rss"]
---

Velog public RSS CLI — 최신 Velog 포스트를 손쉽게 가져오는 도구이다. 인증이나 키가 필요하지 않으며 `https://v2.velog.io/rss/<username>` 피드를 파싱하여 Markdown 또는 JSON으로 출력한다.

## 사용법

```
velog-cli user-posts --username <name> --limit 5 --format md
```

## 설치

```
pipx install .  # 또는 uv tool install .
```

## 참고
- Velog: https://velog.io
- RSS: https://v2.velog.io/rss/<username>
