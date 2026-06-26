/**
 * Email Validator - Local Logic (Client-side)
 * 
 * This is a LOCAL skill that runs entirely in your OpenClaw agent.
 * No external API calls, no API key required. Complete privacy.
 * 
 * Pricing: FREE (runs locally)
 */

// Input type
interface ValidateEmailInput {
  email: string;
}

// Output type
interface ValidateEmailOutput {
  valid: boolean;
  email: string;
  checks: {
    format_valid: boolean;
    domain: string;
    local_part: string;
    is_disposable: boolean;
  };
  risk_score: number;
  suggestion: string | null;
}

// Known disposable email domains
const DISPOSABLE_DOMAINS = [
  'mailinator.com',
  'guerrillamail.com',
  'tempmail.com',
  '10minutemail.com',
  'throwaway.email',
  'maildrop.cc',
  'yopmail.com',
  'temp-mail.org',
  'getnada.com',
  'trashmail.com',
];

// Free email providers (not disposable, but less trustworthy for B2B)
const FREE_EMAIL_PROVIDERS = [
  'gmail.com',
  'yahoo.com',
  'outlook.com',
  'hotmail.com',
  'icloud.com',
  'aol.com',
  'protonmail.com',
  'mail.com',
];

/**
 * Validate email format according to RFC 5322 (simplified)
 */
function isValidEmailFormat(email: string): boolean {
  // Basic email regex (simplified RFC 5322)
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  
  if (!emailRegex.test(email)) {
    return false;
  }
  
  // Check length constraints
  if (email.length < 3 || email.length > 254) {
    return false;
  }
  
  // Check local part length (before @)
  const [localPart, domain] = email.split('@');
  if (localPart.length > 64) {
    return false;
  }
  
  // Check domain has at least one dot and valid TLD
  if (!domain || !domain.includes('.')) {
    return false;
  }
  
  const tld = domain.split('.').pop();
  if (!tld || tld.length < 2) {
    return false;
  }
  
  return true;
}

/**
 * Calculate risk score based on email characteristics
 */
function calculateRiskScore(email: string, domain: string, localPart: string): number {
  let score = 10; // Start with low risk
  
  // Check if disposable domain
  if (DISPOSABLE_DOMAINS.includes(domain.toLowerCase())) {
    score += 70; // High risk
  }
  
  // Check if free email provider
  if (FREE_EMAIL_PROVIDERS.includes(domain.toLowerCase())) {
    score += 10; // Slight risk increase
  }
  
  // Check local part characteristics
  if (localPart.length < 3) {
    score += 20; // Very short local part
  }
  
  if (/^\d+$/.test(localPart)) {
    score += 30; // All numbers
  }
  
  // Cap at 100
  return Math.min(score, 100);
}

/**
 * Main function called by OpenClaw agent
 * @param input - Email address to validate
 * @returns Validation result with risk score
 */
export async function run(input: ValidateEmailInput): Promise<ValidateEmailOutput> {
  // Validate input
  if (!input.email || typeof input.email !== 'string') {
    throw new Error('Missing required field: email (string)');
  }
  
  const email = input.email.trim();
  
  if (email.length < 3 || email.length > 254) {
    throw new Error('email must be between 3 and 254 characters');
  }
  
  // Check format
  const formatValid = isValidEmailFormat(email);
  
  if (!formatValid) {
    return {
      valid: false,
      email: email.toLowerCase(),
      checks: {
        format_valid: false,
        domain: '',
        local_part: '',
        is_disposable: false,
      },
      risk_score: 90,
      suggestion: 'Please check the email format',
    };
  }
  
  // Extract parts
  const [localPart, domain] = email.split('@');
  const isDisposable = DISPOSABLE_DOMAINS.includes(domain.toLowerCase());
  
  // Calculate risk score
  const riskScore = calculateRiskScore(email, domain, localPart);
  
  return {
    valid: true,
    email: email.toLowerCase(),
    checks: {
      format_valid: true,
      domain: domain.toLowerCase(),
      local_part: localPart,
      is_disposable: isDisposable,
    },
    risk_score: riskScore,
    suggestion: null,
  };
}

// Default export for compatibility
export default run;
