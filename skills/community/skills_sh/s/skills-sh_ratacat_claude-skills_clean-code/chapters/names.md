# Chapter 2: Meaningful Names

Names are everywhere in software—variables, functions, arguments, classes, packages, source files, directories. Because we name so much, we'd better do it well.

## Use Intention-Revealing Names

A name should answer: **Why does it exist? What does it do? How is it used?**

If a name requires a comment, the name doesn't reveal its intent.

```java
// Bad
int d; // elapsed time in days

// Good
int elapsedTimeInDays;
int daysSinceCreation;
int fileAgeInDays;
```

**The Minesweeper Example**

```java
// Bad - implicity (context not explicit)
public List<int[]> getThem() {
    List<int[]> list1 = new ArrayList<int[]>();
    for (int[] x : theList)
        if (x[0] == 4)
            list1.add(x);
    return list1;
}

// Good - explicit intent
public List<Cell> getFlaggedCells() {
    List<Cell> flaggedCells = new ArrayList<Cell>();
    for (Cell cell : gameBoard)
        if (cell.isFlagged())
            flaggedCells.add(cell);
    return flaggedCells;
}
```

The second version has the same operators, constants, and nesting—but the intent is clear.

## Avoid Disinformation

Don't leave false clues that obscure meaning:

- **Don't use platform names**: `hp`, `aix`, `sco` look like Unix platforms
- **Don't lie about types**: Don't call it `accountList` unless it's actually a `List`. Use `accounts` or `accountGroup`
- **Avoid subtle differences**: `XYZControllerForEfficientHandlingOfStrings` vs `XYZControllerForEfficientStorageOfStrings` forces scrutiny
- **Watch for confusing characters**: lowercase `l` and uppercase `O` look like `1` and `0`

## Make Meaningful Distinctions

If names must be different, they should *mean* something different.

**Number-series naming is noninformative:**
```java
// Bad
public static void copyChars(char a1[], char a2[]) {
    for (int i = 0; i < a1.length; i++) {
        a2[i] = a1[i];
    }
}

// Good
public static void copyChars(char source[], char destination[]) {
    for (int i = 0; i < source.length; i++) {
        destination[i] = source[i];
    }
}
```

**Noise words are meaningless distinctions:**
- `ProductInfo` vs `ProductData` — what's the difference?
- `NameString` — would a Name ever be a float?
- `CustomerObject` vs `Customer` — which has payment history?
- `getActiveAccount()` vs `getActiveAccounts()` vs `getActiveAccountInfo()` — which to call?
- `moneyAmount` vs `money` — indistinguishable
- `theMessage` vs `message` — no meaningful distinction

## Use Pronounceable Names

Programming is a social activity. You need to discuss code with others.

```java
// Bad - "gen why emm dee aich emm ess"
class DtaRcrd102 {
    private Date genymdhms;
    private Date modymdhms;
    private final String pszqint = "102";
}

// Good - "Hey, look at this record's generation timestamp!"
class Customer {
    private Date generationTimestamp;
    private Date modificationTimestamp;
    private final String recordId = "102";
}
```

## Use Searchable Names

Single-letter names and numeric constants are hard to grep.

```java
// Bad - can't search for 5 or e meaningfully
for (int j=0; j<34; j++) {
    s += (t[j]*4)/5;
}

// Good - searchable names
int realDaysPerIdealDay = 4;
const int WORK_DAYS_PER_WEEK = 5;
int sum = 0;
for (int j=0; j < NUMBER_OF_TASKS; j++) {
    int realTaskDays = taskEstimate[j] * realDaysPerIdealDay;
    int realTaskWeeks = (realTaskDays / WORK_DAYS_PER_WEEK);
    sum += realTaskWeeks;
}
```

**The Rule:** The length of a name should correspond to the size of its scope. Single-letter names only for tiny scopes (small loop counters).

## Avoid Encodings

We have enough encodings to deal with.

### Hungarian Notation
Modern languages have rich type systems. The compiler remembers types. HN is an obsolete crutch:
```java
// Bad - type encoding is redundant
PhoneNumber phoneString; // name not changed when type changed!
```

### Member Prefixes
You don't need `m_` anymore. Classes should be small enough that you see declarations. IDEs highlight members:
```java
// Bad
public class Part {
    private String m_dsc;
    void setName(String name) { m_dsc = name; }
}

// Good
public class Part {
    String description;
    void setDescription(String description) {
        this.description = description;
    }
}
```

### Interfaces and Implementations
Prefer unadorned interfaces. Don't tell users it's an interface—they shouldn't care:
```java
// Bad
IShapeFactory  // The I is noise

// Good
ShapeFactory           // for the interface
ShapeFactoryImpl       // for the implementation (if you must encode)
```

## Avoid Mental Mapping

Readers shouldn't translate your names into names they already know.

Single-letter variables (`i`, `j`, `k`) are acceptable only for traditional loop counters in very small scopes. Using `r` because you "know" it's the URL with host and scheme removed is showing off, not being professional.

**Clarity is king.** Professionals write code that others can understand.

## Class Names vs Method Names

| Type | Rule | Examples |
|------|------|----------|
| **Classes** | Noun or noun phrase | `Customer`, `WikiPage`, `Account`, `AddressParser` |
| **Methods** | Verb or verb phrase | `postPayment`, `deletePage`, `save` |

**Avoid** weasel words like `Manager`, `Processor`, `Data`, `Info` in class names. They hint at unclear responsibilities.

For overloaded constructors, use static factory methods:
```java
// Good - name describes the argument
Complex fulcrumPoint = Complex.FromRealNumber(23.0);

// Less clear
Complex fulcrumPoint = new Complex(23.0);
```

## Don't Be Cute

Choose clarity over entertainment value.

| Cute | Clear |
|------|-------|
| `HolyHandGrenade` | `DeleteItems` |
| `whack()` | `kill()` |
| `eatMyShorts()` | `abort()` |

Say what you mean. Mean what you say.

## Pick One Word per Concept

Pick one word for one abstract concept and stick with it:
- Don't mix `fetch`, `retrieve`, and `get` for equivalent operations
- Don't mix `controller`, `manager`, and `driver` in the same codebase

Function names must stand alone—you can't rely on readers checking comments.

## Don't Pun

Don't use the same word for two different operations.

If `add` means "concatenate two values" in most classes, don't use `add` for "put into collection" in a new class. Use `insert` or `append` instead.

**Goal:** Code should be a quick skim, not an intense study.

## Solution Domain Names vs Problem Domain Names

| When | Use |
|------|-----|
| Technical concepts | CS terms, algorithm names, pattern names (`AccountVisitor`, `JobQueue`) |
| Business concepts | Domain terms (ask domain experts if unclear) |

Programmers will read your code—use technical names when appropriate.

## Add Meaningful Context

Variables often need context. `state` alone is ambiguous. Options:

1. **Prefixing** (last resort): `addrState`, `addrCity`
2. **Better:** Create a class `Address` with `state`, `city` fields

```java
// Bad - unclear context
private void printGuessStatistics(char candidate, int count) {
    String number;
    String verb;
    String pluralModifier;
    // ... long function using these
}

// Good - class provides context
public class GuessStatisticsMessage {
    private String number;
    private String verb;
    private String pluralModifier;

    public String make(char candidate, int count) {
        createPluralDependentMessageParts(count);
        return String.format("There %s %s %s%s",
            verb, number, candidate, pluralModifier);
    }
}
```

## Don't Add Gratuitous Context

In "Gas Station Deluxe" app, don't prefix every class with `GSD`:
- You get a mile-long autocomplete list
- `GSDAccountAddress` has 10/17 irrelevant characters

**Shorter names are better if they're clear.** Add no more context than necessary.

`Address` is fine for a class. If you need to differentiate: `PostalAddress`, `MAC`, `URI`.

## Final Words

The hardest thing about naming is that it requires descriptive skills and shared cultural background—a teaching issue, not a technical one.

**Don't fear renaming.** Use refactoring tools. It pays off short-term and long-term. Code should read like paragraphs and sentences.
