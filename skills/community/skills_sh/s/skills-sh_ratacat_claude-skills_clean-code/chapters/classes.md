# Chapter 10: Classes

We've focused on lines and blocks of code—functions and how they interrelate. But we don't have clean code until we've paid attention to higher levels of organization.

## Class Organization

Standard Java convention:
1. Public static constants
2. Private static variables
3. Private instance variables
4. Public functions
5. Private utilities (right after the public function that calls them)

This follows the stepdown rule—program reads like a newspaper article.

### Encapsulation

Keep variables and utility functions private. Sometimes make them protected for tests. But loosening encapsulation is always a last resort.

## Classes Should Be Small!

The first rule of classes is they should be small. The second rule is they should be smaller than that.

With functions we measured by lines. **With classes we count responsibilities.**

### The Name Test

The name of a class should describe its responsibilities. If you cannot derive a concise name, it's likely too large.

Weasel words like `Manager`, `Processor`, `Super` often hint at too many responsibilities.

### The 25-Word Test

Write a brief description in about 25 words without using "if," "and," "or," or "but."

> "The SuperDashboard provides access to the component that last held the focus, **and** it also allows us to track the version and build numbers."

That "and" is a hint of too many responsibilities.

## The Single Responsibility Principle (SRP)

> A class or module should have one, and only one, reason to change.

This gives us a definition of responsibility and a guideline for class size.

```java
// Bad - two reasons to change (version info AND Swing components)
public class SuperDashboard extends JFrame implements MetaDataUser {
    public Component getLastFocusedComponent()
    public void setLastFocused(Component lastFocused)
    public int getMajorVersionNumber()
    public int getMinorVersionNumber()
    public int getBuildNumber()
}

// Good - version info extracted
public class Version {
    public int getMajorVersionNumber()
    public int getMinorVersionNumber()
    public int getBuildNumber()
}
```

**Why is SRP often violated?**

Getting software to work and making it clean are different activities. We focus on getting code to work, then fail to switch to organization and cleanliness. We move to the next problem instead of breaking overstuffed classes into decoupled units.

**The "too many classes" fear:**

Some developers fear many small classes make it harder to understand the bigger picture. But a system with many small classes has no more moving parts than one with few large classes.

**Which would you prefer?** Toolboxes with many small, well-labeled drawers? Or a few drawers where you toss everything?

> We want systems composed of many small classes, not a few large ones. Each small class encapsulates a single responsibility, has a single reason to change, and collaborates with others to achieve desired behaviors.

## Cohesion

Classes should have a small number of instance variables. Each method should manipulate one or more of those variables.

**High cohesion:** Methods and variables hang together as a logical whole.

```java
// Very cohesive - all methods use the instance variables
public class Stack {
    private int topOfStack = 0;
    List<Integer> elements = new LinkedList<Integer>();

    public int size() { return topOfStack; }

    public void push(int element) {
        topOfStack++;
        elements.add(element);
    }

    public int pop() throws PoppedWhenEmpty {
        if (topOfStack == 0) throw new PoppedWhenEmpty();
        int element = elements.get(--topOfStack);
        elements.remove(topOfStack);
        return element;
    }
}
```

**When cohesion breaks down:**

Small functions with short parameter lists can lead to instance variables used by only a subset of methods. When this happens, there's at least one other class trying to get out.

**Breaking large functions → breaking out classes:** If you extract a function that uses four variables, you might promote them to instance variables. But now the class loses cohesion. Solution: those variables and methods become their own class.

## Organizing for Change

Change is continual. In a clean system, we organize classes to reduce the risk of change.

```java
// Bad - must be opened for any change
public class Sql {
    public Sql(String table, Column[] columns)
    public String create()
    public String insert(Object[] fields)
    public String selectAll()
    public String findByKey(String keyColumn, String keyValue)
    public String select(Column column, String pattern)
    public String select(Criteria criteria)
    private String selectWithCriteria(String criteria)
    // ...
}
```

This class must change for new statement types AND for detail changes to existing types. Two reasons to change → violates SRP.

```java
// Good - closed classes, open for extension
abstract public class Sql {
    public Sql(String table, Column[] columns)
    abstract public String generate();
}

public class CreateSql extends Sql {
    @Override public String generate()
}

public class SelectSql extends Sql {
    @Override public String generate()
}

public class InsertSql extends Sql {
    public InsertSql(String table, Column[] columns, Object[] fields)
    @Override public String generate()
}

public class FindByKeySql extends Sql {
    @Override public String generate()
}
// ... etc.
```

**Benefits:**
- Each class is excruciatingly simple
- Comprehension time drops to almost nothing
- Risk of breaking other code is vanishingly small
- Easy to test in isolation
- Adding `UpdateSql` requires no changes to existing classes

This supports SRP and the **Open-Closed Principle (OCP):** Classes should be open for extension but closed for modification.

## Isolating from Change

Concrete classes contain implementation details. Abstract classes represent concepts.

A client depending on concrete details is at risk when those details change.

```java
// Bad - hard to test, depends on concrete external API
public class Portfolio {
    private TokyoStockExchange exchange = new TokyoStockExchange();
    // ... portfolio value depends on volatile external lookup
}

// Good - depends on abstraction
public interface StockExchange {
    Money currentPrice(String symbol);
}

public class Portfolio {
    private StockExchange exchange;

    public Portfolio(StockExchange exchange) {
        this.exchange = exchange;
    }
}

// Now we can test with a stub
public class PortfolioTest {
    @Test
    public void GivenFiveMSFTTotalShouldBe500() throws Exception {
        FixedStockExchangeStub exchange = new FixedStockExchangeStub();
        exchange.fix("MSFT", 100);
        Portfolio portfolio = new Portfolio(exchange);
        portfolio.add(5, "MSFT");
        Assert.assertEquals(500, portfolio.value());
    }
}
```

**Dependency Inversion Principle (DIP):** Classes should depend upon abstractions, not on concrete details.

If a system is decoupled enough to be tested this way, it will also be more flexible and promote more reuse.
