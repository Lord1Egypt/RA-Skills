# R Test Script
# Purpose: Verify R CLI is working correctly

# Print R version
cat("R Version:\n")
print(R.version.string)

# Print platform info
cat("\nPlatform:\n")
print(Sys.info()["sysname"])

# Simple calculation test
cat("\nCalculation test (2 + 2 = ", 2 + 2, ")\n", sep="")

# Check if common packages are available
cat("\nChecking common packages:\n")
packages <- c("dplyr", "ggplot2")
for (pkg in packages) {
  if (require(pkg, character.only=TRUE, quietly=TRUE)) {
    cat("  ✅", pkg, "is installed\n")
  } else {
    cat("  ⚠️", pkg, "is NOT installed\n")
  }
}

cat("\n✅ R test completed successfully!\n")
