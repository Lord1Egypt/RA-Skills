# Chapter 6: Objects and Data Structures

Why do we keep variables private? To prevent others from depending on them—to keep freedom to change implementation. Why, then, do so many programmers add getters and setters, exposing private variables as if public?

## Data Abstraction

Hiding implementation isn't just putting functions between variables—it's about **abstractions**.

```java
// Concrete - exposes implementation (rectangular coordinates)
public class Point {
    public double x;
    public double y;
}

// Abstract - hides implementation (rectangular? polar? neither?)
public interface Point {
    double getX();
    double getY();
    void setCartesian(double x, double y);
    double getR();
    double getTheta();
    void setPolar(double r, double theta);
}
```

The abstract version enforces an access policy: read coordinates independently, but set them together atomically.

```java
// Concrete - obviously just accessor to gallons
public interface Vehicle {
    double getFuelTankCapacityInGallons();
    double getGallonsOfGasoline();
}

// Abstract - no clue about underlying data form
public interface Vehicle {
    double getPercentFuelRemaining();
}
```

**Don't blithely add getters and setters.** Think about the best way to represent data.

## Data/Object Anti-Symmetry

Objects and data structures are virtual opposites:

| Concept | Hides | Exposes |
|---------|-------|---------|
| **Objects** | Data | Functions that operate on data |
| **Data Structures** | Nothing | Data (no meaningful functions) |

### The Fundamental Dichotomy

**Procedural code** (using data structures):
- Easy to add new functions without changing data structures
- Hard to add new data structures (all functions must change)

**OO code** (using objects):
- Easy to add new classes without changing functions
- Hard to add new functions (all classes must change)

```java
// Procedural - easy to add new function, hard to add new shape
public class Geometry {
    public double area(Object shape) {
        if (shape instanceof Square) {
            return ((Square)shape).side * ((Square)shape).side;
        } else if (shape instanceof Circle) {
            return PI * ((Circle)shape).radius * ((Circle)shape).radius;
        }
        throw new NoSuchShapeException();
    }
}

// OO - easy to add new shape, hard to add new function
public class Square implements Shape {
    private double side;
    public double area() { return side * side; }
}

public class Circle implements Shape {
    private double radius;
    public double area() { return PI * radius * radius; }
}
```

**Mature programmers know that the idea that everything is an object is a myth.** Sometimes you want simple data structures with procedures operating on them.

## The Law of Demeter

A module should not know about the innards of objects it manipulates.

**A method `f` of class `C` should only call methods of:**
- `C` itself
- Objects created by `f`
- Objects passed as arguments to `f`
- Objects held in instance variables of `C`

**Don't call methods on objects returned by allowed functions.** Talk to friends, not strangers.

### Train Wrecks

```java
// Bad - train wreck, knows too much structure
final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();

// Better - but still knows structure
Options opts = ctxt.getOptions();
File scratchDir = opts.getScratchDir();
final String outputDir = scratchDir.getAbsolutePath();
```

Whether this violates Demeter depends on whether these are objects or data structures.

**If data structures:** Demeter doesn't apply—they naturally expose internal structure.
**If objects:** Clear violation—should hide internal structure.

### Hybrids Are Bad

Hybrids (half object, half data structure) have the worst of both worlds:
- Hard to add new functions
- Hard to add new data structures

They indicate muddled design. Avoid creating them.

### Hiding Structure

If objects have real behavior, ask them to *do something*, don't navigate through them.

```java
// Bad - asking for internals, then using them
String outFile = outputDir + "/" + className.replace('.', '/') + ".class";
FileOutputStream fout = new FileOutputStream(outFile);

// Good - tell the object to do the work
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

`ctxt` hides its internals and we don't violate Demeter.

## Data Transfer Objects (DTOs)

A class with public variables and no functions—useful for database communication, parsing messages, etc.

```java
// Bean form (quasi-encapsulation, no real benefit over public fields)
public class Address {
    private String street;
    private String city;
    private String state;

    public String getStreet() { return street; }
    public String getCity() { return city; }
    public String getState() { return state; }
}
```

### Active Records

DTOs with navigational methods like `save` and `find`. Usually direct translations from database tables.

**Problem:** Developers put business rules in them, creating hybrids.

**Solution:** Treat Active Records as data structures. Create separate objects for business rules that hide their data (probably instances of the Active Record).

## Conclusion

| Want to add... | Prefer... |
|----------------|-----------|
| New data types | Objects and OO |
| New behaviors | Data structures and procedures |

Good developers understand this without prejudice and choose the approach best for the job.
