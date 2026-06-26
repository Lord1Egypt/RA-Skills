# Chapter 3: Functions

Functions are the first line of organization in any program. Writing them well is essential.

## Small!

**The first rule of functions is that they should be small. The second rule is that they should be smaller than that.**

Kent Beck showed Uncle Bob a program where every function was just two, three, or four lines long. Each was transparently obvious, told a story, and led to the next in a compelling order.

**How small?** Functions should hardly ever be 20 lines long. Ideal is 2-5 lines.

```java
// This function went from 60+ lines to this:
public static String renderPageWithSetupsAndTeardowns(
        PageData pageData, boolean isSuite) throws Exception {
    if (isTestPage(pageData))
        includeSetupAndTeardownPages(pageData, isSuite);
    return pageData.getHtml();
}
```

### Blocks and Indenting
- Blocks within `if`, `else`, `while` should be one line—probably a function call
- This adds documentary value (the called function has a descriptive name)
- **Indent level should not be greater than one or two**

## Do One Thing

> FUNCTIONS SHOULD DO ONE THING. THEY SHOULD DO IT WELL. THEY SHOULD DO IT ONLY.

**How do you know if a function does "one thing"?**

Describe it as a brief TO paragraph:
> TO RenderPageWithSetupsAndTeardowns, we check to see whether the page is a test page and if so, we include the setups and teardowns. In either case we render the page in HTML.

If a function does only steps one level below its stated name, it's doing one thing.

**Another test:** If you can extract another function from it with a name that isn't merely a restatement of its implementation, the original was doing more than one thing.

### Sections Within Functions
If a function can be divided into sections (declarations, initialization, sieve), it's doing more than one thing.

## One Level of Abstraction per Function

Statements within a function should all be at the same level of abstraction.

```java
// Bad - mixed abstraction levels
getHtml();                              // High level
String pagePathName = PathParser.render(pagePath);  // Medium level
.append("\n");                          // Very low level
```

**Mixing levels is confusing.** Readers can't tell essential concepts from details. Like broken windows, once details mix in, more details accrete.

### The Stepdown Rule

Code should read like a top-down narrative—a set of TO paragraphs:

> To include the setups and teardowns, we include setups, then we include the test page content, and then we include the teardowns.
> To include the setups, we include the suite setup if this is a suite, then we include the regular setup.
> To include the suite setup, we search the parent hierarchy...

Each function introduces the next, each at a consistent level of abstraction.

## Switch Statements

Switch statements always do N things by nature. They're hard to make small.

```java
// Bad - many problems
public Money calculatePay(Employee e) throws InvalidEmployeeType {
    switch (e.type) {
        case COMMISSIONED: return calculateCommissionedPay(e);
        case HOURLY: return calculateHourlyPay(e);
        case SALARIED: return calculateSalariedPay(e);
        default: throw new InvalidEmployeeType(e.type);
    }
}
```

**Problems:**
1. Large, grows with new types
2. Does more than one thing
3. Violates Single Responsibility Principle (multiple reasons to change)
4. Violates Open-Closed Principle (must change for new types)
5. Other functions (`isPayday`, `deliverPay`) will have the same structure

**Solution:** Bury switch in an Abstract Factory, use polymorphism:

```java
public abstract class Employee {
    public abstract boolean isPayday();
    public abstract Money calculatePay();
    public abstract void deliverPay(Money pay);
}

public class EmployeeFactoryImpl implements EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType {
        switch (r.type) {
            case COMMISSIONED: return new CommissionedEmployee(r);
            case HOURLY: return new HourlyEmployee(r);
            case SALARIED: return new SalariedEmployee(r);
            default: throw new InvalidEmployeeType(r.type);
        }
    }
}
```

**Rule:** Switch statements can be tolerated if they appear only once, create polymorphic objects, and are hidden behind an inheritance relationship.

## Use Descriptive Names

Don't be afraid to make a name long. **A long descriptive name is better than a short enigmatic name. A long descriptive name is better than a long descriptive comment.**

Ward's principle: "You know you are working on clean code when each routine turns out to be pretty much what you expected."

Be consistent: `includeSetupAndTeardownPages`, `includeSetupPages`, `includeSuiteSetupPage`, `includeSetupPage` tell a story. You'd expect `includeTeardownPages` next.

## Function Arguments

| Count | Name | Guidance |
|-------|------|----------|
| 0 | Niladic | Ideal |
| 1 | Monadic | Good |
| 2 | Dyadic | Acceptable with care |
| 3 | Triadic | Avoid where possible |
| 3+ | Polyadic | Requires special justification—don't do it |

**Why fewer is better:**
- Arguments require conceptual power to understand
- They're at a different abstraction level than the function name
- Testing all combinations is combinatorially harder

### Common Monadic Forms
1. **Asking a question:** `boolean fileExists("MyFile")`
2. **Transforming:** `InputStream fileOpen("MyFile")` → returns transformed value
3. **Event:** `void passwordAttemptFailedNtimes(int attempts)` → no output, alters state

### Flag Arguments

**Flag arguments are ugly.** Passing a boolean loudly proclaims the function does more than one thing.

```java
// Bad
render(true)  // What does true mean?

// Good
renderForSuite()
renderForSingleTest()
```

### Dyads and Triads

Two arguments are harder than one. `writeField(name)` beats `writeField(outputStream, name)`.

Acceptable dyads: `Point(0, 0)` — ordered components of a single value.

Problematic dyads: `assertEquals(expected, actual)` — no natural ordering, requires practice.

**Convert dyads to monads:**
- Make method a member: `outputStream.writeField(name)`
- Make one argument a field
- Extract a class: `FieldWriter` takes stream in constructor

### Argument Objects

When a function needs 3+ arguments, wrap some in a class:

```java
// Before
Circle makeCircle(double x, double y, double radius);

// After - x,y are a concept worth naming
Circle makeCircle(Point center, double radius);
```

## Have No Side Effects

Side effects are lies. Your function promises to do one thing but does hidden things.

```java
// Bad - hidden side effect
public boolean checkPassword(String userName, String password) {
    User user = UserGateway.findByName(userName);
    if (user != User.NULL) {
        String codedPhrase = user.getPhraseEncodedByPassword();
        String phrase = cryptographer.decrypt(codedPhrase, password);
        if ("Valid Password".equals(phrase)) {
            Session.initialize();  // SIDE EFFECT!
            return true;
        }
    }
    return false;
}
```

`checkPassword` doesn't imply session initialization. Callers will erase session data when they "just want to check."

**If you must have a temporal coupling, make it clear:** `checkPasswordAndInitializeSession()` (though this violates "do one thing").

### Output Arguments

Arguments are naturally inputs. Output arguments cause double-takes.

```java
// Confusing - is s input or output?
appendFooter(s);

// Better - call on the object
report.appendFooter();
```

If your function must change state, have it change the state of its owning object.

## Command Query Separation

Functions should either **do something** OR **answer something**, not both.

```java
// Bad - is this asking or commanding?
if (set("username", "unclebob")) ...
// Does this mean "was it previously set?" or "set it and check if it worked?"

// Good - separate command and query
if (attributeExists("username")) {
    setAttribute("username", "unclebob");
}
```

## Prefer Exceptions to Returning Error Codes

Error codes promote deeply nested structures:

```java
// Bad - deeply nested error handling
if (deletePage(page) == E_OK) {
    if (registry.deleteReference(page.name) == E_OK) {
        if (configKeys.deleteKey(page.name.makeKey()) == E_OK) {
            logger.log("page deleted");
        } else {
            logger.log("configKey not deleted");
        }
    } else {
        logger.log("deleteReference failed");
    }
} else {
    logger.log("delete failed");
}

// Good - exceptions separate happy path from error handling
try {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
} catch (Exception e) {
    logger.log(e.getMessage());
}
```

### Extract Try/Catch Blocks

Try/catch blocks are ugly and mix error processing with normal processing. Extract the bodies:

```java
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
}
```

**Error handling is one thing.** A function that handles errors should do nothing else.

## Don't Repeat Yourself (DRY)

Duplication is the root of all evil in software. It bloats code, requires parallel modifications, and creates opportunities for errors.

Structured programming, OOP, AOP, and COP are all strategies for eliminating duplication.

## How Do You Write Functions Like This?

Writing software is like writing anything else—you write a rough draft, then refine it.

First draft may be clumsy with long functions, nested loops, arbitrary names, duplicated code. Then you refine: break out functions, change names, eliminate duplication, shrink and reorder methods, sometimes break out classes.

**The end result:** Functions that follow the rules in this chapter. Nobody writes them that way from the start.
