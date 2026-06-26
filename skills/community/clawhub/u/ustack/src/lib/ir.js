/**
 * uStack Intermediate Representation (IR)
 *
 * The IR is the normalized, runtime-agnostic description of an upstream
 * agent framework. It sits between the upstream import and the target adapters.
 *
 * Architecture:
 *   Upstream repo → IR extraction → IR schema → Target adapter → Adapted output
 *
 * The IR lets us add new upstreams and new targets independently.
 * Each upstream gets one extractor. Each target gets one renderer.
 * No pairwise adapters.
 */

/**
 * Build an empty IR workspace document.
 */
export function emptyIR(upstreamId) {
  return {
    schema: 'ustack-ir/v1',
    upstreamId,
    extractedAt: new Date().toISOString(),

    // Workspace-level metadata
    workspace: {
      name: '',
      description: '',
      category: '',           // e.g. workflow-skill-framework, skill-library, agent-workspace
      hostConventions: [],    // original host(s): claude-code, codex, etc.
      license: '',
      repoUrl: '',
    },

    // Skills: the core slash-command / invocable units
    skills: [],

    // Workflow graph: how skills connect
    workflow: {
      stages: [],             // e.g. think, plan, build, review, test, ship, reflect
      edges: [],              // { from, to, artifact } — what flows between stages
    },

    // Artifacts: named documents that flow between skills
    artifacts: [],

    // Tooling services: long-running daemons or binaries
    services: [],

    // Install model: how the framework is installed
    install: {
      methods: [],            // { id, description, targetPath, steps }
      bootstrapCommand: '',
      perRepoSupported: false,
      userGlobalSupported: false,
    },

    // Compatibility notes
    compatibility: {
      portableComponents: [],
      needsAdaptation: [],
      hostSpecific: [],
      notes: '',
    },
  };
}

/**
 * IR Skill schema:
 * {
 *   id: string,               // e.g. 'review'
 *   name: string,             // human name, e.g. 'Staff Engineer Review'
 *   trigger: string,          // e.g. '/review'
 *   category: string,         // workflow | power-tool | safety | browser | memory
 *   description: string,
 *   purpose: string,
 *   requiredTools: string[],  // e.g. ['browser', 'git']
 *   safetyLevel: string,      // safe | caution | destructive
 *   upstreamArtifacts: string[],  // artifacts consumed
 *   downstreamArtifacts: string[], // artifacts produced
 *   hostNotes: {              // host-specific implementation notes
 *     [hostId]: string
 *   },
 *   portability: string,      // portable | needs-adaptation | host-specific
 *   sourceFile: string,       // relative path in upstream repo
 * }
 */
export function emptySkill(id) {
  return {
    id,
    name: '',
    trigger: `/${id}`,
    category: 'workflow',
    description: '',
    purpose: '',
    requiredTools: [],
    safetyLevel: 'safe',
    upstreamArtifacts: [],
    downstreamArtifacts: [],
    hostNotes: {},
    portability: 'portable',
    sourceFile: '',
  };
}

/**
 * IR Artifact schema:
 * {
 *   id: string,
 *   name: string,
 *   description: string,
 *   format: string,           // markdown | json | yaml | text
 *   producedBy: string[],     // skill ids
 *   consumedBy: string[],     // skill ids
 *   typicalPath: string,      // e.g. 'DESIGN.md', '.claude/design-doc.md'
 * }
 */
export function emptyArtifact(id) {
  return {
    id,
    name: '',
    description: '',
    format: 'markdown',
    producedBy: [],
    consumedBy: [],
    typicalPath: '',
  };
}

/**
 * IR Service schema:
 * {
 *   id: string,
 *   name: string,
 *   description: string,
 *   type: string,             // daemon | binary | script
 *   startCommand: string,
 *   stateFile: string,
 *   protocol: string,         // http | stdio | none
 *   portRange: string,        // e.g. '10000-60000'
 *   auth: string,             // bearer-token | none
 *   hostSpecific: boolean,
 * }
 */
export function emptyService(id) {
  return {
    id,
    name: '',
    description: '',
    type: 'daemon',
    startCommand: '',
    stateFile: '',
    protocol: 'none',
    portRange: '',
    auth: 'none',
    hostSpecific: false,
  };
}

/**
 * Validate an IR document. Returns { valid, errors }.
 */
export function validateIR(ir) {
  const errors = [];

  if (ir.schema !== 'ustack-ir/v1') errors.push('schema must be ustack-ir/v1');
  if (!ir.upstreamId) errors.push('upstreamId is required');
  if (!Array.isArray(ir.skills)) errors.push('skills must be an array');
  if (!Array.isArray(ir.artifacts)) errors.push('artifacts must be an array');
  if (!Array.isArray(ir.services)) errors.push('services must be an array');

  for (const skill of (ir.skills || [])) {
    if (!skill.id) errors.push(`skill missing id: ${JSON.stringify(skill)}`);
    if (!['portable', 'needs-adaptation', 'host-specific'].includes(skill.portability)) {
      errors.push(`skill ${skill.id}: invalid portability value "${skill.portability}"`);
    }
    if (!['workflow', 'power-tool', 'safety', 'browser', 'memory', 'update'].includes(skill.category)) {
      errors.push(`skill ${skill.id}: invalid category "${skill.category}"`);
    }
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Merge a partial IR update into an existing IR document.
 * Skills and artifacts are merged by id (upsert).
 */
export function mergeIR(base, patch) {
  const result = { ...base, ...patch };

  // Merge skills by id
  const skillMap = new Map((base.skills || []).map(s => [s.id, s]));
  for (const s of (patch.skills || [])) {
    skillMap.set(s.id, { ...(skillMap.get(s.id) || {}), ...s });
  }
  result.skills = Array.from(skillMap.values());

  // Merge artifacts by id
  const artifactMap = new Map((base.artifacts || []).map(a => [a.id, a]));
  for (const a of (patch.artifacts || [])) {
    artifactMap.set(a.id, { ...(artifactMap.get(a.id) || {}), ...a });
  }
  result.artifacts = Array.from(artifactMap.values());

  // Merge services by id
  const serviceMap = new Map((base.services || []).map(sv => [sv.id, sv]));
  for (const sv of (patch.services || [])) {
    serviceMap.set(sv.id, { ...(serviceMap.get(sv.id) || {}), ...sv });
  }
  result.services = Array.from(serviceMap.values());

  return result;
}
