/**
 * Knowledge Base - Curated examples and patterns
 */

// Built-in knowledge base
const knowledgeBase = [
  // Security patterns
  {
    intent: 'security',
    languages: ['javascript', 'typescript'],
    category: 'common-pitfalls',
    title: 'DON\'T: Plain text passwords',
    content: `// ❌ NEVER store passwords as plain text
const user = { password: inputPassword }; // Vulnerable!

// ✅ ALWAYS hash passwords
import bcrypt from 'bcrypt';
const saltRounds = 12;
const hashedPassword = await bcrypt.hash(inputPassword, saltRounds);
const isValid = await bcrypt.compare(inputPassword, hashedPassword);`,
    tags: ['auth', 'password', 'security', 'bcrypt'],
    votes: 950
  },
  {
    intent: 'security',
    languages: ['javascript', 'typescript'],
    category: 'common-pitfalls',
    title: 'DON\'T: SQL injection via string concatenation',
    content: `// ❌ NEVER build SQL with string concatenation
const query = "SELECT * FROM users WHERE id = " + userId; // SQL Injection!

// ✅ Use parameterized queries
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);`,
    tags: ['sql', 'injection', 'security', 'database'],
    votes: 920
  },
  {
    intent: 'security',
    languages: ['javascript', 'typescript'],
    category: 'common-pitfalls',
    title: 'DON\'T: Use eval() for dynamic code',
    content: `// ❌ NEVER use eval() or new Function()
const perms = eval(userInput); // Code injection!

// ✅ Use safe alternatives
const actions = {
  read: () => doRead(),
  write: () => doWrite()
};
actions[userInput]?.();`,
    tags: ['eval', 'injection', 'security'],
    votes: 880
  },
  {
    intent: 'security',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ JWT best practices',
    content: `// ✅ JWT Security Checklist:
// 1. Use RS256 (asymmetric) not HS256
// 2. Set short expiration (15min access, 7d refresh)
// 3. Store refresh token in httpOnly cookie
// 4. Validate issuer (iss) and audience (aud)
// 5. Blacklist tokens on logout

import jwt from 'jsonwebtoken';
const token = jwt.sign(payload, privateKey, {
  algorithm: 'RS256',
  expiresIn: '15m',
  issuer: 'your-app'
});`,
    tags: ['jwt', 'auth', 'token', 'security'],
    votes: 850
  },
  {
    intent: 'security',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Helmet.js for Express',
    content: `// ✅ Use Helmet to set secure HTTP headers
import helmet from 'helmet';
app.use(helmet());

// Fine-tune specific headers
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
  }
}));`,
    tags: ['express', 'helmet', 'headers', 'security'],
    votes: 720
  },
  
  // General JavaScript patterns
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Async/await error handling',
    content: `// ✅ Proper async error handling
async function fetchData() {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(\`HTTP \${response.status}\`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error; // Re-throw or handle
  }
}`,
    tags: ['async', 'error-handling', 'promise'],
    votes: 810
  },
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Environment config pattern',
    content: `// ✅ Use environment variables with defaults
import dotenv from 'dotenv';
dotenv.config();

export const config = {
  db: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    name: process.env.DB_NAME || 'app_dev',
  },
  jwt: {
    secret: process.env.JWT_SECRET, // Required - fail if missing
    expiresIn: process.env.JWT_EXPIRES_IN || '15m',
  }
};

// Validate required vars at startup
if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET is required');
}`,
    tags: ['config', 'environment', 'dotenv'],
    votes: 780
  },
  
  // Node.js/Express patterns
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Express route handler structure',
    content: `// ✅ Clean Express route handler
import { Router } from 'express';
const router = Router();

// Controller functions separated from routes
const userController = {
  async getUser(req, res, next) {
    try {
      const user = await User.findById(req.params.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      next(error); // Pass to error middleware
    }
  }
};

router.get('/:id', userController.getUser);
export default router;`,
    tags: ['express', 'router', 'structure', 'clean-code'],
    votes: 750
  },
  {
    intent: 'fix',
    languages: ['javascript', 'typescript'],
    category: 'common-pitfalls',
    title: 'DON\'T: Mutation in React state',
    content: `// ❌ NEVER mutate state directly
setUser({ ...user });
user.name = newName; // Won't trigger re-render!

// ✅ Use immutable patterns
setUser(prev => ({
  ...prev,
  name: newName
}));

// Or with Immer
setUser(draft => {
  draft.name = newName;
});`,
    tags: ['react', 'state', 'mutation', 'immutable'],
    votes: 840
  },
  {
    intent: 'optimize',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Debounce and throttle utilities',
    content: `// ✅ Debounce - wait for idle
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// ✅ Throttle - limit frequency
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Usage
const handleSearch = debounce(async (query) => {
  const results = await search(query);
  setResults(results);
}, 300);`,
    tags: ['performance', 'debounce', 'throttle', 'optimize'],
    votes: 820
  },
  
  // Python patterns
  {
    intent: 'write',
    languages: ['python'],
    category: 'recommended-patterns',
    title: '✅ Python type hints',
    content: `from typing import Optional, List

def get_user(user_id: int) -> Optional[dict]:
    """Get user by ID with type hints."""
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    return user if user else None

def process_items(items: List[str]) -> List[str]:
    """Process a list of items."""
    return [item.strip().lower() for item in items]`,
    types: ['python', 'typing', 'type-hints'],
    votes: 700
  },
  {
    intent: 'security',
    languages: ['python'],
    category: 'recommended-patterns',
    title: '✅ Python SQL injection prevention',
    content: `# ✅ Use parameterized queries in Python
cursor.execute(
    "SELECT * FROM users WHERE id = %s",  # Note: %s not f-string!
    (user_id,)
)

# ✅ Or use SQLAlchemy ORM
user = session.query(User).filter(User.id == user_id).first()

# ❌ NEVER do this:
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")`,
    tags: ['python', 'sql', 'injection', 'sqlalchemy'],
    votes: 850
  },
  
  // API design
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ RESTful API response format',
    content: `// ✅ Consistent API response format
function successResponse(data, meta = {}) {
  return {
    success: true,
    data,
    meta: { timestamp: new Date().toISOString(), ...meta }
  };
}

function errorResponse(message, code = 'ERROR', status = 400) {
  return {
    success: false,
    error: { message, code, status }
  };
}

// Usage
app.get('/api/users', (req, res) => {
  const users = User.findAll();
  res.json(successResponse(users, { total: users.length }));
});`,
    tags: ['api', 'rest', 'response-format'],
    votes: 680
  },

  // Docker patterns
  {
    intent: 'write',
    languages: ['bash'],
    category: 'recommended-patterns',
    title: '✅ Docker multi-stage build for Node.js',
    content: `# ✅ Multi-stage build for smaller images
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]`,
    tags: ['docker', 'node', 'container', 'build'],
    votes: 800
  },
  {
    intent: 'write',
    languages: ['bash'],
    category: 'common-pitfalls',
    title: "DON'T: Run containers as root",
    content: `# ❌ NEVER run as root in production
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "index.js"]

# ✅ Always create and use non-root user
FROM node:20-alpine
WORKDIR /app
COPY --chown=node:node . .
USER node
CMD ["node", "index.js"]`,
    tags: ['docker', 'security', 'root'],
    votes: 750
  },

  // Git patterns
  {
    intent: 'write',
    languages: ['bash'],
    category: 'recommended-patterns',
    title: '✅ Conventional commits',
    content: `# ✅ Use conventional commits for clear changelog
feat: add user authentication
fix: resolve CORS issue in API
docs: update README with installation
style: format code with prettier
refactor: simplify error handling
test: add unit tests for auth controller
chore: update dependencies

# ✅ Use git hooks to enforce
npx husky add .husky/commit-msg 'npx commitlint --edit "$1"'`,
    tags: ['git', 'commit', 'conventional'],
    votes: 700
  },

  // Testing patterns
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Jest unit test structure',
    content: `// ✅ Clean Jest test structure
describe('UserService', () => {
  let userService;
  let mockDb;

  beforeEach(() => {
    mockDb = { findById: jest.fn() };
    userService = new UserService(mockDb);
  });

  describe('getUser', () => {
    it('should return user when found', async () => {
      const mockUser = { id: 1, name: 'John' };
      mockDb.findById.mockResolvedValue(mockUser);

      const result = await userService.getUser(1);

      expect(result).toEqual(mockUser);
      expect(mockDb.findById).toHaveBeenCalledWith(1);
    });

    it('should throw NotFoundError when user missing', async () => {
      mockDb.findById.mockResolvedValue(null);

      await expect(userService.getUser(999)).rejects.toThrow(NotFoundError);
    });
  });
});`,
    tags: ['jest', 'test', 'unit-test', 'tdd'],
    votes: 820
  },
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ React Testing Library best practices',
    content: `// ✅ Test behavior, not implementation
import { render, screen, fireEvent } from '@testing-library/react';

test('should login user with valid credentials', async () => {
  render(<Login />);

  // Query by accessible name (label, placeholder, aria-label)
  const emailInput = screen.getByLabelText(/email/i);
  const passwordInput = screen.getByLabelText(/password/i);
  const submitButton = screen.getByRole('button', { name: /submit/i });

  fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
  fireEvent.change(passwordInput, { target: { value: 'password123' } });
  fireEvent.click(submitButton);

  // Assert the outcome, not the implementation
  await screen.findByText(/welcome/i);
});`,
    tags: ['react', 'testing-library', 'jest', 'test'],
    votes: 780
  },

  // TypeScript patterns
  {
    intent: 'write',
    languages: ['typescript'],
    category: 'recommended-patterns',
    title: '✅ TypeScript strict null handling',
    content: `// ✅ Use strict null checks
interface User {
  id: number;
  name: string;
  email?: string; // Optional
}

function getEmail(user: User): string {
  // ❌ BAD: user.email could be undefined!
  return user.email.toLowerCase();

  // ✅ GOOD: Handle undefined
  return user.email?.toLowerCase() ?? 'no email';
}

// ✅ Use type guards
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}

function process(obj: unknown) {
  if (isUser(obj)) {
    console.log(obj.name); // TypeScript knows it's User
  }
}`,
    tags: ['typescript', 'null', 'undefined', 'type-guard'],
    votes: 750
  },
  {
    intent: 'write',
    languages: ['typescript'],
    category: 'recommended-patterns',
    title: '✅ TypeScript discriminated unions',
    content: `// ✅ Use discriminated unions for type-safe state
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function handleState(state: RequestState<User>) {
  switch (state.status) {
    case 'idle':
      return 'Start loading';
    case 'loading':
      return 'Loading...';
    case 'success':
      return state.data.name; // TypeScript knows data exists
    case 'error':
      return state.error.message; // TypeScript knows error exists
  }
}

// ✅ Exhaustiveness check
function exhaustive(state: RequestState<User>) {
  // TypeScript errors if we miss a case
  const _exhaustive: never = state;
}`,
    tags: ['typescript', 'union', 'state', 'pattern'],
    votes: 720
  },

  // Error handling
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Custom error classes',
    content: `// ✅ Create custom errors for better error handling
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR'
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(\`\${resource} not found\`, 404, 'NOT_FOUND');
  }
}

class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

// Usage
throw new NotFoundError('User');`,
    tags: ['error', 'exception', 'class', 'handling'],
    votes: 710
  },

  // Redis patterns
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Redis caching with TTL',
    content: `// ✅ Cache with expiration
const CACHE_TTL = 300; // 5 minutes

async function getCachedUser(userId: number) {
  const cacheKey = \`user:\${userId}\`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Fetch from DB
  const user = await db.findUser(userId);

  // Store in cache with TTL
  if (user) {
    await redis.setex(cacheKey, CACHE_TTL, JSON.stringify(user));
  }

  return user;
}

// ✅ Invalidate cache on update
async function updateUser(userId: number, data: UserData) {
  const user = await db.updateUser(userId, data);
  await redis.del(\`user:\${userId}\`); // Invalidate
  return user;
}`,
    tags: ['redis', 'cache', 'performance'],
    votes: 680
  },

  // Rate limiting
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Express rate limiting',
    content: `// ✅ Rate limiting in Express
import rateLimit from 'express-rate-limit';

// General API limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per window
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

// Strict limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 attempts
  skipSuccessfulRequests: true,
});

app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);`,
    tags: ['express', 'rate-limit', 'security', 'ddos'],
    votes: 740
  },

  // Input validation
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Zod schema validation',
    content: `// ✅ Use Zod for runtime validation
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  age: z.number().int().min(13).max(120).optional(),
  role: z.enum(['user', 'admin', 'moderator']),
});

type User = z.infer<typeof UserSchema>;

// Validate incoming request
function validateUser(data: unknown): User {
  return UserSchema.parse(data);
}

// Express middleware with Zod
import { zodMiddleware } from './middleware';

app.post('/users', zodMiddleware(UserSchema), createUser);`,
    tags: ['validation', 'zod', 'schema', 'runtime'],
    votes: 760
  },

  // Environment variables
  {
    intent: 'write',
    languages: ['javascript', 'typescript', 'python'],
    category: 'common-pitfalls',
    title: "DON'T: Secret keys in source code",
    content: `// ❌ NEVER hardcode secrets
const apiKey = 'sk_live_123456789'; // Exposed in git!
const dbPassword = 'mysecretpass';

// ✅ Use environment variables
const apiKey = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;

if (!apiKey) {
  throw new Error('API_KEY is required');
}

// ✅ Use .env file (add to .gitignore)
// .env:
// API_KEY=sk_live_123456789
// DB_PASSWORD=secret

// ✅ Validate at startup
const config = {
  apiKey: z.string().parse(process.env.API_KEY),
  port: z.number().default(3000).parse(process.env.PORT),
};`,
    tags: ['security', 'env', 'secrets', 'configuration'],
    votes: 890
  },

  // Logging
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Structured logging with Pino',
    content: `// ✅ Use Pino for structured JSON logging
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
});

// ✅ Log with context
logger.info({ userId: user.id, action: 'login' }, 'User logged in');
logger.error({ err: error, userId: user.id }, 'Login failed');

// ✅ Child loggers for request context
const childLogger = logger.child({ requestId: req.id });
childLogger.info('Processing request');

// ✅ Avoid string interpolation
// ❌ BAD: logger.info('User ' + user.id + ' logged in');
// ✅ GOOD: logger.info({ userId: user.id }, 'User logged in');`,
    tags: ['logging', 'pino', 'structured', 'monitoring'],
    votes: 650
  },

  // React patterns
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ React custom hooks',
    content: `// ✅ Extract logic into custom hooks
function useUser(userId: number) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}

// Usage in component
function UserProfile({ userId }: { userId: number }) {
  const { user, loading, error } = useUser(userId);

  if (loading) return <Spinner />;
  if (error) return <Error error={error} />;

  return <div>{user.name}</div>;
}`,
    tags: ['react', 'hooks', 'custom', 'reuse'],
    votes: 800
  },

  // File handling
  {
    intent: 'write',
    languages: ['python'],
    category: 'common-pitfalls',
    title: "DON'T: Leave files open",
    content: `# ❌ BAD: May leave file open on error
f = open('file.txt', 'r')
data = f.read()
f.close()

# ✅ GOOD: Use context manager
with open('file.txt', 'r') as f:
    data = f.read()
# File automatically closed

# ✅ BEST: Use pathlib
from pathlib import Path
content = Path('file.txt').read_text()

# Write with encoding
Path('output.txt').write_text(data, encoding='utf-8')`,
    tags: ['python', 'file', 'io', 'context-manager'],
    votes: 720
  },

  // SQL/ORM patterns
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ Prisma query patterns',
    content: `// ✅ Prisma - always include select/where
const user = await prisma.user.findUnique({
  where: { id: userId },
  select: { id: true, email: true, name: true } // Only what you need
});

// ✅ Pagination
const page = 1;
const limit = 10;
const users = await prisma.user.findMany({
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { createdAt: 'desc' }
});

// ✅ Transaction for related writes
await prisma.$transaction([
  prisma.order.create({ data: orderData }),
  prisma.inventory.update({ where: { id: itemId }, data: { stock: { decrement: 1 } } })
]);`,
    tags: ['prisma', 'orm', 'database', 'query'],
    votes: 700
  },

  // WebSocket
  {
    intent: 'write',
    languages: ['javascript', 'typescript'],
    category: 'recommended-patterns',
    title: '✅ WebSocket with reconnection',
    content: `// ✅ WebSocket with auto-reconnection
class WSClient {
  constructor(url) {
    this.url = url;
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => console.log('Connected');
    this.ws.onclose = () => this.reconnect();
    this.ws.onerror = (err) => console.error('WS Error:', err);
  }

  reconnect() {
    setTimeout(() => {
      console.log('Reconnecting...');
      this.connect();
    }, 1000);
  }

  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}`,
    tags: ['websocket', 'reconnection', 'realtime'],
    votes: 650
  }
];

let customKB = [];

// Security-related keywords that should boost security patterns
const SECURITY_KEYWORDS = ['auth', 'jwt', 'token', 'password', 'login', 'security', 'secure', 'credential', 'session', 'oauth', 'access', 'permission', 'role'];

/**
 * Search the knowledge base
 */
export function searchKnowledgeBase(parsed) {
  const results = [];
  
  // Check for security keywords in the parsed query
  const hasSecurityKeyword = parsed.keywords.some(k => 
    SECURITY_KEYWORDS.some(sk => k.toLowerCase().includes(sk))
  );

  const intentMatch = (item) => {
    if (!parsed.intents.length) return true;
    return parsed.intents.some(i => item.intent === i || item.content.toLowerCase().includes(i));
  };
  
  const langMatch = (item) => {
    if (!parsed.languages.length) return true;
    return parsed.languages.some(l => item.languages?.includes(l));
  };
  
  const keywordMatch = (item) => {
    if (!parsed.keywords.length) return true;
    return parsed.keywords.some(k => 
      item.title.toLowerCase().includes(k) || 
      item.content.toLowerCase().includes(k) ||
      item.tags?.some(t => t.includes(k))
    );
  };

  const allItems = [...knowledgeBase, ...customKB];
  
  for (const item of allItems) {
    let score = 0;
    
    // Intent match (highest weight)
    if (parsed.intents.some(i => item.intent === i)) score += 5;
    else if (intentMatch(item)) score += 1;
    
    // Language match - stronger weight for language-specific patterns
    if (parsed.languages.length && langMatch(item)) score += 5;
    // Penalize items with language restrictions that don't match
    else if (item.languages?.length && !langMatch(item)) score -= 3;
    
    // Keyword match in title/content/tags
    const km = keywordMatch(item);
    if (km) score += 3;
    
    // Security items get bonus for security keywords in query
    if (hasSecurityKeyword && (item.category === 'common-pitfalls' || item.tags?.some(t => SECURITY_KEYWORDS.includes(t)))) {
      score += 5;
    }
    
    // Security items get bonus for high security level
    if (parsed.securityLevel === 'high' && item.category === 'common-pitfalls') {
      score += 4;
    }

    if (score > 0) {
      results.push({
        ...item,
        score,
        relevance: score > 8 ? 'high' : score > 4 ? 'medium' : 'low'
      });
    }
  }

  // Sort by score, then by votes
  results.sort((a, b) => b.score - a.score || (b.votes || 0) - (a.votes || 0));
  
  return results.slice(0, 8);
}

/**
 * Add items to custom knowledge base
 */
export function addToKnowledgeBase(items) {
  customKB.push(...items);
  console.log(`📚 Added ${items.length} items to knowledge base`);
}