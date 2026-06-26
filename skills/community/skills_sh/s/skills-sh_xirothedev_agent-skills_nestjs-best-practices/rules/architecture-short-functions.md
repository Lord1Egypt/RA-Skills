---
title: Keep Functions Short and Single Purpose
impact: MEDIUM
section: 3
impactDescription: Improves testability and reduces bugs
tags: code-quality, functions, SRP, maintainability
---

## Keep Functions Short and Single Purpose

Long functions with multiple responsibilities are hard to test, debug, and maintain. Short functions (<20 lines) with one clear purpose are easier to understand. **Extract logic into focused helper functions.**

**Incorrect (god function):**

```typescript
@Post()
async createUser(@Body() data: any) {
  // 3 responsibilities mixed 🚨
  const hashedPassword = await bcrypt.hash(data.password, 10);
  const user = await this.prisma.user.create({ data: {...data, password: hashedPassword} });
  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET);
  await this.sendWelcomeEmail(user.email);
  return { user, token };
}
```

**Correct (single responsibility):**

```typescript
@Post()
async createUser(@Body() data: CreateUserDto) {
  const hashedPassword = await this.hashPassword(data.password);
  const user = await this.usersRepository.create({ ...data, password: hashedPassword });
  const token = this.generateToken(user.id);
  await this.emailService.sendWelcome(user.email);
  return { user, token };  // ✅ Orchestration only
}

private async hashPassword(password: string) {
  return bcrypt.hash(password, 10);
}
```