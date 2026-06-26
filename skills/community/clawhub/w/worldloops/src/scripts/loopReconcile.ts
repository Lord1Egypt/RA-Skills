import { loadOpenLoopStates, transitionOpenLoopState } from '../storage/openLoopStates';
import { evaluateStuckLoop, getDefaultStuckLoopPolicyConfig } from '../policy/stuckLoopPolicy';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function main(): void {
  const nowIso = new Date().toISOString();
  const loops = loadOpenLoopStates();
  const transitions = [];

  for (const loop of loops) {
    const evaluation = evaluateStuckLoop(loop, nowIso);

    if (!evaluation.shouldTransition) {
      continue;
    }

    const updated = transitionOpenLoopState(loop.id, evaluation.to, {
      actor: 'worldloops.local',
      note: evaluation.note,
    });

    transitions.push({
      id: loop.id,
      canonicalKey: loop.canonicalKey,
      from: evaluation.from,
      to: evaluation.to,
      reason: evaluation.reason,
      note: evaluation.note,
      updatedAt: updated.updatedAt,
    });
  }

  printJson({
    ok: true,
    source: 'worldloops.local',
    checkedAt: nowIso,
    policy: getDefaultStuckLoopPolicyConfig(),
    loopsChecked: loops.length,
    transitionsApplied: transitions.length,
    transitions,
    capabilityBoundary: getCapabilityBoundary(),
    safety: { externalWrite: false },
  });
}

main();
