# Code Hygiene

## Secrets & Security

- Never hardcode API keys, tokens, or secrets in source files.
- Store secrets in `local.properties` (gitignored) and read via `BuildConfig`.
- For runtime secrets, use encrypted `SharedPreferences` or the Android Keystore.
- Never log sensitive user data.


## Testing

### Unit Tests

- All ViewModel logic must have unit tests.
- Test `UiState` transitions: given initial state + event → expected state.
- Use `kotlinx-coroutines-test` with `StandardTestDispatcher` and `runTest`.
- Use `turbine` for testing `Flow` / `StateFlow` emissions.

```kotlin
@Test
fun `loading books emits success state`() = runTest {
    val viewModel = HomeViewModel(FakeRepository())
    viewModel.uiState.test {
        assertEquals(HomeUiState.Loading, awaitItem())
        assertEquals(HomeUiState.Success(fakeBooks), awaitItem())
    }
}
```

### Composable Tests

- Use `ComposeTestRule` (`createComposeRule()`) for composable UI tests.
- Test composables in isolation with controlled state — do not use real ViewModels
  in composable tests.

```kotlin
@Test
fun bookCard_displaysTitle() {
    composeTestRule.setContent {
        BookCard(book = fakeBook, onClick = {})
    }
    composeTestRule.onNodeWithText(fakeBook.title).assertIsDisplayed()
}
```

### Screenshot Tests

For visual regression testing of design-critical screens, use screenshot tests
with `paparazzi` or `roborazzi`.


## Lint & Static Analysis

- All lint warnings must be resolved or explicitly suppressed with a comment
  explaining why.
- Configure `detekt` for Kotlin static analysis. No detekt errors on CI.
- Enable Compose-specific lint rules via `androidx.compose.lint`.


## No Magic Numbers

Replace hardcoded numeric values with named constants:

```kotlin
// Wrong
Modifier.padding(16.dp)

// Correct
object Spacing {
    val medium = 16.dp
    val large = 24.dp
}
Modifier.padding(Spacing.medium)
```

Or use `MaterialTheme`-derived values when applicable.


## Resource Naming

- Follow Android resource naming conventions:
  - Strings: `feature_component_description` (e.g., `home_book_card_title`)
  - Drawables: `ic_` for icons, `img_` for images, `bg_` for backgrounds
  - Colors: defined in the theme, not in `colors.xml` for M3 projects
- All user-facing strings must be in `strings.xml` — no hardcoded strings
  in composables.


## Compose Version Alignment

- Always use the Compose BOM to manage Compose library versions. Do not specify
  individual Compose library versions manually.
- Keep the BOM and `composeOptions.kotlinCompilerExtensionVersion` in sync.
