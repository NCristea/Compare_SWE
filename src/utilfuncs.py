import geojson
import numpy as np

# function to convert bounding box to geojson
def bbox(coord_list):
    "TODO - integrate this function better when needed - not working "
    box = []
    for i in (0,1):
        res = sorted(coord_list, key=lambda x:x[i])
        box.append((res[0][i],res[-1][i]))
    ret = f"({box[0][0]} {box[1][0]}, {box[0][1]} {box[1][1]})"
    return ret

def bounding_box(lower_left_longitude,
                 lower_left_latitude,
                 upper_right_longitude,
                 upper_right_latitude):
    "TODO - explain function"
    bb_array = np.array([[lower_left_longitude, upper_right_latitude], [upper_right_longitude, upper_right_latitude], [upper_right_longitude, lower_left_latitude], [lower_left_longitude,  lower_left_latitude]])
    return bb_array

def get_selection_mask(region_mask, dataset):
    """
    Return the difference in days between the current date and game release date.
    Parameter
    ---------
    mask : regionmask mask https://regionmask.readthedocs.io/en/stable/ in lat long
    dataset : xarray data set in lat long

    Returns
    -------
    out_sel : selected data using regionmask in an xarray dataset
    """
    mask_poly = region_mask.mask(dataset)
    sel_mask_poly = mask_poly.where(mask_poly == 0).values
    lat = mask_poly.lat.values
    lon = mask_poly.lon.values
    id_lon = lon[np.where(~np.all(np.isnan(sel_mask_poly), axis=0))]
    id_lat = lat[np.where(~np.all(np.isnan(sel_mask_poly), axis=1))]
    out_sel = dataset.sel(lat=slice(id_lat[0], id_lat[-1]), lon=slice(id_lon[0],
                                                                      id_lon[-1])).compute().where(mask_poly == 0)
    return out_sel

def calc_water_year(da):
    return da.dt.year + (da.dt.month >= 10).astype(int)


def nse(sim, obs):
    num = np.sum((obs - sim) ** 2)
    den = np.sum((obs - np.mean(obs)) ** 2)
    return 1 - (num /den)


def kge(simulation_s, evaluation):
    sim_mean = np.mean(simulation_s, axis=0, dtype=np.float64)
    obs_mean = np.mean(evaluation, dtype=np.float64)
    r = np.sum((simulation_s - sim_mean) * (evaluation - obs_mean), axis=0, dtype=np.float64) / \
        np.sqrt(np.sum((simulation_s - sim_mean) ** 2, axis=0, dtype=np.float64) *
                np.sum((evaluation - obs_mean) ** 2, dtype=np.float64))
    alpha = np.std(simulation_s, axis=0) / np.std(evaluation, dtype=np.float64)
    beta = np.sum(simulation_s, axis=0, dtype=np.float64) / np.sum(evaluation, dtype=np.float64)
    kge_ = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
    return kge_


def snow_disappearance_date(swe):
    try:
        date_of_peak = swe['time'].values[swe.argmax()]
        end_date = swe['time'].values[-1]
        sub_swe = swe.sel(time=slice(date_of_peak, end_date))
        has_no_swe = sub_swe == 0
        only_no_swe = np.argwhere(has_no_swe.values)
        return sub_swe['time'].values[only_no_swe[0][0]]
    except:
        return np.datetime64('NaT')


def sdd_diff(swe1, swe2):
    diff = snow_disappearance_date(swe1) - snow_disappearance_date(swe2)
    if isinstance(diff, np.timedelta64):
        return diff.astype('timedelta64[h]') / np.timedelta64(1, 'D')
    else:
        return np.datetime64('NaT')


def peak_swe(swe):
    return swe.max().values[()]


def ps_diff(swe1, swe2):
    return peak_swe(swe1) - peak_swe(swe2)


def mbe(sim, obs):
    return np.nanmean(obs - sim)
