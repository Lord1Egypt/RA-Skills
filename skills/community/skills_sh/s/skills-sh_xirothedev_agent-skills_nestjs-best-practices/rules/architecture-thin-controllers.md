---
title: Single Responsibility - Separate Controller and Service
section: 3
impact: HIGH
impactDescription: Makes testing and maintenance easier
tags: architecture, separation, testing, SRP
---

Fat controllers mix HTTP concerns with business logic, making unit testing impossible. Controllers should only parse HTTP requests and delegate. **Controllers are thin, services are smart.**

> **Hint**: Controllers handle HTTP-specific concerns (validation, parsing, status codes). Services handle business logic (calculations, workflows, data transformations). This separation makes both layers independently testable.

## Controller vs Service Responsibilities

| Controllers (HTTP Layer) | Services (Business Layer) |
|--------------------------|---------------------------|
| Parse request bodies | Execute business logic |
| Validate with DTOs | Perform calculations |
| Return HTTP status codes | Transform data |
| Handle routing | Manage transactions |
| Set headers/cookies | Call external APIs |
| Upload/download files | Enforce business rules |

**Incorrect:**

```typescript
@Controller('orders')
export class OrdersController {
  constructor(private repository: OrdersRepository) {}

  @Post()
  async createOrder(@Body() data: any) {
    // 🚨 Validation logic
    if (!data.email || !this.isValidEmail(data.email)) {
      throw new BadRequestException('Invalid email');
    }

    // 🚨 Business logic - checking inventory
    const product = await this.repository.getProduct(data.productId);
    if (product.stock < data.quantity) {
      throw new BadRequestException('Insufficient stock');
    }

    // 🚨 Business logic - calculating discount
    let discount = 0;
    if (data.quantity > 10) {
      discount = 0.1;
    } else if (data.quantity > 5) {
      discount = 0.05;
    }

    // 🚨 Business logic - calculating total
    const subtotal = product.price * data.quantity;
    const total = subtotal * (1 - discount);

    // 🚨 Data access logic
    const order = await this.repository.save({
      productId: data.productId,
      quantity: data.quantity,
      total,
    });

    // 🚨 External service call
    await this.emailService.sendConfirmation(data.email, order.id);

    return order;
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

**Problems:**
- Cannot test business logic without HTTP context
- Cannot reuse business logic in other contexts (CLI, GraphQL, WebSocket)
- Difficult to mock dependencies for testing
- Changes to business logic require HTTP layer changes

**Correct:**

```typescript
// orders/orders.controller.ts
@Controller('orders')
export class OrdersController {
  constructor(private ordersService: OrdersService) {}

  @Post()
  createOrder(@Body() createOrderDto: CreateOrderDto) {
    // ✅ Only handles HTTP concerns
    return this.ordersService.create(createOrderDto);
  }

  @Get()
  findAll(@Query('status') status?: OrderStatus) {
    // ✅ Pass query params, let service handle filtering
    return this.ordersService.findAll(status);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.ordersService.findOne(id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateOrderDto: UpdateOrderDto) {
    return this.ordersService.update(id, updateOrderDto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id') id: string) {
    return this.ordersService.remove(id);
  }
}

// orders/orders.service.ts
@Injectable()
export class OrdersService {
  constructor(
    private ordersRepository: OrdersRepository,
    private productsRepository: ProductsRepository,
    private emailService: EmailService,
  ) {}

  async create(createOrderDto: CreateOrderDto) {
    // ✅ Business logic: validate inventory
    const product = await this.productsRepository.findOne(createOrderDto.productId);
    if (!product) {
      throw new NotFoundException('Product not found');
    }

    if (product.stock < createOrderDto.quantity) {
      throw new BadRequestException('Insufficient stock');
    }

    // ✅ Business logic: calculate pricing
    const pricing = this.calculatePricing(product, createOrderDto.quantity);

    // ✅ Business logic: create order
    const order = await this.ordersRepository.create({
      ...createOrderDto,
      subtotal: pricing.subtotal,
      discount: pricing.discount,
      total: pricing.total,
    });

    // ✅ Business logic: send confirmation
    await this.emailService.sendOrderConfirmation(order);

    return order;
  }

  private calculatePricing(product: Product, quantity: number) {
    const subtotal = product.price * quantity;

    // Volume discount rules
    let discount = 0;
    if (quantity >= 10) {
      discount = 0.1;
    } else if (quantity >= 5) {
      discount = 0.05;
    }

    return {
      subtotal,
      discount,
      total: subtotal * (1 - discount),
    };
  }

  findAll(status?: OrderStatus) {
    return this.ordersRepository.findAll(status);
  }

  findOne(id: string) {
    return this.ordersRepository.findOne(id);
  }

  update(id: string, updateOrderDto: UpdateOrderDto) {
    return this.ordersRepository.update(id, updateOrderDto);
  }

  remove(id: string) {
    return this.ordersRepository.remove(id);
  }
}
```

## Controller-Specific Concerns

Controllers SHOULD handle HTTP-specific details:

```typescript
@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)  // ✅ HTTP status codes
  async create(@Body() createUserDto: CreateUserDto, @Res() response: Response) {
    const user = await this.usersService.create(createUserDto);

    // ✅ Set headers
    response.setHeader('X-Resource-ID', user.id);

    // ✅ Custom response format
    response.json({
      success: true,
      data: user,
    });
  }

  @Get('export')
  @Header('Content-Type', 'text/csv')  // ✅ Content negotiation
  async export(@Res() response: Response) {
    const csv = await this.usersService.exportToCsv();
    response.send(csv);
  }

  @Post('upload')
  @UseInterceptors(FileInterceptor('file'))  // ✅ File upload handling
  async upload(@UploadedFile() file: Express.Multer.File) {
    return this.usersService.processUploadedFile(file);
  }

  @Get('search')
  async search(
    @Query('q') query: string,  // ✅ Query param parsing
    @Query('page', ParseIntPipe) page: number,  // ✅ Type transformation
    @Query('limit', new ParseIntPipe({ optional: true })) limit?: number,
  ) {
    return this.usersService.search(query, { page, limit });
  }
}
```

## Service Layer Best Practices

### Keep Services Pure Business Logic

```typescript
@Injectable()
export class PaymentsService {
  constructor(
    private stripeService: StripeService,
    private ordersRepository: OrdersRepository,
  ) {}

  async processPayment(orderId: string, paymentDto: PaymentDto) {
    // ✅ Business logic: retrieve order
    const order = await this.ordersRepository.findOne(orderId);
    if (!order) {
      throw new NotFoundException('Order not found');
    }

    // ✅ Business logic: validate order can be paid
    if (order.status !== OrderStatus.PENDING) {
      throw new BadRequestException('Order cannot be paid');
    }

    // ✅ Business logic: create payment intent
    const paymentIntent = await this.stripeService.createIntent({
      amount: order.total,
      currency: 'usd',
      metadata: { orderId: order.id },
    });

    // ✅ Business logic: update order status
    await this.ordersRepository.update(orderId, {
      paymentIntentId: paymentIntent.id,
      status: OrderStatus.PAID,
    });

    return paymentIntent;
  }
}
```

### Use Domain Events for Decoupling

```typescript
// orders/orders.service.ts
@Injectable()
export class OrdersService {
  constructor(
    private ordersRepository: OrdersRepository,
    private eventEmitter: EventEmitter2,
  ) {}

  async create(createOrderDto: CreateOrderDto) {
    const order = await this.ordersRepository.create(createOrderDto);

    // ✅ Emit event instead of directly calling email service
    this.eventEmitter.emit('order.created', {
      orderId: order.id,
      customerId: order.customerId,
      total: order.total,
    });

    return order;
  }
}

// email/email.service.ts
@Injectable()
export class EmailService {
  @OnEvent('order.created')
  async handleOrderCreated(payload: OrderCreatedEvent) {
    await this.sendOrderConfirmation(payload);
  }
}
```

## Testing Benefits

### Testing Controllers (HTTP Layer)

```typescript
describe('UsersController', () => {
  let controller: UsersController;
  let service: jest.Mocked<UsersService>;

  beforeEach(() => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: {
            create: jest.fn(),
            findAll: jest.fn(),
            findOne: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<UsersController>(UsersController);
    service = module.get(UsersService);
  });

  it('should create a user', () => {
    const createUserDto: CreateUserDto = {
      email: 'test@example.com',
      password: 'password123',
      name: 'Test User',
    };

    const expectedUser = { id: '1', ...createUserDto };
    service.create.mockResolvedValue(expectedUser);

    expect(controller.create(createUserDto)).resolves.toEqual(expectedUser);
    expect(service.create).toHaveBeenCalledWith(createUserDto);
  });
});
```

### Testing Services (Business Logic)

```typescript
describe('OrdersService', () => {
  let service: OrdersService;
  let repository: jest.Mocked<OrdersRepository>;

  beforeEach(() => {
    service = new OrdersService(repository);
  });

  it('should apply volume discount for 10+ items', () => {
    const product = { price: 100 };
    const quantity = 10;

    const pricing = service['calculatePricing'](product, quantity);

    expect(pricing.subtotal).toBe(1000);
    expect(pricing.discount).toBe(0.1);
    expect(pricing.total).toBe(900);
  });

  it('should throw error for insufficient stock', async () => {
    repository.getProduct.mockResolvedValue({ stock: 5 });

    await expect(
      service.create({ productId: '1', quantity: 10 })
    ).rejects.toThrow('Insufficient stock');
  });
});
```

## Common Anti-Patterns to Avoid

### ❌ Database Queries in Controllers

```typescript
@Controller('users')
export class UsersController {
  constructor(private dataSource: DataSource) {}  // 🚨 Wrong!

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.dataSource.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}
```

### ❌ Business Logic in Controllers

```typescript
@Controller('orders')
export class OrdersController {
  @Post()
  async create(@Body() data: any) {
    // 🚨 Business rules in controller
    if (data.total > 1000) {
      data.discount = 0.1;
    }
    // ...
  }
}
```

### ❌ External API Calls in Controllers

```typescript
@Controller('payments')
export class PaymentsController {
  @Post()
  async processPayment(@Body() data: any) {
    // 🚨 Direct API call in controller
    const response = await axios.post('https://stripe.com/charges', data);
    return response.data;
  }
}
```

## Summary: Clean Layer Separation

```
┌─────────────────────────────────────────────────────┐
│                   Controller Layer                   │
│  - Parse HTTP requests                               │
│  - Validate with DTOs                                │
│  - Set status codes and headers                      │
│  - Delegate to services                              │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    Service Layer                     │
│  - Execute business logic                            │
│  - Enforce business rules                            │
│  - Coordinate multiple repositories                  │
│  - Emit domain events                                │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  Repository Layer                    │
│  - Data access                                       │
│  - Database queries                                  │
│  - Entity persistence                                │
└─────────────────────────────────────────────────────┘
```

**Sources:**
- [Controllers | NestJS - Official Documentation](https://docs.nestjs.com/controllers)
- [Providers | NestJS - Official Documentation](https://docs.nestjs.com/providers)
- [Single Responsibility Principle | Wikipedia](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Clean Architecture | Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
