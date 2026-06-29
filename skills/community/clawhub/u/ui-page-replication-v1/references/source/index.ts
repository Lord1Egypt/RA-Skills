import { UIReplicationSkillConfig } from "./config"
import { UIReplicationPipeline } from "./pipeline"

export const UIReplicationSkill = {
  config: UIReplicationSkillConfig,

  match(input: string) {
    return this.config.triggers.some(trigger =>
      input.includes(trigger)
    )
  },

  execute(input: {
    pagePath: string
    steps?: string[]
    screenshots?: string[]
  }) {
    return UIReplicationPipeline.run(input)
  }
}