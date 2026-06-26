const turf = require('@turf/turf');

module.exports = {
  point(args) {
    return turf.point(args.coordinates, args.properties || {});
  },
  lineString(args) {
    return turf.lineString(args.coordinates, args.properties || {});
  },
  polygon(args) {
    return turf.polygon(args.coordinates, args.properties || {});
  },
  multiPoint(args) {
    return turf.multiPoint(args.coordinates, args.properties || {});
  },
  multiLineString(args) {
    return turf.multiLineString(args.coordinates, args.properties || {});
  },
  multiPolygon(args) {
    return turf.multiPolygon(args.coordinates, args.properties || {});
  },
  featureCollection(args) {
    return args.input;
  },
  randomPoint(args) {
    return turf.randomPoint(args.count || 10, { bbox: args.bbox || [-180, -90, 180, 90] });
  },
  randomLineString(args) {
    return turf.randomLineString(args.count || 1, { bbox: args.bbox || [-180, -90, 180, 90] });
  },
  randomPolygon(args) {
    return turf.randomPolygon(args.count || 1, { bbox: args.bbox || [-180, -90, 180, 90] });
  },
};
