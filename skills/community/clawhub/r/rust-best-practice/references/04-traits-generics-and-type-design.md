# Traits, Generics, and Type Design

## Table of contents
1. Generics vs. trait objects (`dyn Trait`)
2. Designing good traits
3. `From`/`Into`, `TryFrom`/`TryInto`
4. Operator overloading
5. The builder pattern
6. Newtype pattern
7. Typestate pattern
8. Sealed traits and the orphan rule
9. Marker traits and blanket impls
10. Anti-patterns checklist

---

## 1. Generics vs. trait objects (`dyn Trait`)

| | Generics (`impl Trait` / `<T: Trait>`) | Trait objects (`Box<dyn Trait>` / `&dyn Trait`) |
|---|---|---|
| Dispatch | Static (monomorphized at compile time) | Dynamic (vtable lookup at runtime) |
| Binary size | Larger (code duplicated per concrete type) | Smaller |
| Runtime cost | None — often fully inlined | Indirect call + no inlining across the boundary |
| Heterogeneous collections | Not directly possible | `Vec<Box<dyn Trait>>` works naturally |
| Object safety required? | No | Yes (see below) |

Default to generics unless you specifically need runtime polymorphism (a collection of different concrete types behind one interface, a plugin system, or reducing compile times/binary size in a huge codebase). A trait is **object-safe** (can be used as `dyn Trait`) only if it has no generic methods, doesn't return `Self` by value, and its methods take `&self`/`&mut self`/`Box<self>` rather than `self` by value in most cases — see the Reference's "Trait objects" chapter for the precise rules.

```rust
// Generic: zero-cost, monomorphized per call site
fn render<W: Write>(writer: &mut W, doc: &Document) -> io::Result<()> { /* ... */ }

// Trait object: needed because the list holds different concrete plugin types
struct App { plugins: Vec<Box<dyn Plugin>> }
```

## 2. Designing good traits

- Keep traits small and focused (interface segregation) — prefer several small traits over one large "god trait"; downstream code can compose bounds (`T: Read + Seek`).
- Provide default method implementations where a sensible general implementation exists, so implementors only need to override what's specific to them.
- Use associated types (not generic type parameters) when a trait implementation determines a type uniquely per `Self` (e.g. `Iterator::Item`); use generic type parameters when a type can implement the trait multiple times for different type arguments (e.g. `From<T>` for multiple `T`).

```rust
trait Storage {
    type Error: std::error::Error;
    fn get(&self, key: &str) -> Result<Option<Vec<u8>>, Self::Error>;
    fn set(&mut self, key: &str, value: &[u8]) -> Result<(), Self::Error>;
}
```

## 3. `From`/`Into`, `TryFrom`/`TryInto`

Implement `From<T> for U` (never implement `Into` directly — the blanket impl `impl<T, U: From<T>> Into<U> for T` gives you `Into` for free) whenever a conversion is infallible and doesn't lose information in a surprising way. Implement `TryFrom` when the conversion can fail:

```rust
struct Meters(f64);
struct Feet(f64);

impl From<Feet> for Meters {
    fn from(f: Feet) -> Self { Meters(f.0 * 0.3048) }
}

impl TryFrom<i64> for Age {
    type Error = AgeError;
    fn try_from(value: i64) -> Result<Self, Self::Error> {
        if (0..=150).contains(&value) { Ok(Age(value as u8)) } else { Err(AgeError::OutOfRange) }
    }
}
```

This is also the mechanism that makes `?` automatically convert error types (see `references/03-error-handling.md` §2).

## 4. Operator overloading

Implement `std::ops` traits (`Add`, `Sub`, `Mul`, `Index`, etc.) only when the operator has an unsurprising, mathematically-conventional meaning for your type (API Guidelines `C-OVERLOAD`) — e.g. `Add` for a `Vector2` or `Money` type is natural; `Add` meaning "concatenate unrelated things" is surprising and should be a named method instead.

```rust
impl std::ops::Add for Point {
    type Output = Point;
    fn add(self, rhs: Point) -> Point { Point { x: self.x + rhs.x, y: self.y + rhs.y } }
}
```

## 5. The builder pattern

Use when a type has many optional/defaultable construction parameters (avoids unreadable multi-argument constructors and telescoping `Option` parameters):

```rust
#[derive(Default)]
pub struct RequestBuilder {
    url: String,
    timeout: Option<Duration>,
    retries: u32,
}

impl RequestBuilder {
    pub fn new(url: impl Into<String>) -> Self { Self { url: url.into(), ..Default::default() } }
    pub fn timeout(mut self, d: Duration) -> Self { self.timeout = Some(d); self }
    pub fn retries(mut self, n: u32) -> Self { self.retries = n; self }
    pub fn build(self) -> Request { /* validate + construct */ }
}
```

For crates targeting a wide audience, consider the `bon` or `typed-builder` crates, which generate this boilerplate (including compile-time enforcement of required fields) from a derive macro.

## 6. Newtype pattern

Wrap a primitive/foreign type in a tuple struct to (a) get a distinct type the compiler won't let you mix up, (b) attach semantics/invariants, or (c) implement a foreign trait for a foreign type, working around the orphan rule (§8):

```rust
struct UserId(u64);
struct ProductId(u64);
// fn charge(user: UserId, amount: Money) — now impossible to accidentally pass a ProductId
```

This is the single highest-leverage technique for "make invalid states unrepresentable" (see SKILL.md core philosophy) — reach for it liberally for IDs, units, validated strings (`Email(String)` constructed only via a validating `TryFrom<&str>`), etc.

## 7. Typestate pattern

Encode a state machine's valid transitions in the type system so illegal transitions are compile errors, not runtime bugs:

```rust
struct Locked;
struct Unlocked;
struct Door<State> { _state: std::marker::PhantomData<State> }

impl Door<Locked> {
    fn unlock(self, key: &Key) -> Door<Unlocked> { Door { _state: PhantomData } }
}
impl Door<Unlocked> {
    fn open(&self) { /* ... */ }
    fn lock(self) -> Door<Locked> { Door { _state: PhantomData } }
}
// Door<Locked>::open() simply doesn't exist — caught at compile time.
```

Powerful for protocol implementations, builders with required-field enforcement, and resource lifecycle management — but adds real complexity; reserve for cases where illegal-state bugs are costly (protocol correctness, safety-critical sequencing), not every small struct.

## 8. Sealed traits and the orphan rule

The **orphan rule**: you may only `impl Trait for Type` if either the trait or the type is defined in your own crate. This prevents conflicting impls across the ecosystem. Work around needing a foreign trait on a foreign type via the newtype pattern (§6).

**Sealed traits** prevent downstream crates from implementing your trait for their own types, when you want to keep the set of implementors closed (e.g. to add methods later without it being a breaking change):

```rust
mod sealed { pub trait Sealed {} }

pub trait MyTrait: sealed::Sealed { /* ... */ }
impl sealed::Sealed for MyConcreteType {}
impl MyTrait for MyConcreteType { /* ... */ }
// External crates cannot impl sealed::Sealed, so cannot impl MyTrait either.
```

## 9. Marker traits and blanket impls

Marker traits (`Send`, `Sync`, `Sized`, `Copy`) carry no methods — they describe a property checked by the compiler or opted into. Blanket impls (`impl<T: Display> ToString for T`) implement a trait for every type satisfying a bound — powerful but can make error messages harder to read and can conflict with downstream impls; use judiciously in library code and document clearly.

## 10. Anti-patterns checklist

- [ ] `Box<dyn Trait>` used where a generic parameter would be zero-cost and equally simple
- [ ] Giant "god traits" with 20+ methods that no single type naturally implements fully
- [ ] Manually implementing `Into` instead of `From` (loses the automatic blanket impl and is redundant)
- [ ] Operator trait impls (`Add`, `Index`, ...) with non-obvious/surprising semantics
- [ ] Primitive obsession: raw `u64`/`String` used for IDs, currency, validated input instead of newtypes
- [ ] Long constructors with many positional `Option<T>` parameters instead of a builder
- [ ] Public structs with all fields `pub` where a smart constructor should enforce invariants

---

## Real references

- The Rust Programming Language, ch. 10 (Traits & Generics) and ch. 17/18 (trait objects, patterns): https://doc.rust-lang.org/book/ch10-00-generics.html
- The Rust Reference — Trait objects, object safety: https://doc.rust-lang.org/reference/types/trait-object.html
- Rust API Guidelines — full guideline set (naming, interoperability, C-OVERLOAD, C-NEWTYPE): https://rust-lang.github.io/api-guidelines/
- `std::convert` module (`From`/`Into`/`TryFrom`): https://doc.rust-lang.org/std/convert/index.html
- "Rust for Rustaceans" by Jon Gjengset (O'Reilly/No Starch Press) — ch. 3 "Designing Interfaces" covers builders, sealed traits, typestate in depth: https://rust-for-rustaceans.com/
- "Effective Rust" by David Drysdale — Items on trait design and error handling: https://effective-rust.com/
- `typed-builder` crate: https://docs.rs/typed-builder/latest/typed_builder/
