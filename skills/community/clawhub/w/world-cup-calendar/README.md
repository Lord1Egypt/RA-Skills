# world-cup-calendar

把 2026 FIFA 世界杯赛程同步到飞书日历。

默认效果：
- 全部 104 场比赛按北京时间创建日程。
- 普通比赛不提醒。
- 阿根廷比赛提前 1 天提醒。
- 日程详情仅自己可见。
- 忙闲状态为空闲，不影响同事约你开会。

## 1. 安装到 Codex

把这个仓库放到 Codex skills 目录：

```bash
git clone https://github.com/kekenana272/world-cup-calendar.git ~/.codex/skills/world-cup-calendar
```

也可以手动下载后，把整个文件夹放到：

```bash
~/.codex/skills/world-cup-calendar
```

## 2. 检查环境

进入 Skill 目录：

```bash
cd ~/.codex/skills/world-cup-calendar
```

检查 Python、Node.js、npm 和飞书 CLI：

```bash
python3 scripts/world_cup_calendar.py doctor
```

如果提示没有 `lark-cli`，可以自动安装飞书 CLI：

```bash
python3 scripts/world_cup_calendar.py doctor --install-cli
```

也可以手动安装：

```bash
npm install -g @larksuite/cli
```

如果电脑没有 `node` 或 `npm`，请先安装 Node.js LTS：

https://nodejs.org/

## 3. 先预览

只看赛程，不访问飞书：

```bash
python3 scripts/world_cup_calendar.py preview --focus-team ARG --limit 12
```

预览将要写入飞书的内容，不真正创建：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG
```

## 4. 同步到飞书

确认预览没问题后执行：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG --execute
```

第一次执行时，飞书会要求授权。脚本会提示你打开授权链接。

常见需要授权的权限：
- `calendar:calendar:read`
- `calendar:calendar:create`
- `calendar:calendar.event:create`

## 5. 关注其他球队

关注多个球队时，用英文代码逗号分隔：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG,BRA,FRA --execute
```

只同步关注球队比赛：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG --only-focus --execute
```

## 6. 删除日程

删除前先预览：

```bash
python3 scripts/world_cup_calendar.py delete --match-numbers 19,43,70
```

确认后真正删除：

```bash
python3 scripts/world_cup_calendar.py delete --match-numbers 19,43,70 --execute
```

删除全部 104 场世界杯日程：

```bash
python3 scripts/world_cup_calendar.py delete --all
python3 scripts/world_cup_calendar.py delete --all --execute
```

删除整个 `world-cup-calendar` 日历：

```bash
python3 scripts/world_cup_calendar.py delete --delete-calendar
python3 scripts/world_cup_calendar.py delete --delete-calendar --execute
```

删除时可能需要额外授权：
- `calendar:calendar.event:read`
- `calendar:calendar.event:delete`
- `calendar:calendar:delete`

## 数据来源

赛程来自 FIFA 官方 PDF：

https://digitalhub.fifa.com/m/1be9ce37eb98fcc5/original/FWC26-Match-Schedule_English.pdf

FIFA 标注赛程可能调整，重要比赛前建议再次核对官方信息。
