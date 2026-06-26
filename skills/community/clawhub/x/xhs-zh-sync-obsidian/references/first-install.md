# 首次初始化访谈

首次安装时不要直接运行默认 `setup.py --init`。先向用户确认下面三组选择，再执行命令和写配置。

推荐使用交互式安装器完成访谈和初始化：

```bash
python install.py
```

如果 `npx skills install` 的执行环境需要显式脚本路径，使用：

```bash
python scripts/interactive_install.py
```

## 1. CookieCloud 部署方式

必须询问：

- 是否在本机安装 CookieCloud 服务端？
- 如果本机安装：确认本机有 Docker / Docker Compose 环境，并准备使用 `assets/docker-compose.cookiecloud.yml`。
- 如果不在本机安装：要求用户提供 CookieCloud 服务端地址、UUID 和 Password。

本机安装时：

```bash
Copy-Item assets/docker-compose.cookiecloud.yml docker-compose.yml
docker compose up -d cookiecloud
python scripts/setup.py --init --cookiecloud-server-url http://127.0.0.1:8088
```

`setup.py --init` 会自动生成 `COOKIECLOUD_UUID` 和 `COOKIECLOUD_PASSWORD`，并写入 `cookiecloud.env`。生成后必须告诉用户：

- 在自己常用的 Chrome 浏览器中安装 CookieCloud 插件。
- 插件服务器地址填写运行 CookieCloud 服务端的 IP 和端口；如果插件和服务端在同一台机器上可以用 `http://127.0.0.1:8088`，否则要用其它设备能访问到的 `http://<本机局域网IP>:8088`。
- 插件 UUID 填写生成的 `COOKIECLOUD_UUID`。
- 插件密码填写生成的 `COOKIECLOUD_PASSWORD`。
- 在浏览器中登录小红书和知乎后，执行 CookieCloud 插件同步。

非本机服务端时：

```bash
python scripts/setup.py --init --cookiecloud-server-url http://<host>:8088
```

然后编辑 `~/.config/social-favorites-to-obsidian/cookiecloud.env`，写入用户提供的：

```text
COOKIECLOUD_SERVER_URL=http://<host>:8088
COOKIECLOUD_UUID=<uuid>
COOKIECLOUD_PASSWORD=<password>
COOKIECLOUDUUID=<uuid>
COOKIECLOUDPASSWORD=<password>
```

如果用户还没有 CookieCloud 凭据，则用 `setup.py --init` 生成的 UUID/password，引导用户把这组值填到浏览器 CookieCloud 插件里。

## 2. Obsidian Vault 与同步方式

必须询问用户选择一种：

1. 自动创建本地 vault，并使用官方 Obsidian Sync。
2. 自动创建本地 vault，但只本地导出，不自动同步。
3. 使用当前已有本地 vault 目录。

选择官方 Obsidian Sync 时，还必须询问：

- Obsidian 官方账号邮箱/用户名。
- Obsidian 官方账号密码；如果用户不愿提供，让 `ob login` 交互输入。
- 远程 vault 名字或 ID。
- 如果远程 vault 使用端到端加密，还需要 Obsidian Sync 加密密码；如果不提供，让 `ob sync-setup` 交互输入。

执行顺序：

```bash
python scripts/setup.py --init --obsidian-mode headless-sync
python scripts/setup.py --install-ob
ob login
python scripts/setup.py --setup-ob-sync --obsidian-sync-vault "<远程vault名或ID>"
```

如果用户提供已有本地 vault 目录，并且也要官方同步：

```bash
python scripts/setup.py --init --obsidian-mode headless-sync --obsidian-vault "<本地vault目录>"
python scripts/setup.py --install-ob
ob login
python scripts/setup.py --setup-ob-sync --obsidian-sync-vault "<远程vault名或ID>"
```

只本地导出时：

```bash
python scripts/setup.py --init --obsidian-mode local-only
```

使用已有本地 vault 且不自动同步时：

```bash
python scripts/setup.py --init --obsidian-mode local-only --obsidian-vault "<本地vault目录>"
```

注意：`setup.py --setup-ob-sync` 不会自动执行 `ob login`。如果 `ob` 未登录，先运行 `ob login`。

## 3. 文章分类标准

必须询问用户选择一种：

1. 由 LLM 根据常见知识管理场景初始化生成分类规则。
2. 用户稍后自行编辑分类规则，先使用默认 `其他/待整理`。

如果选择 LLM 初始化，生成并写入：

```text
~/.config/social-favorites-to-obsidian/classify_rules.yaml
```

规则格式：

```yaml
rules:
  - level1: "技术"
    level2: "AI"
    keywords: ["AI", "LLM", "模型", "agent"]
  - level1: "生活"
    level2: "旅行"
    keywords: ["旅行", "城市", "路线"]
```

如果选择稍后自定义，不要过度生成规则；保留脚本初始化出来的示例或默认分类即可，并告诉用户稍后编辑 `classify_rules.yaml`。

## 4. 安装后必须执行

hctec 第三方技能安装后运行知乎格式补丁：

```bash
python scripts/patch_hctec_zhihu_format.py
```

然后检查：

```bash
python scripts/setup.py --doctor
```

最后做小规模验证：

```bash
python scripts/sync.py --platform xhs
python scripts/sync.py --platform zhihu
python scripts/export_obsidian.py --platform all --incremental
```
