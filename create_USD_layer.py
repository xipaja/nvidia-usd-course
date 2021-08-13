from pxr import Usd, UsdGeom

# Create temp stage in memory
stage = Usd.Stage.CreateInMemory("TestLayer.usda")

# Create transform and add sphere
xformPrim = UsdGeom.Xform.Define(stage, "/TestSphere")

# Set translation
UsdGeom.XformCommonAPI(xformPrim).SetTranslate((7, 8, 9))
spherePrim = UsdGeom.Sphere.Define(stage, "/TestSphere/MeshData")

# Get sphere as generic prim
sphere = stage.GetPrimAtPath("/TestSphere/MeshData")

# Get extent and radius params for prim
radiusAttr = sphere.GetAttribute("radius")  
extentAttr = sphere.GetAttribute("extent")

# Access sphere schema to see color
colorAttr = spherePrim.GetDisplayColorAttr()

# Set radius to 2
radiusAttr.Set(2)

#Expand extents to match new radius
extentAttr.Set(extentAttr.Get() * 2)

# Make sphere blue
colorAttr.Set([(0.0, 0.0, 1.0)])

# Print out stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("C:/Users/xipaj/Desktop/TestLayer.usda")