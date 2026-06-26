"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateBadge = generateBadge;
exports.generateBadgeMarkdown = generateBadgeMarkdown;
exports.generateBadgeJSON = generateBadgeJSON;
const TIER_CONFIG = {
    verified: { color: '#22c55e', label: 'Tork Verified' },
    reviewed: { color: '#eab308', label: 'Tork Reviewed' },
    flagged: { color: '#ef4444', label: 'Tork Flagged' },
    unverified: { color: '#6b7280', label: 'Tork Unverified' },
};
function generateBadge(report) {
    const tier = scoreToBadgeTier(report.riskScore);
    const config = TIER_CONFIG[tier];
    return {
        tier,
        color: config.color,
        label: config.label,
        riskScore: report.riskScore,
        scannedAt: report.scannedAt,
        verifyUrl: `https://tork.network/verify/${report.skillName}`,
    };
}
function generateBadgeMarkdown(badge) {
    const encodedLabel = encodeURIComponent(badge.label);
    const encodedTier = encodeURIComponent(badge.tier);
    const colorHex = badge.color.replace('#', '');
    return `[![${badge.label}](https://img.shields.io/badge/${encodedLabel}-${encodedTier}-${colorHex})](${badge.verifyUrl})`;
}
function generateBadgeJSON(badge) {
    return JSON.stringify(badge, null, 2);
}
function scoreToBadgeTier(score) {
    if (score < 30)
        return 'verified';
    if (score < 50)
        return 'reviewed';
    return 'flagged';
}
//# sourceMappingURL=badge.js.map