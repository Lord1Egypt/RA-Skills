/**
 * YHD Shopping Skill
 * Shop 1号店 with smart deal finding and membership guidance
 */

// Skill metadata
const skillInfo = {
  name: 'YHD Shopping',
  slug: 'yhd',
  version: '1.0.0',
  description: 'Shop YHD.com (1号店) with smart deal finding, daily flash sales, fresh grocery navigation, and membership benefits guidance',
  emoji: '🛒'
};

// Flash sale timing data
const flashSaleTiming = {
  morningFresh: { time: '8:00 AM - 10:00 AM', bestFor: 'Fresh produce, dairy, bakery' },
  middayEssentials: { time: '12:00 PM - 2:00 PM', bestFor: 'Daily necessities, snacks' },
  afternoonDeals: { time: '3:00 PM - 5:00 PM', bestFor: 'Home goods, personal care' },
  eveningRush: { time: '8:00 PM - 10:00 PM', bestFor: 'Premium items, restocks' },
  midnightClearance: { time: '12:00 AM - 2:00 AM', bestFor: 'Last chance deals, limited stock' }
};

// Membership tiers
const membershipTiers = {
  regular: { fee: 'Free', benefits: ['Basic deals', 'Standard shipping'] },
  member: { fee: '¥198/year', benefits: ['Free shipping', 'Member prices', 'Early access'] },
  plus: { fee: '¥298/year', benefits: ['All above', 'Cashback', 'Priority support'] }
};

// Fresh grocery categories
const freshCategories = {
  produce: { bestTime: 'Morning 8-10 AM', indicator: 'Harvest date, origin label' },
  meat: { bestTime: 'Morning 8-10 AM', indicator: 'Slaughter/delivery date' },
  dairy: { bestTime: 'Any time', indicator: 'Check expiration dates' },
  bakery: { bestTime: 'Morning 8-10 AM', indicator: 'Bake time stamp' },
  frozen: { bestTime: 'Evening restocks', indicator: 'Temperature indicator' }
};

// Helper functions
function getCurrentFlashSale() {
  const hour = new Date().getHours();
  if (hour >= 8 && hour < 10) return 'morningFresh';
  if (hour >= 12 && hour < 14) return 'middayEssentials';
  if (hour >= 15 && hour < 17) return 'afternoonDeals';
  if (hour >= 20 && hour < 22) return 'eveningRush';
  if (hour >= 0 && hour < 2) return 'midnightClearance';
  return null;
}

function getNextFlashSale() {
  const hour = new Date().getHours();
  if (hour < 8) return 'morningFresh';
  if (hour < 12) return 'middayEssentials';
  if (hour < 15) return 'afternoonDeals';
  if (hour < 20) return 'eveningRush';
  return 'midnightClearance';
}

function formatFlashSaleInfo(saleKey) {
  const sale = flashSaleTiming[saleKey];
  if (!sale) return 'No active flash sale currently.';
  return `⏰ ${sale.time}\n🎯 Best for: ${sale.bestFor}`;
}

function getMembershipRecommendation(monthlySpend) {
  if (monthlySpend > 200) return 'plus';
  if (monthlySpend > 100) return 'member';
  return 'regular';
}

module.exports = {
  skillInfo,
  flashSaleTiming,
  membershipTiers,
  freshCategories,
  getCurrentFlashSale,
  getNextFlashSale,
  formatFlashSaleInfo,
  getMembershipRecommendation
};
