// Test: does SQL use single-quote doubling for string literals?
// DuckDB, PostgreSQL, and standard SQL all use single-quote doubling
// to escape a single quote within a string literal.

// Example: to represent the string: it's here
// SQL: 'it''s here'

// The claim is: "the escaping is insufficient"
// Let's think about what could break it:

// 1. If glob = "it's here"
//    After escaping: "it''s here"
//    SQL: FROM read_parquet('it''s here')
//    This is CORRECT SQL and will work fine.

// 2. If glob = "'; DROP TABLE settlements; --"
//    After escaping: "''; DROP TABLE settlements; --"
//    SQL: FROM read_parquet(''''; DROP TABLE settlements; --')
//    DuckDB sees: read_parquet('''''...') which is:
//    - First '' = escaped single quote (yields one ')
//    - Second '' = escaped single quote (yields one ')
//    - Then: ; DROP TABLE settlements; --')
//    But wait, that's INSIDE the string literal, so DROP wouldn't execute!
//    The semicolon inside a string literal is just a character.

// Actually, the real issue is if the escape itself is wrong.
// Let's verify: In DuckDB, is '' the correct escape for '?

// Standard SQL: yes, '' is the escape for '
// PostgreSQL: yes, '' is the standard way (also supports \')
// DuckDB: Let me check...

console.log("Testing SQL string escaping...");

// The claim says: "If the glob contains DuckDB-specific metacharacters (e.g., $, {})"
// But these are NOT SQL metacharacters. These are glob metacharacters that
// read_parquet() interprets AFTER receiving the string as a parameter.

// So the escaping IS sufficient for SQL injection protection.
// The question is: does the double-quote escaping correctly represent the string?

// Answer: YES. In DuckDB SQL, '' is the correct way to escape a single quote.
