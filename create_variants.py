from pxr import Usd, UsdGeom
import os.path

# Create stage
path = "C:/Users/xipaj/Desktop/NVIDIA_USD_layers"
variantUSDAFile = path + "/VariantExample.usda"  

stage = Usd.Stage.CreateNew(variantUSDAFile)

variantSphere = stage.OverridePrim('/variantSphere')

variantSphere.GetReferences().AddReference(path + '/SampleLayer.usda', '/MySphere')

print(stage.GetRootLayer().ExportToString())

# Remove translation op on base sphere
variantXform = stage.GetPrimAtPath('/variantSphere')

# Clear any color on base sphere
overMeshData = UsdGeom.Sphere.Get(stage, '/variantSphere/MeshData')
colorAttr = overMeshData.GetDisplayColorAttr()
colorAttr.Clear()

# Add the variant set
colorVariants = variantXform.GetVariantSets().AddVariantSet('ColorsRGB')

# Add variants to variant set
colorVariants.AddVariant('red')
colorVariants.AddVariant('green')
colorVariants.AddVariant('blue')

# Set variant values
colorVariants.SetVariantSelection('red')
with colorVariants.GetVariantEditContext():
    colorAttr.Set([(1,0,0)])

colorVariants.SetVariantSelection('green')
with colorVariants.GetVariantEditContext():
    colorAttr.Set([(0,1,0)])

colorVariants.SetVariantSelection('blue')
with colorVariants.GetVariantEditContext():
    colorAttr.Set([(0, 0, 1)])

# Set color to green
colorVariants.SetVariantSelection('green')

print(stage.GetRootLayer().ExportToString())

# if it already exists, replace
if(os.path.isfile(variantUSDAFile)):
    os.remove(variantUSDAFile)
    print("file replaced")
 
# Export root later to see variant dropdown in usdview 
stage.GetRootLayer().Export(variantUSDAFile)