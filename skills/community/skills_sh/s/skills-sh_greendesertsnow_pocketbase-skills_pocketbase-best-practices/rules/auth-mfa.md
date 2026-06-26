---
title: Implement Multi-Factor Authentication
impact: HIGH
impactDescription: Additional security layer for sensitive applications
tags: authentication, mfa, security, 2fa, otp
---

## Implement Multi-Factor Authentication

MFA requires users to authenticate with two different methods. PocketBase supports OTP (One-Time Password) via email as the second factor.

**Incorrect (single-factor only for sensitive apps):**

```javascript
// Insufficient for sensitive applications
async function login(email, password) {
  const authData = await pb.collection('users').authWithPassword(email, password);
  // User immediately has full access - no second factor
  return authData;
}
```

**Correct (MFA flow with OTP):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

async function loginWithMFA(email, password) {
  try {
    // First factor: password
    const authData = await pb.collection('users').authWithPassword(email, password);

    // If MFA not required, auth succeeds immediately
    return { success: true, authData };

  } catch (error) {
    // MFA required - returns 401 with mfaId
    if (error.status === 401 && error.response?.mfaId) {
      return {
        success: false,
        mfaRequired: true,
        mfaId: error.response.mfaId
      };
    }
    throw error;
  }
}

async function requestOTP(email) {
  // Request OTP to be sent via email
  const result = await pb.collection('users').requestOTP(email);

  // Returns otpId - needed to verify the OTP
  // Note: Returns otpId even if email doesn't exist (prevents enumeration)
  return result.otpId;
}

async function completeMFAWithOTP(mfaId, otpId, otpCode) {
  try {
    // Second factor: OTP verification
    const authData = await pb.collection('users').authWithOTP(
      otpId,
      otpCode,
      { mfaId }  // Include mfaId from first factor
    );

    return { success: true, authData };
  } catch (error) {
    if (error.status === 400) {
      throw new Error('Invalid or expired code');
    }
    throw error;
  }
}

// Complete flow example
async function fullMFAFlow(email, password, otpCode = null) {
  // Step 1: Password authentication
  const step1 = await loginWithMFA(email, password);

  if (step1.success) {
    return step1.authData;  // MFA not required
  }

  if (step1.mfaRequired) {
    // Step 2: Request OTP
    const otpId = await requestOTP(email);

    // Step 3: UI prompts user for OTP code...
    // (In real app, wait for user input)

    if (otpCode) {
      // Step 4: Complete MFA
      const step2 = await completeMFAWithOTP(step1.mfaId, otpId, otpCode);
      return step2.authData;
    }

    return { pendingMFA: true, mfaId: step1.mfaId, otpId };
  }
}
```

**Configure MFA (Admin UI or API):**

```javascript
// Enable MFA on auth collection (superuser only)
await pb.collections.update('users', {
  mfa: {
    enabled: true,
    duration: 1800,  // MFA session duration (30 min)
    rule: ''  // When to require MFA (empty = always for all users)
    // rule: '@request.auth.role = "admin"' // Only for admins
  },
  otp: {
    enabled: true,
    duration: 300,  // OTP validity (5 min)
    length: 6,      // OTP code length
    emailTemplate: {
      subject: 'Your verification code',
      body: 'Your code is: {OTP}'
    }
  }
});
```

**MFA best practices:**
- Always enable for admin accounts
- Consider making MFA optional for regular users
- Use short OTP durations (5-10 minutes)
- Implement rate limiting on OTP requests
- Log MFA events for security auditing

Reference: [PocketBase MFA](https://pocketbase.io/docs/authentication/#mfa)
