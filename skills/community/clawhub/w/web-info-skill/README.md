# Web Info Extractor - Implementation Notes

## Architecture

This skill uses a simple bash script with curl to fetch web pages and regex-based parsing to extract structured information.

## Parsing Strategy

- **Title**: Extracts from `<title>` tag
- **Description**: Checks both `meta name="description"` and Open Graph `og:description`
- **Headers**: Uses grep with PCRE to extract H1-H6 content
- **Links**: Parses `<a href="">` tags with text content
- **Images**: Extracts `src` and `alt` attributes from `<img>` tags

## Limitations

- Does not execute JavaScript (static HTML only)
- Limited to publicly accessible pages
- Regex-based parsing may miss complex nested structures
- Does not handle malformed HTML gracefully

## Future Enhancements

- Add support for xpath/css selectors
- Add caching for repeated requests
- Support for authenticated pages
- Better HTML entity decoding
- Rate limiting support
