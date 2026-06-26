const path = require('path');

const { AppError, EXIT_CODES } = require('../errors');
const { PROFILE_FILENAME, loadUserProfile } = require('./user-profile');

const LEARN_TITLE = 'WordPal 学习推送';
const LEARN_DESCRIPTION = '[WordPal:type=learn] WordPal 学习推送';

function toRegistration(pushTime, index) {
  return {
    index,
    time: pushTime,
    kind: 'learn',
    title: LEARN_TITLE,
    description: LEARN_DESCRIPTION,
  };
}

function buildPushPlan({ workspaceDir }) {
  const profileFile = path.join(workspaceDir, PROFILE_FILENAME);
  const current = loadUserProfile(profileFile);

  if (!current.exists) {
    throw new AppError(
      'PROFILE_NOT_FOUND',
      'user profile does not exist yet',
      EXIT_CODES.BUSINESS_RULE,
    );
  }

  const pushTimes = current.profile.pushTimes;
  if (pushTimes.length === 0) {
    throw new AppError(
      'PUSH_TIMES_EMPTY',
      'profile has no push-times configured',
      EXIT_CODES.BUSINESS_RULE,
    );
  }

  return {
    registrations: pushTimes.map((pushTime, index) => toRegistration(pushTime, index)),
  };
}

module.exports = {
  LEARN_DESCRIPTION,
  LEARN_TITLE,
  buildPushPlan,
  toRegistration,
};
