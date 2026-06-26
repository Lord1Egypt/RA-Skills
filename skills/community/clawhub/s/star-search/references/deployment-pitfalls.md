# star-search 部署常见坑 (2026-06-04 汇总)

## 坑1: GitHub 443 推送超时 (75s 拒连)

**症状**:
- `git push` 30s timeout → exit 124
- 重试 60s → still timeout
- 重试 75s → `Failed to connect to github.com port 443 after 75011 ms`
- 不是限速，是**完全断连**

**根因**: GitHub 整体被墙/限流，与 git 协议无关。`http.version=HTTP/1.1` 没用。

**修法**:
1. **等 5 分钟再试**（实测 5min 后 `curl https://github.com` 1.0s 通了）
2. 本地 commit 必须先存好（`git commit` 不依赖 GitHub）
3. push 用 `GIT_ASKPASS=echo GIT_TERMINAL_PROMPT=0 git push <token_url> main` 避免交互
4. push 走 background + `process wait` 避免阻塞

**工作流**:
```bash
# 1. 本地 commit（不依赖 GitHub）
cd ~/.hermes/skills/research/star-search
git add -A
git commit -m "v17.X.0: ..."

# 2. 测试 GitHub 是否通
curl -sS -o /dev/null -w "%{http_code} %{time_total}s\n" -m 20 https://github.com/
# 200 = 通；timeout = 断

# 3. 通了就 push
GIT_ASKPASS=echo GIT_TERMINAL_PROMPT=0 git push https://${TOKEN}@github.com/muchenhengxin/Star.git main
```

**clawhub 不受影响**: clawhub publish 用 token 走不同 URL，不依赖 GitHub 443。所以**先发 clawhub 再 push GitHub**。

## 坑2: nginx 静态文件路径 ≠ home 目录

**症状**: 上传 `index.html` 到 `/home/ubuntu/star-search/`, 公网访问还是旧版。

**根因**: nginx 静态文件 root 是 `/var/www/star-search/`, **不是** home 目录。

**修法**: 先看 nginx conf
```bash
ssh -i ~/.ssh/muchenhengxin.pem ubuntu@62.234.39.247 \
  'cat /etc/nginx/sites-enabled/search-token-star.conf | grep -A 3 "location /"'
# 看到 root /var/www/star-search; 才确定路径
```

**正确上传**:
```bash
echo "$BASE64" | base64 -d > /var/www/star-search/index.html
# 验证
curl -s "https://search.token-star.cn/?nocache=N" | grep "<v17.X 标识>"
```

## 坑3: New-API PostgreSQL 容器名

**症状**: `docker exec new-api-postgres-1 psql` 失败。

**根因**: 本服务器 PostgreSQL 容器名就是 `postgres`, 不带前缀。

**正确命令**:
```bash
docker exec postgres psql -U root -d new-api -c "SELECT ..."
# 用户/密码/库: root / 123456 / new-api
```

## 坑4: LLM 答案层走哪个渠道 = 黑盒

**症状**: star-search 答案层有时 3s, 有时 12s, 不知道走哪个上游。

**根因**: New-API 按模型名自动路由，但**没有**渠道选择日志暴露给用户。

**排查方法**:
```bash
# 1. 看 New-API 日志
docker logs new-api --tail 50 | grep -i "DeepSeek-V4-Flash"

# 2. 直接查数据库
docker exec postgres psql -U root -d new-api -c \
  "SELECT * FROM abilities WHERE model LIKE '%DeepSeek%';"

# 3. 看真实日志里的 channel_id
docker logs new-api --tail 200 | grep -oE 'channel_id=[0-9]+' | sort -u
```

**2026-06-04 实测**: star-search 答案层用的 `DeepSeek-V4-Flash` **没有任何 channels 配这个模型**, 路由时找不到 → 退化或超时。

**解法**: 必须给 DeepSeek-V4-Flash 配专属渠道 (优先级 P0)。

## 坑5: Mac heredoc + SSH 传文件失效

**症状**: `ssh user@host 'cat > /tmp/file' < local_file` 把本地文件内容当命令, 不传到远端。

**根因**: Mac shell 重定向由本地处理, 不通过 SSH 管道。

**修法**:
```bash
# 错误
ssh ubuntu@host 'cat > /tmp/file' < /local/file

# 正确 1: base64 编码
echo "$B64" | base64 -d > /tmp/file

# 正确 2: scp
scp -i ~/.ssh/key.pem /local/file ubuntu@host:/tmp/file
```

## 坑6: server prompt 在 /home 找不到 ~/.hermes/

**症状**: 服务器上跑 `python3 answer.py` 报 "LLM_API_KEY not configured"。

**根因**: server 是 ubuntu 用户, 没 `~/.hermes/auth.json`。

**修法**: 在 `/home/ubuntu/<project>/.env` 写 LLM_API_KEY, answer.py 三层查找:
```python
# 1. 环境变量 LLM_API_KEY
# 2. /home/ubuntu/<project>/.env
# 3. ~/.hermes/auth.json
LLM_API_KEY = (
    os.environ.get("LLM_API_KEY")
    or _load_from_env_file("/home/ubuntu/<project>/.env")
    or _load_from_auth_json()
)
```

## 部署 checklist (v17.X 发布流程)

1. ✅ 本地测试新功能 (Python 单元 + API 调用)
2. ✅ 改 SKILL.md 文档 + 加 version 标记
3. ✅ 改 CHANGELOG / 端到端公网测试
4. ✅ 本地 git commit (不依赖 GitHub)
5. ✅ 传到服务器 + pkill 重启 + watchdog 拉起
6. ✅ 公网验证 (curl + 浏览器)
7. ✅ **先 clawhub publish** (不依赖 GitHub)
8. ⚠️ **再 git push GitHub** (可能 443 失败, 5min 后重试)
9. ✅ 跟用户报告结果 (GitHub 状态 + clawhub ID + 公网链接)
