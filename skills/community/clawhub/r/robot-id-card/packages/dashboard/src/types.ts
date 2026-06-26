export type Grade = 'unknown' | 'healthy' | 'dangerous'

export interface BotSummary {
  id: string
  name: string
  purpose: string
  grade: Grade
  developer_org: string
  created_at: string
}

export interface BotDetail {
  ric_version: string
  id: string
  created_at: string
  grade: Grade
  grade_updated_at: string
  public_key: string
  developer: {
    name: string
    email: string
    org?: string
    website?: string
    verified: boolean
  }
  bot: {
    name: string
    version: string
    purpose: string
    capabilities: string[]
    user_agent: string
  }
}
