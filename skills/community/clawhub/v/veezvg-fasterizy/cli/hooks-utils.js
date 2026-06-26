function hasFasterizyHook(settings, event) {
  const arr = settings.hooks && settings.hooks[event];
  return (
    Array.isArray(arr) &&
    arr.some(
      (e) =>
        e.hooks &&
        e.hooks.some((h) => h.command && h.command.toLowerCase().includes('fasterizy'))
    )
  );
}

function stripFasterizyHookEntries(settingsObj) {
  if (!settingsObj.hooks) return false;
  let changed = false;
  for (const event of ['SessionStart', 'UserPromptSubmit']) {
    const arr = settingsObj.hooks[event];
    if (!Array.isArray(arr)) continue;
    const filtered = arr
      .map((group) => {
        if (!group.hooks || !Array.isArray(group.hooks)) return group;
        const remaining = group.hooks.filter(
          (h) => !(h.command && h.command.toLowerCase().includes('fasterizy'))
        );
        if (remaining.length === group.hooks.length) return group;
        changed = true;
        return remaining.length ? { ...group, hooks: remaining } : null;
      })
      .filter(Boolean);
    if (filtered.length === 0) {
      delete settingsObj.hooks[event];
    } else {
      settingsObj.hooks[event] = filtered;
    }
  }
  return changed;
}

module.exports = { hasFasterizyHook, stripFasterizyHookEntries };
