const ProposalGenerator = require('./generator');

module.exports = {
  ProposalGenerator,
  generate: (config) => {
    const generator = new ProposalGenerator(config);
    return generator.generate();
  }
};
