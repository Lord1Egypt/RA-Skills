---
title: Use Bun's Built-in Crypto for Secure Password Hashing
impact: CRITICAL
section: 7
impactDescription: Prevents password leak breaches
tags: auth, security, password-hashing, bun, crypto, argon2, bcrypt
---

Storing passwords in plain text is a critical security vulnerability. When a database is compromised, plain text passwords expose users to credential stuffing and account takeover across all services where they reuse passwords. **Never store plain text passwords or use weak hashing.**

> **Hint**: Bun provides a built-in `Crypto` module with secure password hashing supporting both **argon2** (default) and **bcrypt** algorithms. The algorithm is configurable at runtime via `algorithm: 'argon2id' | 'bcrypt'` option. No external packages needed.

## For AI Agents

When implementing or reviewing password handling, **always** follow these steps:

### Step 1: Check for Plain Text or Weak Hashing
**Pattern to check:** Look for passwords being stored directly or hashed with weak algorithms.

```typescript
// ❌ WRONG - Plain text storage
async register(password: string) {
  return this.prisma.user.create({
    data: { password },  // ❌ Stored as plain text!
  });
}

// ❌ WRONG - Weak hashing (MD5, SHA1, SHA256)
import { createHash } from 'crypto';
async hashPassword(password: string) {
  return createHash('sha256').update(password).digest('hex');  // ❌ Fast, crackable
}

// ❌ WRONG - Manual salt with SHA256
async hashPassword(password: string, salt: string) {
  return createHash('sha256').update(password + salt).digest('hex');  // ❌ Still weak
}

// ✅ CORRECT - Bun's native password hashing
async hashPassword(password: string) {
  return Bun.password.hash(password);  // ✅ Secure, automatic salt
}
```

**If found:** Replace with Bun's `Crypto.password.hash()`.

### Step 2: Create Password Service
**File:** `src/auth/password.service.ts`

```typescript
// ✅ REQUIRED: Password service using Bun's native crypto
import { Injectable } from '@nestjs/common';

@Injectable()
export class PasswordService {
  // ✅ Hash with default algorithm (argon2id)
  async hash(password: string): Promise<string> {
    return Bun.password.hash(password);
  }

  // ✅ Verify a password against a hash (auto-detects algorithm)
  async verify(password: string, hash: string): Promise<boolean> {
    return Bun.password.verify(password, hash);
  }

  // ✅ Hash with specific algorithm (argon2id or bcrypt)
  async hashWithAlgorithm(password: string, algorithm: 'argon2id' | 'bcrypt' = 'argon2id'): Promise<string> {
    return Bun.password.hash(password, { algorithm });
  }
}
```

### Step 3: Use Password Service in AuthService

```typescript
// ✅ REQUIRED: Hash passwords on registration
@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private passwordService: PasswordService,
  ) {}

  async register(data: RegisterDto) {
    // ✅ Hash password before storing
    const hashedPassword = await this.passwordService.hash(data.password);

    const user = await this.prisma.user.create({
      data: {
        email: data.email,
        password: hashedPassword,  // ✅ Store hash, not plain text
      },
    });

    return user;
  }

  async login(data: LoginDto) {
    const user = await this.prisma.user.findUnique({
      where: { email: data.email },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // ✅ Verify password with timing-safe comparison
    const isValid = await this.passwordService.verify(data.password, user.password);

    if (!isValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    return this.generateTokens(user);
  }
}
```

### Step 4: Add Password Strength Validation
**File:** `src/auth/dto/register.dto.ts`

```typescript
// ✅ REQUIRED: Enforce strong passwords
import { IsString, MinLength, Matches } from 'class-validator';

export class RegisterDto {
  @IsString()
  @MinLength(12, { message: 'Password must be at least 12 characters' })
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/, {
    message: 'Password must contain uppercase, lowercase, number, and special character',
  })
  password: string;

  @IsEmail()
  email: string;
}
```

### Step 5: Implement Password Migration (if needed)

```typescript
// ✅ OPTIONAL: Migrate from old hashing
@Injectable()
export class PasswordService {
  async verifyAndMigrate(password: string, hash: string): Promise<{
    isValid: boolean;
    needsMigration: boolean;
    newHash?: string;
  }> {
    // Check if using old hash format
    if (hash.startsWith('old_$')) {
      const isValid = this.verifyOldHash(password, hash);

      if (isValid) {
        // Rehash with Bun's secure algorithm
        const newHash = await this.hash(password);
        return { isValid: true, needsMigration: true, newHash };
      }

      return { isValid: false, needsMigration: false };
    }

    // Use Bun's native verify
    const isValid = await Bun.password.verify(password, hash);
    return { isValid, needsMigration: false };
  }

  private verifyOldHash(password: string, hash: string): boolean {
    // Old verification logic
    return true;
  }
}
```

## Installation

```bash
# No packages needed! Bun's Crypto is built-in.
# Just ensure you're using Bun runtime
bun --version
```

## Quick Reference Checklist

Use this checklist when reviewing or creating password handling:

- [ ] Passwords are never stored in plain text
- [ ] Passwords are hashed with `Bun.password.hash()`
- [ ] Passwords are verified with `Bun.password.verify()`
- [ ] Passwords have minimum length requirement (12+ characters)
- [ ] Passwords require mixed case, numbers, special characters
- [ ] Database column for hashed password is `TEXT` or `VARCHAR(255)`
- [ ] Error messages don't reveal if user exists

**Incorrect:**

```typescript
// auth/auth.service.ts - Insecure 🚨
import { Injectable } from '@nestjs/common';
import { createHash, randomBytes } from 'crypto';

@Injectable()
export class AuthService {
  // ❌ Plain text storage
  async register(email: string, password: string) {
    return this.prisma.user.create({
      data: { email, password },  // ❌ Stored as-is!
    });
  }

  // ❌ Fast hash (SHA256, MD5) - crackable with GPUs
  async hashPassword(password: string) {
    return createHash('sha256').update(password).digest('hex');
  }

  // ❌ Manual salt - still vulnerable to GPU cracking
  async hashWithSalt(password: string) {
    const salt = randomBytes(16).toString('hex');
    const hash = createHash('sha512')
      .update(password + salt)
      .digest('hex');
    return `${salt}:${hash}`;
  }

  // ❌ Timing-sensitive string comparison
  async verifyPassword(password: string, hash: string) {
    const [salt, originalHash] = hash.split(':');
    const computedHash = createHash('sha512')
      .update(password + salt)
      .digest('hex');
    return computedHash === originalHash;  // ❌ Timing attack vulnerable
  }

  // ❌ Weak password requirements
  @MinLength(6)  // ❌ Too short!
  password: string;
}
```

**Correct:**

```typescript
// auth/password.service.ts - Secure ✅
import { Injectable } from '@nestjs/common';

@Injectable()
export class PasswordService {
  /**
   * Hash a password using Bun's built-in argon2 implementation.
   * Automatically handles salt generation and hashing parameters.
   */
  async hash(password: string): Promise<string> {
    return Bun.password.hash(password);
  }

  /**
   * Verify a password against a stored hash.
   * Uses timing-safe comparison to prevent timing attacks.
   */
  async verify(password: string, hash: string): Promise<boolean> {
    return Bun.password.verify(password, hash);
  }

  /**
   * Hash with custom algorithm and options
   * Bun supports both argon2id (default, more secure) and bcrypt (widely compatible)
   * Algorithm is stored in the hash prefix, so verify() auto-detects it
   */
  async hashWithOptions(password: string): Promise<string> {
    return Bun.password.hash(password, {
      algorithm: 'argon2id',  // 'argon2id' or 'bcrypt'
      memoryCost: 16,         // Memory in MB (argon2 only)
      timeCost: 3,            // Number of iterations
    });
  }

  /**
   * Hash with bcrypt for legacy compatibility
   * Use when migrating from bcrypt or need broader library compatibility
   */
  async hashWithBcrypt(password: string): Promise<string> {
    return Bun.password.hash(password, {
      algorithm: 'bcrypt',
      cost: 12,  // bcrypt work factor (4-31, default 10)
    });
  }

  /**
   * Generate a secure random password for reset tokens
   */
  generateSecureToken(length: number = 32): string {
    const bytes = new Uint8Array(length);
    crypto.getRandomValues(bytes);
    return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
  }
}

// auth/auth.service.ts - Secure ✅
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { PasswordService } from './password.service';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private passwordService: PasswordService,
    private jwtService: JwtService,
  ) {}

  /**
   * Register a new user with secure password hashing
   */
  async register(dto: RegisterDto) {
    // ✅ Check if user exists first
    const existingUser = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });

    if (existingUser) {
      // ✅ Generic error message - don't reveal if user exists
      throw new BadRequestException('Unable to create account');
    }

    // ✅ Hash password with Bun's secure implementation
    const hashedPassword = await this.passwordService.hash(dto.password);

    const user = await this.prisma.user.create({
      data: {
        email: dto.email,
        password: hashedPassword,
        // ✅ Store only the hash
      },
      select: {
        id: true,
        email: true,
        createdAt: true,
        // ✅ Never return password in responses
      },
    });

    // ✅ Generate tokens
    const tokens = await this.generateTokens(user);

    return {
      user,
      ...tokens,
    };
  }

  /**
   * Login with timing-safe password verification
   */
  async login(dto: LoginDto) {
    // ✅ Always perform lookup to prevent timing attacks
    const user = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });

    if (!user) {
      // ✅ Use the same error message as invalid password
      throw new UnauthorizedException('Invalid credentials');
    }

    // ✅ Timing-safe password verification
    const isValid = await this.passwordService.verify(dto.password, user.password);

    if (!isValid) {
      // ✅ Same error message - don't reveal if user exists
      throw new UnauthorizedException('Invalid credentials');
    }

    // ✅ Check if hash needs rehashing (algorithm upgraded)
    if (Bun.password.needsRehash(user.password)) {
      // Rehash with current best algorithm
      const newHash = await this.passwordService.hash(dto.password);
      await this.prisma.user.update({
        where: { id: user.id },
        data: { password: newHash },
      });
    }

    return this.generateTokens(user);
  }

  /**
   * Change password with old password verification
   */
  async changePassword(userId: string, dto: ChangePasswordDto) {
    const user = await this.prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // ✅ Verify old password
    const isValid = await this.passwordService.verify(dto.oldPassword, user.password);

    if (!isValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // ✅ Hash new password
    const newHashedPassword = await this.passwordService.hash(dto.newPassword);

    await this.prisma.user.update({
      where: { id: userId },
      data: { password: newHashedPassword },
    });

    return { message: 'Password changed successfully' };
  }

  /**
   * Reset password with secure token
   */
  async resetPassword(token: string, newPassword: string) {
    // Find valid reset token
    const resetToken = await this.prisma.passwordResetToken.findUnique({
      where: { token },
      include: { user: true },
    });

    if (!resetToken || resetToken.expiresAt < new Date()) {
      throw new BadRequestException('Invalid or expired reset token');
    }

    // ✅ Hash new password
    const hashedPassword = await this.passwordService.hash(newPassword);

    await this.prisma.$transaction([
      this.prisma.user.update({
        where: { id: resetToken.user.id },
        data: { password: hashedPassword },
      }),
      this.prisma.passwordResetToken.delete({
        where: { id: resetToken.id },
      }),
    ]);

    return { message: 'Password reset successfully' };
  }

  private async generateTokens(user: any) {
    const payload = { sub: user.id, email: user.email };
    const accessToken = await this.jwtService.signAsync(payload);
    return { accessToken };
  }
}

// auth/dto/register.dto.ts - Strong password requirements ✅
import { IsEmail, IsString, MinLength, Matches } from 'class-validator';

export class RegisterDto {
  @IsEmail({}, { message: 'Please provide a valid email address' })
  email: string;

  @IsString()
  @MinLength(12, { message: 'Password must be at least 12 characters long' })
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/, {
    message: 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*?&)',
  })
  password: string;
}

// auth/dto/change-password.dto.ts ✅
import { IsString, MinLength, Matches } from 'class-validator';

export class ChangePasswordDto {
  @IsString()
  oldPassword: string;

  @IsString()
  @MinLength(12)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/)
  newPassword: string;
}

// prisma/schema.prisma - Correct schema ✅
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String   // ✅ Store hash as TEXT (can be up to 255 chars)

  // ✅ Index for faster login lookups
  @@index([email])
}
```

## Algorithm Selection: Argon2 vs Bcrypt

Bun's password hashing supports both algorithms at runtime. The algorithm choice is stored in the hash prefix, so `verify()` auto-detects which algorithm was used.

### When to Use Argon2 (Default)

```typescript
// ✅ Recommended for new applications
async hash(password: string) {
  return Bun.password.hash(password);  // Uses argon2id by default
}

// Or explicitly
async hash(password: string) {
  return Bun.password.hash(password, {
    algorithm: 'argon2id',
    memoryCost: 16,  // MB of memory (higher = more GPU-resistant)
    timeCost: 2,     // Number of iterations
  });
}
```

**Use argon2id when:**
- Starting a new application (recommended default)
- Maximum security against GPU/ASIC attacks is required
- Memory-hard hashing is acceptable
- Compliance requirements mandate modern algorithms

### When to Use Bcrypt

```typescript
// ✅ For legacy compatibility or cross-platform needs
async hash(password: string) {
  return Bun.password.hash(password, {
    algorithm: 'bcrypt',
    cost: 12,  // Work factor (2^12 iterations)
  });
}
```

**Use bcrypt when:**
- Migrating from existing bcrypt hashes
- Need compatibility with older systems/libraries
- Memory constraints prevent argon2 usage
- Regulatory requirements specifically mandate bcrypt

### Runtime Algorithm Flexibility

```typescript
// ✅ Configure algorithm per environment
@Injectable()
export class PasswordService {
  constructor(private configService: ConfigService) {}

  private get algorithm(): 'argon2id' | 'bcrypt' {
    // Runtime configuration from environment
    return this.configService.get('PASSWORD_ALGORITHM', 'argon2id');
  }

  async hash(password: string): Promise<string> {
    return Bun.password.hash(password, { algorithm: this.algorithm });
  }

  // ✅ verify() auto-detects algorithm from hash prefix
  async verify(password: string, hash: string): Promise<boolean> {
    return Bun.password.verify(password, hash);
  }
}
```

### Hash Format and Auto-Detection

Bun stores the algorithm in the hash prefix, enabling seamless migration:

```typescript
// Argon2 hash format: $argon2id$v=19$m=16,t=3,p=1$...
const argon2Hash = '$argon2id$v=19$m=16,t=3,p=1$salt$hash';

// Bcrypt hash format: $2b$12$...
const bcryptHash = '$2b$12$salt$hash';

// ✅ verify() auto-detects from prefix
await Bun.password.verify(password, argon2Hash);  // Uses argon2
await Bun.password.verify(password, bcryptHash);  // Uses bcrypt
```

### Migration Strategy

```typescript
// ✅ Gradual migration from bcrypt to argon2
@Injectable()
export class PasswordService {
  async hash(password: string): Promise<string> {
    // Use argon2 for new passwords
    return Bun.password.hash(password, { algorithm: 'argon2id' });
  }

  async verify(password: string, hash: string): Promise<boolean> {
    const isValid = await Bun.password.verify(password, hash);

    // Rehash bcrypt passwords with argon2 on successful login
    if (isValid && hash.startsWith('$2b$')) {
      // bcrypt detected - rehash with argon2
      const newHash = await this.hash(password);
      await this.updateUserPassword(newHash);
    }

    return isValid;
  }
}
```

## Migration Strategy

### Migrating from bcrypt/argon2 Packages

```typescript
// auth/migration/password-migration.service.ts ✅
import { Injectable, Logger } from '@nestjs/common';
import { PasswordService } from '../password.service';

@Injectable()
export class PasswordMigrationService {
  private readonly logger = new Logger(PasswordMigrationService.name);

  constructor(
    private prisma: PrismaService,
    private passwordService: PasswordService,
  ) {}

  /**
   * Migrate all passwords to Bun's native hashing
   */
  async migratePasswords() {
    const users = await this.prisma.user.findMany({
      where: {
        // Identify old hashes by prefix or pattern
        password: { startsWith: '$2a$' },  // bcrypt prefix
      },
      take: 100,  // Process in batches
    });

    let migrated = 0;

    for (const user of users) {
      try {
        // Note: We can't directly migrate without knowing original passwords
        // Instead, rehash on next login

        this.logger.log(`User ${user.email} will be migrated on next login`);

        // Set a flag to indicate migration needed
        await this.prisma.user.update({
          where: { id: user.id },
          data: { needsPasswordMigration: true },
        });

        migrated++;
      } catch (error) {
        this.logger.error(`Failed to migrate user ${user.id}`, error);
      }
    }

    return { migrated, total: users.length };
  }

  /**
   * Migrate on login (in AuthService)
   */
  async migrateOnLogin(user: User, plainPassword: string): Promise<void> {
    if (!user.needsPasswordMigration) {
      return;
    }

    // Verify with old method first
    const oldHashValid = await this.verifyOldPassword(plainPassword, user.password);

    if (oldHashValid) {
      // Rehash with Bun
      const newHash = await this.passwordService.hash(plainPassword);

      await this.prisma.user.update({
        where: { id: user.id },
        data: {
          password: newHash,
          needsPasswordMigration: false,
        },
      });

      this.logger.log(`Migrated password for user ${user.email}`);
    }
  }

  private async verifyOldPassword(password: string, hash: string): Promise<boolean> {
    // Old verification logic (bcrypt, etc.)
    return true;
  }
}
```

## Security Best Practices

### Password Requirements

```typescript
// auth/constants/password-requirements.ts ✅
export const PASSWORD_REQUIREMENTS = {
  minLength: 12,
  maxLength: 128,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
  allowedSpecialChars: '@$!%*?&',
  commonPasswordsBlacklist: [
    'password', '123456', 'qwerty', 'admin', 'welcome',
    // Add more common passwords
  ],
};
```

### Rate Limiting for Auth Endpoints

```typescript
// auth/auth.controller.ts ✅
import { Throttle } from '@nestjs/throttler';

@Controller('auth')
export class AuthController {
  @Post('register')
  @Throttle({ default: { limit: 3, ttl: 3600000 } })  // 3 per hour
  async register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }

  @Post('login')
  @Throttle({ default: { limit: 5, ttl: 60000 } })  // 5 per minute
  async login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }
}
```

### Logging Security Events

```typescript
// auth/auth.service.ts ✅
@Injectable()
export class AuthService {
  async login(dto: LoginDto) {
    const user = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });

    const isValid = user
      ? await this.passwordService.verify(dto.password, user.password)
      : false;

    // ✅ Log failed attempts (but not passwords!)
    if (!isValid) {
      await this.auditService.log({
        event: 'LOGIN_FAILED',
        email: dto.email,
        ip: dto.ip,
        userAgent: dto.userAgent,
      });
    }

    // ... rest of logic
  }
}
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Use `Bun.password.hash()` | Argon2/bcrypt with runtime algorithm selection |
| Use `Bun.password.verify()` | Auto-detects algorithm, timing-safe comparison |
| Prefer argon2 for new apps | Memory-hard, GPU-resistant, modern standard |
| Use bcrypt for compatibility | Legacy systems, cross-platform needs |
| Configure algorithm at runtime | Environment-specific, flexible migration |
| Enforce strong passwords | Prevents brute force attacks |
| Generic error messages | Prevents user enumeration |
| Never log passwords | Logs can be compromised |
| Rehash on algorithm upgrade | Seamless migration between algorithms |
| Rate limit auth endpoints | Prevents brute force attacks |

**Sources:**
- [Bun Crypto Documentation](https://bun.sh/docs/api/crypto)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Argon2 RFC](https://datatracker.ietf.org/doc/html/rfc9106)
