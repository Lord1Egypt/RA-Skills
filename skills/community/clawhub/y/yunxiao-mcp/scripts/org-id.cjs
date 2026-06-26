function resolveOrgId({ explicitOrgId, envOrgId, organizations }) {
  if (explicitOrgId) return explicitOrgId;
  if (envOrgId) return envOrgId;

  if (Array.isArray(organizations) && organizations.length > 0) {
    return organizations[0].id || null;
  }

  return null;
}

module.exports = {
  resolveOrgId
};
