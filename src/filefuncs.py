import geopandas as gpd
def convertShpToGeojson(path_to_shp: str, path_to_json: str):
    """
    Converts a shapefile (.shp) to a GeoJSON format.

    This function reads a shapefile from the specified path and converts it
    into a GeoJSON file, saving it at the desired output path.

    Parameters
    ----------
    path_to_shp : str
        The file path to the input shapefile (.shp) that will be converted.
    path_to_json : str
        The file path where the output GeoJSON will be saved.

    Returns
    -------
    None
        The function does not return any value. It writes the GeoJSON file
        directly to the specified output path.

    Notes
    -----
    This function requires the `geopandas` library to be installed for reading
    and writing the shapefile and GeoJSON files.

    Examples
    --------
    convertShpToGeojson('data/input.shp', 'data/output.json')

    This will read the `input.shp` file and save the converted GeoJSON file to
    `output.json`.

    """
    myshpfile = gpd.read_file(path_to_shp)
    myshpfile.to_file(path_to_json, driver='GeoJSON')
    return
