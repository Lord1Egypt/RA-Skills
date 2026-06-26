import { db } from './db.js'
import { nanoid } from 'nanoid'

export interface AuditEntry {
  id: string
  ric_id: string
  event: string
  old_grade?: string
  new_grade?: string
  reason?: string
  reporter?: string
  description?: string
  timestamp: string
}

const stmts = {
  insert: db.prepare(`
    INSERT INTO audit_log (id, ric_id, event, old_grade, new_grade, reason, reporter, description, timestamp)
    VALUES (@id, @ric_id, @event, @old_grade, @new_grade, @reason, @reporter, @description, @timestamp)
  `),

  findByRicId: db.prepare(`
    SELECT * FROM audit_log WHERE ric_id = ? ORDER BY timestamp DESC
  `),
}

export const auditStore = {
  append(entry: Omit<AuditEntry, 'id' | 'timestamp'>): AuditEntry {
    const full: AuditEntry = {
      id: `evt_${nanoid(12)}`,
      timestamp: new Date().toISOString(),
      ...entry,
    }
    stmts.insert.run({
      id: full.id,
      ric_id: full.ric_id,
      event: full.event,
      old_grade: full.old_grade ?? null,
      new_grade: full.new_grade ?? null,
      reason: full.reason ?? null,
      reporter: full.reporter ?? null,
      description: full.description ?? null,
      timestamp: full.timestamp,
    })
    return full
  },

  findByRicId(ric_id: string): AuditEntry[] {
    return stmts.findByRicId.all(ric_id) as AuditEntry[]
  },
}
