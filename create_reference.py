from pxr import Usd, UsdGeom

# Create a temporary stage in memory
refStage = Usd.Stage.CreateNew('C:/Users/xipaj/Desktop/ReferenceExampleGreen2.usda')

# Create a place for the reference to live
refSphere = refStage.OverridePrim('/refSphere2')

# Create the reference
refSphere.GetReferences().AddReference('./SampleLayer.usda', '/MySphere')
refStage.GetRootLayer().Save()

# Create New Stage From File -> Open the file on Desktop

print(refStage.GetRootLayer().ExportToString())

# Remove the translation operation applied to the base sphere's transform
refXform = UsdGeom.Xformable(refSphere)
refXform.SetXformOpOrder([])

# Override the color of the sphere to be red
overMeshData = UsdGeom.Sphere.Get(refStage, '/refSphere2/MeshData')
overMeshData.GetDisplayColorAttr().Set([(0,1,1)])


# Save the resulting layer
refStage.GetRootLayer().Export('../../../Users/xipaj/Desktop/RefExamplePlsWork.usda')