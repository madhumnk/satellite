import streamlit as st
import requests
from skyfield.api import EarthSatellite, load, wgs84
import folium
from streamlit_folium import st_folium

# Load time scale
ts = load.timescale()

# Satellite category URLs
sat_categories = {
    "ISS (Space Station)": "https://celestrak.org/NORAD/elements/stations.txt",
    "Starlink": "https://celestrak.org/NORAD/elements/starlink.txt",
    "GPS": "https://celestrak.org/NORAD/elements/gps-ops.txt",
    "NOAA (Weather)": "https://celestrak.org/NORAD/elements/weather.txt",
    "Iridium": "https://celestrak.org/NORAD/elements/iridium.txt"
}

# Sidebar for input
st.sidebar.title("Observer Location")
latitude = st.sidebar.number_input("Latitude", value=12.9716)
longitude = st.sidebar.number_input("Longitude", value=77.5946)
altitude = st.sidebar.number_input("Altitude (m)", value=0)

# Select satellite category
category = st.selectbox("Select Satellite Category", list(sat_categories.keys()))
tle_url = sat_categories[category]

# Fetch and parse TLE data
response = requests.get(tle_url)
lines = response.text.strip().splitlines()

# Extract TLE blocks
tle_data = []
for i in range(0, len(lines), 3):
    if i+2 < len(lines):
        name, line1, line2 = lines[i], lines[i+1], lines[i+2]
        tle_data.append((name, line1, line2))

# Select satellite by name
sat_names = [entry[0] for entry in tle_data]
selected_name = st.selectbox("Select a Satellite", sat_names)

# Get the selected TLE
satellite = None
for name, line1, line2 in tle_data:
    if name == selected_name:
        satellite = EarthSatellite(line1, line2, name, ts)
        break

if satellite:
    # Compute satellite location
    t = ts.now()
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    sat_lat = subpoint.latitude.degrees
    sat_lon = subpoint.longitude.degrees

    # Observer position
    observer = wgs84.latlon(latitude, longitude, elevation_m=altitude)
    difference = satellite - observer
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    # Display information
    st.title("🛰️ Satellite Tracker")
    st.write(f"**Category:** {category}")
    st.write(f"**Satellite:** {selected_name}")
    st.write(f"**Location:** Lat: {sat_lat:.2f}, Lon: {sat_lon:.2f}")
    st.write(f"**Altitude from you:** {alt.degrees:.2f}°")
    st.write(f"**Azimuth:** {az.degrees:.2f}°")
    st.write(f"**Distance:** {distance.km:.2f} km")

    # Map
    try:
        m = folium.Map(location=[sat_lat, sat_lon], zoom_start=2)
        folium.Marker([sat_lat, sat_lon], tooltip=selected_name).add_to(m)
        folium.Marker([latitude, longitude], tooltip="You").add_to(m)
        st_folium(m, width=700, height=500)
    except ValueError as e:
        st.error(f"🚫 Error creating map: {e}")
