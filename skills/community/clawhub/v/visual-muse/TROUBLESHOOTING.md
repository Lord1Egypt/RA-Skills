# Visual Muse 踩坑指南

## 问题1：生成图片全黑（5KB或更小）

**根因**：SDXL的VAE在fp16精度下有bug，MPS设备尤其严重。

**修复**：启动ComfyUI时加 `--fp32-vae`：
```bash
python main.py --listen 0.0.0.0 --port 8188 --highvram --fp32-vae
```
⚠️ 参数是 `--fp32-vae`，不是 `--force-fp32-vae`（后者不存在会报错）。

如果仍有黑图，额外下载修复版VAE：
```bash
curl -L -o models/vae/sdxl_vae_fp16fix.safetensors \
  "https://hf-mirror.com/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors"
```

## 问题2：Agent不按SKILL.md执行，自己写Python脚本

**根因**：模型工具调用能力不足（DeepSeek等常见），Skill过于复杂时模型会绕过。

**修复**：
1. 精简Skill为单轮调用，封装成一个bash脚本
2. SKILL.md明确写"禁止自己写Python脚本"
3. 使用Claude Sonnet替代DeepSeek处理出图任务

| 指标 | DeepSeek自写脚本 | Claude按Skill走 |
|------|-----------------|----------------|
| 黑图率 | ~75% | 0% |
| 耗时 | 30-45分钟 | 1-2分钟 |
| Skill遵守 | 否 | 是 |

## 问题3：Token消耗过高

**根因**：无contextTokens限制 + safeguard压缩模式 + workspace大文件注入。

**修复**：
```bash
openclaw config set agents.defaults.contextTokens 32000
openclaw config set agents.defaults.compaction.mode default
openclaw config set agents.defaults.compaction.reserveTokens 4000
openclaw config set tools.profile messaging
```
⚠️ 字段名是 `contextTokens` 不是 `maxContextTokens`。`compaction.mode` 只支持 `default` 和 `safeguard`，不支持 `full`。

清理workspace和session：
```bash
mkdir -p ~/.openclaw/workspace/archive
mv ~/.openclaw/workspace/*.log ~/.openclaw/workspace/archive/ 2>/dev/null
cp -r ~/.openclaw/agents/main/sessions ~/.openclaw/agents/main/sessions.bak
rm -rf ~/.openclaw/agents/main/sessions/*
docker restart openclaw-gateway
```

优化效果：从$0.37/次降到$0.07/次（出图），$0.003/次（聊天）。

## 问题4：LanceDB记忆系统崩溃

**症状**：`Cannot find module '@lancedb/lancedb'`

**临时修复**：
```bash
docker exec openclaw-gateway npm install @lancedb/lancedb
docker restart openclaw-gateway
```
ARM Docker容器下会反复出现，建议长期切换到MEMORY.md文件记忆。

## 问题5：图片在容器内找不到

**临时方案**：
```bash
docker cp openclaw-gateway:/home/node/ai-outputs/ ~/ai-studio/outputs/latest/
```

**永久方案**：docker-compose添加映射：
```yaml
volumes:
  - ${HOME}/ai-studio/outputs:/home/node/ai-outputs
```

## 问题6：Impact Pack未加载

**修复**：
```bash
source ~/ai-studio/comfyui-venv/bin/activate
cd ~/ai-studio/comfyui/custom_nodes/ComfyUI-Impact-Pack
pip install -r requirements.txt
python install.py
```

## 推荐模型配置

| 场景 | 模型 | 成本 |
|------|------|------|
| 出图+复杂任务 | Claude Sonnet 4.6 | ~$0.07/次 |
| 日常聊天 | DeepSeek V3.2 | ~$0.001/次 |
| 分析任务 | Claude Haiku 4.5 | ~$0.01/次 |

通过Ofox等API聚合平台接入Claude，避免封号风险。

## 问题8：Agent说"我没有生成图像的能力"（SOUL.md优先级问题）

**现象**：明明 agentDir 里的 SOUL.md 写了出图指令，但 agent 说"我是文字/代码型 AI，不是画图工具"，推荐用户去 Midjourney。

**根因**：OpenClaw 给每个 agent 自动创建 `workspace-{agentId}/` 目录，里面的 SOUL.md **优先级高于** agentDir 里的。如果 workspace-painter/SOUL.md 是通用人格模板，agent 就不知道自己是画师。

**诊断方法**：
```bash
# 看 agent 实际读取的是哪个 SOUL.md
docker exec openclaw-gateway cat /home/node/.openclaw/workspace-painter/SOUL.md
# 对比 agentDir 里的
docker exec openclaw-gateway cat /home/node/.openclaw/agents/painter/agent/SOUL.md
```

**修复**：
```bash
# 用正确的 SOUL.md 覆盖 workspace 里的
cp /home/node/.openclaw/agents/painter/agent/SOUL.md \
   /home/node/.openclaw/workspace-painter/SOUL.md
# 清理垃圾文件
rm -f /home/node/.openclaw/workspace-painter/*.svg
rm -f /home/node/.openclaw/workspace-painter/*.py
rm -f /home/node/.openclaw/workspace-painter/cyberpunk_cat.*
docker restart openclaw-gateway
```

⚠️ **重要**：以后修改 SOUL.md 必须同时更新两个位置（agentDir 和 workspace-painter），否则改了等于没改。

## 问题9：Agent连续生成不停（Gemini等模型）

**现象**：让画一张图，agent 生成完后自动继续生成变体，停不下来。

**根因**：部分模型（如Gemini）倾向于"主动服务"，把"画一张"理解成"画到满意为止"。

**修复**：在 SOUL.md 末尾添加数量规则：
```
## 数量规则（严格遵守）
- 默认只生成1张图，生成完立即停止
- 不要自动生成变体
- 只有用户明确说「再来一张」「多几张」时才生成更多
```

## 问题10：模型切换后出图失败

**现象**：切换模型后 agent 行为异常，不调用 paint-dispatch.sh。

**修复**：
```bash
# 切换模型一行命令
bash ~/openclaw/switch-painter-model.sh gemini    # 便宜
bash ~/openclaw/switch-painter-model.sh claude     # 最强
bash ~/openclaw/switch-painter-model.sh gpt-nano   # 最便宜

# 如果新模型不听话，切回 Claude
bash ~/openclaw/switch-painter-model.sh claude
```
