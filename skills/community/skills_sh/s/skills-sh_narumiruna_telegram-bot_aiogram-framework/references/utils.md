# Utilities: keyboards, formatting, i18n

Keyboard builder
- Use `InlineKeyboardBuilder` / `ReplyKeyboardBuilder` for dynamic layouts.
- Prefer explicit markup for static keyboards.
- Adjust grid with `builder.adjust(...)` and export with `builder.as_markup()`.
- See `docs/utils/keyboard.rst`.

Formatting helpers
- `aiogram.utils.formatting` builds message entities without manual HTML/Markdown.
- Use `Text`, `Bold`, `Italic`, `HashTag`, `as_list`, `as_section`, etc., then `as_kwargs()`.
- See `docs/utils/formatting.rst`.

I18n
- Uses gettext and Babel; install extras with `aiogram[i18n]`.
- Use `gettext` (`_`) for runtime strings, `lazy_gettext` (`__`) when language is not known.
- Use an I18n middleware (`SimpleI18nMiddleware`, `FSMI18nMiddleware`, etc.).
- See `docs/utils/i18n.rst`.
