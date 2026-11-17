# Linux 全链路自测

`linux_e2e.sh` 在**真实 Linux** 上跑完整个工作流，用于验证扫描 → dry-run → 修复 → 校验 → 回滚 → 报告 → HTTPS 网页端。

## 前置条件

- 一次性测试机 / 已有快照可回滚的虚拟机（脚本会临时改写系统配置）
- root 权限（`sudo bash tests/linux_e2e.sh`）
- `python3`（3.8+）、`sshd`；生成证书优先用 `openssl`，没有则回退 Python `cryptography`
- 建议 Ubuntu 22.04 / 24.04 或 Rocky/Alma 9

## 运行

```bash
# 1) 把 skill 目录拷到测试机（或直接在虚拟机里解压 zip）
scp -r server-security-guard/ user@vm:/tmp/

# 2) 在虚拟机上执行
ssh user@vm 'sudo bash /tmp/server-security-guard/tests/linux_e2e.sh'
```

退出码 `0` 表示全部通过；`1` 表示有失败项；`2` 表示环境不满足（非 root / 无 python3）。

## 它会改动什么（全部自动恢复）

| 目标 | 操作 | 恢复方式 |
|------|------|----------|
| `/etc/ssh/sshd_config` | 备份后写入弱配置（`PermitRootLogin yes` 等），用于产生可检出漏洞 | `trap` 在退出/中断时还原并 reload |
| `/var/log/auth.log`（或 `secure`） | 追加 6 条伪造的 Failed password 记录 | 还原备份 |
| `/root/.ssh/id_rsa` | 仅在**不存在**时生成，并临时 `chmod 644` 触发 CFG-06 | 删除本脚本创建的密钥 |
| 端口 `18443` | 启动 HTTPS 网页端做自检 | 退出时 kill |

失败的用例会打印 `FAIL` 与原因；环境缺项（无 sshd、无 auth.log）标记 `SKIP` 而不是失败。

## 覆盖范围

- Phase 1 扫描：检出 CFG-01/02/03（有私钥时含 CFG-06）
- Phase 2 修复：dry-run 返回 `would_fix`；`--apply` 真实改写配置；生成 `.guard-bak` 备份；回滚命令存在；备份还原后内容正确
- Phase 3 感知：从日志检出 `brute_force` 事件（源 IP 203.0.113.66）
- Phase 4 防御：封禁 dry-run 返回 `would_block` + 回滚命令；加固 dry-run 返回 `would_harden`
- Phase 5 报告：HTML 生成、无残留 `{{}}` 占位符、含目标标识
- 网页端：HTTPS 200、无 token 403、带 token 200、拒绝 TLS1.1

## 不在覆盖范围

- 远程 `ssh://` 目标的真实执行（脚本用 `local`；远程仅在本地单测里 mock 验证）
- `block` 的**真实**封禁（linux_e2e.sh 只做 dry-run）
- `harden --apply`（只做 dry-run，避免改动内核参数）

补充脚本 `tests/linux_extra.sh` 覆盖了其中两项（需 root、会临时改 sshd_config 并加 iptables 规则，trap 自动还原）：

```bash
sudo bash tests/linux_extra.sh
```

- 网页端「管理员权限（sudo）」真实 apply：以非 root 用户启动 UI，勾选提权后扫描→预览→apply，验证 `/etc/ssh/sshd_config` 确实被改
- iptables 真实封禁：加 `DROP` 规则 → `iptables -C` 校验存在 → `--rollback` → 校验规则移除

需要验证 `harden --apply` 时，在快照机上手动执行：

```bash
sudo python3 scripts/attack_defend.py --target local --input monitor.json --action harden --apply
```
