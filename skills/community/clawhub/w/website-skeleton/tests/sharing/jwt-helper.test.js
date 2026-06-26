import { describe, it, expect, beforeAll, vi } from 'vitest';

// We need actual crypto.subtle — Node.js 22+ has Web Crypto built-in.
// For RS256 we need real RSA key pair. We'll generate one with crypto.subtle.

const HS256_SECRET = 'test-hs256-secret-key-for-unit-tests';

// We'll generate an RSA key pair at module scope so it's available to all tests
let rsaKeyPair;
let env;

beforeAll(async () => {
  rsaKeyPair = await crypto.subtle.generateKey(
    { name: 'RSA-PSS', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' },
    true,
    ['sign', 'verify']
  );

  // Export to SPKI/PKCS8 PEM strings (as the module expects them)
  const spkiBuf = await crypto.subtle.exportKey('spki', rsaKeyPair.publicKey);
  const pkcs8Buf = await crypto.subtle.exportKey('pkcs8', rsaKeyPair.privateKey);

  const spkiPem = arrayBufferToPem(spkiBuf, 'PUBLIC KEY');
  const pkcs8Pem = arrayBufferToPem(pkcs8Buf, 'PRIVATE KEY');

  env = {
    JWT_PRIVATE_KEY: pkcs8Pem,
    JWT_PUBLIC_KEY: spkiPem,
    JWT_SECRET: HS256_SECRET,
  };
});

function arrayBufferToPem(buf, label) {
  const bytes = new Uint8Array(buf);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  const base64 = btoa(binary);
  // Split into 64-char lines
  const lines = base64.match(/.{1,64}/g) || [base64];
  return `-----BEGIN ${label}-----\n${lines.join('\n')}\n-----END ${label}-----`;
}

// Now import the module under test (must be dynamic after env setup, or static is fine since it uses env at call time)
import {
  signAccessToken,
  signRefreshToken,
  signJWT,
  verifyJWT,
  verifyAccessToken,
  verifyRefreshToken,
  importPrivateKey,
  importRSAPublicKey,
  importHS256Secret,
  parseJWTWithoutVerify,
  extractToken,
  extractRefreshToken,
} from '../../sharing/jwt-helper.js';

describe('jwt-helper.js — Key import', () => {
  it('importPrivateKey returns a CryptoKey', async () => {
    const key = await importPrivateKey(env.JWT_PRIVATE_KEY);
    expect(key).toBeInstanceOf(CryptoKey);
    expect(key.type).toBe('private');
  });

  it('importRSAPublicKey returns a CryptoKey', async () => {
    const key = await importRSAPublicKey(env.JWT_PUBLIC_KEY);
    expect(key).toBeInstanceOf(CryptoKey);
    expect(key.type).toBe('public');
  });

  it('importHS256Secret returns a CryptoKey', async () => {
    const key = await importHS256Secret(HS256_SECRET);
    expect(key).toBeInstanceOf(CryptoKey);
    expect(key.type).toBe('secret');
  });
});

describe('jwt-helper.js — signJWT', () => {
  it('signs and verifies a JWT round-trip', async () => {
    const payload = { sub: '123', name: 'test' };
    const token = await signJWT(payload, 60000, env);
    expect(token).toBeTruthy();
    expect(token.split('.').length).toBe(3);

    const result = await verifyJWT(token, env);
    expect(result).toBeTruthy();
    expect(result.sub).toBe('123');
    expect(result.name).toBe('test');
    expect(result.tenant).toBe('default'); // auto-set
    expect(result.role).toBe('user'); // auto-set
    expect(result.jti).toBeTruthy();
    expect(result.iat).toBeTruthy();
    expect(result.exp).toBeTruthy();
    expect(result._alg).toBe('RS256');
  });

  it('signs with custom tenant and role', async () => {
    const payload = { sub: '456', tenant: 'acme-corp', role: 'admin' };
    const token = await signJWT(payload, 60000, env);
    const result = await verifyJWT(token, env);
    expect(result.tenant).toBe('acme-corp');
    expect(result.role).toBe('admin');
  });
});

describe('jwt-helper.js — signAccessToken', () => {
  it('signs and verifies an access token', async () => {
    const token = await signAccessToken({ sub: 'user1' }, env);
    const result = await verifyAccessToken(token, env);
    expect(result).toBeTruthy();
    expect(result.sub).toBe('user1');
    // RT type tokens should be rejected by verifyAccessToken
  });

  it('rejects refresh tokens used as access tokens', async () => {
    const rt = await signRefreshToken('u1', 1, env);
    const result = await verifyAccessToken(rt, env);
    expect(result).toBeNull();
  });
});

describe('jwt-helper.js — signRefreshToken', () => {
  it('signs and verifies a refresh token', async () => {
    const token = await signRefreshToken('u1', 1, env);
    const result = await verifyRefreshToken(token, env);
    expect(result).toBeTruthy();
    expect(result.sub).toBe('u1');
    expect(result.type).toBe('refresh');
    expect(result.v).toBe(1);
  });
});

describe('jwt-helper.js — verifyJWT rejection', () => {
  it('rejects a tampered token', async () => {
    const token = await signAccessToken({ sub: 'u1' }, env);
    const parts = token.split('.');
    // Tamper with the body
    const tampered = [parts[0], 'eyJmYWtlIjp0cnV9', parts[2]].join('.');
    const result = await verifyJWT(tampered, env);
    expect(result).toBeNull();
  });

  it('rejects an expired token', async () => {
    // Mock Date.now to be in the past, sign a token, then restore Date.now
    const realDateNow = Date.now;
    const pastNow = 1000000000000; // arbitrary past timestamp
    vi.useFakeTimers();
    vi.setSystemTime(pastNow);

    const payload = { sub: 'exp-test' };
    // expiry = 1 second from mocked time
    const token = await signJWT(payload, 1000, env);

    // Advance time past expiry
    vi.setSystemTime(pastNow + 2000);
    // Needed because verifyJWT uses Date.now() internally via the closure
    // but vi.useFakeTimers should intercept it
    const result = await verifyJWT(token, env);
    expect(result).toBeNull();

    vi.useRealTimers();
  });

  it('rejects malformed token', async () => {
    const result = await verifyJWT('not-a-jwt', env);
    expect(result).toBeNull();
  });

  it('rejects token with wrong number of parts', async () => {
    const result = await verifyJWT('a.b', env);
    expect(result).toBeNull();
  });
});

describe('jwt-helper.js — parseJWTWithoutVerify', () => {
  it('parses payload from a valid token', async () => {
    const token = await signAccessToken({ sub: 'p1', foo: 'bar' }, env);
    const payload = parseJWTWithoutVerify(token);
    expect(payload.sub).toBe('p1');
    expect(payload.foo).toBe('bar');
  });

  it('returns null for malformed token', () => {
    expect(parseJWTWithoutVerify('invalid')).toBeNull();
  });

  it('returns null for non-3-part token', () => {
    expect(parseJWTWithoutVerify('a.b')).toBeNull();
  });
});

describe('jwt-helper.js — extractToken', () => {
  it('extracts Bearer token from Authorization header', () => {
    const req = new Request('http://test.com', {
      headers: { Authorization: 'Bearer my-access-token' },
    });
    const result = extractToken(req);
    expect(result).toEqual({ token: 'my-access-token', source: 'Bearer' });
  });

  it('extracts token from Cookie', () => {
    const req = new Request('http://test.com', {
      headers: { Cookie: 'at=my-cookie-token; rt=refresh-token' },
    });
    const result = extractToken(req);
    expect(result).toEqual({ token: 'my-cookie-token', source: 'Cookie' });
  });

  it('returns null when no token is present', () => {
    const req = new Request('http://test.com');
    expect(extractToken(req)).toBeNull();
  });

  it('prioritizes Bearer over Cookie', () => {
    const req = new Request('http://test.com', {
      headers: {
        Authorization: 'Bearer bearer-token',
        Cookie: 'at=cookie-token',
      },
    });
    const result = extractToken(req);
    expect(result.token).toBe('bearer-token');
    expect(result.source).toBe('Bearer');
  });
});

describe('jwt-helper.js — extractRefreshToken', () => {
  it('extracts refresh token from Cookie', () => {
    const req = new Request('http://test.com', {
      headers: { Cookie: 'at=access; rt=my-refresh-token' },
    });
    expect(extractRefreshToken(req)).toBe('my-refresh-token');
  });

  it('returns null when no rt cookie', () => {
    const req = new Request('http://test.com', {
      headers: { Cookie: 'at=access-only' },
    });
    expect(extractRefreshToken(req)).toBeNull();
  });

  it('returns null when no cookies', () => {
    const req = new Request('http://test.com');
    expect(extractRefreshToken(req)).toBeNull();
  });
});
