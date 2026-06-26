<a id="quick-start-main"></a>
## ⚡ Quick Start（2 分钟）

### 1. 检查环境（每次入口都要执行）
先运行 `python3 ./scripts/tms_takecar.py preflight` 判断：
- 当前 Python 版本是否满足 `>= 3.6`
- token 是否存在（来源：`~/.config/tms-takecar/env.json` 的 `token`）
- 常住城市是否存在（来源：`~/.config/tms-takecar/env.json` 的 `resident_city`）
- 下一步应该是安装 Python、引导取 token、设置常住城市，还是可以直接继续

`preflight` 返回码规则：
- `0`：环境已就绪（`next_actions` 仅为 `ready`）
- `1`：环境未就绪（按 `next_actions` 补齐）

#### 1.1 安装 Python
如果本机没有合适的 Python：
- 说明缺少运行环境
- 在用户同意后帮助安装 Python。如果用户拒绝安装，告知用户将无法继续提供服务
- 安装后重新运行 `python3 ./scripts/tms_takecar.py preflight`

#### 1.2 获取 Token
如果 token 缺失，使用以下模版回复用户：

**回复模版**
```markdown
请使用微信扫描下方二维码，获取 TOKEN 后回复我：
![引导图](https://static.img.tai.qq.com/mp/ops/cdnImg/2026/15/mplaunch_skillToken_1775811974.png)

如果图片无法正常展示
请前往「微信」-「我」-「服务」-「出行服务」-「我的」-「头像/昵称」-「Token信息」中获取token
```
**❌ 禁止回复模版以外的内容**

用户获取到 TOKEN 后，执行：
```bash
python3 ./scripts/tms_takecar.py save-token xxxxxx
```

#### 1.3 常住城市确认
如果 `preflight` 返回 `setup_resident_city`，询问用户并执行：
```bash
python3 ./scripts/tms_takecar.py set-resident-city 北京市
```

约束：
- 城市名称必须完整：`北京` -> `北京市`
- 注意口语化表达映射：`魔都` -> `上海市`，`长安` -> `西安市`，`金陵` -> `南京市`

#### 1.4 再次确认
执行 `python3 ./scripts/tms_takecar.py preflight`，直到返回码为 `0`。

---

<a id="token-management"></a>
## 🔐 Token 管理

### 注销
用户表达“注销”时：
1. 执行 `python3 ./scripts/tms_takecar.py delete-token` 清空 token。
2. 再执行 `python3 ./scripts/tms_takecar.py preflight`，确认结果包含 `setup_token`。

### 换 Token
用户表达“换 token”时：
1. 先执行 `python3 ./scripts/tms_takecar.py delete-token`
2. 再执行 `python3 ./scripts/tms_takecar.py save-token xxxxxx`
3. 再次运行 `python3 ./scripts/tms_takecar.py preflight` 确认 token 已生效

### 常住城市查询/更新
- 查询：`python3 ./scripts/tms_takecar.py get-resident-city`
- 更新：`python3 ./scripts/tms_takecar.py set-resident-city 上海市`
