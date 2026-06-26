import crypto from 'crypto';

const hashCalculator = {
  md5(str) {
    return crypto.createHash('md5').update(str).digest('hex');
  },

  sha1(str) {
    return crypto.createHash('sha1').update(str).digest('hex');
  },

  sha256(str) {
    return crypto.createHash('sha256').update(str).digest('hex');
  },

  sha512(str) {
    return crypto.createHash('sha512').update(str).digest('hex');
  },

  hash(str, algorithm = 'sha256') {
    const algos = {
      md5: this.md5,
      sha1: this.sha1,
      sha256: this.sha256,
      sha512: this.sha512
    };
    if (algos[algorithm]) {
      return algos[algorithm](str);
    }
    throw new Error(`Unsupported algorithm: ${algorithm}`);
  },

  listAlgorithms() {
    return ['md5', 'sha1', 'sha256', 'sha512'];
  }
};

export default hashCalculator;
