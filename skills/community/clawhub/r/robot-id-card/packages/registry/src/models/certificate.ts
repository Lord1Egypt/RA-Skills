import { z } from 'zod'

export const GradeSchema = z.enum(['unknown', 'healthy', 'dangerous'])
export type Grade = z.infer<typeof GradeSchema>

export const BotCapabilitySchema = z.enum([
  'read_articles',
  'read_images',
  'follow_links',
  'view_threads',
  'react',
  'post_content',
  'direct_chat',
])

export const RICCertificateSchema = z.object({
  ric_version: z.literal('1.0'),
  id: z.string().startsWith('ric_'),
  created_at: z.string().datetime(),
  developer: z.object({
    name: z.string().min(1),
    email: z.string().email(),
    org: z.string().optional(),
    website: z.string().url().optional(),
    verified: z.boolean().default(false),
  }),
  bot: z.object({
    name: z.string().min(1).max(64),
    version: z.string(),
    purpose: z.string().min(10).max(500),
    capabilities: z.array(BotCapabilitySchema),
    user_agent: z.string(),
  }),
  grade: GradeSchema.default('unknown'),
  grade_updated_at: z.string().datetime(),
  public_key: z.string().startsWith('ed25519:'),
  signature: z.string(),
})

export type RICCertificate = z.infer<typeof RICCertificateSchema>

/**
 * Permission level based on grade and bot capabilities.
 * Level 0 = blocked, Level 5 = full trusted access
 */
export function getPermissionLevel(cert: RICCertificate): number {
  if (cert.grade === 'dangerous') return 0

  const caps = cert.bot.capabilities
  if (cert.grade === 'unknown') return 1  // read-only

  // healthy bots get progressive levels
  if (caps.includes('direct_chat')) return 5
  if (caps.includes('post_content')) return 4
  if (caps.includes('react')) return 3
  if (caps.includes('view_threads')) return 2
  return 1
}

export const PERMISSION_LABELS: Record<number, string> = {
  0: 'Blocked',
  1: 'Read articles',
  2: 'View threads',
  3: 'Like / react',
  4: 'Post content',
  5: 'Direct chat',
}
