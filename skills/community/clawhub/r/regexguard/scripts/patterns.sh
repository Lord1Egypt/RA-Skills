#!/usr/bin/env bash
# RegexGuard -- Regex Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Immediate safety risk (ReDoS, injection, exponential blowup)
#   high     -- Significant correctness or portability bug requiring prompt fix
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   CB (Catastrophic Backtracking) -- 15 patterns (CB-001 to CB-015)
#   PE (Portability Errors)        -- 15 patterns (PE-001 to PE-015)
#   CE (Correctness Errors)        -- 15 patterns (CE-001 to CE-015)
#   MA (Maintainability Issues)    -- 15 patterns (MA-001 to MA-015)
#   AN (Anchoring & Boundaries)    -- 15 patterns (AN-001 to AN-015)
#   PI (Pattern Injection)         -- 15 patterns (PI-001 to PI-015)

set -euo pipefail

# ============================================================================
# 1. CATASTROPHIC BACKTRACKING (CB-001 through CB-015)
#    Detects nested quantifiers, exponential patterns, overlapping
#    alternations, unbounded repetitions with backtracks, and ReDoS vectors.
# ============================================================================

declare -a REGEXGUARD_CB_PATTERNS=()

REGEXGUARD_CB_PATTERNS+=(
  # CB-001: Nested quantifiers like (a+)+ or (x*)*  -- exponential blowup
  '\([^)]*[+*]\)[+*]|critical|CB-001|Nested quantifier detected (e.g. (a+)+ or (.*)*) causing exponential backtracking|Refactor to use atomic grouping or possessive quantifiers; flatten nested repetitions into a single quantifier'

  # CB-002: .* followed by .* on the same line -- overlapping greedy match
  '\.\*.*\.\*|high|CB-002|Multiple .* quantifiers on same line causing overlapping greedy match|Replace one .* with a more specific character class or use lazy .*? if supported'

  # CB-003: .+ followed by .+ on the same line -- overlapping greedy
  '\.\+.*\.\+|high|CB-003|Multiple .+ quantifiers on same line causing overlapping greedy match|Use specific character classes instead of repeated .+ to prevent backtracking'

  # CB-004: Quantifier applied to a group containing .* like (.*)+ or (.*){2,}
  '\([^)]*\.\*[^)]*\)[+*{]|critical|CB-004|Quantifier applied to group containing .* (catastrophic backtracking risk)|Remove outer quantifier or replace .* with a bounded character class inside the group'

  # CB-005: Backreference inside a repeated group like (\1)+ or (a\1)+
  '\([^)]*\\[0-9][^)]*\)[+*]|high|CB-005|Backreference inside a repeated group risks exponential backtracking|Move backreference outside the repeated group or use a non-backtracking assertion'

  # CB-006: Deeply nested groups with quantifiers like ((a+)+)+
  '\(\([^)]*[+*]\)[^)]*[+*]\)|critical|CB-006|Deeply nested groups with quantifiers (triple-nested repetition)|Flatten nested repetitions; use a single quantifier on the outermost group'

  # CB-007: Unbounded repetition {n,} with large n on complex subpattern
  '\([^)]+\)\{[0-9]+,\}|medium|CB-007|Unbounded repetition {n,} on a grouped subpattern risks excessive backtracking|Set an upper bound on the repetition or simplify the subpattern'

  # CB-008: Alternation where branches share a common prefix inside repetition
  '\([[:alnum:]]+[^)]*[[:alnum:]]+\)[+*]|medium|CB-008|Repeated group with alternation branches sharing common prefix|Factor out the common prefix before the alternation to reduce backtracking'

  # CB-009: Star-height > 1 pattern with character class like [a-z]*[a-z]*
  '\[[^]]+\][*+]\[[^]]+\][*+]|medium|CB-009|Adjacent repeated character classes with overlapping ranges|Merge adjacent character classes into a single quantified expression'

  # CB-010: .{0,N} with large N used multiple times
  '\.\{0,[0-9]{3,}\}|medium|CB-010|Unbounded repetition .{0,N} with large N creates excessive permutations|Reduce the upper bound or use a more specific character class'

  # CB-011: Greedy quantifier followed by the same character class
  '\[[^]]+\][+*][[:space:]]*\[[^]]+\]|low|CB-011|Greedy quantifier followed by overlapping character class|Combine into a single quantified expression to prevent backtracking on overlap'

  # CB-012: Optional group followed by same required pattern like (a*)?a
  '\([^)]*[*+]\)\?|low|CB-012|Optional group containing a quantifier (redundant nesting)|Remove the outer optional marker or simplify the inner quantifier'

  # CB-013: Dot-star at start of pattern without anchor
  '^[[:space:]]*["\x27/]\.\*|medium|CB-013|Pattern starting with .* without anchor causes full-string scan on every position|Add ^ anchor before .* or replace with a more specific prefix'

  # CB-014: Multiple optional groups in sequence like (a?)?(b?)?
  '\([^)]*\?\)[[:space:]]*\([^)]*\?\)|low|CB-014|Multiple optional groups in sequence creating exponential match paths|Simplify sequential optional groups into a single optional expression'

  # CB-015: Repetition of alternation group without possessive/atomic
  '\([^)]*\)\{[0-9]+,[0-9]+\}|low|CB-015|Bounded repetition on a complex group may cause polynomial backtracking|Consider using atomic groups or simplify the group contents'
)

# ============================================================================
# 2. PORTABILITY ERRORS (PE-001 through PE-015)
#    Detects non-POSIX features used in portable contexts, engine-specific
#    syntax, lookbehind in engines that lack support, named groups where
#    unsupported, and flag misuse across engines.
# ============================================================================

declare -a REGEXGUARD_PE_PATTERNS=()

REGEXGUARD_PE_PATTERNS+=(
  # PE-001: \d used instead of [0-9] (not supported in POSIX ERE/BRE)
  '\\d|critical|PE-001|\\d shorthand used (not portable to POSIX ERE/BRE, grep, awk -- silent match failure)|Replace \\d with [0-9] for POSIX-portable digit matching'

  # PE-002: \w used instead of [[:alnum:]_] (not supported in POSIX)
  '\\w|critical|PE-002|\\w shorthand used (not portable to POSIX ERE/BRE -- silent match failure)|Replace \\w with [[:alnum:]_] or [a-zA-Z0-9_] for POSIX portability'

  # PE-003: \s used instead of [[:space:]] (not supported in POSIX)
  '\\s|high|PE-003|\\s shorthand used (not portable to POSIX ERE/BRE)|Replace \\s with [[:space:]] for POSIX-portable whitespace matching'

  # PE-004: Lookahead used in a context that may not support it
  '\(\?=|medium|PE-004|Lookahead assertion used (not supported in POSIX, sed, grep -E)|Replace lookahead with capturing groups and post-match logic if targeting POSIX tools'

  # PE-005: Lookbehind used in a context that may not support it
  '\(\?<=|medium|PE-005|Lookbehind assertion used (not supported in many engines including JS pre-ES2018)|Replace lookbehind with alternative matching strategy for broader engine support'

  # PE-006: Negative lookahead used in possibly non-supporting context
  '\(\?!|medium|PE-006|Negative lookahead assertion used (not supported in POSIX/BRE tools)|Replace negative lookahead with post-match filtering for POSIX portability'

  # PE-007: Negative lookbehind used -- limited engine support
  '\(\?<!|medium|PE-007|Negative lookbehind assertion used (limited engine support)|Replace negative lookbehind with alternative approach for cross-engine compatibility'

  # PE-008: Named capture group (?P<name>...) -- Python-specific syntax
  '\(\?P<[[:alnum:]]+>|high|PE-008|Python-specific named group syntax used|Use JS/C# named groups or numbered groups for broader portability'

  # PE-009: Possessive quantifier (++, *+, ?+) -- not widely supported
  '[+*?]\+|medium|PE-009|Possessive quantifier used (not supported in Python, JS, POSIX)|Replace possessive quantifier with atomic group or standard quantifier with anchoring'

  # PE-010: Atomic group (?>...) -- limited engine support
  '\(\?>|medium|PE-010|Atomic group (?>...) used (not supported in Python, JS)|Replace atomic group with careful quantifier design or engine-specific alternative'

  # PE-011: \b word boundary used in POSIX context (not POSIX ERE)
  '\\b|low|PE-011|\\b word boundary used (not available in all POSIX implementations)|Use explicit boundary patterns like [^[:alnum:]_] for POSIX portability'

  # PE-012: Unicode property escape \p{...} -- engine-specific support
  '\\p\{|high|PE-012|Unicode property escape \\p{...} used (requires Unicode-aware engine)|Use explicit character ranges or verify target engine supports Unicode properties'

  # PE-013: Inline flags (?i) or (?m) used -- not universally supported
  '\(\?[imsx]+\)|low|PE-013|Inline flag modifier (?imsx) used (not supported in all engines)|Set flags via engine API or compile options instead of inline modifiers'

  # PE-014: \D \W \S uppercase shorthand used (non-POSIX)
  '\\[DWS]|low|PE-014|Uppercase shorthand \\D, \\W, or \\S used (not portable to POSIX)|Replace with negated POSIX classes: [^0-9], [^[:alnum:]_], [^[:space:]]'

  # PE-015: Conditional pattern (?(condition)yes-pattern) -- rare support
  '\(\?\([^)]+\)|low|PE-015|Conditional pattern (?(condition)...) used (Perl/.NET only)|Replace conditional pattern with alternation or separate regex for portability'
)

# ============================================================================
# 3. CORRECTNESS ERRORS (CE-001 through CE-015)
#    Detects unescaped dots matching anything, incorrect character class
#    ranges, off-by-one in quantifiers, greedy-when-lazy-needed issues.
# ============================================================================

declare -a REGEXGUARD_CE_PATTERNS=()

REGEXGUARD_CE_PATTERNS+=(
  # CE-001: Unescaped dot in what should be a literal match (e.g. file.txt)
  '[[:alnum:]]\.[[:alnum:]]|high|CE-001|Unescaped dot in pattern that appears to match a literal period (e.g. domain.com)|Escape the dot \\. when matching literal periods in filenames, domains, or IPs'

  # CE-002: Character class range with inverted endpoints like [z-a]
  '\[[^]]*[z-a][^]]*\]|high|CE-002|Inverted character class range [z-a] produces empty or error range|Correct the range order: use [a-z] instead of [z-a]'

  # CE-003: Character class range [A-z] includes non-alpha chars [\]^_`
  '\[A-z\]|critical|CE-003|Character class [A-z] includes non-alphabetic characters [\\]^_` between Z and a (security bypass risk)|Use [A-Za-z] or [[:alpha:]] for alphabetic-only matching'

  # CE-004: Greedy .* in a capture group that should be lazy
  '\([^)]*\.\*[^)]*\)|high|CE-004|Greedy .* inside capture group may overcapture content|Use .*? (lazy) or a specific character class to capture only the intended content'

  # CE-005: Quantifier {0,1} used where ? is clearer
  '\{0,1\}|low|CE-005|Verbose quantifier {0,1} used where ? is more readable|Replace {0,1} with ? for clarity and brevity'

  # CE-006: Quantifier {1,1} is redundant -- matches exactly once
  '\{1,1\}|low|CE-006|Redundant quantifier {1,1} matches exactly once|Remove {1,1} as it has no effect on the preceding element'

  # CE-007: Quantifier {0,} used where * is clearer
  '\{0,\}|low|CE-007|Verbose quantifier {0,} used where * is more readable|Replace {0,} with * for clarity and brevity'

  # CE-008: Quantifier {1,} used where + is clearer
  '\{1,\}|low|CE-008|Verbose quantifier {1,} used where + is more readable|Replace {1,} with + for clarity and brevity'

  # CE-009: Empty alternation branch (trailing or leading pipe in regex)
  '\(\)|high|CE-009|Empty group () or empty alternation branch in regex (always matches, likely bug)|Remove empty group or fill with intended pattern; empty branches always match'

  # CE-010: Escaped character that does not need escaping inside char class
  '\[([^]]*\\[-.][^]]*)\]|medium|CE-010|Unnecessarily escaped character inside character class|Place dash at start or end of class [a-z-] or dot directly [.] without backslash'

  # CE-011: Using . instead of [^/] or [^\\] for path matching
  '["\x27][^"]*\.\*[^"]*path|medium|CE-011|Using .* for path matching catches path separators unintentionally|Use [^/]* or [^\\\\]* instead of .* when matching path segments'

  # CE-012: Anchored pattern with unnecessary capture group ^(pattern)$
  '\^\([^)]+\)\$|low|CE-012|Entire pattern wrapped in capture group with ^ and $ anchors|Remove outer capture group if not referenced; use non-capturing (?:...) if needed'

  # CE-013: Duplicate character in character class like [aab]
  '\[([^]]*)(.).*\2.*\]|medium|CE-013|Duplicate character in character class has no effect|Remove duplicate characters from character class for clarity'

  # CE-014: Escaped digit \\0 outside valid backreference range
  '\\0[^-9]|critical|CE-014|Escaped \\0 used outside character class (null byte injection or invalid backref)|Use explicit null matching or correct the backreference number'

  # CE-015: Using [0-9] where \\d semantics differ (Unicode digits)
  '\\d.*[Uu]nicode|medium|CE-015|\\d used in Unicode context where it matches non-ASCII digits (e.g. Arabic numerals)|Use [0-9] if only ASCII digits intended; \\d matches all Unicode digit categories'
)

# ============================================================================
# 4. MAINTAINABILITY ISSUES (MA-001 through MA-015)
#    Detects overly complex patterns, missing comments, duplicated regex,
#    magic regex strings, and patterns that should be named constants.
# ============================================================================

declare -a REGEXGUARD_MA_PATTERNS=()

REGEXGUARD_MA_PATTERNS+=(
  # MA-001: Regex literal longer than 80 characters (overly complex)
  '[/][^/]{80,}[/]|critical|MA-001|Regex literal exceeds 80 characters (unmaintainable, likely contains hidden bugs)|Break into named sub-patterns or use regex builder with comments'

  # MA-002: Regex string longer than 80 characters in quotes
  '["\x27][^"]*\\[.*]{80,}["\x27]|critical|MA-002|Regex string exceeds 80 characters (unmaintainable, likely unreviewable)|Decompose into named parts using string concatenation or regex builder'

  # MA-003: Same regex literal repeated -- indicates duplication
  'new RegExp\([[:space:]]*["\x27][^"]{20,}["\x27]|high|MA-003|RegExp constructor with long literal string (potential duplication)|Extract to a named constant: const MY_PATTERN = /pattern/ or similar'

  # MA-004: Inline regex without any comments in surrounding context
  're\.compile\([[:space:]]*["\x27r][^"]{30,}|high|MA-004|Complex re.compile() pattern without explanatory comment|Add a comment explaining the regex purpose, or use re.VERBOSE with inline comments'

  # MA-005: Magic regex string passed directly to match/test/search
  '\.match\([[:space:]]*["\x27/][^"\x27/]{25,}|medium|MA-005|Long magic regex string passed directly to .match()|Extract to a named constant and add a descriptive comment'

  # MA-006: Magic regex string passed directly to replace
  '\.replace\([[:space:]]*[/][^/]{25,}|medium|MA-006|Long magic regex in .replace() call (hard to understand intent)|Extract regex to a named constant with a comment describing the replacement purpose'

  # MA-007: Regex with more than 5 capture groups
  '\([^)]*\)[^(]*\([^)]*\)[^(]*\([^)]*\)[^(]*\([^)]*\)[^(]*\([^)]*\)[^(]*\([^)]*\)|low|MA-007|Regex with 6+ capture groups is difficult to maintain|Use named capture groups or break into multiple simpler patterns'

  # MA-008: Regex repeated across multiple lines -- DRY violation
  'pattern[[:space:]]*=[[:space:]]*["\x27/][^"\x27/]{20,}|low|MA-008|Regex assigned to a local variable (check for duplication across files)|Centralize shared regex patterns in a constants file or patterns module'

  # MA-009: Regex with deeply nested groups (4+ levels)
  '\(\([^(]*\([^(]*\([^)]*\)|low|MA-009|Regex with 4+ levels of nested groups is overly complex|Flatten nesting by extracting inner groups into named sub-patterns'

  # MA-010: Hardcoded email regex (complex, usually wrong)
  '[[:alnum:]]+@[[:alnum:]]+\.[[:alnum:]]|high|MA-010|Hardcoded email validation regex (usually incomplete or incorrect)|Use a well-tested email validation library instead of custom regex'

  # MA-011: Hardcoded URL regex (complex, usually incomplete)
  'https\?:[/][/][^[:space:]]*|high|MA-011|Hardcoded URL validation regex (usually incomplete)|Use a URL parsing library instead of custom regex for validation'

  # MA-012: Hardcoded IP address regex pattern
  '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|low|MA-012|Hardcoded IPv4 regex (does not validate range 0-255)|Use a network address validation library or validate octets programmatically'

  # MA-013: Regex with no test coverage indication nearby
  'RegExp\([[:space:]]*["\x27][^"]{15,}|low|MA-013|Complex RegExp construction without nearby test coverage|Add unit tests covering edge cases for complex regex patterns'

  # MA-014: TODO or FIXME comment near a regex pattern
  '[Tt][Oo][Dd][Oo].*[Rr]eg[Ee]x|low|MA-014|TODO/FIXME comment near regex indicates known unfinished pattern|Resolve the TODO and finalize the regex pattern'

  # MA-015: Variable interpolation in regex string -- fragile
  '`[^`]*\$\{[^}]+\}[^`]*`.*[Rr]eg|medium|MA-015|Template literal with variable interpolation used as regex (fragile)|Use RegExp constructor with explicit escaping or parameterized pattern builder'
)

# ============================================================================
# 5. ANCHORING & BOUNDARIES (AN-001 through AN-015)
#    Detects missing ^ or $ allowing partial matches, \b misuse,
#    multiline flag missing for ^ in multiline input, and over-anchoring.
# ============================================================================

declare -a REGEXGUARD_AN_PATTERNS=()

REGEXGUARD_AN_PATTERNS+=(
  # AN-001: Validation regex without ^ anchor (allows prefix bypass)
  'valid.*=[[:space:]]*[/][^/^][^/]*[/]|critical|AN-001|Validation regex missing ^ start anchor (allows partial match bypass)|Add ^ anchor at the start of validation patterns to prevent prefix injection'

  # AN-002: Validation regex without $ anchor (allows suffix bypass)
  'valid.*=[[:space:]]*[/]\^[^$]*[/]|critical|AN-002|Validation regex missing $ end anchor (allows partial match bypass)|Add $ anchor at the end of validation patterns to prevent suffix injection'

  # AN-003: Pattern uses ^ without multiline flag on multiline input
  '\.match\([[:space:]]*[/]\^[^/]*[/][^m]*\)|medium|AN-003|Pattern with ^ anchor used without multiline flag on potential multiline input|Add m flag if input may contain newlines: /^pattern/m'

  # AN-004: Pattern uses $ without multiline flag on multiline input
  '\.match\([[:space:]]*[/][^/]*\$[/][^m]*\)|medium|AN-004|Pattern with $ anchor used without multiline flag on potential multiline input|Add m flag if input may contain newlines: /pattern$/m'

  # AN-005: Using ^ and $ in test() without considering multiline
  '\.test\([[:space:]]*[/]\^[^/]*\$[/][[:space:]]*\)|medium|AN-005|Anchored pattern in .test() without multiline consideration|Verify input is single-line or add m flag for multiline matching'

  # AN-006: Word boundary \\b used adjacent to non-word character
  '\\b[^[:alnum:]_]|low|AN-006|Word boundary \\b placed adjacent to a non-word character (always matches)|Remove \\b next to non-word characters as it provides no filtering'

  # AN-007: Missing anchor in security-sensitive regex (allowlist/denylist)
  'allow.*[/][^/^][[:alnum:]]|high|AN-007|Security allowlist regex without ^ anchor (bypassable)|Always anchor allowlist/denylist patterns with ^ and $ to prevent bypass'

  # AN-008: Missing anchor in deny/block regex
  'deny.*[/][^/^][[:alnum:]]|high|AN-008|Security denylist regex without ^ anchor (bypassable)|Always anchor denylist patterns with ^ and $ to match complete input'

  # AN-009: Line-start anchor in non-multiline split/replace
  '\.split\([[:space:]]*[/]\^|medium|AN-009|Line-start anchor ^ used in .split() (usually incorrect behavior)|Remove ^ from split pattern or verify multiline splitting intent'

  # AN-010: Using \\b for Unicode text (\\b is ASCII-only in most engines)
  '\\b.*[Uu]nicode|medium|AN-010|Word boundary \\b used with Unicode text (ASCII-only in most engines)|Use Unicode-aware boundary assertion or explicit boundary characters'

  # AN-011: Anchor $ does not match before \\n in some engines
  '\$[/][[:space:]]*[)][[:space:]]*[;]|low|AN-011|Pattern ending with $ may not match before \\n in all engines|Use \\z or \\Z for absolute end-of-string matching when newline handling matters'

  # AN-012: Double anchor ^^  or $$ in pattern (typo)
  '\^\^|high|AN-012|Double start anchor ^^ in pattern (likely typo)|Remove the duplicate ^ anchor'

  # AN-013: Double end anchor $$ in pattern (typo)
  '\$\$|high|AN-013|Double end anchor $$ in pattern (likely typo)|Remove the duplicate $ anchor'

  # AN-014: Using .* at pattern boundaries instead of proper anchor
  '[/]\.\*[^/]*\.\*[/]|low|AN-014|Pattern uses .* at both boundaries instead of anchors|Replace leading/trailing .* with ^ and $ anchors for clarity and performance'

  # AN-015: Pattern anchor followed immediately by quantifier ^* or ^+
  '\^[*+?]|low|AN-015|Anchor ^ followed immediately by quantifier (meaningless)|Remove the quantifier after ^ as anchors are zero-width assertions'
)

# ============================================================================
# 6. PATTERN INJECTION (PI-001 through PI-015)
#    Detects user input concatenated into regex without escaping, regex
#    DoS vectors, unsanitized pattern compilation, and dynamic regex abuse.
# ============================================================================

declare -a REGEXGUARD_PI_PATTERNS=()

REGEXGUARD_PI_PATTERNS+=(
  # PI-001: new RegExp() with user-controlled variable (injection risk)
  'new[[:space:]]RegExp\([[:space:]]*[a-zA-Z_][[:alnum:]_]*[[:space:]]*\)|critical|PI-001|RegExp constructor with unsanitized variable input (regex injection risk)|Escape user input with escapeRegExp() before passing to RegExp constructor'

  # PI-002: String concatenation into RegExp constructor
  'new[[:space:]]RegExp\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*[+]|critical|PI-002|String concatenation into RegExp constructor (injection vector)|Use template with escapeRegExp() for dynamic parts: new RegExp(escapeRegExp(input))'

  # PI-003: Python re.compile with variable (unsanitized)
  're\.compile\([[:space:]]*[a-zA-Z_][[:alnum:]_.]*[[:space:]]*\)|critical|PI-003|re.compile() with unsanitized variable input (regex injection risk)|Use re.escape() on user input before compiling: re.compile(re.escape(user_input))'

  # PI-004: Python re.compile with string concatenation
  're\.compile\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*[+]|high|PI-004|re.compile() with string concatenation (injection vector)|Use re.escape() on dynamic parts: re.compile(prefix + re.escape(user_input))'

  # PI-005: Ruby Regexp.new with variable input
  'Regexp\.new\([[:space:]]*[a-zA-Z_]|high|PI-005|Regexp.new() with unsanitized variable input (regex injection)|Use Regexp.escape() on user input: Regexp.new(Regexp.escape(input))'

  # PI-006: Go regexp.Compile with variable (unsanitized)
  'regexp\.Compile\([[:space:]]*[a-zA-Z_]|high|PI-006|regexp.Compile() with unsanitized variable input (regex injection)|Use regexp.QuoteMeta() on user input before compiling'

  # PI-007: Java Pattern.compile with variable
  'Pattern\.compile\([[:space:]]*[a-zA-Z_]|high|PI-007|Pattern.compile() with unsanitized variable input (regex injection)|Use Pattern.quote() on user input: Pattern.compile(Pattern.quote(input))'

  # PI-008: Template literal used in regex (JS/TS injection vector)
  'new[[:space:]]RegExp\([[:space:]]*`|high|PI-008|Template literal in RegExp constructor (dynamic injection vector)|Escape all interpolated variables with escapeRegExp() before constructing regex'

  # PI-009: f-string used in re.compile (Python injection vector)
  're\.compile\([[:space:]]*f["\x27]|high|PI-009|f-string in re.compile() (dynamic regex injection vector)|Use re.escape() on all interpolated variables in the f-string'

  # PI-010: User input from request/query used in regex
  'req\.[a-z]*\.[[:alnum:]]*.*[Rr]eg[Ee]xp|medium|PI-010|Request parameter used in regex construction (injection/DoS risk)|Sanitize and validate request input before using in regex; prefer allowlists'

  # PI-011: eval() or exec() with regex pattern
  'eval\([^)]*[Rr]eg|medium|PI-011|eval() used with regex construction (code injection risk)|Never use eval() for regex construction; use the RegExp constructor safely'

  # PI-012: URL parameter or query string used in regex
  'params\[["\x27][^"]*["\x27]\].*[Rr]eg|medium|PI-012|URL parameter used in regex construction (injection risk)|Validate and escape URL parameters before using in regex patterns'

  # PI-013: grep/sed/awk with variable expansion in pattern
  'grep.*\$[{(a-zA-Z]|medium|PI-013|Shell variable expanded in grep/sed pattern without quoting (injection risk)|Quote variables and escape special characters: grep -F "$var" or grep -E "$(printf "%s" "$var")"'

  # PI-014: Dynamic regex without length or complexity limit
  '[Rr]eg[Ee]xp\([^)]*\).*[Rr]eq|low|PI-014|Dynamic regex from user input without length or complexity validation|Add length limits and complexity checks before compiling user-supplied patterns'

  # PI-015: Regex timeout not configured for user-supplied patterns
  '[Rr]eg[Ee]x.*[Tt]imeout|low|PI-015|Regex execution without timeout configuration for user-supplied patterns|Set a regex execution timeout (e.g. RE2 safe regex or timeout wrapper) for user input'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
regexguard_pattern_count() {
  local count=0
  count=$((count + ${#REGEXGUARD_CB_PATTERNS[@]}))
  count=$((count + ${#REGEXGUARD_PE_PATTERNS[@]}))
  count=$((count + ${#REGEXGUARD_CE_PATTERNS[@]}))
  count=$((count + ${#REGEXGUARD_MA_PATTERNS[@]}))
  count=$((count + ${#REGEXGUARD_AN_PATTERNS[@]}))
  count=$((count + ${#REGEXGUARD_PI_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
regexguard_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_regexguard_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_regexguard_patterns_for_category() {
  local category="$1"
  case "$category" in
    CB|cb) echo "REGEXGUARD_CB_PATTERNS" ;;
    PE|pe) echo "REGEXGUARD_PE_PATTERNS" ;;
    CE|ce) echo "REGEXGUARD_CE_PATTERNS" ;;
    MA|ma) echo "REGEXGUARD_MA_PATTERNS" ;;
    AN|an) echo "REGEXGUARD_AN_PATTERNS" ;;
    PI|pi) echo "REGEXGUARD_PI_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_regexguard_category_label() {
  local category="$1"
  case "$category" in
    CB|cb) echo "Catastrophic Backtracking" ;;
    PE|pe) echo "Portability Errors" ;;
    CE|ce) echo "Correctness Errors" ;;
    MA|ma) echo "Maintainability Issues" ;;
    AN|an) echo "Anchoring & Boundaries" ;;
    PI|pi) echo "Pattern Injection" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_regexguard_categories() {
  echo "CB PE CE MA AN PI"
}

# Get categories available for a given tier level
# free=0 -> CB, PE (30 patterns)
# pro=1  -> CB, PE, CE, MA (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_regexguard_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "CB PE CE MA AN PI"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "CB PE CE MA"
  else
    echo "CB PE"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
regexguard_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in CB PE CE MA AN PI; do
      regexguard_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_regexguard_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_regexguard_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_regexguard_category() {
  local category="$1"
  case "$category" in
    CB|cb|PE|pe|CE|ce|MA|ma|AN|an|PI|pi) return 0 ;;
    *) return 1 ;;
  esac
}
