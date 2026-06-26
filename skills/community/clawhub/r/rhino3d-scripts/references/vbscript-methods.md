# VBScript Methods

This reference file is an extension of [methods-and-functions.md](methods-and-functions.md). It contains methods and properties exclusive to VBScript's `RhinoScript` API.

## Layer State Methods

Rhino's **LayerStateManager** command allows you to save the states of layers and restore them at a
later time. The command is implemented in the Rhino Bonus Tools plug-in, or *RhinoBonusTools.rhp*.
Because the **LayerStateManager** command resides in a plug-in, you will first need to get the
plug-in's scriptable object, using
[GetPlugInObject](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/application_methods/getpluginobject.htm),
before you can call any of these methods.

### Example

```vb
Sub TestLayerStates
  Dim objPlugIn
  On Error Resume Next
  Set objPlugIn = Rhino.GetPluginObject("Rhino Bonus Tools")
  If Err Then
    MsgBox Err.Description
    Exit Sub
  End If
  'TODO: call a layer state method...
End Sub
```

| Method | Description |
| --- | --- |
| [DeleteLayerState](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/deletelayerstate.htm) | Deletes a layer state. |
| [ExportLayerStates](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/exportlayerstates.htm) | Exports layer states to a file. |
| [ImportLayerStates](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/importlayerstates.htm) | Import layer states from a file. |
| [IsLayerState](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/islayerstate.htm) | Verifies that a layer state exists. |
| [LayerStateCount](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/layerstatecount.htm) | Returns the number of layer states. |
| [LayerStateNames](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/layerstatenames.htm) | Returns layer state names. |
| [RenameLayerStates](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/renamelayerstate.htm) | Renames a layer state. |
| [RestoreLayerStates](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/restorelayerstate.htm) | Restores a saved layer state. |
| [SaveLayerState](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/layer_state_methods/savelayerstate.htm) | Saves a layer state. |

## Math Methods

The following is a list of functions and operators that are provided by native VBScript:

| Function | Description |
| :-- | :-- |
| `^` | Raises a number to the power of an exponent. |
| `*` | Multiplies two numbers. |
| `/` | Divides two numbers and returns a floating-point result. |
| `\` | Divides two numbers and returns an integer result. |
| `Mod` | Divides two numbers and returns only the remainder. |
| `+` | Sums two numbers. |
| `-` | Finds the difference between two numbers or indicates the negative value of a numeric expression. |
| `&` | Forces string concatenation of two expressions. |
| `Abs` | Returns the absolute value of a number. |
| `Atn` | Returns the arctangent of a number. |
| `Cos` | Returns the cosine of an angle. |
| `Exp` | Returns e (the base of natural logarithms) raised to a power. |
| `Int` | Returns the integer portion of a number. |
| `Fix` | Returns the integer portion of a number. |
| `Log` | Returns the natural logarithm of a number. |
| `Rnd` | Returns a random number. |
| `Sgn` | Returns an integer indicating the sign of a number. |
| `Sin` | Returns the sine of an angle. |
| `Sqr` | Returns the square root of a number. |
| `Tan` | Returns the tangent of an angle. |

RhinoScript extents the math capabilities of VBScript by adding the following methods:

| Method | Description |
| :-- | :-- |
| [`ACos`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/acos\E.htm) | Returns the inverse cosine of a number. |
| [`ACosH`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/acosh.htm) | Returns the inverse hyperbolic cosine of a number. |
| [`Angle`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/angle.htm) | Measures the angle between two points. |
| [`Angle2`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/angle2.htm) | Measures the angle between two lines. |
| [`ASin`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/asin.htm) | Returns the inverse sine of a number. |
| [`ASinH`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/asinh.htm) | Returns the inverse hyperbolic sine of a number. |
| [`ATan2`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/atan2.htm) | Returns the angle from the X axis to a point (y,x). |
| [`ATanH`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/atanh.htm) | Returns the inverse hyperbolic tangent of a number. |
| [`Ceil`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/ceil.htm) | Returns the ceiling of a number. |
| [`CosH`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/cosh.htm) | Returns the hyperbolic cosine of an angle. |
| [`Deviation`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/deviation.htm) | Returns the standard deviation from an array of numbers. |
| [`Distance`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/distance.htm) | Returns the distance between two points. |
| [`E`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/e.htm) | Returns the value of the base of the natural system of logarithms (e). |
| [`Floor`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/floor.htm) | Returns the floor of a number. |
| [`FMod`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/fmod.htm) | Returns the floating-point remainder. |
| [`Hypot`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/hypot.htm) | Calculates the hypotenuse. |
| [`Log10`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/log10.htm) | Returns the base 10 logarithm of a specified number. |
| [`Max`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/max.htm) | Returns the maximum number from an array of numbers. |
| [`Mean`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/mean.htm) | Returns the mean, or average, value from an array of numbers. |
| [`Median`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/median.htm) | Return the median value from an array of numbers. |
| [`Min`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/min.htm) | Returns the minimum number from an array of numbers. |
| [`PI`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/pi.htm) | Returns the PI constant. |
| [`Polar`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/polar.htm) | Returns a point at an angle and distance from the point. |
| [`Rnd`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/rnd.htm) | Returns a random number. |
| [`SinH`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/sinh.htm) | Returns the hyperbolic sine of an angle. |
| [`SolveQuadratic`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/solvequadratic.htm) | Solves a quadratic equation. |
| [`Sum`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/sum.htm) | Returns the sum number from an array of numbers. |
| [`TanH`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/tanh.htm) | Returns the hyperbolic tangent of an angle. |
| [`ToDegrees`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/todegrees.htm) | Converts an angle in radians to degrees. |
| [`ToRadians`](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/math_methods/toradians.htm) | Converts an angle in degrees to radians. |

> [!NOTE]
> the following non-intrinsic math functions can be derived from the intrinsic math functions:

| Function | Derived Equivalent |
| :-- | :-- |
| `Secant` | `Sec(X) = 1 / Cos(X)` |
| `Cosecant` | `Cosec(X) = 1 / Sin(X)` |
| `Cotangent` | `Cotan(X) = 1 / Tan(X)` |
| `Inverse Sine` | `Arcsin(X) = Atn(X / Sqr(-X * X + 1))` |
| `Inverse Cosine` | `Arccos(X) = Atn(-X / Sqr(-X * X + 1)) + 2 * Atn(1)` |
| `Inverse Secant` | `Arcsec(X) = Atn(X / Sqr(X * X - 1)) + Sgn((X) -1) * (2 * Atn(1))` |
| `Inverse Cosecant` | `Arccosec(X) = Atn(X / Sqr(X * X - 1)) + (Sgn(X) - 1) * (2 * Atn(1))` |
| `Inverse Cotangent` | `Arccotan(X) = Atn(X) + 2 * Atn(1)` |
| `Hyperbolic Sine` | `HSin(X) = (Exp(X) - Exp(-X)) / 2` |
| `Hyperbolic Cosine` | `HCos(X) = (Exp(X) + Exp(-X)) / 2` |
| `Hyperbolic Tangent` | `HTan(X) = (Exp(X) - Exp(-X)) / (Exp(X) + Exp(-X))` |
| `Hyperbolic Secant` | `HSec(X) = 2 / (Exp(X) + Exp(-X))` |
| `Hyperbolic Cosecant` | `HCosec(X) = 2 / (Exp(X) - Exp(-X))` |
| `Hyperbolic Cotangent` | `HCotan(X) = (Exp(X) + Exp(-X)) / (Exp(X) - Exp(-X))` |
| `Inverse Hyperbolic Sine` | `HArcsin(X) = Log(X + Sqr(X * X + 1))` |
| `Inverse Hyperbolic Cosine` | `HArccos(X) = Log(X + Sqr(X * X - 1))` |
| `Inverse Hyperbolic Tangent` | `HArctan(X) = Log((1 + X) / (1 - X)) / 2` |
| `Inverse Hyperbolic Secant` | `HArcsec(X) = Log((Sqr(-X * X + 1) + 1) / X)` |
| `Inverse Hyperbolic Cosecant` | `HArccosec(X) = Log((Sgn(X) * Sqr(X * X + 1) +1) / X)` |
| `Inverse Hyperbolic Cotangent` | `HArccotan(X) = Log((X + 1) / (X - 1)) / 2` |
| `Logarithm to base N` | `LogN(X) = Log(X) / Log(N)` |

## Named Position Methods

Rhino's **NamedPosition** command allows you to save the locations of objects and restore them at a
later time. The command is implemented in the Named Positions plug-in, or *NamedPositions.rhp*.
Because the **NamedPosition** command resides in a plug-in, you will first need to get the plug-in's
scriptable object, using
[GetPlugInObject](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/application_methods/getpluginobject.htm),
before you can call any of these methods.

### Example

```vb
Sub TestNamedPositions
  Dim objPlugIn
  On Error Resume Next
  Set objPlugIn = Rhino.GetPluginObject("Named Position")
  If Err Then
    MsgBox Err.Description
    Exit Sub
  End If
  'TODO: call a named position method...
End Sub
```

| Method | Description |
| --- | --- |
| [AppendNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/appendnamedposition.htm) | Adds objects to an existing named position.. |
| [DeleteNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/deletenamedposition.htm) | Deletes a named position. |
| [NamedPositionCount](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/namedpositioncount.htm) | Returns the number of named positions. |
| [NamedPositions](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/namedpositions.htm) | Returns the names of the named positions. |
| [RenameNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/renamenamedposition.htm) | Renames an existing named position. |
| [RestoreNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/restorenamedposition.htm) | Restores an existing named position. |
| [SaveNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/savenamedposition.htm) | Saves a new named position. |
| [SelectObjectsOfNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/selectobjectsofnamedposition.htm) | Select the objects of a named position. |
| [UpdateNamedPosition](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/named_position_methods/updatenamedposition.htm) | Updates an existing named position. |

## Rhino Properties & Methods

The following methods and properties are available on the Rhino automation (COM) objects, both
**Rhino.Application** and **Rhino.Interface**. The Rhino automation objects are used when
[automating Rhino externally](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/introduction/external_access.htm).

| Methods | Description |
| --- | --- |
| [BringToTop](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/bringtotop.htm) | Brings Rhino into the foreground and activates the window. |
| [GetPlugInObject](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/getpluginobject.htm) | Retrieves an automation (COM) object from a plug-in. |
| [GetScriptObject](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/getscriptobject.htm) | Retrieves the RhinoScript automation (COM) object. |
| [IsInitialized](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/isinitialized.htm) | Verifies that Rhino is initialized and ready for use. |
| [RunScript](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/runscript.htm) | Runs a Rhino command script |

| Properties | Description |
| --- | --- |
| [ReleaseWithoutClosing](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/releasewithoutclosing.htm) | Releases the Rhino object without closing the Rhino application. |
| [Visible](https://mcneel.github.io/rhinoscript-api-docs/api/rhinoscript/rhino_properties_methods/visible.htm) | Shows or hides the Rhino application window. |
