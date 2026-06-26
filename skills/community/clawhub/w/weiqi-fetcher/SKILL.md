---
name: weiqi-fetcher
description: 围棋分享棋谱下载器 - 从分享链接自动下载SGF棋谱
---

# 围棋分享棋谱下载器

从围棋网站/平台的分享链接自动下载SGF格式棋谱文件。

## 支持的平台

| 平台 | 状态 | 实现方式 | 速度 |
|------|------|----------|------|
| **OGS** | ✅ 可用 | REST API | ~0.3s |
| **野狐围棋** | ✅ 可用 | REST API | ~0.1s |
| **101围棋网** | ✅ 可用 | WebSocket | ~1s |
| **弈客围棋** | ✅ 可用 | Playwright浏览器 | ~10s |
| **元萝卜围棋** | ✅ 可用 | REST API | ~0.3s |
| **星阵围棋** | ✅ 可用 | Playwright + localStorage | ~10s |
| **隐智智能棋盘** | ✅ 可用 | Playwright + REST API | ~8s |
| **弈客少儿版** | ✅ 可用 | Playwright + API | ~8s |
| **弈城围棋** | ✅ 可用 | REST API | ~1s |
| **腾讯围棋** | ✅ 可用 | Playwright + JSONP | ~8s |
| **新博对弈** | ✅ 可用 | Playwright + WebSocket | ~10s |
| **对弈曲折/手谈赛场** | ✅ 可用 | REST API | ~0.5s |

## 使用方法

### 自动识别下载

```bash
cd /path/to/weiqi-fetcher/scripts

# OGS对局
python3 main.py "https://online-go.com/game/{GAME_ID}"

# 野狐对局
python3 main.py "https://h5.foxwq.com/yehunewshare/?chessid={CHESS_ID}"

# 101围棋网
python3 main.py "https://www.101weiqi.com/play/p/{PLAY_ID}/"

# 弈客围棋（需要Playwright）
python3 main.py "https://home.yikeweiqi.com/mobile.html#/golive/room/{ROOM_ID}/..."

# 元萝卜围棋
python3 main.py "https://jupiter.yuanluobo.com/robot-public/all-in-app/go/review?session_id={SESSION_ID}"

# 星阵围棋
python3 main.py "https://m.19x19.com/app/dark/zh/sgf/{SGF_ID}"

# 隐智智能棋盘
python3 main.py "http://app.izis.cn/web/#/live_detail?gameId={GAME_ID}&type=2"

# 弈客少儿版
python3 main.py "https://shaoer.yikeweiqi.com/statichtml/game_analysis_mobile.html?p={PARAMS}"

# 弈城围棋
python3 main.py "http://mobile.eweiqi.com/index_ZHCN.html?LNK=1&GNO={GAME_NO}"

# 腾讯围棋
python3 main.py "https://h5.txwq.qq.com/txwqshare/index.html?chessid={CHESS_ID}"

# 新博对弈
python3 main.py "https://weiqi.xinboduiyi.com/golive/index.html#/?gamekey={GAME_KEY}"

# 对弈曲折/手谈赛场
python3 main.py "https://v.dzqzd.com/Kifu/chessmanualdetail?kifuId={KIFU_ID}"
```

### 指定输出文件

```bash
python3 main.py "https://online-go.com/game/{GAME_ID}" -o ~/games/mygame.sgf
```

### 强制指定来源

```bash
python3 main.py "{URL}" --source ogs
```

### 列出支持的来源

```bash
python3 main.py --list-sources
```

### 静默模式（仅输出文件路径）

```bash
python3 main.py "{URL}" --silent
```

## 临时目录

默认下载路径: `/tmp/weiqi_fetch/YYYYMMDD_HHMMSS/<来源>/`

## 输出示例

```
============================================================
🎯 围棋分享棋谱下载器
============================================================

🌐 识别到来源: OGS (Online-Go)

✅ 下载成功！

🌐 来源: ogs
🔗 URL: https://online-go.com/game/{GAME_ID}

📋 对局信息:
  黑棋: {BLACK_NAME} {BLACK_RANK}
  白棋: {WHITE_NAME} {WHITE_RANK}
  规则: japanese
  贴目: 6.5
  手数: {MOVES_COUNT}
  结果: {RESULT}

💾 文件保存: /tmp/weiqi_fetch/YYYYMMDD_HHMMSS/ogs_{GAME_ID}.sgf

⏱️ 性能统计:
  extract_id          : 0.000s
  api_request         : 0.312s
  sgf_generation      : 0.001s
  save_file           : 0.000s
  总计                : 0.313s

============================================================
```

## 各平台技术说明

### OGS (Online-Go.com)

- **API端点**: `https://online-go.com/api/v1/games/{id}`
- **特点**: 公开API，无需登录
- **数据格式**: JSON，包含完整着法数据
- **坐标系统**: (0,0)=左上，需要转换为SGF格式

### 野狐围棋 (foxwq.com)

- **API端点**: 
  - 棋谱: `https://h5.foxwq.com/yehuDiamond/chessbook_local/YHWQFetchChess?chessid={id}`
  - 详情: `https://h5.foxwq.com/yehuDiamond/chessbook_local/FetchChessSummaryByChessID?chessid={id}`
- **特点**: 直接返回SGF格式
- **限制**: 历史棋谱API可用，进行中对局需WebSocket

### 101围棋网 (101weiqi.com)

- **数据提取**: 
  - Step=0: 页面 `playInfo` 直接获取
  - Step>0: WebSocket `wss://playdo.101weiqi.com/9001/pp/playroom`
- **URL模式**: `https://www.101weiqi.com/play/p/{id}/`
- **特点**: 
  - 段位显示为等级分制（如 7K, 16K）
  - 默认中国规则，贴目7.5
  - 支持让子棋
- **坐标系统**: 字母坐标 (如 'pc', 'dq') → SGF格式
- **WebSocket协议**: 
  1. 连接后发送 `{"cmd": "init_user", "pkey": "play:{id}", "userkey": "..."}`
  2. 发送 `{"cmd": "getinitdata"}` 获取棋谱
  3. 返回数据包含 `pos` 数组（字母坐标格式）

### 弈客围棋 (yikeweiqi.com)

- **实现方式**: Playwright浏览器自动化
- **URL模式**: `https://home.yikeweiqi.com/mobile.html#/golive/room/{id}/...`
- **特点**:
  - 支持实时直播对局
  - 自动提取完整SGF棋谱
  - 需要Playwright和Chromium浏览器
- **依赖安装**:
  ```bash
  pip install playwright
  playwright install chromium
  ```
- **数据来源**:
  - `hawkeye_analyses` API: 比赛基本信息
  - `api.yikeweiqi.com/v2/golive/dtl`: 对局详情
  - `hawkeye.yikeweiqi.com/api/report/live/move`: 棋谱数据

### 元萝卜围棋 (yuanluobo.com)

- **实现方式**: 纯REST API
- **URL模式**: `https://jupiter.yuanluobo.com/robot-public/all-in-app/go/review?session_id={id}`
- **特点**:
  - AI围棋机器人对局记录
  - 支持让子棋
  - 无需浏览器，速度最快（约0.3秒）
- **API端点**: `POST https://jupiter.yuanluobo.com/r2/chess/wq/sdr/v3/record/detail`
- **请求参数**: `{"sessionId": "..."}`
- **数据来源**:
  - `recording.moves`: 棋谱数据
  - `coordinate` 字段: 已是SGF格式（如 `W[cd]`、`B[qp]`）

## 扩展新平台

1. 在 `scripts/sources/` 下创建新文件（如 `fetch_newsite.py`）
2. 继承 `BaseSourceFetcher`，实现 `fetch()` 方法
3. 设置 `name`, `display_name`, `url_patterns`
4. 在 `__init__.py` 中导入

示例:

```python
from .base import BaseSourceFetcher, FetchResult, register_fetcher

@register_fetcher
class NewsiteFetcher(BaseSourceFetcher):
    name = "newsite"
    display_name = "新站点"
    url_patterns = [r'newsite\.com/game/(\d+)']
    url_examples = ["https://newsite.com/game/{GAME_ID}"]
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        # 实现下载逻辑
        pass
```

## 安装

### 基础依赖

所有平台都需要：
```bash
pip3 install requests
```

### Playwright 额外依赖

弈客围棋、星阵围棋、隐智智能棋盘、弈客少儿版、腾讯围棋、新博对弈使用浏览器自动化，需要安装 Playwright：
```bash
pip3 install playwright
playwright install chromium
```

### 完整安装（推荐）

```bash
# 安装所有依赖
pip3 install requests playwright websocket-client

# 安装 Chromium 浏览器
playwright install chromium
```

## 目录结构

```
weiqi-fetcher/
├── SKILL.md                    # 本文档
├── scripts/
│   ├── main.py                 # 主入口程序
│   └── sources/                # 各平台实现
│       ├── __init__.py
│       ├── base.py             # 基类定义
│       ├── fetch_ogs.py        # OGS平台
│       ├── fetch_fox.py        # 野狐围棋
│       ├── fetch_101.py        # 101围棋网
│       ├── fetch_yike.py       # 弈客围棋
│       ├── fetch_yuanluobo.py  # 元萝卜围棋
│       ├── fetch_1919.py       # 星阵围棋
│       ├── fetch_izis.py       # 隐智智能棋盘
│       ├── fetch_yike_shaoer.py # 弈客少儿版
│       ├── fetch_eweiqi.py     # 弈城围棋
│       ├── fetch_txwq.py       # 腾讯围棋
│       ├── fetch_xinboduiyi.py # 新博对弈
        │       └── fetch_dzqzd.py       # 对弈曲折/手谈赛场
└── tmp/                        # 临时下载目录
```

## 注意事项

### 腾讯围棋（txwq.qq.com）

- **实现方式**: Playwright + JSONP响应监听
- **URL模式**: `https://h5.txwq.qq.com/txwqshare/index.html?chessid={id}`
- **特点**:
  - 使用Playwright拦截 jsonp.php 响应
  - 棋谱数据在 `chess` 字段（JSON转义SGF）
  - 支持职业段位显示（P4段 = 职业四段）

### 新博对弈（xinboduiyi.com）

- **实现方式**: Playwright + WebSocket监听
- **URL模式**: `https://weiqi.xinboduiyi.com/golive/index.html#/?gamekey={id}`
- **WebSocket端点**: `wss://live.xinboduiyi.com:40442/ws`
- **特点**:
  - 实时对弈平台，支持教室记谱分享
  - 棋谱数据在 `part_qipu` 数组中，使用 `part_id=0` 的分谱
  - 数据格式: `B[CD];W[QR];...`（分号分隔的类SGF格式）
- **坐标映射规则**:
  - 第一个字母 = 纵坐标 → SGF的y
  - 第二个字母 = 横坐标 → SGF的x
  - 横坐标映射: T=a, S=b, R=c, Q=d, P=e, O=f, N=g, M=h, L=i, K=j, J=k, H=l, G=m, F=n, E=o, D=p, C=q, B=r, A=s
  - 纵坐标映射: A=a, B=b, C=c, D=d, E=e, F=f, G=g, H=h, J=i, K=j, L=k, M=l, N=m, O=n, P=o, Q=p, R=q, S=r, T=s
  - 示例: `B[CD]` → C(纵)=c, D(横)=p → `B[pc]`

### 对弈曲折/手谈赛场（dzqzd.com）

- **实现方式**: 纯REST API（无需Playwright）
- **URL模式**: `https://v.dzqzd.com/Kifu/chessmanualdetail?kifuId={id}`
- **API端点**: `https://v.dzqzd.com/Kifu/Details?kifuid={id}`
- **特点**:
  - 使用丹朱对局集系统的比赛直播/记录平台
  - 返回YAML格式数据，包含头部信息和着法列表
  - 速度快（约0.5秒），无需浏览器
- **数据格式**:
  - 头部: GM, AP, SZ, PB, PW, SO, EV, DT 等
  - 着法: `- B: pd`, `- W: dc` 格式

### SGF文件编码

下载的SGF文件使用UTF-8编码，兼容所有现代围棋软件（如Sabaki、Lizzie、棋魂等）。

### 临时文件清理

下载的SGF文件默认保存在 `/tmp/weiqi_fetch/` 目录下。系统重启后会自动清理，如需保留请使用 `-o` 参数指定保存位置。

## 故障排除

### 问题："Playwright未安装"

**解决**：
```bash
pip3 install playwright
playwright install chromium
```

### 问题："WebSocket获取棋谱失败"（101围棋网）

**原因**：网络连接问题或页面结构变化
**解决**：检查网络，或稍后再试

### 问题："API请求失败"

**原因**：对方网站服务不可用或URL错误
**解决**：
1. 检查URL是否正确
2. 确认对局是否公开可访问
3. 稍后再试

## 依赖

- Python 3.8+
- requests
- playwright（部分平台需要）
- websocket-client（部分平台需要）
