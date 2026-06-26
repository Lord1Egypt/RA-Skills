<?php
/**
 * Register Rank Math SEO meta fields for WordPress REST API access.
 * 
 * This code allows OpenClaw to set RankMath SEO metadata when publishing
 * articles via the WordPress REST API.
 * 
 * INSTALLATION:
 * 1. Go to WordPress Admin → Appearance → Theme File Editor
 * 2. Select your active theme's functions.php (use child theme if available)
 * 3. Add this entire code block at the end of functions.php
 * 4. Click "Update File"
 * 
 * ALTERNATIVE: Use the "Code Snippets" plugin to manage this code
 * without modifying theme files directly.
 * 
 * REQUIRED: RankMath SEO plugin must be installed and activated.
 * 
 * SECURITY NOTE:
 * - This snippet only registers the 3 meta keys that the publisher script
 *   actually uses. Do NOT add extra keys unless your workflow requires them.
 * - The auth_callback restricts write access to users with the 'edit_posts'
 *   capability, matching WordPress's built-in permission model.
 * - If you uninstall this skill, remove this snippet from functions.php
 *   to revoke the REST API exposure of these fields.
 */

add_action('init', function () {
    // Only the 3 RankMath meta keys used by the publisher script.
    // Kept minimal to reduce the REST API attack surface.
    $meta_keys = [
        'rank_math_title',              // SEO Title
        'rank_math_description',        // Meta Description
        'rank_math_focus_keyword',      // Focus Keyword
    ];

    foreach ($meta_keys as $key) {
        register_meta('post', $key, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => function () {
                return current_user_can('edit_posts');
            },
        ]);
    }
});
