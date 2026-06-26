const turf = require('@turf/turf');

module.exports = {
  booleanPointInPolygon(args) {
    return turf.booleanPointInPolygon(args.input, args.input2);
  },
  booleanContains(args) {
    return turf.booleanContains(args.input, args.input2);
  },
  booleanCrosses(args) {
    return turf.booleanCrosses(args.input, args.input2);
  },
  booleanDisjoint(args) {
    return turf.booleanDisjoint(args.input, args.input2);
  },
  booleanEqual(args) {
    return turf.booleanEqual(args.input, args.input2);
  },
  booleanIntersects(args) {
    return turf.booleanIntersects(args.input, args.input2);
  },
  booleanOverlap(args) {
    return turf.booleanOverlap(args.input, args.input2);
  },
  booleanWithin(args) {
    return turf.booleanWithin(args.input, args.input2);
  },
  booleanParallel(args) {
    return turf.booleanParallel(args.input, args.input2);
  },
  booleanPointOnLine(args) {
    return turf.booleanPointOnLine(args.input, args.input2);
  },
  nearestPoint(args) {
    return turf.nearestPoint(args.input, args.input2);
  },
};
