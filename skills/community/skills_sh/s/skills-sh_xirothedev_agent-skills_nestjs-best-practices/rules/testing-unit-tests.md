---
title: Write Comprehensive Unit Tests
section: 10
impact: MEDIUM
impactDescription: Catches bugs early and enables safe refactoring
tags: testing, tdd, jest, quality
---

## Write Comprehensive Unit Tests

Untested code leads to regressions and production bugs. NestJS + Jest provides full testing support for controllers, services, and repositories. **Aim for 80%+ coverage on business logic.**

**Incorrect (no tests):**

```typescript
// users.service.ts - No tests 🚨
@Injectable()
export class UsersService {
  async createUser(data: CreateUserDto) {
    return this.prisma.user.create({ data });
  }
}
```

**Correct (full test suite):**

```typescript
// users.service.spec.ts
describe('UsersService', () => {
  let service: UsersService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [UsersService, { provide: PrismaService, useValue: mockPrisma }],
    }).compile();
    service = module.get(UsersService);
  });

  it('should create user successfully', async () => {
    const dto: CreateUserDto = { email: 'test@example.com', name: 'Test' };
    const mockUser = { id: '1', ...dto };

    jest.spyOn(prisma.user, 'create').mockResolvedValue(mockUser);

    const result = await service.createUser(dto);
    expect(result).toEqual(mockUser);
    expect(prisma.user.create).toHaveBeenCalledWith(expect.any(Object));
  });
});
```
