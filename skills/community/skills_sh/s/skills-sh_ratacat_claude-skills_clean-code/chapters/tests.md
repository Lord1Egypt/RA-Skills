# Chapter 9: Unit Tests

The Agile and TDD movements have encouraged many programmers to write automated unit tests. But in the rush to add testing, many have missed the more subtle, important points of writing good tests.

## The Three Laws of TDD

1. **First Law:** You may not write production code until you have written a failing unit test.
2. **Second Law:** You may not write more of a unit test than is sufficient to fail, and not compiling is failing.
3. **Third Law:** You may not write more production code than is sufficient to pass the currently failing test.

These three laws lock you into a cycle perhaps thirty seconds long. Tests and production code are written together, with tests just seconds ahead.

## Keeping Tests Clean

A team decided their test code didn't need to be maintained to the same quality as production code. "Quick and dirty" was the watchword.

**The problem:** Dirty tests are equivalent to (or worse than) having no tests.

Tests must change as production code evolves. The dirtier the tests, the harder they are to change. Eventually:
- Old tests fail as production changes
- Mess in test code makes them hard to fix
- Tests become a liability
- Cost of maintaining tests rises
- Team discards test suite entirely
- Without tests, defect rate rises
- Fear of making changes
- Production code rots

**The moral:** Test code is just as important as production code. It requires thought, design, and care. Keep it as clean as production code.

## Tests Enable the -ilities

**Unit tests keep code flexible, maintainable, and reusable.**

Without tests, every change is a possible bug. You become reluctant to make changes out of fear of introducing undetected bugs.

With tests that fear disappears. You can improve architecture and design without fear. **Tests enable change.**

If your tests are dirty, your ability to change code is hampered. The dirtier your tests, the dirtier your code becomes. Eventually you lose the tests, and your code rots.

## Clean Tests

What makes a clean test? Three things: **Readability, readability, and readability.**

What makes tests readable? Clarity, simplicity, and density of expression. Say a lot with as few expressions as possible.

```java
// Bad - too many details, hard to understand
public void testGetPageHieratchyAsXml() throws Exception {
    crawler.addPage(root, PathParser.parse("PageOne"));
    crawler.addPage(root, PathParser.parse("PageOne.ChildOne"));
    crawler.addPage(root, PathParser.parse("PageTwo"));
    request.setResource("root");
    request.addInput("type", "pages");
    Responder responder = new SerializedPageResponder();
    SimpleResponse response = (SimpleResponse) responder.makeResponse(
        new FitNesseContext(root), request);
    String xml = response.getContent();
    assertEquals("text/xml", response.getContentType());
    assertSubString("<name>PageOne</name>", xml);
    assertSubString("<name>PageTwo</name>", xml);
    assertSubString("<name>ChildOne</name>", xml);
}

// Good - BUILD-OPERATE-CHECK pattern, domain-specific language
public void testGetPageHierarchyAsXml() throws Exception {
    makePages("PageOne", "PageOne.ChildOne", "PageTwo");
    submitRequest("root", "type:pages");
    assertResponseIsXML();
    assertResponseContains(
        "<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>"
    );
}
```

The **BUILD-OPERATE-CHECK** pattern:
1. Build up test data
2. Operate on that data
3. Check expected results

## Domain-Specific Testing Language

Build functions and utilities that make tests convenient to write and easy to read. This testing API evolves from continued refactoring of test code.

## A Dual Standard

Test code has different engineering standards than production code. It must be simple, succinct, and expressive—but doesn't need to be as efficient.

```java
// Hard to read - eyes bounce between state and sense
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    hw.setTemp(WAY_TOO_COLD);
    controller.tic();
    assertTrue(hw.heaterState());
    assertTrue(hw.blowerState());
    assertFalse(hw.coolerState());
    assertFalse(hw.hiTempAlarm());
    assertTrue(hw.loTempAlarm());
}

// Better - compact encoding (H=heater on, h=off, etc.)
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold();
    assertEquals("HBchL", hw.getState());
}

// Easy to understand many tests at a glance
@Test public void turnOnCoolerAndBlowerIfTooHot() throws Exception {
    tooHot();
    assertEquals("hBChl", hw.getState());
}
@Test public void turnOnHeaterAndBlowerIfTooCold() throws Exception {
    tooCold();
    assertEquals("HBchl", hw.getState());
}
```

Things acceptable in tests but not production: inefficient string concatenation, memory concerns. But **never** compromise on cleanliness.

## One Assert per Test

A good guideline: minimize the number of asserts per test. Single conclusion, quick to understand.

But don't be afraid of multiple asserts if they test a single concept.

## Single Concept per Test

**Better rule:** Test one concept per test function.

```java
// Bad - tests three independent things
public void testAddMonths() {
    // Test 1: adding 1 month when last day is 31 and next month has 30 days
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);
    SerialDate d2 = SerialDate.addMonths(1, d1);
    assertEquals(30, d2.getDayOfMonth());  // Should be 30, not 31

    // Test 2: adding 2 months
    SerialDate d3 = SerialDate.addMonths(2, d1);
    assertEquals(31, d3.getDayOfMonth());

    // Test 3: adding 1 month twice
    SerialDate d4 = SerialDate.addMonths(1, SerialDate.addMonths(1, d1));
    assertEquals(30, d4.getDayOfMonth());
}
```

Split into three tests, each testing one concept clearly.

## F.I.R.S.T.

Clean tests follow five rules:

### Fast
Tests should run quickly. When tests are slow, you won't run them frequently. Without frequent runs, you won't find problems early, won't feel free to clean up code. Code will rot.

### Independent
Tests should not depend on each other. One test should not set up conditions for the next. Run each test independently, in any order. When tests depend on each other, failures cascade, making diagnosis difficult.

### Repeatable
Tests should be repeatable in any environment—production, QA, your laptop on the train. If tests aren't repeatable, you'll have excuses for failures and can't run them when environment isn't available.

### Self-Validating
Tests should have boolean output: pass or fail. Don't read log files or compare text files manually. Non-self-validating tests make failure subjective.

### Timely
Write tests just before the production code. If you write tests after, you may find production code hard to test, decide some code is "too hard to test," or not design for testability.

## Conclusion

Tests are as important to project health as production code—perhaps more so, because they preserve and enhance flexibility, maintainability, and reusability.

Keep tests clean. Make them expressive and succinct. Invent testing APIs as domain-specific languages.

**If you let the tests rot, your code will rot too.**
