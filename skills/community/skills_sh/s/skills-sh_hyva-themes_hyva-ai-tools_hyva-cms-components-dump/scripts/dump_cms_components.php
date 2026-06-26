#!/usr/bin/env php
<?php
/**
 * Dumps all Hyvä CMS components from active modules.
 *
 * Reads app/etc/config.php to get active modules in load order,
 * finds all etc/hyva_cms/components.json files, and merges them.
 *
 * Usage: php dump_cms_components.php
 * Output: Merged JSON of all CMS component definitions
 */

declare(strict_types=1);

/**
 * Find Magento root by traversing up from current directory
 */
function findMagentoRoot(): ?string
{
    $dir = getcwd();

    while ($dir !== '/' && $dir !== '') {
        if (file_exists($dir . '/app/etc/config.php')) {
            return $dir;
        }
        $parent = dirname($dir);
        if ($parent === $dir) {
            break; // Reached filesystem root
        }
        $dir = $parent;
    }

    return null;
}

$magentoRoot = findMagentoRoot();

if ($magentoRoot === null) {
    fwrite(STDERR, "Error: app/etc/config.php not found. Run from within a Magento project directory.\n");
    exit(1);
}

$configPath = $magentoRoot . '/app/etc/config.php';

// Load module configuration
$config = require $configPath;
$modules = $config['modules'] ?? [];

// Filter to only enabled modules (value === 1)
$enabledModules = array_keys(array_filter($modules, fn($status) => $status === 1));

// Build a map of module name -> components.json path
$moduleComponentsMap = [];

// Search in app/code/
$appCodePattern = $magentoRoot . '/app/code/*/*/etc/hyva_cms/components.json';
foreach (glob($appCodePattern) as $componentsFile) {
    $moduleName = getModuleNameFromPath($componentsFile, $magentoRoot);
    if ($moduleName) {
        $moduleComponentsMap[$moduleName] = $componentsFile;
    }
}

// Search in vendor/
// Pattern: vendor/{vendor}/{package}/src/etc/hyva_cms/components.json
// or: vendor/{vendor}/{package}/etc/hyva_cms/components.json
$vendorDirs = glob($magentoRoot . '/vendor/*/*', GLOB_ONLYDIR);
foreach ($vendorDirs as $vendorDir) {
    // Check various possible locations for components.json
    $possiblePaths = [
        $vendorDir . '/etc/hyva_cms/components.json',
        $vendorDir . '/src/etc/hyva_cms/components.json',
    ];

    // Also check subdirectories (for packages with multiple modules)
    $subDirs = glob($vendorDir . '/*/etc/hyva_cms/components.json');
    $srcSubDirs = glob($vendorDir . '/src/*/etc/hyva_cms/components.json');
    $possiblePaths = array_merge($possiblePaths, $subDirs, $srcSubDirs);

    foreach ($possiblePaths as $componentsFile) {
        if (file_exists($componentsFile)) {
            $moduleName = getModuleNameFromPath($componentsFile, $magentoRoot);
            if ($moduleName) {
                $moduleComponentsMap[$moduleName] = $componentsFile;
            }
        }
    }
}

// Merge components in module load order
$mergedComponents = [];

foreach ($enabledModules as $moduleName) {
    if (isset($moduleComponentsMap[$moduleName])) {
        $componentsFile = $moduleComponentsMap[$moduleName];
        $content = file_get_contents($componentsFile);
        $components = json_decode($content, true);

        if (json_last_error() !== JSON_ERROR_NONE) {
            fwrite(STDERR, "Warning: Invalid JSON in $componentsFile: " . json_last_error_msg() . "\n");
            continue;
        }

        if (is_array($components)) {
            $mergedComponents = array_merge($mergedComponents, $components);
        }
    }
}

// Output the merged JSON
echo json_encode($mergedComponents, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
echo "\n";

/**
 * Extract module name from a components.json file path by reading module.xml
 */
function getModuleNameFromPath(string $componentsFile, string $magentoRoot): ?string
{
    // components.json is in etc/hyva_cms/, so module root is 2 levels up
    $moduleRoot = dirname($componentsFile, 3);

    // For vendor packages with src/ directory, check one level up
    if (basename($moduleRoot) === 'src') {
        $moduleRoot = dirname($moduleRoot);
    }

    $moduleXmlPath = $moduleRoot . '/etc/module.xml';

    // Try src/etc/module.xml for vendor packages
    if (!file_exists($moduleXmlPath)) {
        $moduleXmlPath = $moduleRoot . '/src/etc/module.xml';
    }

    if (!file_exists($moduleXmlPath)) {
        // Try to derive from path for app/code modules
        // Path format: app/code/Vendor/Module/etc/hyva_cms/components.json
        $relativePath = str_replace($magentoRoot . '/', '', $componentsFile);
        if (preg_match('#^app/code/([^/]+)/([^/]+)/#', $relativePath, $matches)) {
            return $matches[1] . '_' . $matches[2];
        }
        return null;
    }

    $xml = @simplexml_load_file($moduleXmlPath);
    if ($xml === false) {
        return null;
    }

    $moduleName = (string) ($xml->module['name'] ?? '');
    return $moduleName ?: null;
}