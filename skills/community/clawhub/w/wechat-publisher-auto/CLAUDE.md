# CLAUDE.md

wechat-publish-pro 项目开发维护指南。

## 项目结构

```
wechat-publish-pro/
├── SKILL.md              # Skill 使用文档
├── scripts/
│   └── publish.sh        # 发布脚本（Markdown → HTML → 微信）
├── src/wechat_publisher/
│   ├── __init__.py
│   ├── cli.py            # CLI 入口 (typer)
│   ├── config.py         # 配置管理
│   ├── humanizer/        # AI 去痕模块
│   │   └── __init__.py
│   └── platforms/        # 平台适配器
│       ├── base.py       # 抽象基类
│       ├── __init__.py
│       └── wechat.py     # 微信公众号实现
└── pyproject.toml
```

## 常用命令

```bash
# 安装/更新
pip install .

# 开发模式安装
pip install -e .

# 测试 CLI
wechat-publish-pro --help
wechat-publish-pro config show
wechat-publish-pro test

# 测试 wenyan-cli
wenyan render -f example.md -t lapis
```

## 依赖

- **wenyan-cli**: Node.js CLI，`npm install -g @wenyan-md/cli`
- **wechat-publish-pro**: Python 包，本项目

## 微信公众号 API

- 草稿箱 API: `POST /cgi-bin/draft/add`
- 素材上传: `POST /cgi-bin/material/add_material`
- Token 获取: `GET /cgi-bin/token`

## 故障排查

1. **Import Error**: 确保 pyproject.toml 中 packages 路径正确
2. **CLI 找不到**: `pip install .` 后重新加载 PATH 或检查 entry_points
3. **微信 45166**: IP 不在白名单，添加当前 IP 到公众号后台
