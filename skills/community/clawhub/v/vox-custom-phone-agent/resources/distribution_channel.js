'use strict';

function resolveDistribution({ env = process.env, options = {} } = {}) {
  const rawSource = options.distributionChannel || options.source || env.SKILL_DISTRIBUTION_CHANNEL || env.SKILL_SOURCE || 'skillhub';
  const source = normalizeSource(rawSource);
  return {
    source,
    distribution_channel: source,
    registry: options.registry || env.SKILL_REGISTRY || defaultRegistry(source)
  };
}

function normalizeSource(source) {
  const normalized = String(source || 'unknown').trim().toLowerCase();
  if (normalized === 'clawhub') return 'clawhub';
  if (normalized === 'skillhub') return 'skillhub';
  if (normalized === 'internal') return 'internal';
  return 'unknown';
}

function defaultRegistry(source) {
  if (source === 'clawhub') return 'clawhub.ai';
  if (source === 'skillhub') return 'skillhub.cn';
  return 'unknown';
}

module.exports = {
  defaultRegistry,
  normalizeSource,
  resolveDistribution
};
