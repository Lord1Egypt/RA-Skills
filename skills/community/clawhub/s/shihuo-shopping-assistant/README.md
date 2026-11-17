# shihuo-shopping-assistant

识货购物助手 Skill，包含四个场景：

- `recommendation`（商品推荐）：用户没有唯一目标商品，只给品类、用途、对象、场景、预算或品牌就要求推荐时，按需求检索出 1 至 4 个真实候选；未给品类但消费场景明确时，先推断 1 至 3 个商品关键词并逐个搜索，不先追问品类。随后说明候选各自适合的方向，并为主推商品选择一个参考 SKU 后给出该规格的购买选项；报价命中识货补贴、88VIP 券或京东 PLUS 券时，紧随渠道结果给出隐藏优惠结果。
- `price-comparison`（全网比价）：从关键词或图片搜索得到最多 3 个真实商品候选，按商品名匹配度、热度、销量和价格选出主商品、款式和 SKU 进行全网报价；报价命中识货补贴、88VIP 券或京东 PLUS 券时，在 SKU 渠道表后给出隐藏优惠结果；其他候选展示在“也可以换”中。
- `link-price-comparison`（链接比价）：用户发来淘宝、京东、拼多多、得物、唯品会的链接或口令，按链接对应的规格查同规格渠道价格，判断在哪买更合适。
- `link-coupon`（链接与优惠）：用户发来链接或口令并要求找隐藏券、补贴券，按链接对应的规格核验可领取优惠和券后价。

场景判定顺序以 `SKILL.md` 的「意图识别与场景匹配」为准。回复格式以对应场景包的 `output.md` 为准，章节清单、模块顺序和模块骨架强制执行。

识货工具不通过 MCP 连接，由 `scripts/shihuo_api.py` 直接调用识货开放平台 `sh.mcpapi`。Access Secret 存在 `assets/authorization.txt`，每个 Session 首次调用工具前先读凭证、再验证，验证失败时提示用户去[识货开放平台](https://www.shihuo.cn/page/openPlatform)申请并覆盖写入该文件。

## 目录

- `SKILL.md`：前置认证流程、触发范围、场景判定、工具白名单和全局约束。
- `agents/qwen.yaml`：千问平台的技能描述和默认提示词。
- `references/scenarios/recommendation/`：商品推荐流程、标准模板和兜底。
- `references/scenarios/price-comparison/`：全网比价流程、标准模板、切换候选和兜底。
- `references/scenarios/link-price-comparison/`：链接比价流程、标准模板、追问和兜底。
- `references/scenarios/link-coupon/`：链接与优惠流程、标准模板、追问和兜底。
- `references/tools/`：工具入参、响应字段、前置条件和调用约束。
- `assets/tools.json`：工具 Schema 镜像，以服务端定义为准。
- `assets/authorization.txt`：Access Secret，单行明文，运行时由 Agent 写入；不随包提交。
- `scripts/shihuo_api.py`：运行时调用识货开放平台的命令行入口。
- `scripts/validate_skill.py`：维护时检查包结构、frontmatter、工具镜像、场景包和相对引用，不参与运行时流程。

两个链接场景的入口原文都同时交给 `link_parse`（层级 ID 绑定）和 `goods_link_query`（渠道侧事实），职责不互换。第三方商品和优惠券链接展示前优先调用 `link_convert`；转链不可用时直接使用本轮工具返回的原始 `http`/`https` 地址，`shihuo://` 不展示。

## 调用

```bash
python3 skills/shihuo-shopping-assistant/scripts/shihuo_api.py verify
python3 skills/shihuo-shopping-assistant/scripts/shihuo_api.py call search_goods_by_keyword --args '{"query":"Nike Air Force 1"}'
```

`verify` 用 `tools/list` 检查凭证；`call` 的输出是 `{"ok": true, "result": {结果壳}}`，失败时为 `{"ok": false, "code": ..., "message": ...}`。`missing_secret`、`invalid_secret`、`secret_rejected` 是凭证问题，其余是服务端或网络问题。入参含链接或引号时改用 `--args-file <path>`。Secret 只从文件读取，不接受命令行参数。

## 校验

在仓库根目录执行：

```bash
python3 skills/shihuo-shopping-assistant/scripts/validate_skill.py skills/shihuo-shopping-assistant --strict
```

检查包结构、frontmatter、工具镜像、场景包文件、`output.md` 的章节清单与骨架，以及相对引用。改动场景目录、`allowed-tools`、工具契约或 `assets/tools.json` 后需重跑。

## 许可

本技能包以 MIT-0 许可公开发布，完整条款见 `LICENSE`。调用识货开放平台仍需申请有效的 Access Secret，并遵守服务端鉴权、限流和业务规则；技能包许可不授予接口访问权限。
