import { code, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: '{{ID}}',
  description: '{{DESCRIPTION}}',
  input: z.object({
    // TODO: declare input fields
    value: z.string(),
  }),
  output: z.object({
    // TODO: declare output fields
    result: z.string(),
  }),
  steps: [
    code({
      id: 'process',
      run: (ctx) => {
        const { value } = ctx.input as { value: string }
        // TODO: implement
        return { result: value }
      },
    }),
  ],
})
