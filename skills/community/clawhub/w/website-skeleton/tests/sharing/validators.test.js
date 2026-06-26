import { describe, it, expect } from 'vitest';
import {
  validateString,
  validateEmail,
  validatePassword,
  validateOrderId,
  validateAmount,
  validateQuantity,
  validateTenantId,
  validateProductName,
  detectInjection,
  safeValidate,
  validateBody,
  safeParseInt,
  parsePagination,
} from '../../sharing/validators.js';

describe('validators.js — validateString', () => {
  it('validates required string', () => {
    expect(validateString('hello')).toEqual({ valid: true, sanitized: 'hello' });
  });

  it('fails on empty required string', () => {
    const result = validateString('');
    expect(result.valid).toBe(false);
    expect(result.error).toBe('此项不能为空');
  });

  it('fails when undefined and required', () => {
    const result = validateString(undefined);
    expect(result.valid).toBe(false);
    expect(result.error).toBe('此项为必填');
  });

  it('passes when undefined and not required', () => {
    const result = validateString(undefined, { required: false });
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe('');
  });

  it('enforces min length', () => {
    const result = validateString('ab', { min: 3 });
    expect(result.valid).toBe(false);
    expect(result.error).toContain('3');
  });

  it('enforces max length', () => {
    const result = validateString('a'.repeat(300), { max: 10 });
    expect(result.valid).toBe(false);
    expect(result.error).toContain('10');
  });

  it('trims whitespace', () => {
    const result = validateString('  hi  ');
    expect(result).toEqual({ valid: true, sanitized: 'hi' });
  });
});

describe('validators.js — validateEmail', () => {
  it('validates a correct email', () => {
    const result = validateEmail('test@example.com');
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe('test@example.com');
  });

  it('lowercases the email', () => {
    const result = validateEmail('USER@Example.COM');
    expect(result.sanitized).toBe('user@example.com');
  });

  it('fails on missing email', () => {
    expect(validateEmail(null).valid).toBe(false);
    expect(validateEmail(undefined).valid).toBe(false);
    expect(validateEmail('').valid).toBe(false);
  });

  it('fails on invalid format', () => {
    expect(validateEmail('notanemail').valid).toBe(false);
    expect(validateEmail('@domain.com').valid).toBe(false);
    expect(validateEmail('user@').valid).toBe(false);
  });

  it('fails on email too long', () => {
    const long = 'a'.repeat(250) + '@b.com';
    const result = validateEmail(long);
    expect(result.valid).toBe(false);
    expect(result.error).toBe('邮箱地址过长');
  });

  it('fails on non-string input', () => {
    expect(validateEmail(123).valid).toBe(false);
  });
});

describe('validators.js — validatePassword', () => {
  it('validates a strong password', () => {
    const result = validatePassword('Password1');
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe('Password1');
  });

  it('fails when missing', () => {
    expect(validatePassword(null).valid).toBe(false);
    expect(validatePassword(undefined).valid).toBe(false);
  });

  it('fails when too short', () => {
    const result = validatePassword('Ab1');
    expect(result.valid).toBe(false);
    expect(result.error).toContain('8');
  });

  it('fails when too long', () => {
    const result = validatePassword('A1' + 'x'.repeat(130));
    expect(result.valid).toBe(false);
    expect(result.error).toContain('128');
  });

  it('fails without letters', () => {
    const result = validatePassword('12345678');
    expect(result.valid).toBe(false);
    expect(result.error).toContain('字母');
  });

  it('fails without digits', () => {
    const result = validatePassword('abcdefgh');
    expect(result.valid).toBe(false);
    expect(result.error).toContain('数字');
  });

  it('fails on non-string input', () => {
    expect(validatePassword(12345678).valid).toBe(false);
  });
});

describe('validators.js — validateOrderId', () => {
  it('validates correct order ID', () => {
    expect(validateOrderId('ORD123456').valid).toBe(true);
    expect(validateOrderId('ORDER9876543210').sanitized).toBe('ORDER9876543210');
  });

  it('fails when missing', () => {
    expect(validateOrderId(null).valid).toBe(false);
    expect(validateOrderId(undefined).valid).toBe(false);
  });

  it('fails on invalid format (lowercase)', () => {
    expect(validateOrderId('ord123456').valid).toBe(false);
  });

  it('fails on too short', () => {
    expect(validateOrderId('AB12').valid).toBe(false);
  });

  it('fails on non-string input', () => {
    expect(validateOrderId(12345).valid).toBe(false);
  });
});

describe('validators.js — validateAmount', () => {
  it('validates a positive amount', () => {
    const result = validateAmount(99.99);
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe(99.99);
  });

  it('rounds to two decimal places', () => {
    const result = validateAmount(10.456);
    expect(result.sanitized).toBe(10.46);
  });

  it('fails when missing and required', () => {
    expect(validateAmount(undefined).valid).toBe(false);
  });

  it('passes when missing and not required', () => {
    const result = validateAmount(undefined, { required: false });
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe(0);
  });

  it('fails on NaN', () => {
    expect(validateAmount('abc').valid).toBe(false);
  });

  it('fails below minimum', () => {
    const result = validateAmount(0.001);
    expect(result.valid).toBe(false);
    expect(result.error).toContain('0.01');
  });

  it('fails above maximum', () => {
    const result = validateAmount(10000000);
    expect(result.valid).toBe(false);
  });

  it('accepts zero when not required with custom min', () => {
    const result = validateAmount(0, { required: false, min: 0 });
    expect(result.valid).toBe(true);
  });
});

describe('validators.js — validateQuantity', () => {
  it('validates a positive integer quantity', () => {
    const result = validateQuantity(5);
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe(5);
  });

  it('fails when missing and required', () => {
    expect(validateQuantity(undefined).valid).toBe(false);
  });

  it('passes when missing and not required (defaults to 1)', () => {
    const result = validateQuantity(undefined, { required: false });
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe(1);
  });

  it('fails below minimum', () => {
    expect(validateQuantity(0).valid).toBe(false);
  });

  it('fails above maximum', () => {
    expect(validateQuantity(1000).valid).toBe(false);
  });

  it('parses string input', () => {
    const result = validateQuantity('3');
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe(3);
  });
});

describe('validators.js — validateTenantId', () => {
  it('validates correct tenant ID', () => {
    expect(validateTenantId('acme-corp').valid).toBe(true);
    expect(validateTenantId('tenant_1').valid).toBe(true);
  });

  it('lowercases and trims', () => {
    const result = validateTenantId('  ACME  ');
    expect(result.sanitized).toBe('acme');
  });

  it('fails when missing', () => {
    expect(validateTenantId(null).valid).toBe(false);
    expect(validateTenantId(undefined).valid).toBe(false);
  });

  it('fails when starting with number', () => {
    expect(validateTenantId('1test').valid).toBe(false);
  });

  it('fails when too long', () => {
    expect(validateTenantId('a' + 'x'.repeat(40)).valid).toBe(false);
  });

  it('fails on non-string input', () => {
    expect(validateTenantId(123).valid).toBe(false);
  });
});

describe('validators.js — validateProductName', () => {
  it('validates a product name', () => {
    const result = validateProductName('iPhone 15');
    expect(result.valid).toBe(true);
    expect(result.sanitized).toBe('iPhone 15');
  });

  it('fails when missing', () => {
    expect(validateProductName(null).valid).toBe(false);
  });

  it('fails when too long', () => {
    const result = validateProductName('x'.repeat(300));
    expect(result.valid).toBe(false);
    expect(result.error).toContain('200');
  });

  it('trims whitespace', () => {
    const result = validateProductName('  Product  ');
    expect(result.sanitized).toBe('Product');
  });
});

describe('validators.js — detectInjection', () => {
  it('detects SQL injection patterns', () => {
    expect(detectInjection('x UNION SELECT * FROM users')).toBe(true);
    expect(detectInjection('DROP TABLE users')).toBe(true);
    expect(detectInjection('OR 1=1')).toBe(true);
  });

  it('detects XSS patterns', () => {
    expect(detectInjection('<script>alert(1)</script>')).toBe(true);
  });

  it('detects template injection', () => {
    expect(detectInjection('${process.env.SECRET}')).toBe(true);
  });

  it('returns false for safe input', () => {
    expect(detectInjection('hello world')).toBe(false);
    expect(detectInjection('normal query')).toBe(false);
  });

  it('returns false for non-string input', () => {
    expect(detectInjection(null)).toBe(false);
    expect(detectInjection(undefined)).toBe(false);
    expect(detectInjection(123)).toBe(false);
  });
});

describe('validators.js — safeValidate', () => {
  it('rejects injection payloads', () => {
    const result = safeValidate(validateString, "1' OR 1=1");
    expect(result.valid).toBe(false);
    expect(result.error).toBe('输入包含非法字符');
  });

  it('passes through valid input to validator', () => {
    const result = safeValidate(validateString, 'hello');
    expect(result.valid).toBe(true);
  });
});

describe('validators.js — validateBody', () => {
  const schema = {
    email: validateEmail,
    password: validatePassword,
  };

  it('validates all fields successfully', () => {
    const result = validateBody({ email: 'a@b.com', password: 'Pass1234' }, schema);
    expect(result.valid).toBe(true);
    expect(result.sanitized.email).toBe('a@b.com');
    expect(result.sanitized.password).toBe('Pass1234');
  });

  it('collects field-level errors', () => {
    const result = validateBody({ email: 'bad', password: 'weak' }, schema);
    expect(result.valid).toBe(false);
    expect(result.errors.email).toBeTruthy();
    expect(result.errors.password).toBeTruthy();
  });

  it('skips missing non-required validators', () => {
    const result = validateBody({}, { name: validateString });
    expect(result.valid).toBe(false);
  });
});

describe('validators.js — safeParseInt', () => {
  it('parses valid integers', () => {
    expect(safeParseInt('42')).toBe(42);
    expect(safeParseInt('0')).toBe(0);
  });

  it('returns fallback for NaN', () => {
    expect(safeParseInt('abc')).toBe(0);
    expect(safeParseInt('')).toBe(0);
  });

  it('returns fallback for out of range', () => {
    expect(safeParseInt('9999999999')).toBe(0);
  });

  it('custom fallback', () => {
    expect(safeParseInt('abc', -1)).toBe(-1);
  });
});

describe('validators.js — parsePagination', () => {
  it('returns default pagination with no query', () => {
    const result = parsePagination({});
    expect(result).toEqual({ page: 1, pageSize: 20, offset: 0 });
  });

  it('parses page and pageSize', () => {
    const result = parsePagination({ page: '3', pageSize: '10' });
    expect(result).toEqual({ page: 3, pageSize: 10, offset: 20 });
  });

  it('clamps page to min 1', () => {
    expect(parsePagination({ page: '0' }).page).toBe(1);
    expect(parsePagination({ page: '-5' }).page).toBe(1);
  });

  it('clamps pageSize between 1 and 100', () => {
    expect(parsePagination({ pageSize: '0' }).pageSize).toBe(1);
    expect(parsePagination({ pageSize: '200' }).pageSize).toBe(100);
  });

  it('handles null/undefined query', () => {
    const result = parsePagination(null);
    expect(result).toEqual({ page: 1, pageSize: 20, offset: 0 });

    const result2 = parsePagination(undefined);
    expect(result2).toEqual({ page: 1, pageSize: 20, offset: 0 });
  });
});
