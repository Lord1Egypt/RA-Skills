# Debugging Mental Models

## 1. Reproduce first, fix second
If you can't reproduce it reliably, you can't prove you fixed it.

## 2. Binary search the problem space
- Comment out half the code → does it still happen?
- Use `git bisect` to find the offending commit.
- Divide and conquer beats reading line by line.

## 3. Check your assumptions
The bug is usually where you're *not* looking because you're sure that part works.
Read that part anyway.

## 4. Rubber duck
Explain the bug out loud to an imaginary (or real) listener.
Half the time you'll spot the issue mid-sentence.

## 5. Read the error message
Really read it. The whole thing. Twice.
Most people skim and miss the actual cause.

## 6. Log before you debug
Add one log line at each boundary. Narrow down where reality diverges from expectation.

## 7. Sleep on it
If you've been stuck for an hour, walk away.
Your brain keeps working offline; fresh eyes see more.
