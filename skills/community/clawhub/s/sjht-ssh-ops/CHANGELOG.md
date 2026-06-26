# Changelog — ssh-ops

所有格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [0.1.0] — 2026-03-19

### 新增
- 初始版本发布
- **SSH 密钥管理脚本** `scripts/ssh-key-setup.sh`
  - `gen` — 生成 ed25519 密钥对（已存在则提示）
  - `pub` — 查看公钥
  - `deploy` — 通过 sshpass + ssh-copy-id 部署公钥到远程主机
  - `test` — BatchMode 免密登录测试
  - `list` — 列出已有密钥
  - `info` — 查看远程主机信息（系统/内核/内存/磁盘/负载）
  - 自动检测并安装 sshpass（支持 apt-get 和 yum）

### 首次验证
- 成功生成密钥对并部署到
- 免密登录测试通过
- 远程主机信息查询正常
