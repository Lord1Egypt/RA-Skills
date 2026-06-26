import { defineConfig } from 'skelm'
// import { createPiSdkBackend } from '@skelm/pi'

export default defineConfig({
  // Backend selectors and definitions. The CLI wires these by id automatically:
  //   openai, anthropic, opencode, copilot-acp, acp, pi (RPC variant)
  // Use `instances:` (below) for the pi SDK backend or any custom backend.
  backends: {
    default: 'openai', // used by llm() and agent() unless overridden
    // llm:    'openai',
    // agent:  'pi',
    // openai: {
    //   baseUrl: 'https://api.openai.com/v1',  // or any OpenAI-compatible URL
    //   apiKey:  { secret: 'OPENAI_API_KEY' },
    //   model:   'gpt-4o-mini',
    // },
  },

  // Pre-built backend instances. Useful for the pi SDK backend (which the
  // string-keyed `backends:` form does not wire up) or custom backends.
  instances: [
    // createPiSdkBackend({ id: 'pi' }),
  ],

  // Workflow discovery.
  pipelines: { discovery: 'auto', glob: 'workflows/**/*.workflow.ts' },

  registries: {
    workflows: { glob: 'workflows/**/*.workflow.ts' },
    skills: { glob: 'skills/**/SKILL.md' },

    // MCP servers the gateway hosts; steps reference them by id.
    mcpServers: [
      // { id: 'github',     transport: 'http',  url: 'http://127.0.0.1:9100' },
      // { id: 'filesystem', transport: 'stdio', command: 'mcp-server-filesystem', args: ['.'] },
    ],

    // Gateway-supervised agents (lifecycle/command/env). Optional — only
    // needed when the gateway should manage the agent process itself.
    agents: [
      // { id: 'claude-code', runtime: 'claude-code', lifecycle: 'ephemeral',
      //   command: 'claude', args: ['--print'] },
    ],
  },

  defaults: {
    // Project-wide permission baseline. Step-level permissions intersect with these.
    permissions: {
      allowedExecutables: [],
      allowedTools: [],
      allowedSkills: [],
      allowedMcpServers: [],
      fsRead: ['./'],
      fsWrite: [],
      networkEgress: 'deny',
    },

    // Named profiles steps can apply via permissions: { profile: '...' }
    permissionProfiles: {
      // 'read-only': {
      //   fsRead: ['./'],
      //   networkEgress: 'deny',
      // },
      // 'github-write': {
      //   allowedExecutables: ['git'],
      //   allowedTools: ['gh.*'],
      //   allowedMcpServers: ['github'],
      //   fsRead: ['./'],
      //   fsWrite: ['./'],
      //   networkEgress: { allowHosts: ['api.github.com'] },
      // },
    },
  },

  secrets: { driver: 'env' },

  storage: {
    runs: { driver: 'sqlite', path: '.skelm/runs.sqlite' },
    state: { driver: 'sqlite', path: '.skelm/state.sqlite' },
  },

  server: {
    port: 14738, // skelm gateway port
    host: '127.0.0.1',
    auth: { mode: 'none' }, // set to 'bearer' with an env-resolved token for remote access
  },
})
