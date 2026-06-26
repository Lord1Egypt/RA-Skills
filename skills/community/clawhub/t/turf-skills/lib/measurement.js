const turf = require('@turf/turf');

module.exports = {
  distance(args) {
    return turf.distance(args.input, args.input2, { units: args.units || 'kilometers' });
  },
  area(args) {
    return turf.area(args.input);
  },
  length(args) {
    return turf.length(args.input, { units: args.units || 'kilometers' });
  },
  bearing(args) {
    return turf.bearing(args.input, args.input2);
  },
  destination(args) {
    return turf.destination(args.input, args.distance, args.direction || args.bearing_val || 0, { units: args.units || 'kilometers' });
  },
  midpoint(args) {
    return turf.midpoint(args.input, args.input2);
  },
  center(args) {
    return turf.center(args.input);
  },
  centroid(args) {
    return turf.centroid(args.input);
  },
  centerOfMass(args) {
    return turf.centerOfMass(args.input);
  },
  along(args) {
    return turf.along(args.input, args.distance, { units: args.units || 'kilometers' });
  },
  bbox(args) {
    return turf.bbox(args.input);
  },
  bboxPolygon(args) {
    const box = args.bbox || turf.bbox(args.input);
    return turf.bboxPolygon(box);
  },
  envelope(args) {
    return turf.envelope(args.input);
  },
};
