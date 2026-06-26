import { agent, code, pipeline } from 'skelm'
import { z } from 'zod'

// Requires skelm.config.ts with the agent backend declared under `backends`
// (or pre-built and registered via `instances`), and any MCP server under
// `registries.mcpServers` if used. See references/config.md for the full shape.

export default pipeline({
  id: '{{ID}}',
  description: '{{DESCRIPTION}}',
  input: z.object({
    // TODO: declare input fields
    task: z.string().min(1),
  }),
  output: z.object({
    // TODO: declare output fields
    result: z.string(),
  }),
  steps: [
    code({
      id: 'prepare',
      run: (ctx) => {
        const { task } = ctx.input as { task: string }
        return { prompt: `Complete the following task: ${task}` }
      },
    }),
    agent({
      id: 'execute',
      // backend: 'pi',  // uncomment and set to your backend id (recommended: pi SDK)
      prompt: (ctx) => (ctx.steps.prepare as { prompt: string }).prompt,
      permissions: {
        // profile: 'my-profile',   // optional: named profile from skelm.config.ts
        // Declare only what the agent actually needs; everything else stays denied.
        allowedTools: [], // e.g. ['gh.*'] or ['bash', 'rg']
        allowedExecutables: [], // e.g. ['git', 'node']
        allowedMcpServers: [], // ids from skelm.config.ts registries.mcpServers
        allowedSkills: [], // skill ids the agent may load
        fsRead: ['./'], // path roots agent may read
        fsWrite: [], // path roots agent may write
        networkEgress: 'deny', // 'allow' | 'deny' | { allowHosts: [...] }
      },
      workspace: {
        mode: 'ephemeral',
        seed: { copy: [] }, // e.g. ['./src/', './package.json']
        cleanup: 'on-run-end',
      },
      output: z.object({ result: z.string() }),
    }),
  ],
  finalize: (ctx) => {
    return ctx.steps.execute as { result: string }
  },
})
