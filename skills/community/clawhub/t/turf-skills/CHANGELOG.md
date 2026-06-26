# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- ESLint and Prettier configuration for code quality
- CI/CD with GitHub Actions (test and release workflows)
- Enhanced test coverage with error handling and edge case tests
- Coverage reporting with nyc
- CONTRIBUTING.md with development guidelines
- Natural language patterns section to SKILL.md
- More comprehensive package.json metadata
- Development scripts (lint, format, coverage)

### Changed

- Improved SKILL.md description with more active language
- Expanded trigger keywords and examples
- Better organization of documentation

### Fixed

- Improved .npmignore to exclude development files properly

## [1.0.0] - 2024-XX-XX

### Added

- Initial release of turf-skills
- Support for 60+ Turf.js operations across 6 categories:
  - Measurement: distance, area, length, bearing, destination, midpoint, center, centroid, centerOfMass, along, bbox, bboxPolygon, envelope
  - Query: booleanPointInPolygon, booleanContains, booleanCrosses, booleanDisjoint, booleanEqual, booleanIntersects, booleanOverlap, booleanWithin, booleanParallel, booleanPointOnLine, nearestPoint
  - Transformation: buffer, union, intersect, difference, simplify, convex, concave, dissolve, voronoi, tin, bezierSpline, transformRotate, transformScale, transformTranslate
  - Helpers: point, lineString, polygon, multiPoint, multiLineString, multiPolygon, featureCollection, randomPoint, randomLineString, randomPolygon
  - Interpolation: interpolate, isobands, isolines, hexGrid, pointGrid, squareGrid, triangleGrid
  - Clustering: clustersKmeans, clustersDbscan
- CLI interface with comprehensive options
- Bilingual documentation (English and Chinese)
- 32 test cases with 100% pass rate
- File input/output support
- Unit conversion (kilometers, miles, meters)

[Unreleased]: https://github.com/zhyt1985/turf-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/zhyt1985/turf-skills/releases/tag/v1.0.0
