# Recommendation Design

## Goal

The recommender is a decision aid, not an objective ranking system. It should lower choice cost by combining WeRead signals with the user's current reading goal.

## Candidate Sources

Use multiple sources to avoid repeating the WeRead homepage:

- `/book/recommend`: platform personalized recommendations.
- `/book/similar`: similar books for seed books.
- `/user/notebooks`: high-note books become strong preference seeds.
- `/readdata/detail`: high-read-time books and preferred categories become preference signals.
- `/store/search`: topic or goal expansion when the user gives a theme.
- `/shelf/sync`: remove or flag books already on the shelf, and hard-exclude books whose `finishReading == 1` unless the user explicitly asks to include finished books. Also treat different editions of the same normalized title and author as already finished when one edition is finished.

## Modes

### safe

For "give me something I will probably like." Prefer candidates close to books with high read time, many notes, or finished status.

### expand

Default mode. Keep taste fit, but add adjacent categories, authors, and themes. Avoid recommending only more of the same.

### challenge

For "push me." Prefer denser, more serious, more foundational books when signals exist, and explain the friction.

## Score Factors

The helper script returns transparent factors. The agent should use them as evidence, not as truth.

Positive factors:

- Personalized recommendation source
- Similar to a high-investment seed book
- Topic or goal terms match title, category, intro, or platform reason
- Strong public rating
- High reading count
- Category match with the user's reading profile
- Not already on the shelf
- Not already finished

Negative or caution factors:

- Already on shelf or already read
- `finishReading == 1` means already finished; do not recommend it for a future reading plan unless the user asks for rereads
- A newer/older edition can look unfinished while an equivalent edition is already finished; compare normalized title and author before planning
- Overlaps too much with recent reading
- Weak public rating
- Thin reason or missing metadata
- Challenge mode candidate may be harder to finish

## Explanation Template

For each recommended book:

- "Why this": 1-2 concrete signals.
- "Possible mismatch": one honest caveat.
- "Best use": read now, sample first, compare, save for later, or use as a reference book.

For the top pick, add:

- why it beats the other candidates
- what to read next if the user likes it

## Do Not

- Do not claim the score is scientific.
- Do not recommend a book only because the rating is high.
- Do not hide that the book is already on the user's shelf.
- Do not put books from `readLongest` into a reading plan directly; treat them as taste evidence and verify unfinished status first.
- Do not recommend a second edition, revised edition, or alternate package when a same-title/same-author edition is already finished, unless the user asks for rereading or edition comparison.
- Do not overfit to one seed book unless the user explicitly asks for similar books.
