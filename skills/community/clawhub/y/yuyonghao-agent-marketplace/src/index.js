/**
 * Agent Marketplace - Main Entry Point
 * Skill discovery, rating, and installation management
 */

const { CatalogManager } = require('./catalog');
const { RatingSystem } = require('./rating');
const { SearchEngine } = require('./search');
const { RegistryManager } = require('./registry');

module.exports = {
  CatalogManager,
  RatingSystem,
  SearchEngine,
  RegistryManager
};

// If run directly, create a demo instance
if (require.main === module) {
  const marketplace = new CatalogManager({
    registry: 'https://clawhub.com/registry',
    dataDir: './.marketplace-cache'
  });

  console.log('Agent Marketplace Demo Started');
  console.log('Ready to discover and install skills');
}
