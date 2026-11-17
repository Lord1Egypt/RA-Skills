// TaskFlow orchestration shape for the publish flow.
// Illustrative: bind via api.runtime.tasks.flow.fromToolContext(ctx).

const flow = api.runtime.tasks.flow.fromToolContext(ctx);
const created = flow.createManaged({
  controllerId: "taskflow-clawhub-publish",
  goal: "validate, publish, and verify a skill on ClawHub",
  currentStep: "validate",
  stateJson: { skillFolder, slug, name, version, changelog, validated: false },
});

const validate = flow.runTask({
  flowId: created.flowId,
  runtime: "acp",
  childSessionKey: "agent:main:subagent:publish-validate",
  runId: `${created.flowId}-validate`,
  task: `clawhub publish ${skillFolder} --slug ${slug} --dry-run --json`,
  status: "running",
  startedAt: Date.now(),
  lastEventAt: Date.now(),
});

// On success: setWaiting or proceed; carry expectedRevision forward.
const publish = flow.runTask({
  flowId: created.flowId,
  runtime: "acp",
  childSessionKey: "agent:main:subagent:publish-write",
  runId: `${created.flowId}-publish`,
  task: `clawhub publish ${skillFolder} --slug ${slug} --name ${name} --version ${version} --changelog ${changelog} --json`,
  status: "running",
  startedAt: Date.now(),
  lastEventAt: Date.now(),
});

flow.finish({
  flowId: created.flowId,
  expectedRevision: publish.revision ?? created.revision,
  stateJson: { ...created.stateJson, validated: true, publishedVersion: version },
});
