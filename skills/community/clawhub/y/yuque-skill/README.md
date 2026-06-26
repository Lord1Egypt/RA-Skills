# 语雀 Skill (Yuque Skill for Openclaw & Claude Code)

把语雀(Yuque)的开放API包装成一组可被 **Openclaw / Claude Code / Claude Agent SDK** 直接调用的Python脚本,让Claude能像操作本地文件一样操作云端语雀文档:增删改查、目录重排、Markdown排版调整、全文搜索、批量导入导出。

> 仓库结构遵循 Anthropic Skill 规范,可被任一支持 Skill 的 Claude 客户端识别与触发。

## 目录结构

```
yuque-skill/
├── SKILL.md                       # 触发描述与使用入口(Openclaw / Claude Code 会自动读这一份)
├── README.md                      # 本文件:安装、部署、调用说明
├── scripts/
│   ├── yuque_client.py            # 通用API客户端(零依赖,标准库 urllib)
│   ├── docs.py                    # 文档/知识库 CRUD
│   ├── toc.py                     # 目录管理
│   ├── search.py                  # 搜索
│   ├── batch.py                   # 批量导入/导出/正则替换
│   └── format_helpers.py          # Markdown格式化生成器
└── references/
    ├── api_reference.md           # 语雀v2 API速查表
    ├── markdown_format.md         # 语雀Markdown扩展语法
    └── toc_operations.md          # TOC action字段与典型场景
```

## 一、在 Openclaw 中安装

Openclaw 的 Skill 加载机制会扫描 `~/.openclaw/skills/` 与项目级 `.openclaw/skills/` 目录。任选以下方式之一:

### 方法 A:终端 — 个人级安装(对所有项目可用)

> 前提：先从 [Releases](https://github.com/feixuelingcloud/yuque-skill/releases) 下载 `yuque.skill`，解压后得到 `yuque-skill/` 目录，再执行：

```bash
mkdir -p ~/.openclaw/skills/
cp -r yuque-skill ~/.openclaw/skills/yuque
```

### 方法 B:终端 — 项目级安装(只对当前工作目录可用)

> 前提：同方法 A，先下载解压得到 `yuque-skill/` 目录，再执行：

```bash
mkdir -p .openclaw/skills/
cp -r yuque-skill .openclaw/skills/yuque
```

### 方法 C:终端 — 从 GitHub 直接安装(推荐)

```bash
# 个人级安装
git clone https://github.com/feixuelingcloud/yuque-skill ~/.openclaw/skills/yuque

# 或项目级安装
git clone https://github.com/feixuelingcloud/yuque-skill .openclaw/skills/yuque
```

日后更新只需:

```bash
git -C ~/.openclaw/skills/yuque pull
```

### 方法 D:终端 — 作为 Claude Code Plugin 打包

```bash
# 在 yuque-skill 父目录下
zip -r yuque.skill yuque-skill/
```

把生成的 `yuque.skill` 放进 Openclaw / Claude Code 的 plugin marketplace 即可。

### 方法 E:在 Openclaw 对话页面中安装

直接在对话框输入:

> 从 GitHub 安装 skill：https://github.com/feixuelingcloud/yuque-skill

Openclaw 会自动执行 git clone 到个人级 skills 目录。

> Skill 加载完成后,Openclaw 启动时会在系统提示里看到 `yuque` 这个 skill 及其触发条件,无需额外注册。

## 二、配置语雀 Token

语雀API所有写操作都需要 `X-Auth-Token`。Token 在 [https://www.yuque.com/settings/tokens](https://www.yuque.com/settings/tokens) 创建,勾选至少 `doc:read / doc:write / repo:read / repo:write` 四项 scope。

本 skill 支持两种凭证来源,**环境变量优先**:

### 方式1:环境变量(推荐 CI / 长期任务)

```bash
export YUQUE_TOKEN='你的token'
# 私有部署用户额外指定:
export YUQUE_BASE_URL='https://yuque.your-company.com/api/v2'
```

把上面两行写入 `~/.bashrc` / `~/.zshrc` / Openclaw 或 Claude Code 启动脚本,Openclaw / Claude Code 调用脚本时即可自动读取。

### 方式2:配置文件 `~/.yuque/config.json`

```bash
mkdir -p ~/.yuque
cat > ~/.yuque/config.json <<'EOF'
{
  "token": "你的token",
  "base_url": "https://www.yuque.com/api/v2"
}
EOF
chmod 600 ~/.yuque/config.json
```

## 三、自检

```bash
python ~/.openclaw/skills/yuque/scripts/yuque_client.py whoami
```

返回当前用户的 JSON 即说明 Token 已生效。返回 401 → Token 无效 / scope 不足。

## 四、在 Openclaw / Claude Code 中怎么用

安装并配好 Token 之后,直接用自然语言描述需求即可,Openclaw / Claude Code 会自动加载 SKILL.md 并选择合适的脚本。常见用法举例:

| 你说什么 | Openclaw / Claude Code 会执行的脚本 |
|---|---|
| "看看我的语雀里有哪些知识库" | `docs.py list-repos` |
| "把这份会议纪要发到「我的笔记」知识库,标题叫《4月复盘》" | `docs.py create user/notes --title "4月复盘" --body-file ...` |
| "把语雀里那篇《入职指南》的第二章标红加大字号" | `docs.py get` → 用 `format_helpers.styled` 改写 → `docs.py update` |
| "把语雀「项目文档」目录重排成 前言/正文/附录 三层" | `toc.py show` → 编辑 → `toc.py apply` |
| "搜一下我语雀里所有提到 GPU 的文档" | `search.py docs GPU --scope user` |
| "把整本《工程笔记》导出成本地Markdown,文件名按slug命名" | `batch.py export user/eng-notes --out-dir ./eng-notes` |

## 五、安全与配额

- 默认指数退避 (2/4/8s) 处理限流,无需上层额外控制。
- 公有云默认 5000 req/h,批量任务请保持每秒 ≤ 5 个写。
- `batch.py replace` 对正文做正则替换,**强烈建议先 `--dry-run`** 看影响面。
- `toc.py remove` 默认会连同底层文档一起删,需要保留请加 `--keep-doc`。

## 六、卸载

```bash
rm -rf ~/.openclaw/skills/yuque
unset YUQUE_TOKEN YUQUE_BASE_URL
rm -f ~/.yuque/config.json
```

## 七、许可证

本 skill 以 MIT 协议发布。语雀 API 的使用须遵守 [语雀开发者协议](https://www.yuque.com/yuque/developer/agreement)。
