import argparse
import csv
import pandas as pd
import folium
from folium import plugins
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
from functools import lru_cache

parser = argparse.ArgumentParser(description='Find films '
                                             'that were made in particular location and time.')
parser.add_argument('year', type=str, help='The year when film was made.')
parser.add_argument('latitude', type=float, help='The latitude of the location')
parser.add_argument('longitude', type=float, help='The longitude of the location')
parser.add_argument('path', type=str, help='Path to data set')
args = parser.parse_args()


def make_csv_file(path: str, year: str):
    """
    Creates a CSV file with name: 'film_locations.csv'.
    This file contains needed data from given file.
    args:
    args:
        path(str): Path to initial file
        year(str): Year needed to sort data
    returns:
        None
    """
    file_contents = []
    with open(path, 'r', encoding="UTF-8") as file:
        for line in file:
            if line.startswith('"'):
                if year in line:
                    index_1 = line.rfind('"')
                    lines = [line[2:index_1], line[index_1 + 3: index_1 + 7]]
                    location = line[index_1+8:].strip()
                    if "{" in line:
                        index_2 = line.find('}')
                        location = line[index_2+1:].strip()
                    if '(' in location:
                        index_3 = location.find('(')
                        lines.append(location[:index_3].strip())
                    else:
                        lines.append(location)
                    file_contents.append(lines)
    with open('film_locations.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(file_contents)


def distance(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
    """
    Returns distance between two locations.
    args:
        lat_1(float): latitude of 1st location
        lon_1(float): longitude of 1st location
        lat_2(float): latitude of 2nd location
        lon_2(float): longitude of 2nd location
    returns:
        float: distance between locations
    """
    initial_location = (lat_1, lon_1)
    coords = (lat_2, lon_2)
    dist = geodesic(initial_location, coords).km
    return dist


@lru_cache
def create_df(latitude_1: float, longitude_1: float):
    """
    Returns DataFrame with all needed information for the map.
    args:
        latitude_1(float): latitude of a given location
        longitude_1(float): longitude of a given location
    returns:
        DataFrame: information needed to create a map
    """
    column_names = ['Film Name', 'Year', 'Location']
    film_df = pd.read_csv('film_locations.csv', names=column_names, header=None)
    geocoder = RateLimiter(Nominatim(user_agent="sth").geocode, min_delay_seconds=1,
                           return_value_on_exception=None)
    film_df['Location'] = film_df['Location'].apply(geocoder)
    film_df['Latitude'] = film_df['Location'].apply(lambda x: x.latitude if x else None)
    film_df['Longitude'] = film_df['Location'].apply(lambda x: x.longitude if x else None)
    film_df['Distance'] = film_df.apply(lambda row: distance(latitude_1,
                                                             longitude_1, row['Latitude'],
                                                             row['Longitude']), axis=1)
    new_df = film_df.sort_values(by=['Distance']).head(10)
    return new_df.reset_index(drop=True)


def color_creator(interval: float) -> str:
    """
    Returns color for CircleMarker depending on distance.
    args:
        interval(float): distance between location
    returns:
        str: color of the map marker
    """
    if interval < 1500:
        return 'green'
    elif 1500 <= interval <= 3000:
        return 'yellow'
    else:
        return 'red'


def creating_map(film_df, latitude: float, longitude: float):
    """
    Creates and saves an HTML map with markers on the nearest locations
    where movies were shot in the particular year.
    args:
        film_df(DataFrame): information about the films that would be displayed on the map
        latitude(float): latitude of a given location
        longitude(float): longitude of a given location
    returns:
        None
    """
    created_map = folium.Map(location=[latitude, longitude], zoom_start=15)
    mini_map = plugins.MiniMap(toggle_display=True)
    created_map.add_child(mini_map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(created_map)
    plugins.Fullscreen(position='topright').add_to(created_map)
    plugins.ScrollZoomToggler().add_to(created_map)
    nearest_fg = folium.FeatureGroup(name="Nearest Film Scenes")
    title = film_df['Film Name']
    lat = film_df['Latitude']
    lon = film_df['Longitude']
    dis = film_df['Distance']
    for tl, lt, ln, ds in zip(title, lat, lon, dis):
        nearest_fg.add_child(folium.CircleMarker(location=(lt, ln), radius=20,
                                                 popup='"' + str(tl) + '"' +
                                                       '\n' + "Distance from location: " +
                                                       str(round(ds, 2)),
                                                 fill_color=color_creator(ds),
                                                 color='white', fill_opacity=1))
    created_map.add_child(nearest_fg)
    folium.LayerControl(position='topleft').add_to(created_map)
    created_map.save('FilmMap.html')


def main():
    """
    Main function
    """
    make_csv_file(args.path, args.year)
    film_df = create_df(args.latitude, args.longitude)
    creating_map(film_df, args.latitude, args.longitude)


if __name__ == '__main__':
    main()
