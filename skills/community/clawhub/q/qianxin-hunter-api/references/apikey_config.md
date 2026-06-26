# 在 OpenClaw 中配置 API KEY

- 不要通过对话配置 API KEY，应通过 OpenClaw Web UI 的 Skills 配置区或 OpenClaw 配置文件配置。
- 请注意即使这样也并不能保证 API KEY 的绝对安全，因为 OpenClaw 的权限太高了，注意不要在对话中配置、查询和修改 API
  KEY，以免泄露给外部模型和第三方工具等。
- 若发生 API KEY 泄露，请及时更新 API KEY。

## 1、配置 API KEY

### 通过 OpenClaw Web UI 配置

在 `**技能**` 页面展开 `**Workspace Skills**`，找到 `qianxin-hunter-api`，配置 API KEY

### 可通过 OpenClaw 配置文件查看已配置的 API KEY

找到 `~/.openclaw/openclaw.json`，找到类似下面的内容，后续也可以在此修改 API KEY

```json
{
  "skills": {
    "entries": {
      "qianxin-hunter-api": {
        "apikey": "xxx"
      }
    }
  }
}
```

## 2、重启 OpenClaw

```bash
openclaw gateway restart
```

## 3、验证案例

- 1、从 hunter 查询 ip="1.1.1.1" 的资产，获取第1页10条资产，fields="ip,port,domain"。不要使用其他工具或技能。
    - 预期：
        - Tool: script/query.py search --search 'ip="1.1.1.1"' --page 1 --page_size 10 --fields "ip,port,domain"

- 2、使用 qianxin-hunter-api 技能导出 ip="1.1.1.1" 的资产，返回全部字段，时间范围为20260301-20260320，最多获取100条资产。下载后不要分析结果文件。不要使用其他工具或技能。
    - 预期：
        - Tool: script/query.py batch submit --search 'ip="1.1.1.1"' --start 2026-03-01 --end 2026-03-20 --limit 100
        - Tool: script/query.py batch status --task_id 1234
        - Tool: script/query.py batch download --task_id 1234
    - 注意：文件保存位置一般在工作空间下：/root/.openclaw/workspace/results_1234.csv

- 3、从 hunter 导出我工作空间下 ip.csv 的资产，文件类型为ip，返回全部字段，时间范围为20260301-20260320，最多获取100条资产。下载后不要分析结果文件。不要使用其他工具或技能。
    - 预期：
        - Tool: script/query.py batch submit --file '/root/.openclaw/workspace/ip.csv' --type ip --start 2026-03-01
          --end 2026-03-20 --limit 100
        - Tool: script/query.py batch status --task_id 1234
        - Tool: script/query.py batch download --task_id 1234
