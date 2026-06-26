# VBTI · Vibe-coding Type Indicator

> 给苦逼程序员搓的 MBTI。
> 扫你的 vibe coding 历史记录，把你审判为 16 型 vibe coder 中的一种。
> 生成一张诊断书风格的 HTML 卡片到桌面，可直接截图发小红书。

![SORY 道歉精 示例卡片](assets/sory-sample.png)

## 这是什么

`/vbti` 是一个 vibe-coding 诊断 skill。它会：

1. 扫你机器上的 vibe coding session 记录（默认从 `~/.claude/projects/` 读 JSONL transcript）
2. 统计你的关键词词频、Bash 命令分布、文件操作类型、时间分布
3. 给 16 个 vibe coder 型号打分，挑分数最高的
4. 把你的真实数据填进诊断书模板
5. 输出 HTML 到 `~/Desktop/我的-VBTI-{TYPE}.html` 并自动 open

没有任何外部依赖。不联网，不上报，不读你的代码。只读你和 AI 说过的话。

## 16 型一览

| 代号 | 中文名 | Emoji | 一句话 |
|------|--------|-------|--------|
| SOON | 大饼批发商 | 🥧 | 下周一定上线 |
| MONK | 赛博苦行 | 🧘 | git push 0 次 |
| SHOW | 橱窗工程师 | 🎭 | 能截图就行 |
| VIBE | 氛围工程师 | 🌀 | 感觉很对就是跑不起来 |
| BLAM | 甩锅大师 | 🫵 | 你又写错了 |
| YEET | 删库飞人 | 💣 | 凌晨三点 rm -rf |
| GHST | 凌晨幽魂 | 👻 | 灵感寿命 6 小时 |
| LOOP | 重构教主 | 🔁 | 第八次推倒重来 |
| MOSS | 长草老登 | 🌿 | README 比代码勤 |
| SORY | 道歉精 | 🙇 | 对 AI 比对自己客气 |
| NODE | 全自动 yes 党 | ✅ | "ok 继续" 按了 N 次 |
| DUMP | 报错投掷手 | 🗑️ | 这是什么错 |
| TOYS | 工具试色师 | 🧸 | 这库比那个好吗 |
| TIDY | 格式洁癖家 | 🎨 | 改个变量名 |
| LERN | 解释依赖症 | 🎓 | 你能解释下吗 |
| TEST | 测试绝缘体 | 🧪 | 没测过应该没事 |

## 安装

### OpenClaw / Claw 用户

```bash
git clone https://github.com/TinaDu-AI/vbti.git ~/.claw/skills/vbti
```

### Claude Code 用户

```bash
git clone https://github.com/TinaDu-AI/vbti.git ~/.claude/skills/vbti
```

## 怎么用

在你的 vibe coding 终端里输入：

```
/vbti
```

或者说：
- "测一下我的 vibe coding 人格"
- "我是哪型 vibe coder"
- "生成我的 VBTI"

也可以直接命令行跑：

```bash
python3 ~/.claw/skills/vbti/run.py    # OpenClaw / Claw 用户
python3 ~/.claude/skills/vbti/run.py  # Claude Code 用户
```

## 输出

```
🔍 扫历史记录 ...
📊 排行前 5：[('DUMP', 1525.6), ('VIBE', 1060.5), ('TOYS', 948.3), ('SORY', 757.5), ('LOOP', 650.5)]
🎯 你的 VBTI 是：DUMP · 报错投掷手 🗑️
📄 卡片已生成：/Users/<you>/Desktop/我的-VBTI-DUMP.html
```

HTML 自动在浏览器打开，截图就能发小红书。

## 隐私

- 全部本地运行
- 只读本地 vibe coding 历史 JSONL
- 不上传，不联网，不调用 API

## 文件结构

```
vbti/
├── SKILL.md              # skill manifest
├── run.py                # 主程序：扫 → 算 → 渲染
├── vbti_types.py         # 16 型定义 + 评分权重
├── templates/
│   └── card.html         # 共享诊断书模板
└── assets/
    └── sory-sample.png   # 示例图
```

## License

MIT.

---

发小红书别忘了带 `#VBTI`。
