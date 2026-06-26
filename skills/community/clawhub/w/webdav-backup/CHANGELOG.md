# Changelog

## 1.2.2 - 2026-03-10

- 统一环境变量命名为 `WEBDAV_PASSWORD`，移除 `WEBDAV_PASS` 兼容分支
- 调整 `SKILL.md` metadata 为更标准的 `openclaw.requires.env` 结构，降低 ClawHub 扫描中的不一致提示

## 1.2.1 - 2026-03-10

- 移除明文密码写入 shell 启动文件的文档建议
- 移除关闭 TLS 校验的建议，改为更安全的证书排查说明
- 补充恢复前先检查 manifest 的安全建议
- 清理发布包中的杂质文件与本地元数据目录（如 `.DS_Store`、`__pycache__`、`.clawhub`、`.ace-tool`）

## 1.2.0 - 2026-03-10

- 默认本地输出目录统一到 `~/openclaw/output`
- 默认备份范围扩展为 `workspace + openclaw.json + cron + workspace/config`
- 新增 `backup-manifest.json`
- 新增默认排除规则，跳过 `.git`、缓存、临时目录、输出目录等内容
- 新增本地恢复能力：支持 `--restore latest`、`--restore-dir`、`--force`
- 在 `SKILL.md` 中补充恢复判断建议，交由 agent 按场景自主决策

## 1.1.0 - 2026-03-10

- 新增本地备份能力
- 支持 `--local-only`、`--remote-only`、`--list`、`--list-remote`
- 默认本地输出目录从原先备份目录逻辑收敛为统一输出目录方案

## 1.0.2

- 初始 WebDAV 备份版本
