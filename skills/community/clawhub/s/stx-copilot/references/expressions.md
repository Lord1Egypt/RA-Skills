# Map Rules and Expressions Reference

## Syntax

Rules are assigned per output field. Begin with `=`.

```
= InputField                             -- copy field value
= LEFT(TRIM(Name), 35)                  -- string transform
= IF(Type = "MT103", "CREDIT", "OTHER") -- conditional
= TONUMBER(Amount) * 100                -- numeric operation
= CURRENTDATETIME("YYYYMMDD")           -- date
= FAIL("Mandatory field missing")       -- explicit failure
```

## WHEN Clause (Component-Level)

Controls whether a component (record/group) is produced. Returns boolean.

```
WHEN InputRecord.MsgType = "MT103"
WHEN COUNT(LineItem) > 0
WHEN NOT ISNUMBER(Field)
```

Iteration stops when condition is false. Used on repeating output components.

## Initialization Rules

Default values applied before input parsing. Useful for mandatory fields not always present in input:
```
= "USD"                   -- default currency
= CURRENTDATE("YYYYMMDD") -- today as default date
```

## Component Rules vs Map Rules

| Type | Context | Returns |
|---|---|---|
| **Component rule** | Applied to a type in the type tree | Boolean (true/false) |
| **Map rule** | Applied to an output field in a map | Data value |

## Built-in Functions — Full Reference

### String
| Function | Usage |
|---|---|
| `LEFT(str, n)` | First n characters |
| `RIGHT(str, n)` | Last n characters |
| `MID(str, start, n)` | Substring from position |
| `FIND(str, search)` | Position of search in str |
| `SUBSTITUTE(str, old, new)` | Replace all occurrences |
| `TRIM(str)` | Remove leading/trailing spaces |
| `TRIMLEFT(str)` | Remove leading spaces only |
| `TRIMRIGHT(str)` | Remove trailing spaces only |
| `SQUEEZE(str)` | Collapse internal whitespace |
| `UPPERCASE(str)` | Convert to upper case |
| `LOWERCASE(str)` | Convert to lower case |
| `FILLRIGHT(str, n, char)` | Right-pad to length n with char |
| `FILLLEFT(str, n, char)` | Left-pad to length n with char |
| `PACKAGE(str, delim)` | Join multiple values with delimiter |
| `WORD(str, n, delim)` | Extract nth word |
| `COUNTSTRING(str, search)` | Count occurrences of search |

### Numeric
| Function | Usage |
|---|---|
| `INT(n)` | Integer part (truncate) |
| `ROUND(n, decimals)` | Round to decimal places |
| `TRUNCATE(n, decimals)` | Truncate to decimal places |
| `MOD(n, divisor)` | Modulus |
| `ABS(n)` | Absolute value |
| `SQRT(n)` | Square root |
| `POWER(base, exp)` | Exponentiation |
| `SUM(field)` | Sum over iterated instances |
| `COUNT(field)` | Count instances |
| `MIN(a, b)` | Minimum of two values |
| `MAX(a, b)` | Maximum of two values |
| `LOG(n)` | Natural log |
| `EXP(n)` | e raised to n |

### Date/Time
| Function | Usage |
|---|---|
| `CURRENTDATE(format)` | Today's date, e.g. `"YYYYMMDD"` |
| `CURRENTDATETIME(format)` | Now, e.g. `"YYYY-MM-DDThh:mm:ss"` |
| `CURRENTTIME(format)` | Current time |
| `DATETOTEXT(date, fromFmt, toFmt)` | Reformat date string |
| `TEXTTODATE(str, format)` | Parse date string |
| `ADDDAYS(date, n, format)` | Add n days to date |
| `ADDHOURS(datetime, n, format)` | Add n hours |
| `DATETONUMBER(date, format)` | Date → numeric (e.g., epoch) |
| `NUMBERTODATE(n, format)` | Numeric → date string |
| `FROMDATETIME(datetime, component)` | Extract part: YEAR, MONTH, DAY, HOUR, MINUTE |
| `TODATETIME(y, m, d, h, min, s)` | Construct datetime from parts |

### Conversion
| Function | Usage |
|---|---|
| `TONUMBER(str)` | String → number |
| `NUMBERTOTEXT(n, format)` | Number → string with format |
| `TEXTTONUMBER(str)` | Explicit string → number |
| `PACK(str)` | ASCII → packed decimal (BCD) |
| `UNPACK(bcd)` | Packed decimal → ASCII |
| `ZONE(str)` | ASCII → zoned decimal |
| `UNZONE(str)` | Zoned decimal → ASCII |
| `TEXTTOBCD(str)` | Text → binary-coded decimal |
| `BCDTOTEXT(bcd)` | BCD → text |
| `BASE64TOTEXT(b64)` | Base64 decode |
| `TEXTTOBASE64(str)` | Base64 encode |
| `CONVERT(str, fromCP, toCP)` | Code page conversion |
| `HEXTEXTTOSTREAM(hex)` | Hex string → byte stream |
| `STREAMTOHEXTEXT(bytes)` | Byte stream → hex string |

### Lookup / Reference
| Function | Usage |
|---|---|
| `LOOKUP(key, table, keyCol, valCol)` | Table lookup from file |
| `DBLOOKUP(key, table, keyCol, valCol)` | Database lookup |
| `DBQUERY(sql)` | Arbitrary SQL query |
| `SEARCHUP(val, array)` | Binary search ascending array |
| `SEARCHDOWN(val, array)` | Binary search descending array |
| `SORTUP(field)` | Sort instances ascending |
| `SORTDOWN(field)` | Sort instances descending |
| `INDEX(field, n)` | Nth instance of a repeating field |
| `INDEXABS(field, n)` | Nth instance (absolute position) |
| `MEMBER(val, list)` | True if val in list |
| `UNIQUE(field)` | Deduplicate instances |
| `CHOOSE(n, v1, v2, ...)` | Select nth value from list |
| `EXTRACT(field, filter)` | Extract matching instances |

### Logical
| Function | Usage |
|---|---|
| `IF(cond, true, false)` | Conditional value |
| `ALL(cond)` | True if all instances match |
| `EITHER(a, b)` | First non-empty value |
| `OR(a, b)` | Logical OR |
| `NOT(cond)` | Logical NOT |
| `ISALPHA(str)` | True if all alphabetic |
| `ISNUMBER(str)` | True if numeric |
| `ISLOWER(str)` | True if all lower case |
| `ISUPPER(str)` | True if all upper case |
| `VALID(expr)` | True if expression does not error |

### Error Handling
| Function | Usage |
|---|---|
| `FAIL(msg)` | Raise fatal error with message |
| `REJECT(msg)` | Reject current record with message |
| `ISERROR(expr)` | True if expression errored |
| `ONERROR(expr, fallback)` | Return fallback if expr errors |
| `CONTAINSERRORS(field)` | True if field has error instances |
| `LASTERRORCODE()` | Code of last error |
| `LASTERRORMSG()` | Message of last error |

### Environment / Runtime
| Function | Usage |
|---|---|
| `GETRESOURCEALIAS(name)` | Resolve resource alias (connection pooling) |
| `GETTXINSTALLDIRECTORY()` | ITX installation path |
| `GETLOCALE()` | Current locale string |
| `GETPARTITIONNAME()` | Launcher partition name |
| `GETFILENAME(card)` | Filename being processed by card |
| `GETANDSET(var, val)` | Get current value and set new value (thread-safe counter) |

## Common Patterns

### MT Amount Field (15 chars, 2 decimal places)
```
= FILLRIGHT(NUMBERTOTEXT(TONUMBER(Amount), "0.00"), 15, " ")
```

### SWIFT Date YYMMDD → ISO YYYY-MM-DD
```
= "20" + LEFT(SWIFTDate, 2) + "-" + MID(SWIFTDate, 3, 2) + "-" + RIGHT(SWIFTDate, 2)
```

### BIC 8 → 11 (append XXX)
```
= IF(LEN(BIC) = 8, BIC + "XXX", BIC)
```

### Safe numeric with fallback
```
= IF(ISNUMBER(RawAmount), TONUMBER(RawAmount), 0)
```

### Multi-branch conditional (use nested IF or CHOOSE)
```
= IF(Type = "C", "CREDIT", IF(Type = "D", "DEBIT", FAIL("Unknown type: " + Type)))
```
