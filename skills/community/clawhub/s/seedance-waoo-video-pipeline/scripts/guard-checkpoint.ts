export type GuardCheckpoint = {
  stage: 'panel-guard' | 'merge-guard'
  status: 'pass' | 'stop' | 'confirm'
  summary: string
  reasons: string[]
  nextStep: string
}

export function buildGuardCheckpoint(stage: GuardCheckpoint['stage'], errors: string[], warnings: string[]): GuardCheckpoint {
  if (errors.length > 0) {
    return {
      stage,
      status: 'stop',
      summary: stage === 'panel-guard' ? '当前 panel 目标存在硬冲突，已停止继续生成。' : '当前 merge 顺序存在硬冲突，已停止继续导出。',
      reasons: errors,
      nextStep: stage === 'panel-guard' ? '先修正 panelId / panelIndex / 图文归属，再继续生成。' : '先修正 merge 输入顺序/重复项，再继续导出。',
    }
  }

  if (warnings.length > 0) {
    return {
      stage,
      status: 'confirm',
      summary: stage === 'panel-guard' ? '当前 panel 可继续，但有风险，建议先人工确认。' : '当前 merge 可继续，但有顺序风险，建议先人工确认。',
      reasons: warnings,
      nextStep: stage === 'panel-guard' ? '确认首图、字幕、prompt 是否都属于同一 panel。' : '确认 panelIndex 顺序是否允许跳过或 selective cut。',
    }
  }

  return {
    stage,
    status: 'pass',
    summary: stage === 'panel-guard' ? 'panel guard 已通过，可继续正式生成。' : 'merge guard 已通过，可继续正式导出。',
    reasons: [],
    nextStep: stage === 'panel-guard' ? '继续提交官方视频任务。' : '继续执行 merge/export。',
  }
}
