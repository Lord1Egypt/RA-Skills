/**
 * SkillTree — Learning Progress Tracker
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

class SkillTree {
  constructor(options = {}) {
    this.dataFile = options.dataFile || './skill-tree.json';
    this.data = this._load();
    if (!this.data.skills) this.data = { skills: {}, completed: [] };
  }

  loadTree(tree) {
    // tree: { "HTML Basics": { prereqs: [], estHours: 10 }, "CSS": { prereqs: ["HTML Basics"], estHours: 15 } }
    this.data.skills = tree;
    this._save();
    return { loaded: Object.keys(tree).length };
  }

  complete(skillName) {
    if (!this.data.skills[skillName]) return { error: `Skill "${skillName}" not in tree` };
    if (!this.data.completed.includes(skillName)) {
      this.data.completed.push(skillName);
      this._save();
    }
    const unlocked = this.getUnlocked();
    const total = Object.keys(this.data.skills).length;
    return {
      skill: skillName,
      totalComplete: this.data.completed.length,
      totalSkills: total,
      percent: total > 0 ? Math.round(this.data.completed.length / total * 100) : 0,
      newlyUnlocked: unlocked.filter(s => !this.data.completed.includes(s)),
      message: `${skillName} complete! ${this.data.completed.length}/${total} (${total > 0 ? Math.round(this.data.completed.length / total * 100) : 0}%)`
    };
  }

  getUnlocked() {
    return Object.entries(this.data.skills)
      .filter(([name, info]) => {
        if (this.data.completed.includes(name)) return false;
        const prereqs = info.prereqs || [];
        return prereqs.every(p => this.data.completed.includes(p));
      })
      .map(([name]) => name);
  }

  suggest() {
    const unlocked = this.getUnlocked();
    if (unlocked.length === 0) return { message: 'All available skills complete! Check for new prerequisites.' };
    // Suggest the one that unlocks the most other skills
    const scores = unlocked.map(name => {
      const wouldUnlock = Object.entries(this.data.skills).filter(([, info]) => {
        const prereqs = info.prereqs || [];
        return prereqs.includes(name) && prereqs.every(p => p === name || this.data.completed.includes(p));
      }).length;
      return { name, wouldUnlock, estHours: this.data.skills[name]?.estHours || 0 };
    });
    scores.sort((a, b) => b.wouldUnlock - a.wouldUnlock);
    return scores[0];
  }

  progress() {
    const total = Object.keys(this.data.skills).length;
    const done = this.data.completed.length;
    const remaining = Object.entries(this.data.skills)
      .filter(([name]) => !this.data.completed.includes(name))
      .reduce((sum, [, info]) => sum + (info.estHours || 0), 0);
    return { total, completed: done, percent: total > 0 ? Math.round(done / total * 100) : 0, estHoursRemaining: remaining };
  }

  _load() { try { return JSON.parse(fs.readFileSync(this.dataFile, 'utf8')); } catch { return { skills: {}, completed: [] }; } }
  _save() { try { fs.writeFileSync(this.dataFile, JSON.stringify(this.data, null, 2)); } catch {} }
}

module.exports = { SkillTree };
