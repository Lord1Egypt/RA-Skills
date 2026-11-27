# 子技能 10 · 循环修复 repair_log
**来源**：ai-short-drama-from-zero（定位真实的上游原因，修完整个受影响的产物，不在下游打补丁），video-use（问题修复后重新渲染，最多 3 次），claude-video-studio（开工前就约定好打磨上限），drama-skills（上游改了以后重跑跨文档检查）。

## 目标
用最少的重做把分数拉上来，并且知道什么时候该停。

## 方法
1. **排序**：把 issues 按 root_stage 在流水线里的顺序排，**从最上游开始修**。修好上游往往会顺带解决下游的问题。
2. **每一轮**：
   1. 读取 root_stage 对应的子技能，修改**整个**受影响的产物，不只改报错的那一条
   2. 跑这个阶段的校验，通过后 stamp
   3. 跑 `uvd_validate.py stale project/`，拿到所有失效的下游阶段，按顺序重做。只重做受影响的 cut 和任务，其他的保留
   4. 重新渲染，重新评审，产出新的 qa_report（round+1）
   5. 在 repair_log 里追加一轮：issue_ids、stage_redone、invalidated、score_before、score_after、result
3. **回滚**：result=regressed（分数下降）时，回退到上一版的产物，换一种修法。
4. **终止**：pass=true，或者轮数达到 max_repair_rounds。到上限时，交付分数最高的那一版，并列出剩下的问题，问用户要不要继续。
5. **成本意识**：要重新生成素材的修复，也要走 07 的预览确认流程。

## 常见错误码
OVER_ROUNDS、REGRESSED（WARNING）
