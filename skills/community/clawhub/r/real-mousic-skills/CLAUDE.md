# Real mousic-skills (真正的音乐)

> 🐄 **Mousic** = **Mou** (奶牛叫声) + **Sic** = 真正的音乐！
> 
> 吉祥物：一头热爱音乐的奶牛 🐄🎵

歌曲下载工具，通过歌曲海网站搜索歌曲并获取下载链接。

## 开发命令

```bash
uv sync                    # 安装依赖
uv run ruff check .        # Lint 检查
uv run ruff format .       # 代码格式化
```

## 架构

```
src/real_mousic/
├── __init__.py           # 包入口
├── cli.py                # CLI 命令行入口
├── chrome_launcher.py    # Chrome 进程管理
├── xhs/                  # CDP 浏览器自动化引擎
│   ├── cdp.py
│   ├── stealth.py
│   └── ...
└── music/                # 歌曲下载模块
    ├── __init__.py
    └── search.py         # 歌曲搜索和下载链接获取

SKILL.md                  # AI Agent 技能定义
```

## CLI 子命令

| 子命令 | 说明 |
|--------|------|
| `search --song <歌曲名>` | 搜索歌曲 |
| `download --detail-url <URL>` | 获取下载链接 |
| `get --song <歌曲名> --index <序号>` | 搜索+下载一步到位 |

## 调用方式

```bash
# 启动 Chrome
python -m real_mousic.chrome_launcher

# 搜索歌曲
python -m real_mousic.cli search --song "渡口"

# 获取下载链接
python -m real_mousic.cli download --detail-url "https://www.gequhai.com/song/xxx" --title "渡口" --artist "蔡琴"

# 搜索+下载一步到位
python -m real_mousic.cli get --song "渡口" --index 1
```

## 代码规范

- 行长度上限 100 字符
- 完整 type hints
- CLI exit code：0=成功，1=错误
- JSON 输出 `ensure_ascii=False`