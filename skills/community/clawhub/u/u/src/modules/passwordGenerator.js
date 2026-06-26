import crypto from 'crypto';

const passwordGenerator = {
  lowercase: 'abcdefghijklmnopqrstuvwxyz',
  uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  numbers: '0123456789',
  symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?',

  generate(options = {}) {
    const {
      length = 12,
      useUppercase = true,
      useLowercase = true,
      useNumbers = true,
      useSymbols = true
    } = options;

    let chars = '';
    if (useLowercase) chars += this.lowercase;
    if (useUppercase) chars += this.uppercase;
    if (useNumbers) chars += this.numbers;
    if (useSymbols) chars += this.symbols;

    if (!chars) {
      throw new Error('At least one character type must be selected');
    }

    let password = '';
    for (let i = 0; i < length; i++) {
      const randomByte = crypto.randomBytes(1)[0];
      password += chars[randomByte % chars.length];
    }

    return password;
  },

  evaluateStrength(password) {
    let score = 0;

    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    if (password.length >= 16) score += 1;

    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^a-zA-Z0-9]/.test(password)) score += 1;

    let strength;
    if (score <= 2) strength = 'weak';
    else if (score <= 4) strength = 'medium';
    else if (score <= 6) strength = 'strong';
    else strength = 'very_strong';

    return { score, strength, maxScore: 7 };
  },

  generateMultiple(count, options = {}) {
    const passwords = [];
    for (let i = 0; i < count; i++) {
      passwords.push(this.generate(options));
    }
    return passwords;
  }
};

export default passwordGenerator;
