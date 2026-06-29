import { UIReplicationPrompt } from "./prompt"

export class UIReplicationPipeline {
  static run(input: {
    pagePath: string
    steps?: string[]
    screenshots?: string[]
  }) {
    return {
      prompt: UIReplicationPrompt,
      context: {
        pagePath: input.pagePath,
        steps: input.steps || [],
        screenshots: input.screenshots || []
      }
    }
  }
}