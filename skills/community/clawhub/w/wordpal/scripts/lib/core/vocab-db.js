const fs = require('fs');
const os = require('os');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const DEFAULT_WORKSPACE_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'wordpal');
const DB_FILENAME = 'vocab.db';
const BUSY_TIMEOUT_MS = 5000;
const SCHEMA_VERSION = 2;

const WORD_COLUMNS = `
  word,
  status,
  first_learned,
  last_reviewed,
  next_review,
  mastered_date,
  srs_due,
  srs_stability,
  srs_difficulty,
  srs_reps,
  srs_lapses,
  srs_state,
  last_op_id,
  created_at,
  updated_at
`;

const PENDING_COLUMNS = `
  word,
  created_at,
  last_op_id
`;

const EVENT_COLUMNS = `
  id,
  op_id,
  word,
  event,
  previous_status,
  next_status,
  study_date,
  result_due,
  result_srs_state,
  created_at
`;

const PROBLEM_WORD_COLUMNS = `
  e.word AS word,
  SUM(CASE WHEN e.event = 'wrong' THEN 1 ELSE 0 END) AS wrong_count,
  SUM(CASE WHEN e.event = 'remembered_after_hint' THEN 1 ELSE 0 END) AS remembered_after_hint_count,
  COUNT(*) AS problematic_count,
  w.status AS current_status,
  w.last_reviewed AS last_reviewed
`;

const USER_PROFILE_COLUMNS = `
  profile_id,
  created,
  learning_goal,
  push_times,
  difficulty_level,
  daily_target,
  updated_at
`;

const RISK_COLUMNS = `
  word,
  status,
  last_reviewed,
  next_review,
  srs_stability,
  srs_difficulty,
  srs_reps,
  srs_lapses,
  srs_state,
  overdue_days
`;

function ensureWorkspaceDir(workspaceDir) {
  fs.mkdirSync(workspaceDir, { recursive: true });
}

function getDbPath(workspaceDir = DEFAULT_WORKSPACE_DIR) {
  return path.join(workspaceDir, DB_FILENAME);
}

function initializeDatabase(db) {
  db.exec(`PRAGMA journal_mode = WAL;`);
  db.exec(`PRAGMA foreign_keys = ON;`);
  db.exec(`PRAGMA busy_timeout = ${BUSY_TIMEOUT_MS};`);

  const { user_version: currentVersion } = db.prepare('PRAGMA user_version').get();

  if (currentVersion < 1) {
    db.exec(`
      CREATE TABLE IF NOT EXISTS words (
        word TEXT PRIMARY KEY,
        status INTEGER NOT NULL CHECK (status BETWEEN 1 AND 8),
        first_learned TEXT NOT NULL,
        last_reviewed TEXT,
        next_review TEXT,
        mastered_date TEXT,
        srs_due TEXT,
        srs_stability REAL,
        srs_difficulty REAL,
        srs_reps INTEGER NOT NULL DEFAULT 0,
        srs_lapses INTEGER NOT NULL DEFAULT 0,
        srs_state TEXT NOT NULL,
        last_op_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS word_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        op_id TEXT NOT NULL UNIQUE,
        word TEXT NOT NULL,
        event TEXT NOT NULL,
        previous_status INTEGER,
        next_status INTEGER NOT NULL,
        study_date TEXT NOT NULL,
        result_due TEXT,
        result_srs_state TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (word) REFERENCES words(word) ON DELETE CASCADE
      );

      CREATE TABLE IF NOT EXISTS pending_words (
        word TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        last_op_id TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS user_profile (
        profile_id INTEGER PRIMARY KEY CHECK (profile_id = 1),
        created TEXT,
        learning_goal TEXT NOT NULL,
        push_times TEXT NOT NULL,
        difficulty_level TEXT NOT NULL,
        daily_target INTEGER NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE INDEX IF NOT EXISTS idx_words_status_due
        ON words(status, next_review, word);
      CREATE INDEX IF NOT EXISTS idx_words_last_reviewed
        ON words(last_reviewed);
      CREATE INDEX IF NOT EXISTS idx_word_events_study_date
        ON word_events(study_date);
      CREATE INDEX IF NOT EXISTS idx_word_events_word_date
        ON word_events(word, study_date);
      CREATE INDEX IF NOT EXISTS idx_pending_words_created_at
        ON pending_words(created_at, word);
    `);
    db.exec(`PRAGMA user_version = 1`);
  }

  if (currentVersion < 2) {
    db.exec(`
      CREATE TABLE IF NOT EXISTS hint_tokens (
        token TEXT PRIMARY KEY,
        word TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
    `);
    db.exec(`PRAGMA user_version = 2`);
  }
}

function openDatabase(workspaceDir = DEFAULT_WORKSPACE_DIR) {
  ensureWorkspaceDir(workspaceDir);
  const db = new DatabaseSync(getDbPath(workspaceDir));
  initializeDatabase(db);
  return db;
}

function buildSrsFromRow(row) {
  const hasSrs = (
    row.srs_state !== null
    || row.srs_due !== null
    || row.srs_stability !== null
    || row.srs_difficulty !== null
    || row.srs_reps !== null
    || row.srs_lapses !== null
  );
  if (!hasSrs) return null;

  return {
    due: row.srs_due ?? null,
    stability: row.srs_stability ?? null,
    difficulty: row.srs_difficulty ?? null,
    reps: row.srs_reps ?? null,
    lapses: row.srs_lapses ?? null,
    state: row.srs_state ?? null,
  };
}

function rowToWordEntry(row) {
  if (!row) return null;
  return {
    word: row.word,
    status: row.status,
    firstLearned: row.first_learned,
    lastReviewed: row.last_reviewed ?? 'never',
    nextReview: row.next_review ?? null,
    masteredDate: row.mastered_date ?? null,
    lastOpId: row.last_op_id,
    srs: buildSrsFromRow(row),
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function rowToPendingEntry(row) {
  if (!row) return null;
  return {
    word: row.word,
    createdAt: row.created_at,
    lastOpId: row.last_op_id,
  };
}

function rowToEventEntry(row) {
  if (!row) return null;
  return {
    id: row.id,
    opId: row.op_id,
    word: row.word,
    event: row.event,
    previousStatus: row.previous_status,
    nextStatus: row.next_status,
    studyDate: row.study_date,
    resultDue: row.result_due ?? null,
    resultSrsState: row.result_srs_state ?? null,
    createdAt: row.created_at,
  };
}

function rowToUserProfileEntry(row) {
  if (!row) return null;
  return {
    profileId: row.profile_id,
    created: row.created ?? null,
    learningGoal: row.learning_goal,
    pushTimes: row.push_times,
    difficultyLevel: row.difficulty_level,
    dailyTarget: row.daily_target,
    updatedAt: row.updated_at,
  };
}

function rowToRiskEntry(row) {
  if (!row) return null;
  return {
    word: row.word,
    status: row.status,
    lastReviewed: row.last_reviewed ?? 'never',
    nextReview: row.next_review ?? null,
    overdueDays: Number.isInteger(row.overdue_days)
      ? row.overdue_days
      : Math.max(0, Math.floor(Number(row.overdue_days) || 0)),
    srs: {
      due: row.next_review ?? null,
      stability: row.srs_stability ?? null,
      difficulty: row.srs_difficulty ?? null,
      reps: row.srs_reps ?? null,
      lapses: row.srs_lapses ?? null,
      state: row.srs_state ?? null,
    },
  };
}

function normalizeWordRecord(record) {
  const isMastered = record.status === 8;
  const rawNextReview = record.nextReview ?? null;
  const rawSrsDue = record.srs && record.srs.due ? record.srs.due : null;

  // P0-3: status=8 must have next_review=null, srs_due='9999-12-31'
  const next_review = isMastered ? null : rawNextReview;
  const srs_due = isMastered ? '9999-12-31' : rawSrsDue;

  // P0-2: enforce srs_due === next_review for non-mastered words
  const effectiveSrsDue = !isMastered && next_review && !srs_due ? next_review : srs_due;

  return {
    word: record.word,
    status: record.status,
    first_learned: record.firstLearned,
    last_reviewed: record.lastReviewed === 'never' ? null : (record.lastReviewed ?? null),
    next_review,
    mastered_date: record.masteredDate ?? null,
    srs_due: effectiveSrsDue,
    srs_stability: record.srs && record.srs.stability !== undefined ? record.srs.stability : null,
    srs_difficulty: record.srs && record.srs.difficulty !== undefined ? record.srs.difficulty : null,
    srs_reps: record.srs && Number.isInteger(record.srs.reps) ? record.srs.reps : 0,
    srs_lapses: record.srs && Number.isInteger(record.srs.lapses) ? record.srs.lapses : 0,
    srs_state: record.srs && record.srs.state ? record.srs.state : 'new',
    last_op_id: record.lastOpId,
    created_at: record.createdAt,
    updated_at: record.updatedAt,
  };
}

function normalizePendingRecord(record) {
  return {
    word: record.word,
    created_at: record.createdAt,
    last_op_id: record.lastOpId,
  };
}

function normalizeUserProfileRecord(record) {
  return {
    profile_id: 1,
    created: record.created ?? null,
    learning_goal: record.learningGoal,
    push_times: record.pushTimes,
    difficulty_level: record.difficultyLevel,
    daily_target: record.dailyTarget,
    updated_at: record.updatedAt,
  };
}

function mapCountRows(rows, dates) {
  const counts = Object.create(null);
  for (const date of dates) {
    counts[date] = 0;
  }
  for (const row of rows) {
    if (Object.prototype.hasOwnProperty.call(counts, row.date)) {
      counts[row.date] = Number(row.count) || 0;
    }
  }
  return dates.map((date) => ({ date, count: counts[date] }));
}

function createRepository(workspaceDir = DEFAULT_WORKSPACE_DIR) {
  const db = openDatabase(workspaceDir);
  const statements = {
    getWord: db.prepare(`SELECT ${WORD_COLUMNS} FROM words WHERE word = ?`),
    listWords: db.prepare(`SELECT ${WORD_COLUMNS} FROM words ORDER BY word`),
    getPendingWord: db.prepare(`SELECT ${PENDING_COLUMNS} FROM pending_words WHERE word = ?`),
    listPendingWords: db.prepare(`SELECT ${PENDING_COLUMNS} FROM pending_words ORDER BY created_at, word`),
    listPendingWordsLimited: db.prepare(`
      SELECT ${PENDING_COLUMNS}
      FROM pending_words
      ORDER BY created_at, word
      LIMIT ?
    `),
    listDueWords: db.prepare(`
      SELECT ${WORD_COLUMNS}
      FROM words
      WHERE status BETWEEN 1 AND 7
        AND last_reviewed IS NOT NULL
        AND next_review IS NOT NULL
        AND next_review <= ?
      ORDER BY
        CASE status
          WHEN 1 THEN 0
          WHEN 2 THEN 1
          WHEN 3 THEN 2
          ELSE 3
        END,
        next_review,
        word
    `),
    listDueWordsLimited: db.prepare(`
      SELECT ${WORD_COLUMNS}
      FROM words
      WHERE status BETWEEN 1 AND 7
        AND last_reviewed IS NOT NULL
        AND next_review IS NOT NULL
        AND next_review <= ?
      ORDER BY
        CASE status
          WHEN 1 THEN 0
          WHEN 2 THEN 1
          WHEN 3 THEN 2
          ELSE 3
        END,
        next_review,
        word
      LIMIT ?
    `),
    wordExists: db.prepare(`SELECT word, status FROM words WHERE word = ?`),
    countPendingWords: db.prepare(`SELECT COUNT(*) AS count FROM pending_words`),
    findEventByOpId: db.prepare(`SELECT op_id, word FROM word_events WHERE op_id = ?`),
    getUserProfile: db.prepare(`SELECT ${USER_PROFILE_COLUMNS} FROM user_profile WHERE profile_id = 1`),
    upsertWord: db.prepare(`
      INSERT INTO words (
        word,
        status,
        first_learned,
        last_reviewed,
        next_review,
        mastered_date,
        srs_due,
        srs_stability,
        srs_difficulty,
        srs_reps,
        srs_lapses,
        srs_state,
        last_op_id,
        created_at,
        updated_at
      ) VALUES (
        $word,
        $status,
        $first_learned,
        $last_reviewed,
        $next_review,
        $mastered_date,
        $srs_due,
        $srs_stability,
        $srs_difficulty,
        $srs_reps,
        $srs_lapses,
        $srs_state,
        $last_op_id,
        $created_at,
        $updated_at
      )
      ON CONFLICT(word) DO UPDATE SET
        status = excluded.status,
        first_learned = excluded.first_learned,
        last_reviewed = excluded.last_reviewed,
        next_review = excluded.next_review,
        mastered_date = excluded.mastered_date,
        srs_due = excluded.srs_due,
        srs_stability = excluded.srs_stability,
        srs_difficulty = excluded.srs_difficulty,
        srs_reps = excluded.srs_reps,
        srs_lapses = excluded.srs_lapses,
        srs_state = excluded.srs_state,
        last_op_id = excluded.last_op_id,
        updated_at = excluded.updated_at
    `),
    stagePendingWord: db.prepare(`
      INSERT INTO pending_words (
        word,
        created_at,
        last_op_id
      ) VALUES (
        $word,
        $created_at,
        $last_op_id
      )
      ON CONFLICT(word) DO NOTHING
    `),
    deletePendingWord: db.prepare(`DELETE FROM pending_words WHERE word = ?`),
    insertEvent: db.prepare(`
      INSERT INTO word_events (
        op_id,
        word,
        event,
        previous_status,
        next_status,
        study_date,
        result_due,
        result_srs_state,
        created_at
      ) VALUES (
        $op_id,
        $word,
        $event,
        $previous_status,
        $next_status,
        $study_date,
        $result_due,
        $result_srs_state,
        $created_at
      )
    `),
    upsertUserProfile: db.prepare(`
      INSERT INTO user_profile (
        profile_id,
        created,
        learning_goal,
        push_times,
        difficulty_level,
        daily_target,
        updated_at
      ) VALUES (
        $profile_id,
        $created,
        $learning_goal,
        $push_times,
        $difficulty_level,
        $daily_target,
        $updated_at
      )
      ON CONFLICT(profile_id) DO UPDATE SET
        created = excluded.created,
        learning_goal = excluded.learning_goal,
        push_times = excluded.push_times,
        difficulty_level = excluded.difficulty_level,
        daily_target = excluded.daily_target,
        updated_at = excluded.updated_at
    `),
    countWordsByStatus: db.prepare(`
      SELECT status, COUNT(*) AS count FROM words GROUP BY status
    `),
    countDueWords: db.prepare(`
      SELECT COUNT(*) AS count
      FROM words
      WHERE status BETWEEN 1 AND 7
        AND last_reviewed IS NOT NULL
        AND next_review IS NOT NULL
        AND next_review <= ?
    `),
    countDueByDateRange: db.prepare(`
      SELECT next_review AS date, COUNT(*) AS count
      FROM words
      WHERE status BETWEEN 1 AND 7
        AND last_reviewed IS NOT NULL
        AND next_review IS NOT NULL
        AND next_review BETWEEN ? AND ?
      GROUP BY next_review
      ORDER BY next_review
    `),
    getEarliestDueDate: db.prepare(`
      SELECT MIN(next_review) AS earliest_due_date
      FROM words
      WHERE status BETWEEN 1 AND 7
        AND last_reviewed IS NOT NULL
        AND next_review IS NOT NULL
    `),
    listRiskWords: db.prepare(`
      SELECT ${RISK_COLUMNS.replace('overdue_days', 'CAST(MAX(0, julianday(?) - julianday(next_review)) AS INTEGER) AS overdue_days')}
      FROM words
      WHERE status BETWEEN 1 AND 7
        AND last_reviewed IS NOT NULL
        AND next_review IS NOT NULL
      ORDER BY overdue_days DESC, status ASC, srs_lapses DESC, word ASC
      LIMIT ?
    `),
    insertHintToken: db.prepare(`
      INSERT OR REPLACE INTO hint_tokens (token, word, created_at)
      VALUES ($token, $word, $created_at)
    `),
    findHintToken: db.prepare(`SELECT token, word, created_at FROM hint_tokens WHERE token = ?`),
    deleteHintToken: db.prepare(`DELETE FROM hint_tokens WHERE token = ?`),
    deleteExpiredHintTokens: db.prepare(`DELETE FROM hint_tokens WHERE created_at < datetime('now', '-30 minutes')`),
    countReviewedDistinctOn: db.prepare(`
      SELECT COUNT(DISTINCT word) AS count
      FROM word_events
      WHERE study_date = ?
        AND event != 'unreviewed'
        AND NOT (event = 'skip' AND previous_status IS NULL)
    `),
    countReviewedByRange: db.prepare(`
      SELECT study_date AS date, COUNT(DISTINCT word) AS count
      FROM word_events
      WHERE event != 'unreviewed'
        AND NOT (event = 'skip' AND previous_status IS NULL)
        AND study_date BETWEEN ? AND ?
      GROUP BY study_date
    `),
    countNewByRange: db.prepare(`
      SELECT first_learned AS date, COUNT(*) AS count
      FROM words
      WHERE first_learned BETWEEN ? AND ?
      GROUP BY first_learned
    `),
    listProblemWordsByDateRange: db.prepare(`
      SELECT ${PROBLEM_WORD_COLUMNS}
      FROM word_events e
      LEFT JOIN words w ON w.word = e.word
      WHERE e.event IN ('wrong', 'remembered_after_hint')
        AND e.study_date BETWEEN ? AND ?
      GROUP BY e.word, w.status, w.last_reviewed
    `),
  };

  return {
    workspaceDir,
    dbPath: getDbPath(workspaceDir),
    close() {
      db.close();
    },
    transaction(fn) {
      db.exec('BEGIN IMMEDIATE');
      try {
        const result = fn();
        db.exec('COMMIT');
        return result;
      } catch (error) {
        try {
          db.exec('ROLLBACK');
        } catch (rollbackErr) {
          console.error('[vocab-db] rollback failed:', rollbackErr.message);
        }
        throw error;
      }
    },
    getWord(word) {
      return rowToWordEntry(statements.getWord.get(word));
    },
    listWords() {
      return statements.listWords.all().map(rowToWordEntry);
    },
    getPendingWord(word) {
      return rowToPendingEntry(statements.getPendingWord.get(word));
    },
    listPendingWords() {
      return statements.listPendingWords.all().map(rowToPendingEntry);
    },
    listPendingWordsLimited(limit) {
      return statements.listPendingWordsLimited.all(limit).map(rowToPendingEntry);
    },
    listDueWords(today) {
      return statements.listDueWords.all(today).map(rowToWordEntry);
    },
    listDueWordsLimited(today, limit) {
      return statements.listDueWordsLimited.all(today, limit).map(rowToWordEntry);
    },
    wordExists(word) {
      const row = statements.wordExists.get(word);
      return row ? { word: row.word, status: row.status } : null;
    },
    countPendingWords() {
      const row = statements.countPendingWords.get();
      return row ? (Number(row.count) || 0) : 0;
    },
    findEventByOpId(opId) {
      return statements.findEventByOpId.get(opId) || null;
    },
    getUserProfile() {
      return rowToUserProfileEntry(statements.getUserProfile.get());
    },
    listEventsByOpIds(opIds) {
      if (!Array.isArray(opIds) || opIds.length === 0) return [];
      const placeholders = opIds.map(() => '?').join(', ');
      const stmt = db.prepare(`
        SELECT ${EVENT_COLUMNS}
        FROM word_events
        WHERE op_id IN (${placeholders})
        ORDER BY id
      `);
      return stmt.all(...opIds).map(rowToEventEntry);
    },
    stagePendingWord(record) {
      const result = statements.stagePendingWord.run(normalizePendingRecord(record));
      return (result && Number(result.changes)) > 0;
    },
    deletePendingWord(word) {
      const result = statements.deletePendingWord.run(word);
      return (result && Number(result.changes)) > 0;
    },
    saveWord(record) {
      statements.upsertWord.run(normalizeWordRecord(record));
    },
    insertEvent(event) {
      statements.insertEvent.run({
        op_id: event.opId,
        word: event.word,
        event: event.event,
        previous_status: event.previousStatus,
        next_status: event.nextStatus,
        study_date: event.studyDate,
        result_due: event.resultDue ?? null,
        result_srs_state: event.resultSrsState ?? null,
        created_at: event.createdAt,
      });
    },
    saveUserProfile(record) {
      statements.upsertUserProfile.run(normalizeUserProfileRecord(record));
    },
    countWordsByStatus() {
      const rows = statements.countWordsByStatus.all();
      const map = {};
      for (const row of rows) {
        map[row.status] = Number(row.count) || 0;
      }
      return map;
    },
    countDueWords(today) {
      const row = statements.countDueWords.get(today);
      return row ? (Number(row.count) || 0) : 0;
    },
    countDueByDateRange(startDate, endDate) {
      return statements.countDueByDateRange.all(startDate, endDate).map((row) => ({
        date: row.date,
        count: Number(row.count) || 0,
      }));
    },
    getEarliestDueDate() {
      const row = statements.getEarliestDueDate.get();
      return row ? (row.earliest_due_date ?? null) : null;
    },
    listRiskWords(today, limit) {
      return statements.listRiskWords.all(today, limit).map(rowToRiskEntry);
    },
    getWordsByList(words) {
      if (!Array.isArray(words) || words.length === 0) return [];
      const placeholders = words.map(() => '?').join(', ');
      const stmt = db.prepare(`SELECT ${WORD_COLUMNS} FROM words WHERE word IN (${placeholders})`);
      return stmt.all(...words).map(rowToWordEntry);
    },
    insertHintToken(record) {
      statements.insertHintToken.run({
        token: record.token,
        word: record.word,
        created_at: record.createdAt,
      });
    },
    findHintToken(token) {
      const row = statements.findHintToken.get(token);
      return row ? { token: row.token, word: row.word, createdAt: row.created_at } : null;
    },
    deleteHintToken(token) {
      statements.deleteHintToken.run(token);
    },
    deleteExpiredHintTokens() {
      statements.deleteExpiredHintTokens.run();
    },
    countDistinctReviewedWordsOn(date) {
      const row = statements.countReviewedDistinctOn.get(date);
      return row ? (Number(row.count) || 0) : 0;
    },
    countReviewedWordsByDates(dates) {
      if (dates.length === 0) return [];
      const rows = statements.countReviewedByRange.all(dates[0], dates[dates.length - 1]);
      return mapCountRows(rows, dates);
    },
    countNewWordsByDates(dates) {
      if (dates.length === 0) return [];
      const rows = statements.countNewByRange.all(dates[0], dates[dates.length - 1]);
      return mapCountRows(rows, dates);
    },
    listProblemWordsByDateRange(startDate, endDate) {
      return statements.listProblemWordsByDateRange.all(startDate, endDate).map((row) => ({
        word: row.word,
        wrongCount: Number(row.wrong_count) || 0,
        rememberedAfterHintCount: Number(row.remembered_after_hint_count) || 0,
        problematicCount: Number(row.problematic_count) || 0,
        currentStatus: Number.isInteger(row.current_status)
          ? row.current_status
          : (Number.isFinite(Number(row.current_status)) ? Number(row.current_status) : null),
        lastReviewed: row.last_reviewed ?? 'never',
      }));
    },
  };
}

module.exports = {
  DB_FILENAME,
  DEFAULT_WORKSPACE_DIR,
  createRepository,
  getDbPath,
};
