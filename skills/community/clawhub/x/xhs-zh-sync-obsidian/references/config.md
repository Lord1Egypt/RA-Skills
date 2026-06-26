# 配置

默认配置文件：

```text
~/.config/social-favorites-to-obsidian/config.yaml
```

创建配置：

```bash
python scripts/setup.py --init
```

首次初始化前，agent 必须先询问用户分类规则策略：

- 由 LLM 初始化生成常用分类规则，并写入 `classify_rules.yaml`。
- 用户稍后自行编辑，先使用默认 `其他/待整理`。

关键字段：

```yaml
data_dir: "~/.local/share/social-favorites-to-obsidian"
cookiecloud_env: "~/.config/social-favorites-to-obsidian/cookiecloud.env"

obsidian:
  vault: "~/.local/share/social-favorites-to-obsidian/obsidian-vault-a1b2c3d4"
  base_dir: "互联网笔记"
  run_ob_sync: false
  sync:
    mode: "local-only"

hctec:
  skills_root: "~/.openclaw/workspace/skills"

platforms:
  xhs:
    max_per_run: 50
    no_headless: false
  zhihu:
    collection_ids: []
    max_per_collection: 100
    max_per_run: 100

classification:
  rules_file: "~/.config/social-favorites-to-obsidian/classify_rules.yaml"
  default_level1: "其他"
  default_level2: "待整理"
```

分类规则示例：

```yaml
rules:
  - level1: "技术"
    level2: "AI"
    keywords: ["AI", "LLM", "模型", "agent"]
  - level1: "生活"
    level2: "旅行"
    keywords: ["旅行", "城市", "路线"]
```

`zhihu.collection_ids` 为空时，会自动发现当前账号可见的收藏夹，然后逐个抓取最近内容。

运行时数据保存在 `data_dir`：

- `<platform>/raw/*.json`：抓取后的结构化原始数据
- `<platform>/state.json`：抓取状态
- `<platform>/export_state.json`：Obsidian 导出状态

这些运行时数据不要提交到公开技能包。

其它 agent 判断是否首次安装时，运行：

```bash
python scripts/setup.py --status --json
```
