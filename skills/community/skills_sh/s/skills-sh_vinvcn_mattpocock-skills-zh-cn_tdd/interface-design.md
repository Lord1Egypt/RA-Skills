# Interface Design for Testability

好的 interfaces 会让测试自然发生：

1. **接收 dependencies，不要自己创建它们**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回 results，不要制造 side effects**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area**
   - Fewer methods = 需要的 tests 更少
   - Fewer params = test setup 更简单
