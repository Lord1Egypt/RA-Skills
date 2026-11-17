# 技能图标（发布时单独用，**必须放在技能目录之外**）

> 从 SKILL.md 正文迁来：只有要出图标时才需要读这一份。

平台创建技能时要求一张图标：**512×512、PNG 或 JPG、≤500KB**。
它是**表单里的一个字段**，不是 zip 里的文件 —— 所以图标单独生成、单独上传。

⚠️ **图标不要放进技能目录。** 技能目录常常同时是 GitHub 仓库，而 SkillHub 绑定仓库
发布时会按「文件类型白名单」逐个校验仓库文件，一张裸 `.png` 会让整次发布被拒
（报「不支持的文件类型: icons/xxx-icon.png」）。默认输出目录在技能目录之外：
`~/.workbuddy/skill-icons/`，可用 `--out` 或环境变量 `SKILLHUB_ICON_DIR` 改。

```bash
# ① 拿提示词（按本技能 SKILL.md 的展示名与描述拼，保证贴合技能身份）
python scripts/make_icon.py --prompt

# ② 交给 ImageGen（size 用 1024x1024），生成图回来做后处理
#    默认：居中裁切 + 清右下角生成标 + 缩到 512×512 + 压到 ≤500KB
python scripts/make_icon.py <生成图>            # 落盘到 ~/.workbuddy/skill-icons/
python scripts/make_icon.py <生成图> --out <目录> --name <技能名>

# ③ 上传前自查
python scripts/make_icon.py --check ~/.workbuddy/skill-icons/*.png
```

| 开关 | 作用 |
|---|---|
| `--prompt [--lang en]` | 只打印给 ImageGen 的提示词，不处理图片 |
| `--check` | 只做合规检查：512×512、PNG/JPG、≤500KB |
| `--no-center` / `--no-clean` | 关掉居中裁切 / 关掉清生成标（默认都开） |
| `--fmt png\|jpg` | 优先输出格式（默认 png；压不进 500KB 时自动降质或换格式） |
| `--out` / `--name` | 输出目录 / 文件名前缀（默认目录可用环境变量 `SKILLHUB_ICON_DIR` 固定） |

**两个真实踩过的坑，脚本默认已经处理：**

- ImageGen 出的是「1024×1024 圆角方块 + 外圈留白」，主体常偏一侧 —— 整图缩放会留白不对称，
  随手按固定框硬切（如 `(0,0,900,900)`）会**一边内容被截、另一边留白**。`--center` 按圆角方块真实边界取正方形。
- 生成图右下角带「AI生成 / WORKBUDDY」标，落在圆角方块**外侧**背景上。`--clean` 用周围背景重建，不碰主体。

图标 prompt 的要点：**单一主体、居中、不要文字**，用 1~2 个具象物件表达「这个技能做什么」，
缩小到 64px 仍能认出来。（画人物头像是**专家**头像的事，技能图标不讲人。）

**依赖**：生成 / 体检 / 打包全流程只用标准库；`make_icon.py` 需要 Pillow，属可选依赖 ——
`python scripts/setup.py --install-pillow`。不装也能跑到出 zip，只是图标得自己压。
