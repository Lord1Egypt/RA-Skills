# Subclip host workflow

This standalone Remotion workflow is unavailable inside a sandboxed Subclip layer. Subclip owns project creation, package versions, media decoding, Player setup, composition registration, provider credentials, and export.

Use native Subclip tools and bundled skills to import media/audio, inspect metadata, validate the component, capture project frames, and export. Do not install packages, execute external CLIs or scripts, start Studio/servers, set up cloud rendering, or request API keys. Use only pinned validated imports and project-library URLs. Read `$subclip-remotion-layer` for the component authoring contract.
