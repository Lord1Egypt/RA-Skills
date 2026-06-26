# 贡献指南（Contributing）

欢迎为 **clawhub-daily** 贡献代码、文档、痛点配置或 Bug 反馈！

## 🤝 如何贡献

### 报告 Bug

在 [GitHub Issues](https://github.com/EdwardWason/clawhub-daily/issues) 提交，请包含：
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（OS / Python 版本 / 输出日志）
- 推荐附上 `data/recommended/<date>.json` 文件

### 提出新功能

在 [GitHub Discussions](https://github.com/EdwardWason/clawhub-daily/discussions) 发起讨论，说明：
- 解决的问题
- 使用场景
- 替代方案
- 是否有能力自己实现

### 提交代码

1. **Fork** 本仓库
2. 创建特性分支（`git checkout -b feature/amazing-feature`）
3. 提交代码（`git commit -m "feat: add amazing feature"`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 创建 **Pull Request**

## 📋 贡献方向

### 1. 痛点库扩展

编辑 `references/pain-points.md` 和 `scripts/daily_recommend.py` 中的 `PAIN_POINTS_DB`：
- 添加新场景（需提供 ≥ 10 个 keywords）
- 调整权重
- 提供 `next_action_template`

### 2. 维度规则优化

编辑 `scripts/daily_recommend.py` 中的 `DIMENSION_CONFIG`：
- 调整过滤条件
- 增加新的 `sort_field`
- 新增维度（需修改 `get_dimension_by_date()` 中的 `dims` 数组）

### 3. 推送渠道扩展

参考 `scripts/push_to_feishu.py` 实现新的推送脚本：
- `scripts/push_to_xxx.py` 实现新渠道
- 凭证放在 `references/config.json`
- 加入 `scripts/push_<channel>.py` 模块化

### 4. 多语言支持

- `references/briefing-template.md` 添加英文/日文模板
- `scripts/daily_recommend.py` 中支持 `language` 参数
- README 添加中英日切换链接

### 5. 简报排版优化

- `scripts/daily_recommend.py` 中的 `generate_markdown()` 和 `generate_feishu_blocks()`
- 增加图表、推荐位、对比表等

## 🧪 本地测试

```bash
# 1. 抓取测试
python scripts/fetch_clawhub.py --num 10 --date $(date -I) --output /tmp/test_snap

# 2. 指标计算
python scripts/compute_metrics.py --input /tmp/test_snap/$(date -I).json

# 3. 推荐生成
python scripts/daily_recommend.py --date $(date -I) --data-dir /tmp/test_data --target 3

# 4. 推送测试
python scripts/push_to_feishu.py --recommendation /tmp/test_data/recommended/$(date -I).json
```

## 📐 代码规范

- Python 风格：函数 docstring 用中文、关键函数加类型注解
- 路径处理：用 `pathlib.Path`
- 异常处理：单文件失败不影响全局（try-except 兜底 + warn 日志）
- 凭证管理：**绝不**硬编码，全部走 `references/config.json` 或环境变量
- 提交信息：`<type>(<scope>): <subject>`，类型见 [Conventional Commits](https://www.conventionalcommits.org/)

## 🔒 隐私要求

**严禁**在 PR 中包含：
- ❌ 真实 `app_id` / `app_secret` / `api_key` / `user_open_id`
- ❌ 个人文件路径
- ❌ 真实邮箱/手机号
- ❌ 内部 API 地址

**正确做法**：
- ✅ 凭证用 `<your_xxx>` 占位符
- ✅ 路径用 `~` 或相对路径
- ✅ 内部地址用 `example.com`

## 📜 License

贡献的代码遵循 [MIT-0](LICENSE) 协议。

## 💬 联系方式

- GitHub Issues: [EdwardWason/clawhub-daily/issues](https://github.com/EdwardWason/clawhub-daily/issues)
- GitHub Discussions: [EdwardWason/clawhub-daily/discussions](https://github.com/EdwardWason/clawhub-daily/discussions)
