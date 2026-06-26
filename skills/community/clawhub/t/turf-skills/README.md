# turf-skills

[![npm version](https://badge.fury.io/js/turf-skills.svg)](https://www.npmjs.com/package/turf-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test](https://github.com/zhyt1985/turf-skills/actions/workflows/test.yml/badge.svg)](https://github.com/zhyt1985/turf-skills/actions/workflows/test.yml)

Claude Code skill for [Turf.js](https://turfjs.org/) spatial analysis.

[中文文档](./README.zh-CN.md) | [Contributing](./CONTRIBUTING.md) | [Changelog](./CHANGELOG.md)

## Install

### As Claude Code skill

```bash
# npm global install
npm install -g turf-skills

# Or clone and link
git clone https://github.com/zhyt1985/turf-skills.git
cd turf-skills && npm install && npm link

# Install as skill
mkdir -p ~/.claude/skills/turf-skills
ln -s $(which turf-skills) ~/.claude/skills/turf-skills/
cp SKILL.md ~/.claude/skills/turf-skills/
```

### As CLI tool

```bash
npm install -g turf-skills
turf-skills --action distance --input '{"type":"Point","coordinates":[120,30]}' --input2 '{"type":"Point","coordinates":[121,31]}'
```

## Features

| Category       | Actions                                                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Measurement    | distance, area, length, bearing, destination, midpoint, center, centroid, centerOfMass, along, bbox, bboxPolygon, envelope                                                                 |
| Query          | booleanPointInPolygon, booleanContains, booleanCrosses, booleanDisjoint, booleanEqual, booleanIntersects, booleanOverlap, booleanWithin, booleanParallel, booleanPointOnLine, nearestPoint |
| Transformation | buffer, union, intersect, difference, simplify, convex, concave, dissolve, voronoi, tin, bezierSpline, transformRotate, transformScale, transformTranslate                                 |
| Helpers        | point, lineString, polygon, multiPoint, multiLineString, multiPolygon, featureCollection, randomPoint, randomLineString, randomPolygon                                                     |
| Interpolation  | interpolate, isobands, isolines, hexGrid, pointGrid, squareGrid, triangleGrid                                                                                                              |
| Clustering     | clustersKmeans, clustersDbscan                                                                                                                                                             |

## Examples

### Basic usage

```bash
# Distance between two points
turf-skills --action distance \
  --input '{"type":"Point","coordinates":[120,30]}' \
  --input2 '{"type":"Point","coordinates":[121,31]}'

# Point in polygon
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[120.5,30.5]}' \
  --input2 '{"type":"Polygon","coordinates":[[[120,30],[121,30],[121,31],[120,31],[120,30]]]}'

# Buffer
turf-skills --action buffer \
  --input '{"type":"Point","coordinates":[120,30]}' \
  --radius 5 --units kilometers

# Read from file
turf-skills --action area --file polygon.geojson

# Hex grid
turf-skills --action hexGrid --bbox '[120,30,121,31]' --cellSide 5

# K-means clustering
turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 5
```

### Real-world scenarios

```bash
# Beijing to Shanghai distance → 1068 km
turf-skills --action distance \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --input2 '{"type":"Point","coordinates":[121.473701,31.230416]}' \
  --units kilometers

# Is Tiananmen inside Beijing's 5th Ring Road? → true
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --input2 '{"type":"Polygon","coordinates":[[[116.1,39.7],[116.8,39.7],[116.8,40.1],[116.1,40.1],[116.1,39.7]]]}'

# Create a 5km buffer around a point
turf-skills --action buffer \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --radius 5 --units kilometers

# Polygon union
turf-skills --action union \
  --input '{"type":"Polygon","coordinates":[[[120,30],[121,30],[121,31],[120,31],[120,30]]]}' \
  --input2 '{"type":"Polygon","coordinates":[[[120.5,30.5],[121.5,30.5],[121.5,31.5],[120.5,31.5],[120.5,30.5]]]}'

# Generate hex grid for a region (28 hexagons)
turf-skills --action hexGrid --bbox '[116,39,117,40]' --cellSide 10 --units kilometers

# K-means clustering into 3 groups
turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 3

# Create a point with properties
turf-skills --action point \
  --coordinates '[116.397428,39.90923]' \
  --properties '{"name":"Tiananmen"}'

# Convex hull of a point set
turf-skills --action convex --file points.geojson

# Find nearest point in a collection
turf-skills --action nearestPoint \
  --input '{"type":"Point","coordinates":[120.3,30.3]}' \
  --file2 points-collection.geojson

# Line length in kilometers
turf-skills --action length --file line.geojson --units kilometers

# Output result to file
turf-skills --action buffer --file point.geojson --radius 10 --output result.geojson
```

## Options

| Option                 | Description                   |
| ---------------------- | ----------------------------- |
| `--action <name>`      | Turf function name (required) |
| `--input <geojson>`    | First GeoJSON input           |
| `--input2 <geojson>`   | Second GeoJSON input          |
| `--file <path>`        | Read first input from file    |
| `--file2 <path>`       | Read second input from file   |
| `--output <path>`      | Write result to file          |
| `--units <km\|mi\|m>`  | Distance units                |
| `--radius <n>`         | Buffer radius                 |
| `--bbox <json>`        | Bounding box                  |
| `--cellSide <n>`       | Grid cell size                |
| `--coordinates <json>` | Coordinates (for helpers)     |
| `--properties <json>`  | Properties (for helpers)      |
| `--list`               | List all actions              |
| `--help`               | Show help                     |

## Natural Language Usage in Claude Code

After installing as a Claude Code skill, you can use natural language to invoke spatial analysis. Claude will automatically translate your request into the appropriate turf-skills command.

| You say                                                                | Claude runs                                                                                                                                                                        |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Calculate the distance from Beijing to Shanghai"                      | `turf-skills --action distance --input '{"type":"Point","coordinates":[116.397428,39.90923]}' --input2 '{"type":"Point","coordinates":[121.473701,31.230416]}' --units kilometers` |
| "Is Tiananmen inside this polygon?"                                    | `turf-skills --action booleanPointInPolygon --input '...' --input2 '...'`                                                                                                          |
| "Create a 5km buffer around this point"                                | `turf-skills --action buffer --input '...' --radius 5 --units kilometers`                                                                                                          |
| "Compute the convex hull of points.geojson and save to result.geojson" | `turf-skills --action convex --file points.geojson --output result.geojson`                                                                                                        |
| "Calculate the area of polygon.geojson"                                | `turf-skills --action area --file polygon.geojson`                                                                                                                                 |
| "Generate a hex grid for the Beijing area"                             | `turf-skills --action hexGrid --bbox '[116,39,117,40]' --cellSide 10 --units kilometers`                                                                                           |
| "Cluster these points into 3 groups"                                   | `turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 3`                                                                                                   |
| "Find the nearest point to [120.3, 30.3]"                              | `turf-skills --action nearestPoint --input '...' --file2 points.geojson`                                                                                                           |
| "Merge these two polygons"                                             | `turf-skills --action union --input '...' --input2 '...'`                                                                                                                          |
| "How long is this line in kilometers?"                                 | `turf-skills --action length --file line.geojson --units kilometers`                                                                                                               |

## License

MIT
