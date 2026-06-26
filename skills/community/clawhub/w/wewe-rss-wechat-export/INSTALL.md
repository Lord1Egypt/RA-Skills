# 安装指南

> 适配 **wewe-rss** 的公众号抓取与文档导出工具。

## 前提条件

确保以下命令可用：

```bash
openclaw gateway status
node --version
pandoc --version
curl --version
python3 --version
```

## 从 zip 安装

假设你已经拿到 `wewe-rss-wechat-export.zip`。

```bash
WORKSPACE=$(python3 - <<'PY'
import json
from pathlib import Path
config = Path.home() / '.openclaw' / 'openclaw.json'
if config.exists():
    data = json.loads(config.read_text())
    print(data.get('agents', {}).get('defaults', {}).get('workspace', str(Path.home() / '.openclaw' / 'workspace')))
else:
    print(Path.home() / '.openclaw' / 'workspace')
PY
)

mkdir -p "$WORKSPACE/skills"
unzip "/path/to/wewe-rss-wechat-export.zip" -d "$WORKSPACE/skills"
chmod +x "$WORKSPACE/skills/wewe-rss-wechat-export/scripts/run-export-feed.sh"
openclaw gateway restart
openclaw skills 2>&1 | grep wewe-rss-wechat-export
```

## 直接复制目录安装

```bash
WORKSPACE=$(python3 - <<'PY'
import json
from pathlib import Path
config = Path.home() / '.openclaw' / 'openclaw.json'
if config.exists():
    data = json.loads(config.read_text())
    print(data.get('agents', {}).get('defaults', {}).get('workspace', str(Path.home() / '.openclaw' / 'workspace')))
else:
    print(Path.home() / '.openclaw' / 'workspace')
PY
)

mkdir -p "$WORKSPACE/skills"
cp -R "/path/to/wewe-rss-wechat-export" "$WORKSPACE/skills/wewe-rss-wechat-export"
chmod +x "$WORKSPACE/skills/wewe-rss-wechat-export/scripts/run-export-feed.sh"
openclaw gateway restart
openclaw skills 2>&1 | grep wewe-rss-wechat-export
```

## 快速验证

```bash
bash "$WORKSPACE/skills/wewe-rss-wechat-export/scripts/run-export-feed.sh" \
  "https://example.com/feed.json" \
  1 \
  "./export/wewe-rss-wechat-export-smoke" \
  --batch-size 1 \
  --output-mode docx \
  --rename-mode dated \
  --zip
```

## 说明

- 若不传 `output_dir`，默认输出到当前工作目录的 `export/`
- 如果想统一输出目录，可设置：

```bash
export EXPORT_FEED_OUTPUT_ROOT="/your/preferred/export/root"
```

- `docx` 模式更适合最终交付
- `full` 模式更适合验收与排查
