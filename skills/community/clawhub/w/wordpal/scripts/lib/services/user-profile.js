const fs = require('fs');
const path = require('path');

const { createRepository, getDbPath } = require('../core/vocab-db');
const { isValidDate, formatLocalDate } = require('../core/fsrs-scheduler');
const { AppError, EXIT_CODES } = require('../errors');

const PROFILE_FILENAME = 'user-profile.md';

const DEFAULT_PROFILE = {
  created: null,
  learningGoal: 'DAILY',
  pushTimes: [],
  difficultyLevel: 'III',
  dailyTarget: 10,
};

const LEARNING_GOALS = ['CET4', 'CET6', 'POSTGRAD', 'IELTS', 'TOEFL', 'GRE', 'DAILY'];
const DIFFICULTY_LEVELS = ['I', 'II', 'III', 'IV', 'V'];

function parseProfileMap(raw) {
  const map = {};
  for (const line of raw.split(/\r?\n/)) {
    const match = /^([a-zA-Z0-9_-]+)\s*:\s*(.+)$/.exec(line.trim());
    if (!match) continue;
    map[match[1].trim().toLowerCase()] = match[2].trim();
  }
  return map;
}

function normalizeEnum(value, allowed, fallback) {
  const normalized = typeof value === 'string' ? value.trim().toUpperCase() : '';
  return allowed.includes(normalized) ? normalized : fallback;
}

function parsePushTimes(rawValue) {
  if (typeof rawValue !== 'string' || rawValue.trim() === '') {
    return [];
  }

  const seen = new Set();
  const out = [];
  for (const token of rawValue.split(',')) {
    const value = token.trim();
    if (!/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(value)) {
      return [];
    }
    if (seen.has(value)) continue;
    seen.add(value);
    out.push(value);
  }

  return out;
}

function normalizePushTimesInput(rawValue, label = '--push-times') {
  const pushTimes = parsePushTimes(rawValue);
  if (typeof rawValue !== 'string' || rawValue.trim() === '' || pushTimes.length === 0) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      `Invalid ${label}: expected comma-separated HH:MM values`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
  return pushTimes;
}

function normalizeCreated(value, fallback = null) {
  return typeof value === 'string' && isValidDate(value, false) ? value : fallback;
}

function normalizeDailyTarget(value, fallback) {
  return Number.isInteger(value) && value >= 1 && value <= 100 ? value : fallback;
}

function normalizeProfile(map) {
  const learningGoal = normalizeEnum(map['learning-goal'], LEARNING_GOALS, DEFAULT_PROFILE.learningGoal);
  const difficultyLevel = normalizeEnum(map['difficulty-level'], DIFFICULTY_LEVELS, DEFAULT_PROFILE.difficultyLevel);
  const dailyTarget = normalizeDailyTarget(Number.parseInt(map['daily-target'] || '', 10), DEFAULT_PROFILE.dailyTarget);

  return {
    created: normalizeCreated(map.created, DEFAULT_PROFILE.created),
    learningGoal,
    pushTimes: parsePushTimes(map['push-times']),
    difficultyLevel,
    dailyTarget,
  };
}

function fileToWorkspaceDir(file) {
  return path.dirname(file);
}

function profileToDbRecord(profile, updatedAt = formatLocalDate()) {
  return {
    created: profile.created,
    learningGoal: profile.learningGoal,
    pushTimes: profile.pushTimes.join(', '),
    difficultyLevel: profile.difficultyLevel,
    dailyTarget: profile.dailyTarget,
    updatedAt,
  };
}

function dbEntryToProfile(entry) {
  if (!entry) return null;
  return normalizeProfile({
    created: entry.created ?? '',
    'learning-goal': entry.learningGoal,
    'push-times': entry.pushTimes,
    'difficulty-level': entry.difficultyLevel,
    'daily-target': String(entry.dailyTarget),
  });
}

function loadUserProfileFromFile(file) {
  if (!fs.existsSync(file)) {
    return {
      exists: false,
      profile: { ...DEFAULT_PROFILE },
    };
  }

  const raw = fs.readFileSync(file, 'utf8');
  return {
    exists: true,
    profile: normalizeProfile(parseProfileMap(raw)),
  };
}

function removeLegacyProfileFile(file) {
  if (!fs.existsSync(file)) return;
  fs.unlinkSync(file);
}

function readUserProfileFromDatabase(workspaceDir) {
  const dbPath = getDbPath(workspaceDir);
  if (!fs.existsSync(dbPath)) {
    return null;
  }

  const repo = createRepository(workspaceDir);
  try {
    return dbEntryToProfile(repo.getUserProfile());
  } finally {
    repo.close();
  }
}

function saveUserProfileToDatabase(workspaceDir, profile, options = {}) {
  const repo = createRepository(workspaceDir);
  try {
    repo.saveUserProfile(profileToDbRecord(profile, options.updatedAt || formatLocalDate()));
  } finally {
    repo.close();
  }
}

function loadUserProfile(file) {
  const workspaceDir = fileToWorkspaceDir(file);
  const dbProfile = readUserProfileFromDatabase(workspaceDir);

  if (dbProfile) {
    removeLegacyProfileFile(file);
    return {
      exists: true,
      profile: dbProfile,
    };
  }

  const fileProfile = loadUserProfileFromFile(file);
  if (fileProfile.exists) {
    const profile = fileProfile.profile;
    saveUserProfileToDatabase(workspaceDir, profile);
    removeLegacyProfileFile(file);
    return {
      exists: true,
      profile,
    };
  }

  return {
    exists: false,
    profile: { ...DEFAULT_PROFILE },
  };
}

function readUserProfile(file) {
  return loadUserProfile(file).profile;
}

function renderUserProfile(profile) {
  const created = profile.created || formatLocalDate();
  const pushTimes = profile.pushTimes.join(', ');
  return [
    '# WordPal 用户画像',
    '',
    `created: ${created}`,
    `learning-goal: ${profile.learningGoal}`,
    `push-times: ${pushTimes}`,
    `difficulty-level: ${profile.difficultyLevel}`,
    `daily-target: ${profile.dailyTarget}`,
    '',
  ].join('\n');
}

function toScriptProfile(profile) {
  return {
    created: profile.created,
    learning_goal: profile.learningGoal,
    push_times: profile.pushTimes,
    difficulty_level: profile.difficultyLevel,
    daily_target: profile.dailyTarget,
  };
}

function writeUserProfile(file, patch, options = {}) {
  const today = options.today || formatLocalDate();
  const current = loadUserProfile(file);
  const currentProfile = current.profile;
  const nextProfile = {
    created: patch.created ?? currentProfile.created ?? today,
    learningGoal: patch.learningGoal ?? currentProfile.learningGoal,
    pushTimes: patch.pushTimes ?? currentProfile.pushTimes,
    difficultyLevel: patch.difficultyLevel ?? currentProfile.difficultyLevel,
    dailyTarget: patch.dailyTarget ?? currentProfile.dailyTarget,
  };

  const updatedFields = [];
  if (nextProfile.created !== currentProfile.created) updatedFields.push('created');
  if (nextProfile.learningGoal !== currentProfile.learningGoal) updatedFields.push('learning_goal');
  if (JSON.stringify(nextProfile.pushTimes) !== JSON.stringify(currentProfile.pushTimes)) updatedFields.push('push_times');
  if (nextProfile.difficultyLevel !== currentProfile.difficultyLevel) updatedFields.push('difficulty_level');
  if (nextProfile.dailyTarget !== currentProfile.dailyTarget) updatedFields.push('daily_target');

  saveUserProfileToDatabase(fileToWorkspaceDir(file), nextProfile, { updatedAt: today });
  removeLegacyProfileFile(file);

  return {
    exists: true,
    created: !current.exists,
    updatedFields,
    profile: nextProfile,
  };
}

module.exports = {
  DEFAULT_PROFILE,
  DIFFICULTY_LEVELS,
  LEARNING_GOALS,
  PROFILE_FILENAME,
  loadUserProfileFromFile,
  loadUserProfile,
  normalizeCreated,
  normalizePushTimesInput,
  readUserProfile,
  renderUserProfile,
  toScriptProfile,
  writeUserProfile,
};
