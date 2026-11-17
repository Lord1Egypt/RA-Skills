# 配套脚本使用指南（WB-SAFE）

本技能随附 4 个本地脚本，全部离线运行、零积分、零网络。

## 1. wb_audit.py — 离线巡检脚本

一键只读体检：健康子集（磁盘/内存/进程）+ 明文凭据扫描（只报位置不回显值）+ 团包结构校验 + 配置基线漂移检测。

```bash
python scripts/wb_audit.py                 # 巡检 + 生成报告 + 更新基线
python scripts/wb_audit.py --init-baseline # 仅重建基线（不报漂移）
```

输出：`定期巡检报告_WB-SAFE_<日期>.md`（工作区根目录）。

设计约束：
- Windows 原生 Python 不认 `/c/` 路径，脚本自动探测用户目录
- 不调用任何云端 API，不消耗积分
- 凭据值绝不出现在 stdout / 报告文件
- baseline 用机器可读 JSON 维护，首次运行建基线，后续比对待漂移

## 2. wb_recovery_full.py — 全量/换机恢复演练脚本

模拟"换机/重装后恢复"的全量演练：身份文件、长期记忆、专家团包、连接器元数据、配置快照。

```bash
python scripts/wb_recovery_full.py            # dry-run（默认，安全，只估算不复制）
python scripts/wb_recovery_full.py --execute  # 真执行（需用户授权，占磁盘）
```

执行约束（红线）：
- 默认 dry-run 只估算复制范围与大小，不碰任何真实数据
- 真执行需显式 `--execute`，且占用磁盘
- 平台托管的 OAuth 凭据恢复后须通过平台重授权，本机无法自动完成
- 单进程内完成 复制→验证→清理，规避 Temp 跨会话被清空的坑
- 绝不拿真实生产数据试恢复；冲突文件只报不改

## 3. gen_avatars.py — 团队头像离线生成器

为团长 + 8 位专家生成 512×512 头像（纯本地 PIL，零积分）。

```bash
python scripts/gen_avatars.py
```

## 4. wb_safe_security_test.py — 安全稳定性实测

对包结构与八条防线逐维打分（0–5），输出 `security_results.json` 供雷达图使用。

```bash
python scripts/wb_safe_security_test.py [包目录] [输出目录]
```

红线：不读取任何真实密钥内容，只检查机制存在性；不发起网络请求；结果只描述行为表现，不披露实现细节。
