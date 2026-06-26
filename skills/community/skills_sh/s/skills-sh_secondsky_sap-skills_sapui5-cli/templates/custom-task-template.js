/**
 * Custom UI5 Build Task Template (CommonJS)
 *
 * Purpose: [Describe what this task does]
 * Use Case: [Describe when to use this task]
 *
 * Module Format: CommonJS (works out-of-the-box)
 * To use ESM instead, see the commented alternative at the bottom of this file.
 *
 * Configuration in ui5.yaml:
 * ---
 * specVersion: "4.0"
 * kind: extension
 * type: task
 * metadata:
 *   name: my-custom-task
 * task:
 *   path: lib/tasks/myCustomTask.js
 * ---
 *
 * Usage in project ui5.yaml:
 * builder:
 *   customTasks:
 *     - name: my-custom-task
 *       beforeTask: generateComponentPreload  # or afterTask
 *       configuration:
 *         # Your custom configuration
 *         enabled: true
 *         quality: 80
 *
 * Specification Version: 4.0+
 * Required Dependencies: [list npm packages]
 */

/**
 * Optional: Declare required dependencies (Spec v3.0+)
 * Only needed if task accesses dependency resources
 *
 * This callback allows advanced dependency selection logic. Use getProject to inspect
 * specific projects and options.configuration for conditional logic based on task settings.
 *
 * @param {object} params
 * @param {Set<string>} params.availableDependencies - Set of available dependency names
 * @param {Function} params.getDependencies - Get all project dependencies
 * @param {Function} params.getProject - Get project by name (for advanced selection)
 * @param {object} params.options - Task options (access configuration for conditional logic)
 * @returns {Promise<Set<string>>} Set of required dependency names
 */
module.exports.determineRequiredDependencies = async function({
    availableDependencies,
    getDependencies,
    getProject,
    options
}) {
    const dependencies = new Set();

    // Example 1: Check if specific dependency exists and is needed
    if (availableDependencies.has("my.required.library")) {
        dependencies.add("my.required.library");
    }

    // Example 2: Include dependencies by pattern
    const allDeps = await getDependencies();
    for (const project of allDeps) {
        if (project.getName().startsWith("my.company.")) {
            dependencies.add(project.getName());
        }
    }

    // Example 3: Conditional dependency based on configuration (advanced)
    // if (options.configuration?.includeThemes) {
    //     const themeLib = await getProject("my.theme.library");
    //     if (themeLib) {
    //         dependencies.add("my.theme.library");
    //     }
    // }

    return dependencies;
};

/**
 * Main task function
 *
 * @param {object} params
 * @param {module:@ui5/fs.DuplexCollection} params.workspace - Reader/Writer for project resources
 * @param {module:@ui5/fs.ReaderCollection} params.dependencies - Reader for dependency resources (if declared)
 * @param {module:@ui5/logger.Logger} params.log - Logger instance (Spec v3.0+)
 * @param {object} params.options - Task options
 * @param {object} params.options.configuration - Custom configuration from ui5.yaml
 * @param {string} params.options.projectName - Project name
 * @param {string} params.options.projectNamespace - Project namespace
 * @param {string} params.options.taskName - Task name
 * @param {module:@ui5/builder.tasks.TaskUtil} params.taskUtil - Task utilities (Spec v2.2+)
 * @returns {Promise<undefined>}
 */
module.exports = async function({workspace, dependencies, log, options = {}, taskUtil}) {
    const {configuration = {}} = options;

    log.info("Starting custom task...");

    // Validate configuration
    if (configuration.enabled === false) {
        log.info("Task disabled by configuration");
        return;
    }

    try {
        // Example 1: Read and process project resources
        const resources = await workspace.byGlob("**/*.js");

        log.info(`Processing ${resources.length} JavaScript files`);

        for (const resource of resources) {
            const content = await resource.getString();

            // Process content (example: add header comment)
            const processedContent = `/* Processed by custom task */\n${content}`;

            // Update resource
            resource.setString(processedContent);
            await workspace.write(resource);
        }

        // Example 2: Create new resource using taskUtil
        if (taskUtil) {
            const newResource = taskUtil.resourceFactory.createResource({
                path: "/resources/generated/metadata.json",
                string: JSON.stringify({
                    generated: new Date().toISOString(),
                    projectName: options.projectName,
                    taskName: options.taskName
                }, null, 2)
            });

            await workspace.write(newResource);
            log.info("Created metadata.json");
        }

        // Example 3: Read from dependencies (if declared in determineRequiredDependencies)
        if (dependencies) {
            const depResources = await dependencies.byGlob("**/*.json");
            log.info(`Found ${depResources.length} JSON files in dependencies`);

            for (const depResource of depResources) {
                const depContent = await depResource.getString();
                // Process dependency resource
                log.info(`Processing dependency: ${depResource.getPath()}`);
            }
        }

        // Example 4: Use configuration
        if (configuration.quality) {
            log.info(`Quality setting: ${configuration.quality}`);
        }

        log.info("Custom task completed successfully");

    } catch (error) {
        log.error(`Task failed: ${error.message}`);
        throw error;
    }
};

/* ============================================================================
 * ESM ALTERNATIVE
 * ============================================================================
 * To use ECMAScript modules instead of CommonJS, replace this entire file with:
 *
 * // Optional dependencies callback (ESM)
 * export async function determineRequiredDependencies({
 *     availableDependencies,
 *     getDependencies,
 *     getProject,
 *     options
 * }) {
 *     const dependencies = new Set();
 *     // ... implementation
 *     return dependencies;
 * }
 *
 * // Main task function (ESM)
 * export default async function({workspace, dependencies, log, options = {}, taskUtil}) {
 *     const {configuration = {}} = options;
 *     // ... implementation
 * }
 *
 * IMPORTANT: ESM requires either:
 * 1. Add to package.json: { "type": "module" }
 * 2. Use .mjs file extension: myCustomTask.mjs
 *
 * Without one of these, Node.js will throw: "SyntaxError: Unexpected token 'export'"
 * ============================================================================
 */
