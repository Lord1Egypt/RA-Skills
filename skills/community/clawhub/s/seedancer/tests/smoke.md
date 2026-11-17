# 冒烟测试（seedancer）

```bash
# 一致性检查器（零依赖，v5 = 19 项断言；逐步状态 `[RUN ]` 打到 stderr）
python scripts/check_consistency.py
exit=0  # 实测：19 项全绿（0 FAIL / 0 WARN）
```

```bash
# 检查器攻击测试（在临时副本上变异；必拦场景 + 显式已知漏检）
python tests/attack_test.py
exit=0  # 实测：全部必拦场景被拦住、0 漏网；真实目录未被触碰
```

```bash
# 提示词助手（模板输出，仅验证可执行）
bash SKILL.sh "10s 9:16 cyberpunk rain night street"
exit=0
```

记录：见父仓库 `generated/seedancer_consistency_s*.out`；
G1 红/绿证据见 `generated/attack_red.txt`、`generated/green_check.txt`。
