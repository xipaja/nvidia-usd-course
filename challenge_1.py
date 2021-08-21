import json
import os.path
from pxr import Usd, UsdGeom

basePath = "C:/Users/xipaj/Desktop/NVIDIA_USD_layers/"

shapes = ["Sphere", "Cube"]

colors = {
    "Red": [(1,0,0)],
    "Green": [(0,1,0)],
    "DarkGreen": [(0,0.4,0)],
    "Blue": [(0,0,1)],
    "Grey": [(0.5,0.5,0.5)],
    "Black": [(0,0,0)],
    "Cyan": [(0,1,1)],
    "Brown": [(0.8,0.5,0.25)],
    "Orange": [(1,0.5,0)],
    "Yellow": [(1,1,0)]
}

def main():
    createShapeUSDs()
    renderJSON(basePath + "json/congrats.json")

def createShapeUSDs():
    for shape in shapes:
        shapeName = "My" + shape
        shapePath = shapeName + ".usda"
        stage = Usd.Stage.CreateNew("C:/Users/xipaj/Desktop/NVIDIA_USD_layers/" + shapePath)
        xformPrim = stage.DefinePrim("/" + shapeName, "Xform")

        shapeMesh = createShapeMesh(stage, shapeName)

        createColorVariants(xformPrim, shapeMesh)

        print(stage.GetRootLayer().ExportToString())

        # if file exists, override it
        overridePrevFile(basePath + shapePath)

        stage.GetRootLayer().Export(basePath + shapePath)

def createShapeMesh(stage, shapeName):
    """
    Args:
        stage - USD Stage
        shapeName - name given to our shape used for file paths

    Returns: 
        Shape mesh 
    """
    meshPath = "/" + shapeName + "/MeshData"
    
    if shapeName == "MySphere":
        shapeMesh = UsdGeom.Sphere.Define(stage, meshPath)
    if shapeName == "MyCube":
        shapeMesh = UsdGeom.Cube.Define(stage, meshPath)
    
    return shapeMesh
        
def createColorVariants(xformPrim, shapeMesh):
    """
    Args: 
        xformPrim - root transform of our stage
        shapeMesh - mesh of the shape we want to build a color variant for
    """
    colorVariants = xformPrim.GetVariantSets().AddVariantSet("ColorsRGB")
    colorAttr = shapeMesh.GetDisplayColorAttr()

    for key, value in colors.items():
        # Add variants to this VariantSet
        colorVariants.AddVariant(key)

        # Set variant values
        colorVariants.SetVariantSelection(key)
        with colorVariants.GetVariantEditContext():
            colorAttr.Set(value)

def renderJSON(path):
    """
    Load shapes from JSON to create a scene

    Args:
        path - JSON file path
    """

    with open(path) as jsonFile:
        shapeObjects = json.load(jsonFile)

    stage = Usd.Stage.CreateNew(basePath + "MyScene.usda")
    xformPrim = stage.DefinePrim("/MyScene", "Xform")

    # Create a place for ref to live
    for idx, shapeProperties in enumerate(shapeObjects):
        shapePrim = createReference(stage, idx, shapeProperties)

        modifyReference(shapePrim, shapeProperties)

    # if file exists, override it
    overridePrevFile(basePath + "MyScene.usda")

    # Save resulting layer
    print(stage.GetRootLayer().ExportToString())
    stage.GetRootLayer().Export(basePath + "MyScene.usda")


def createReference(stage, idx, shapeProperties):
    """
    Create references from JSON objects

    Args:
        stage - USD stage
        idx - numerical index given to current object we're building a ref for
        shapeProperties - properties of current object described in our JSON file
   
    Returns:
        Prim with references
    """

    shapePrim = stage.DefinePrim("/MyScene/shape" + str(idx))
    refPath = basePath + "My" + shapeProperties["shape"] + ".usda"

    shapePrim.GetReferences().AddReference(refPath, "/My" + shapeProperties["shape"])
    
    colorVariants = shapePrim.GetVariantSet("ColorsRGB")
    colorVariants.SetVariantSelection(shapeProperties["color"])

    return shapePrim

def modifyReference(shapePrim, shapeProperties):
    """
    Add translation, rotation, scale to reference

    params:
        shapePrim - prim to transform
        shapeProperties - properties of current object described in our JSON file
    """

    # take in prim and return transformable so we can perform transformations on shapes
    refXform = UsdGeom.Xformable(shapePrim)

    translate = shapeProperties.get("translate")
    rotate = shapeProperties.get("rotate")
    scale = shapeProperties.get("scale")

    # Apply transformations
    if translate:
        UsdGeom.XformCommonAPI(refXform).SetTranslate(translate)
    if rotate:
        UsdGeom.XformCommonAPI(refXform).SetRotate(rotate)
    if scale:
        UsdGeom.XformCommonAPI(refXform).SetScale(scale)

def overridePrevFile(fileName):
    # if usd file already exists, replace
    if(os.path.isfile(fileName)):
        os.remove(fileName)
        print("file replaced")

if __name__ == "__main__":
    main()