# Good and Bad Tests

## Good Tests

**Integration-style**：通过真实 interfaces 测试，而不是 mock internal parts。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特点：

- 测试 users/callers 关心的 behavior
- 只使用 public API
- 能经受 internal refactors
- 描述 WHAT，不描述 HOW
- 每个 test 一个逻辑断言

## Bad Tests

**Implementation-detail tests**：耦合内部结构。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

危险信号：

- Mocking internal collaborators
- Testing private methods
- 断言 call counts/order
- behavior 没变但 refactoring 后 test 失败
- test name 描述 HOW 而不是 WHAT
- 绕过 interface，通过外部手段验证

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```
