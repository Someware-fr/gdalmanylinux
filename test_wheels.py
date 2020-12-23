
import math
import os

from osgeo import ogr, osr

# https://gdal.org/api/python_gotchas.html#python-bindings-do-not-raise-exceptions-unless-you-explicitly-call-useexceptions
ogr.UseExceptions()
osr.UseExceptions()


def test_env_vars():
    assert 'site-packages/osgeo/gdal_data' in os.environ.get('GDAL_DATA', '')
    assert 'site-packages/osgeo/gdal_data/osmconf.ini' in os.environ.get('OSM_CONFIG_FILE', '')
    assert 'site-packages/osgeo/proj_data' in os.environ.get('PROJ_LIB', '')


def test_reproject():
    point = ogr.CreateGeometryFromWkt("POINT (-1.8748739 48.6876905)")

    source_srs = osr.SpatialReference()
    # see https://github.com/OSGeo/gdal/issues/1546
    source_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    source_srs.SetFromUserInput('EPSG:4326')

    dest_srs = osr.SpatialReference()
    dest_srs.SetFromUserInput('EPSG:3948')

    srs_transform = osr.CoordinateTransformation(source_srs, dest_srs)
    point.Transform(srs_transform)

    assert math.fabs(point.GetX() - 1341315.89056397) < 1E-8
    assert math.fabs(point.GetY() - 7287808.08599262) < 1E-8


def test_osm_driver():
    driver = ogr.GetDriverByName('OSM')
    ds = driver.Open(
        '/vsicurl/http://download.openstreetmap.fr/extracts/europe/france/bretagne/ille_et_vilaine.osm.pbf'
    )

