# image-review

用户说评价、改进、优化图片时触发。

## 流程

### Step 1: 检查最近图片
```bash
ls -lt /home/node/ai-outputs/ | head -5
```

### Step 2: 评估（5分制）
构图、色彩、细节、风格一致性、整体印象。

### Step 3: 改进建议
评分<3.5时建议：prompt调整、换checkpoint、用hires workflow。

### Step 4: 记录
```bash
python /home/node/.openclaw/workspace/tools/run-tracker.py --log "评估摘要"
```
