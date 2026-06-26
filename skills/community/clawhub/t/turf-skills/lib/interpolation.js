const turf = require('@turf/turf');

module.exports = {
  interpolate(args) {
    return turf.interpolate(args.input, args.cellSide || 1, {
      gridType: args.gridType || 'square',
      property: args.propertyName || 'elevation',
      units: args.units || 'kilometers',
    });
  },
  isobands(args) {
    return turf.isobands(args.input, args.breaks || [0, 5, 10], {
      zProperty: args.propertyName || 'elevation',
    });
  },
  isolines(args) {
    return turf.isolines(args.input, args.breaks || [0, 5, 10], {
      zProperty: args.propertyName || 'elevation',
    });
  },
  hexGrid(args) {
    return turf.hexGrid(args.bbox, args.cellSide, { units: args.units || 'kilometers' });
  },
  pointGrid(args) {
    return turf.pointGrid(args.bbox, args.cellSide, { units: args.units || 'kilometers' });
  },
  squareGrid(args) {
    return turf.squareGrid(args.bbox, args.cellSide, { units: args.units || 'kilometers' });
  },
  triangleGrid(args) {
    return turf.triangleGrid(args.bbox, args.cellSide, { units: args.units || 'kilometers' });
  },
};
