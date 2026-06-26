# eNSP .topo File Format Reference

## File Structure Overview

```xml
<?xml version="1.0" encoding="UNICODE" ?>
<topo version="1.3.00.100">
    <devices>
        <!-- Device definitions -->
    </devices>
    <lines>
        <!-- Connection lines -->
    </lines>
    <shapes>
        <!-- Area boxes and arrows -->
    </shapes>
    <txttips>
        <!-- Text labels -->
    </txttips>
</topo>
```

## Devices Section

### Basic Device Structure

```xml
<dev id="UUID-HERE" name="DEVICE_NAME" model="MODEL_TYPE" settings="" system_mac="" com_port="2000" bootmode="0" cx="X_POS" cy="Y_POS" edit_left="EDIT_X" edit_top="EDIT_Y">
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="24" />
    </slot>
</dev>
```

### Device Attributes

| Attribute | Description | Notes |
|-----------|-------------|-------|
| id | UUID v4 format | Generate unique per device |
| name | Device name | e.g., "AR1", "LSW1", "PC1" |
| model | Device model | See model reference below |
| settings | Device settings | Leave empty for routers/switches |
| system_mac | MAC address | Optional, auto-generated if empty |
| com_port | COM port | 2000+ for routers/switches, 0 for PC/Cloud |
| bootmode | Boot mode | 0=normal, 1=another mode |
| cx, cy | Center position | Coordinates on canvas |
| edit_left, edit_top | Edit offset | Usually cx+27, cy+54 |

### Device Models Reference

#### AR201 Router
```xml
<dev ... model="AR201" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="8" />
        <interface sztype="Ethernet" interfacename="Ethernet" count="1" />
    </slot>
</dev>
```

#### AR1220 Router
```xml
<dev ... model="AR1220" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="2" />
        <interface sztype="Ethernet" interfacename="Ethernet" count="8" />
    </slot>
    <slot isMainBoard="0" id="1" type="521" />
</dev>
```

#### AR2220 Router
```xml
<dev ... model="AR2220" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="1" />
        <interface sztype="Ethernet" interfacename="GE" count="2" />
        <interface sztype="Serial" interfacename="Serial" count="2" />
    </slot>
    <slot isMainBoard="0" id="3" type="521" />
</dev>
```

#### AR2240 Router
```xml
<dev ... model="AR2240" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="1" />
        <interface sztype="Ethernet" interfacename="GE" count="2" />
    </slot>
</dev>
```

#### AR3260 Router
```xml
<dev ... model="AR3260" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="1" />
        <interface sztype="Ethernet" interfacename="GE" count="2" />
    </slot>
</dev>
```

#### Generic Router
```xml
<dev ... model="Router" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="2" />
        <interface sztype="Ethernet" interfacename="GE" count="4" />
        <interface sztype="Serial" interfacename="Serial" count="4" />
    </slot>
</dev>
```

#### S3700 Switch
```xml
<dev ... model="S3700" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="22" />
        <interface sztype="Ethernet" interfacename="GE" count="2" />
    </slot>
</dev>
```

#### S5700 Switch
```xml
<dev ... model="S5700" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="24" />
    </slot>
</dev>
```

#### PC
```xml
<dev ... model="PC" settings=" -simpc_ip 0.0.0.0 -simpc_mask 0.0.0.0 -simpc_gateway 0.0.0.0 -simpc_mac XX-XX-XX-XX-XX-XX ..." ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="1" />
    </slot>
</dev>
```

#### Laptop
```xml
<dev ... model="Laptop" settings=" -simpc_ip X.X.X.X ..." ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="1" />
    </slot>
</dev>
```

#### Cloud
```xml
<dev ... model="Cloud" settings="" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="3" />
        <interface sztype="Ethernet" interfacename="GE" count="0" />
        <interface sztype="Serial" interfacename="Serial" count="0" />
        <interfaceMap sztype="Ethernet" interfacename="Ethernet" displayNo="1" remoteDisplayNo="2" adapterUid="" isOpen="0" udpPort="0" peerIPAdd="0.0.0.0" peerIP="0" peerPort="0" />
        <interfaceMap sztype="Ethernet" interfacename="Ethernet" displayNo="2" remoteDisplayNo="1" adapterUid="" isOpen="0" udpPort="0" peerIPAdd="0.0.0.0" peerIP="0" peerPort="0" />
    </slot>
</dev>
```

#### Server
```xml
<dev ... model="Server" settings="-domain 0 -eth XX-XX-XX-XX-XX-XX -ipaddr 0.0.0.0 -ipmask 255.255.255.0 -gateway 0.0.0.0 ..." ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="1" />
    </slot>
</dev>
```

#### Client
```xml
<dev ... model="Client" settings="-domain 0 -eth XX-XX-XX-XX-XX-XX -ipaddr 0.0.0.0 -ipmask 255.255.255.0 -gateway 0.0.0.0 ..." ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="1" />
    </slot>
</dev>
```

#### FRSW (Frame Relay Switch)
```xml
<dev ... model="FRSW" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Serial" interfacename="Serial" count="16" />
    </slot>
</dev>
```

#### HUB
```xml
<dev ... model="HUB" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="16" />
    </slot>
</dev>
```

#### MCS (Multicast Server)
```xml
<dev ... model="MCS" settings=" -simpc_ip 1.1.1.2 -simpc_mask 255.255.255.0 -simpc_gateway 1.1.1.1 -simpc_mac XX-XX-XX-XX-XX-XX -simpc_mc_dstip 225.1.1.1 ..." ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="Ethernet" count="1" />
    </slot>
</dev>
```

#### NE40E/NE5000E/NE9000 Router
```xml
<dev ... model="NE40E" ...>
    <slot id="1">
        <interface category="Ethernet" type="Ethernet" slotIndex="1" cardIndex="0" interfaceIndex="0" />
        <interface category="Ethernet" type="Ethernet" slotIndex="1" cardIndex="0" interfaceIndex="1" />
        <!-- ... 共10个接口，interfaceIndex 0-9 -->
    </slot>
</dev>
```

#### CE6800 Switch
```xml
<dev ... model="CE6800" ...>
    <slot id="1">
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="0" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="1" />
        <!-- ... 共20个接口，interfaceIndex 0-19 -->
    </slot>
</dev>
```

#### CE12800 Switch
```xml
<dev ... model="CE12800" ...>
    <slot id="1">
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="0" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="1" />
        <!-- ... 共10个接口，interfaceIndex 0-9 -->
    </slot>
</dev>
```

#### CX Switch
```xml
<dev ... model="CX" ...>
    <slot id="1">
        <interface category="Ethernet" type="Ethernet" slotIndex="1" cardIndex="0" interfaceIndex="0" />
        <interface category="Ethernet" type="Ethernet" slotIndex="1" cardIndex="0" interfaceIndex="1" />
        <!-- ... 共10个接口，interfaceIndex 0-9 -->
    </slot>
</dev>
```

#### USG5500 Firewall
```xml
<dev ... model="USG5500" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="9" />
    </slot>
</dev>
```

#### USG6000V Firewall
```xml
<dev ... model="USG6000V" ...>
    <slot id="1">
        <interface category="Ethernet" type="GE" slotIndex="0" cardIndex="0" interfaceIndex="0" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="0" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="1" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="2" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="3" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="4" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="5" />
        <interface category="Ethernet" type="GE" slotIndex="1" cardIndex="0" interfaceIndex="6" />
    </slot>
</dev>
```

#### AC6005 Wireless Controller
```xml
<dev ... model="AC6005" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="8" />
    </slot>
</dev>
```

#### AC6605 Wireless Controller
```xml
<dev ... model="AC6605" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="24" />
    </slot>
</dev>
```

#### AP6050 Wireless AP
```xml
<dev ... model="AP6050" settings=" -apMac XX-XX-XX-XX-XX-XX -apSN XXXXXXXXXX" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="2" />
    </slot>
</dev>
```

#### AP Series (AP2050/AP3030/AP4030/AP4050/AP5030/AP6050/AP7030/AP7050/AP8030/AP8130/AP9131)
```xml
<!-- AP2050: GE x5 -->
<dev ... model="AP2050" settings=" -apMac XX-XX-XX-XX-XX-XX -apSN XXXXXXXXXX" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="5" />
    </slot>
</dev>

<!-- AP3030: GE x1 -->
<dev ... model="AP3030" settings=" -apMac XX-XX-XX-XX-XX-XX -apSN XXXXXXXXXX" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="1" />
    </slot>
</dev>

<!-- AP4030/AP4050/AP5030/AP6050/AP7030/AP7050/AP9131: GE x2 -->
<dev ... model="AP4030" settings=" -apMac XX-XX-XX-XX-XX-XX -apSN XXXXXXXXXX" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="2" />
    </slot>
</dev>

<!-- AP8030/AP8130: GE x3 -->
<dev ... model="AP8030" settings=" -apMac XX-XX-XX-XX-XX-XX -apSN XXXXXXXXXX" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="3" />
    </slot>
</dev>
```

#### AD9430 (LTE Module)
```xml
<dev ... model="AD9430" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="28" />
    </slot>
</dev>
```

#### R250D Router
```xml
<dev ... model="R250D" settings=" -apMac XX-XX-XX-XX-XX-XX -apSN XXXXXXXXXX" ...>
    <slot number="slot17" isMainBoard="1">
        <interface sztype="Ethernet" interfacename="GE" count="1" />
    </slot>
</dev>
```

#### STA (Wireless Station)
```xml
<dev ... model="STA" settings=" -simsta_ip 0.0.0.0 -simsta_mask 0.0.0.0 -simsta_gateway 0.0.0.0 ..." ...>
    <slot number="slot17" isMainBoard="1" />
</dev>
```

#### Cellphone (Wireless)
```xml
<dev ... model="Cellphone" settings=" -simsta_ip 0.0.0.0 -simsta_mask 0.0.0.0 -simsta_gateway 0.0.0.0 ..." ...>
    <slot number="slot17" isMainBoard="1" />
</dev>
```

## Lines Section

### Basic Line Structure

```xml
<line srcDeviceID="SOURCE_UUID" destDeviceID="DEST_UUID">
    <interfacePair lineName="Copper" srcIndex="0" tarIndex="0" />
</line>
```

### Line with Full Coordinates

```xml
<line srcDeviceID="SOURCE_UUID" destDeviceID="DEST_UUID">
    <interfacePair lineName="Copper" 
        srcIndex="0" 
        srcBoundRectIsMoved="0" 
        srcBoundRect_X="X1" 
        srcBoundRect_Y="Y1" 
        srcOffset_X="0.000000" 
        srcOffset_Y="0.000000" 
        tarIndex="0" 
        tarBoundRectIsMoved="1" 
        tarBoundRect_X="X2" 
        tarBoundRect_Y="Y2" 
        tarOffset_X="-25.000000" 
        tarOffset_Y="0.000000" />
</line>
```

### Line Attributes

| Attribute | Description |
|-----------|-------------|
| srcDeviceID | UUID of source device |
| destDeviceID | UUID of destination device |
| lineName | Copper (Ethernet), Serial, Auto |
| srcIndex | Interface index on source device |
| tarIndex | Interface index on target device |
| srcBoundRectIsMoved | 0 or 1, whether position is adjusted |
| tarBoundRectIsMoved | 0 or 1, whether position is adjusted |
| srcOffset_X/Y | Offset from normal position |
| tarOffset_X/Y | Offset from normal position |

### Interface Index Mapping

For AR1220:
- GE0/0 = index 0
- GE0/1 = index 1
- Ethernet0/0/0 = index 2
- Ethernet0/0/1 = index 3
- ...
- Serial0/0/0 = index 10
- Serial0/0/1 = index 11

For S5700:
- GE0/0/0 = index 0
- GE0/0/1 = index 1
- ...

## Shapes Section

### Shape Types

| Type | Description |
|------|-------------|
| 0 | Line/Arrow (uses startpt/endpt) |
| 1 | Rectangle box (uses upleftcorner + width/height) |
| 2 | Rectangle (uses upleftcorner + width/height) |

### Rectangle Shape (type=1 or type=2)

```xml
<shape 
    type="1" 
    filloption="1" 
    color="12632256" 
    upleftcorner="X,Y" 
    width="W" 
    height="H" 
    startpt="0,0" 
    endpt="0,0" 
    borderStyle="5" 
    borderWidth="1" />
```

### Arrow/Line Shape (type=0)

```xml
<shape 
    type="0" 
    filloption="1" 
    color="0" 
    upleftcorner="0,0" 
    width="0" 
    height="0" 
    startpt="X1,Y1" 
    endpt="X2,Y2" 
    borderStyle="5" 
    borderWidth="1" />
```

### Shape Attributes

| Attribute | Description |
|-----------|-------------|
| type | 0=arrow, 1=rect, 2=rect |
| filloption | 1=filled, 0=stroke only |
| color | Fill color (RGB integer) |
| upleftcorner | Top-left corner (x,y) |
| width | Rectangle width |
| height | Rectangle height |
| startpt | Arrow start point (x,y) |
| endpt | Arrow end point (x,y) |
| borderStyle | Border style (5=dashed?) |
| borderWidth | Border width in pixels |

### Common Colors

| Color Name | RGB Value |
|------------|-----------|
| Yellow | 16776960 |
| Green | 4227327 |
| Blue | 255 |
| Red | 16711680 |
| Orange | 16744448 |
| Gray | 12632256 |
| Light Blue | 16744576 |
| Pink | 8421631 |
| Purple | 15591143 |

## Txttips Section (Text Labels)

### Basic Text Label

```xml
<txttip 
    left="100" 
    top="50" 
    right="250" 
    bottom="70" 
    content="Loopback0:10.0.1.1/24" 
    fontname="Consolas" 
    fontstyle="0" 
    editsize="100" 
    txtcolor="-16777216" 
    txtbkcolor="-7278960" 
    charset="1" />
```

### Multi-line Text (using &#x0D;&#x0A;)

```xml
<txttip 
    content="Loopback0:10.0.1.1/24&#x0D;&#x0A;Loopback1:10.1.0.1/24" ... />
```

### Text Label Attributes

| Attribute | Description |
|-----------|-------------|
| left, top | Top-left corner position |
| right, bottom | Bottom-right corner position |
| content | Text content (use &#x0D;&#x0A; for newlines) |
| fontname | Font family (Consolas recommended) |
| fontstyle | 0=normal, 1=bold |
| editsize | Font size multiplier (100=normal) |
| txtcolor | Text color (RGB, negative=auto) |
| txtbkcolor | Background color (-1=transparent, -7278960=filled) |
| charset | 1=UTF-8/ASCII, 134=GBK/Chinese |

### Common Text Colors

| Color | Value |
|-------|-------|
| Black | -16777216 |
| White | -1 |

## UUID Generation

Use UUID v4 format: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`

Example:
```
4CA76BCE-449E-4dc0-B3E3-E86C85B97033
A3B3E3D3-1BB3-4017-877D-FFDDD58EAE98
```

## Common Layout Calculations

### Device Position Offsets

For a device at (cx, cy):
- edit_left = cx + 27 (approximately)
- edit_top = cy + 54 (approximately)

### Interface BoundRect Calculation

Source device at (sx, sy), target at (tx, ty):
```
srcBoundRect_X = sx + 70  (right side of device)
srcBoundRect_Y = sy       (middle height)
tarBoundRect_X = tx - 70  (left side of device)
tarBoundRect_Y = ty       (middle height)
```

### Shape Area Calculation

For area containing multiple devices:
```
upleftcorner = (min_x - padding, min_y - padding)
width = max_x - min_x + padding*2
height = max_y - min_y + padding*2
```

## Version Compatibility

- `version="1.3.00.100"` - Latest format
- `version="1.2.00.510"` - Older format
- `version="1.2.00.390"` - Older format

All formats are compatible with eNSP. Use latest version for new files.
