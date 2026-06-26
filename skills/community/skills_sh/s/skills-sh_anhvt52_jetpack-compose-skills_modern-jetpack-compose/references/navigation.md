# Navigation Compose

## Standard Setup

Use Navigation Compose (`androidx.navigation:navigation-compose`) as the
navigation solution. Do not use Fragments for Compose-first apps.

```kotlin
// In your root composable
val navController = rememberNavController()

NavHost(
    navController = navController,
    startDestination = HomeRoute
) {
    composable<HomeRoute> { HomeScreen(navController) }
    composable<DetailRoute> { backStackEntry ->
        val route: DetailRoute = backStackEntry.toRoute()
        DetailScreen(bookId = route.bookId)
    }
}
```


## Type-Safe Navigation (Navigation 2.8+)

Use Kotlin Serialization with `@Serializable` for type-safe routes. This
eliminates string-based route definitions and provides compile-time safety.

```kotlin
// Define routes as serializable objects/classes
@Serializable
object HomeRoute

@Serializable
data class DetailRoute(val bookId: String)

// Navigate
navController.navigate(DetailRoute(bookId = "abc123"))

// Retrieve arguments
val route: DetailRoute = backStackEntry.toRoute()
```

Add the dependency: `androidx.navigation:navigation-compose:2.8+` and
`org.jetbrains.kotlinx:kotlinx-serialization-json`.


## rememberNavController Placement

- `rememberNavController()` should be called **at the top level** of the app
  (in `MainActivity` or the root composable). Do not pass it deep into the
  composable tree.
- Pass only callbacks (e.g., `onNavigateToDetail: (String) -> Unit`) to child
  composables, not the `NavController` itself. This keeps composables decoupled
  from navigation.


## Nested Navigation Graphs

Organize routes into nested graphs for feature modules:

```kotlin
NavHost(navController, startDestination = "home") {
    homeGraph(navController)
    settingsGraph(navController)
}

fun NavGraphBuilder.homeGraph(navController: NavController) {
    navigation(startDestination = HomeRoute, route = "home") {
        composable<HomeRoute> { HomeScreen(...) }
        composable<DetailRoute> { DetailScreen(...) }
    }
}
```


## BackStack-Scoped ViewModels

To share state between screens within the same navigation graph, use a
`NavBackStackEntry`-scoped ViewModel:

```kotlin
@Composable
fun HomeScreen(navController: NavController) {
    val backStackEntry = remember(navController) {
        navController.getBackStackEntry("home") // the graph's route
    }
    val sharedViewModel: SharedViewModel = viewModel(backStackEntry)
}
```


## Arguments: Pass IDs, Not Objects

Never pass full domain objects through navigation arguments. Pass an ID and
load the object at the destination.

```kotlin
// Wrong — fragile, size-limited, not type-safe
navController.navigate("detail?bookJson=$encodedJson")

// Correct — pass ID, load in destination ViewModel
navController.navigate(DetailRoute(bookId = book.id))
```


## Deep Links

```kotlin
composable<DetailRoute>(
    deepLinks = listOf(navDeepLink<DetailRoute>(basePath = "https://myapp.com/book"))
) { ... }
```

Declare deep links in `AndroidManifest.xml` with the matching `<intent-filter>`.


## Back Navigation

- Use `BackHandler` for intercepting the back gesture within a composable.
- For predictive back animation support, use Navigation Compose 2.7+ which
  handles it automatically.
