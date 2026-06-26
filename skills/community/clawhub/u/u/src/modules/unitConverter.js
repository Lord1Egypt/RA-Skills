const unitConverter = {
  length: {
    m: 1,
    cm: 100,
    mm: 1000,
    km: 0.001,
    inch: 39.3701,
    foot: 3.28084,
    yard: 1.09361,
    mile: 0.000621371
  },
  weight: {
    kg: 1,
    g: 1000,
    mg: 1000000,
    lb: 2.20462,
    oz: 35.274
  },
  temperature: {
    celsius: 'celsius',
    fahrenheit: 'fahrenheit',
    kelvin: 'kelvin'
  },
  data: {
    b: 1,
    kb: 1024,
    mb: 1024 * 1024,
    gb: 1024 * 1024 * 1024,
    tb: 1024 * 1024 * 1024 * 1024
  },
  time: {
    s: 1,
    min: 60,
    h: 3600,
    day: 86400,
    week: 604800
  },
  currency: {
    usd: 1,
    usdt: 1,
    eur: 0.92,
    gbp: 0.79,
    jpy: 150,
    cny: 7.2
  },

  convert(value, from, to) {
    from = from.toLowerCase();
    to = to.toLowerCase();

    if (this.temperature[from] && this.temperature[to]) {
      return this.convertTemperature(value, from, to);
    }

    for (const category of [this.length, this.weight, this.data, this.time, this.currency]) {
      if (category[from] && category[to]) {
        const baseValue = value / category[from];
        return baseValue * category[to];
      }
    }

    throw new Error(`Unsupported units: ${from} to ${to}`);
  },

  convertTemperature(value, from, to) {
    let celsius;
    if (from === 'celsius') celsius = value;
    else if (from === 'fahrenheit') celsius = (value - 32) * 5 / 9;
    else if (from === 'kelvin') celsius = value - 273.15;

    if (to === 'celsius') return celsius;
    else if (to === 'fahrenheit') return celsius * 9 / 5 + 32;
    else if (to === 'kelvin') return celsius + 273.15;
  },

  listUnits() {
    return {
      length: Object.keys(this.length),
      weight: Object.keys(this.weight),
      temperature: Object.keys(this.temperature),
      data: Object.keys(this.data),
      time: Object.keys(this.time),
      currency: Object.keys(this.currency)
    };
  }
};

export default unitConverter;
