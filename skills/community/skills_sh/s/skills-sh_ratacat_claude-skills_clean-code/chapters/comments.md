# Chapter 4: Comments

> "Don't comment bad code—rewrite it." —Brian W. Kernighan and P. J. Plaugher

## The Truth About Comments

Comments are, at best, a necessary evil. The proper use of comments is to **compensate for our failure to express ourselves in code**.

Every time you express yourself in code, pat yourself on the back. Every time you write a comment, grimace and feel the failure of your ability of expression.

**Why so harsh?** Because comments lie. Not always, not intentionally, but too often. Code changes and evolves. Comments don't always follow—they become orphaned blurbs of ever-decreasing accuracy.

```java
// Comment drifted from its code
MockRequest request;
private final String HTTP_DATE_REGEXP = "[SMTWF][a-z]{2}\\,\\s..."
private Response response;
private FitNesseContext context;
// Example: "Tue, 02 Apr 2003 22:18:49 GMT"  // <-- now far from HTTP_DATE_REGEXP
```

**Truth can only be found in one place: the code.** Only the code can truly tell you what it does.

## Comments Do Not Make Up for Bad Code

When you write messy code and think "I'd better comment that!"—NO! You'd better clean it!

Clear and expressive code with few comments is far superior to cluttered code with lots of comments.

## Explain Yourself in Code

```java
// Bad - comment explains confusing code
// Check to see if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))

// Good - code explains itself
if (employee.isEligibleForFullBenefits())
```

It takes only seconds to express intent in code. Create a function that says the same thing as the comment you want to write.

## Good Comments

Some comments are necessary or beneficial. The only truly good comment is the comment you found a way not to write.

### Legal Comments
Copyright and authorship statements are necessary:
```java
// Copyright (C) 2003,2004,2005 by Object Mentor, Inc. All rights reserved.
// Released under the terms of the GNU General Public License version 2 or later.
```

### Explanation of Intent
Sometimes a comment explains the intent behind a decision:
```java
public int compareTo(Object o) {
    if (o instanceof WikiPagePath) {
        // ... comparison logic
    }
    return 1; // we are greater because we are the right type.
}
```

### Clarification
When you can't alter code (standard library, external API), clarifying comments help:
```java
assertTrue(a.compareTo(a) == 0);    // a == a
assertTrue(a.compareTo(b) == -1);   // a < b
assertTrue(b.compareTo(a) == 1);    // b > a
```

**Warning:** Clarifying comments risk being incorrect. Verify carefully.

### Warning of Consequences
```java
// Don't run unless you have some time to kill.
public void _testWithReallyBigFile()

// SimpleDateFormat is not thread safe,
// so we need to create each instance independently.
SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z");
```

### TODO Comments
Reasonable for marking future work:
```java
// TODO-MdM these are not needed
// We expect this to go away when we do the checkout model
protected VersionInfo makeVersion() throws Exception {
    return null;
}
```

TODOs are not an excuse for bad code. Scan and eliminate them regularly.

### Amplification
Emphasize something that seems inconsequential:
```java
String listItemContent = match.group(3).trim();
// the trim is real important. It removes the starting
// spaces that could cause the item to be recognized
// as another list.
```

### Javadocs in Public APIs
Good javadocs for public APIs are helpful. But even javadocs can be misleading.

## Bad Comments

Most comments fall into this category—crutches for poor code or programmers talking to themselves.

### Mumbling
Comments written in a hurry that don't communicate:
```java
catch (IOException e) {
    // No properties files means all defaults are loaded
}
```
What does this mean? Who loads defaults? Any comment that forces you to look elsewhere for meaning has failed.

### Redundant Comments
```java
// Utility method that returns when this.closed is true. Throws an exception
// if the timeout is reached.
public synchronized void waitForClose(final long timeoutMillis)
```
Takes longer to read than the code. Less precise than the code. Don't accept imprecision in lieu of understanding.

**Useless Javadocs:**
```java
/** The processor delay for this component. */
protected int backgroundProcessorDelay = -1;

/** The lifecycle event support for this component. */
protected LifecycleSupport lifecycle = new LifecycleSupport(this);
```
These serve no documentary purpose—just clutter.

### Misleading Comments
The redundant comment above is also misleading: the method doesn't return *when* `this.closed` becomes true—it returns *if* it's already true, or waits and throws an exception.

Subtle misinformation causes debugging sessions.

### Mandated Comments
Rules requiring javadocs for every function lead to abominations:
```java
/**
 * @param title The title of the CD
 * @param author The author of the CD
 * @param tracks The number of tracks on the CD
 */
public void addCD(String title, String author, int tracks)
```
This adds nothing. Just clutter and potential for lies.

### Journal Comments
```java
* Changes (from 11-Oct-2001)
* --------------------------
* 11-Oct-2001 : Re-organised the class and moved it to new package
* 05-Nov-2001 : Added a getDescription() method...
```
We have source control now. These should be completely removed.

### Noise Comments
```java
/** Default constructor. */
protected AnnualDateRule() { }

/** The day of the month. */
private int dayOfMonth;

/** Returns the day of the month. @return the day of the month. */
public int getDayOfMonth() { return dayOfMonth; }
```
We learn to ignore these. Eventually they become lies.

### Scary Noise
```java
/** The name. */
private String name;
/** The version. */
private String version;
/** The licenceName. */
private String licenceName;
/** The version. */    // <-- Copy-paste error!
private String info;
```
If authors aren't paying attention writing comments, why should readers profit?

### Don't Use a Comment When You Can Use a Function or Variable
```java
// Bad
// does the module from the global list <mod> depend on the subsystem we are part of?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem()))

// Good - no comment needed
ArrayList moduleDependees = smodule.getDependSubsystems();
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem))
```

### Position Markers
```java
// Actions //////////////////////////////////
```
Use very sparingly. If you overuse them, they become background noise.

### Closing Brace Comments
```java
} //while
} //try
} //catch
} //main
```
If you need these, your functions are too long. Shorten them instead.

### Attributions and Bylines
```java
/* Added by Rick */
```
Source control remembers who added what. These stay for years getting less accurate.

### Commented-Out Code

**Few practices are as odious as commenting-out code. Don't do this!**

```java
// InputStream resultsStream = formatter.getResultStream();
// StreamReader reader = new StreamReader(resultsStream);
// response.setContent(reader.read(formatter.getByteCount()));
```

Others won't have courage to delete it—they'll think it's important. It gathers like dregs.

**We have source control.** Just delete the code. We won't lose it. Promise.

### HTML Comments
HTML in source code comments is an abomination. Makes them hard to read in the one place they should be easy to read—the editor.

### Nonlocal Information
Don't offer systemwide information in a local comment:
```java
/**
 * Port on which fitnesse would run. Defaults to 8082.
 */
public void setFitnessePort(int fitnessePort)
```
The function has no control over the default. When the default changes elsewhere, this comment won't be updated.

### Too Much Information
Don't put historical discussions or irrelevant details:
```java
/*
RFC 2045 - Multipurpose Internet Mail Extensions (MIME)
Part One: Format of Internet Message Bodies
section 6.8. Base64 Content-Transfer-Encoding
The encoding process represents 24-bit groups of input bits...
[50 more lines of RFC specification]
*/
```

### Inobvious Connection
```java
/*
 * start with an array that is big enough to hold all the pixels
 * (plus filter bytes), and an extra 200 bytes for header info
 */
this.pngBytes = new byte[((this.width + 1) * this.height * 3) + 200];
```
What's a filter byte? Why 200? The purpose of a comment is to explain code that doesn't explain itself. A comment that needs its own explanation has failed.

### Function Headers
Short functions don't need description. A well-chosen name for a small function that does one thing is better than a comment header.

### Javadocs in Nonpublic Code
Generating javadocs for internal classes is not useful. The extra formality is cruft and distraction.
