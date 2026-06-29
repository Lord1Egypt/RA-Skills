function applyTemplate(template) {
            let option = {};
            let functionString = "";

            switch (template) {
                case 'bar':
                    option = {
                        "title": {
                            "text": "Fruit Sales (Jan-Dec)",
                            "subtext": "Unit: tons",
                            "left": "center"
                        },
                        "tooltip": {
                            "trigger": "axis",
                            "axisPointer": {
                                "type": "shadow"
                            }
                        },
                        "legend": {
                            "data": [
                                "Trend Line",
                                "Apple",
                                "Pear"
                            ],
                            "bottom": "0"
                        },
                        "grid": {
                            "left": "3%",
                            "right": "4%",
                            "containLabel": true
                        },
                        "xAxis": {
                            "type": "category",
                            "data": [
                                "Jan",
                                "Feb",
                                "Mar",
                                "Apr",
                                "May",
                                "Jun",
                                "Jul",
                                "Aug",
                                "Sep",
                                "Oct",
                                "Nov",
                                "Dec"
                            ],
                            "axisLabel": {
                                "interval": 0,
                                "rotate": 45
                            }
                        },
                        "yAxis": {
                            "type": "value",
                            "name": "Sales (tons)"
                        },
                        "series": [{
                                "name": "Trend Line",
                                "type": "line",
                                "smooth": true,
                                "lineStyle": {
                                    "width": 3
                                },
                                "label": {
                                    "show": true
                                },
                                "data": [
                                    21,
                                    51,
                                    65,
                                    73,
                                    12,
                                    92,
                                    81,
                                    125,
                                    123,
                                    122,
                                    123,
                                    120
                                ]
                            },
                            {
                                "name": "Apple",
                                "type": "bar",
                                "itemStyle": {
                                    "color": "#5470c6"
                                },
                                "data": [
                                    120,
                                    132,
                                    101,
                                    134,
                                    90,
                                    230,
                                    210,
                                    182,
                                    191,
                                    234,
                                    290,
                                    330
                                ],
                                "label": {
                                    "show": true,
                                    "position": "top",
                                    "formatter": "(p) => {return `${(p.value * 100 / publicVar.sum).toFixed(2)}%`;}"
                                }
                            },
                            {
                                "name": "Pear",
                                "type": "bar",
                                "data": [
                                    80,
                                    92,
                                    110,
                                    124,
                                    150,
                                    160,
                                    170,
                                    182,
                                    190,
                                    204,
                                    210,
                                    220
                                ],
                                "label": {
                                    "show": true,
                                    "position": "top",
                                    "formatter": "() => {return option.series[1].name;}"
                                }
                            }
                        ]
                    };
                    functionString = '{"sum": 1000}';

                    break;

                case 'line':
                    option = {
                        title: {
                            text: 'Temperature Trend',
                            left: 'center'
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: ['High Temp', 'Low Temp'],
                            bottom: '0%'
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '10%',
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                        },
                        yAxis: {
                            type: 'value',
                            axisLabel: {
                                formatter: '{value} °C'
                            },
                            axisLine: {}
                        },
                        series: [{
                                name: 'High Temp',
                                type: 'line',
                                smooth: true,
                                lineStyle: {
                                    width: 3,
                                    shadowBlur: 10,
                                    shadowOffsetY: 8
                                },
                                data: [21, 21, 25, 23, 22, 23, 20]
                            },

                            {
                                name: 'Low Temp',
                                type: 'line',
                                smooth: true,
                                lineStyle: {
                                    width: 3
                                },
                                data: [11, 11, 10, 13, 8, 0, 10]

                            }
                        ]
                    };

                    break;

                case 'pie':
                    option = {
                        title: {
                            text: 'Market Share',
                            left: 'center'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: '{a} <br/>{b}: {c} ({d}%)'
                        },
                        legend: {
                            orient: 'horizontal',
                            left: 'center',
                            bottom: '2%'
                        },
                        series: [{
                            name: 'Market Share',
                            type: 'pie',
                            radius: ['40%', '70%'],
                            data: [{
                                    value: 1048,
                                    name: 'Chrome'
                                },
                                {
                                    value: 735,
                                    name: 'Firefox'
                                },
                                {
                                    value: 580,
                                    name: 'Safari'
                                },
                                {
                                    value: 484,
                                    name: 'Edge'
                                },
                                {
                                    value: 300,
                                    name: 'Other'
                                }
                            ],
                            avoidLabelOverlap: false,
                            itemStyle: {
                                borderRadius: 10,
                                borderWidth: 2
                            },
                            label: {
                                show: true,
                                position: 'inside',
                                formatter: '{b}:{c}\n\n{d}%',
                                fontSize: 14
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    fontSize: '18',
                                    fontWeight: 'bold'
                                }
                            },
                            labelLine: {
                                show: false
                            }
                        }]
                    };

                    break;
                case 'cloud':
                    option ={
						  "series": [
							{
							  "type": "wordCloud",
							  "shape": "diamond",
							  "gridSize": 8,
							  "sizeRange": [
								12,
								60
							  ],
							  "rotationRange": [
								0,
								0
							  ],
							  "rotationStep": 0,
							  "drawOutOfBound": false,
							  "keepAspect": true,
							  "left": "center",
							  "top": "center",
							  "data": [
								{
								  "name": "Restart",
								  "value": 257
								},
								{
								  "name": "Change",
								  "value": 178
								},
								{
								  "name": "Switch",
								  "value": 124
								},
								{
								  "name": "Rollback",
								  "value": 105
								},
								{
								  "name": "Avoid",
								  "value": 103
								},
								{
								  "name": "Fix",
								  "value": 90
								},
								{
								  "name": "Patch",
								  "value": 97
								},
								{
								  "name": "Isolate",
								  "value": 62
								},
								{
								  "name": "Config",
								  "value": 51
								},
								{
								  "name": "Boot",
								  "value": 48
								},
								{
								  "name": "Toggle",
								  "value": 42
								},
								{
								  "name": "Scale",
								  "value": 34
								},
								{
								  "name": "Notify",
								  "value": 34
								},
								{
								  "name": "Canary",
								  "value": 42
								},
								{
								  "name": "Verify",
								  "value": 28
								},
								{
								  "name": "Replace",
								  "value": 27
								},
								{
								  "name": "Throttle",
								  "value": 30
								},
								{
								  "name": "Retry",
								  "value": 27
								},
								{
								  "name": "Cutover",
								  "value": 26
								},
								{
								  "name": "Scan",
								  "value": 14
								},
								{
								  "name": "Ack",
								  "value": 13
								},
								{
								  "name": "Takeover",
								  "value": 17
								},
								{
								  "name": "PowerOff",
								  "value": 10
								},
								{
								  "name": "Backfill",
								  "value": 10
								},
								{
								  "name": "Rebuild",
								  "value": 10
								},
								{
								  "name": "Explain",
								  "value": 8
								},
								{
								  "name": "Rotate",
								  "value": 9
								},
								{
								  "name": "SignOut",
								  "value": 7
								},
								{
								  "name": "ReRun",
								  "value": 7
								},
								{
								  "name": "Route",
								  "value": 6
								},
								{
								  "name": "Backup",
								  "value": 8
								},
								{
								  "name": "Restore",
								  "value": 7
								},
								{
								  "name": "Promote",
								  "value": 7
								},
								{
								  "name": "SwitchBack",
								  "value": 4
								},
								{
								  "name": "Standby",
								  "value": 6
								},
								{
								  "name": "Reset",
								  "value": 5
								},
								{
								  "name": "Spare",
								  "value": 5
								},
								{
								  "name": "CircuitBreak",
								  "value": 3
								},
								{
								  "name": "Cell",
								  "value": 4
								},
								{
								  "name": "Heal",
								  "value": 4
								},
								{
								  "name": "Enable",
								  "value": 3
								},
								{
								  "name": "Unlock",
								  "value": 3
								},
								{
								  "name": "Compat",
								  "value": 3
								},
								{
								  "name": "Degrade",
								  "value": 4
								},
								{
								  "name": "StartStop",
								  "value": 2
								},
								{
								  "name": "Calm",
								  "value": 2
								},
								{
								  "name": "Backup",
								  "value": 1
								},
								{
								  "name": "SelfIsolate",
								  "value": 1
								},
								{
								  "name": "Reboot",
								  "value": 1
								},
								{
								  "name": "Reinstall",
								  "value": 1
								},
								{
								  "name": "Enable",
								  "value": 1
								},
								{
								  "name": "PowerOn",
								  "value": 1
								},
								{
								  "name": "PowerOff",
								  "value": 1
								},
								{
								  "name": "Retransmit",
								  "value": 1
								},
								{
								  "name": "HotSwap",
								  "value": 1
								},
								{
								  "name": "ReUpload",
								  "value": 1
								}
							  ],
							  "shrinkToFit": true,
							  "layoutAnimation": true,
							  "textStyle": {
								"fontFamily": "sans-serif",
								"fontWeight": "bold",
								"color": "#5470c6"
							  },
							  "emphasis": {
								"focus": "self",
								"textStyle": {
								  "textShadowBlur": 10,
								  "textShadowColor": "#333"
								}
							  }
							}
						  ]
						};

                    break;
            }

            optionInput.value = JSON.stringify(option, null, 2);
            functionInput.value = functionString;
            generateChart();
        }

        