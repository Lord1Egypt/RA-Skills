export type Grade = 'healthy' | 'unknown' | 'dangerous'

export interface RICVerifyResult {
  valid: boolean
  id: string
  bot: { name: string; purpose: string }
  developer: { name: string; org?: string }
  grade: Grade
  permission_level: number  // 0-5
  permission_label: string
  error?: string
}

export interface RICPermissionRule {
  minGrade: Grade
  level: number
  /** Minimum age of bot registration in days before granting this level */
  minAgeDays?: number
}

export interface RICMiddlewareOptions {
  /** Registry API endpoint. Defaults to official registry. */
  registryUrl?: string
  /** Per-route permission rules */
  permissions?: Record<string, RICPermissionRule>
  /** Default rule when no specific route matches */
  defaultRule?: RICPermissionRule
  /** Called when a bot is detected (valid or not) */
  onBotDetected?: (result: RICVerifyResult, req: any) => void
  /** Cache TTL in seconds for certificate lookups. Default: 300 */
  cacheTtl?: number
}
