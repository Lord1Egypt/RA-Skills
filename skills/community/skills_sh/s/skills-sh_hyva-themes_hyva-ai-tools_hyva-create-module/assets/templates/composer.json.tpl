{
    "name": "{{vendor_kebabcase}}/module-{{module_kebabcase}}",
    "description": "{{DESCRIPTION}}",
    "type": "magento2-module",
    "require": {
        "php": ">=8.1"
    },
    "autoload": {
        "files": ["registration.php"],
        "psr-4": {
            "{{VENDOR}}\\{{MODULE}}\\": ""
        }
    }
}
