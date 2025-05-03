# 🛰️ Satellite Tracker Web App

A real-time satellite tracking application built using **Python**, **Streamlit**, and **Skyfield**. It allows users to track satellites like the ISS, Starlink, GPS, NOAA, and Iridium, and visualize their current position on an interactive map.

## 🚀 Features

- Select satellite categories from live TLE data via CelesTrak
- Track real-time position of satellites
- See satellite location, altitude, azimuth, and distance from your location
- Interactive map with markers for both user and satellite positions

## 📦 Built With

- [Streamlit](https://streamlit.io/) - Web app framework
- [Skyfield](https://rhodesmill.org/skyfield/) - Precise orbital calculations
- [Folium](https://python-visualization.github.io/folium/) - Interactive mapping
- [CelesTrak](https://celestrak.org/) - Source for TLE data

## 💻 How to Run

#. Clone the repo:
   ```bash
   git clone https://github.com/madhumnk/satellite.git
   cd satellite
   python -m streamlit run sat_tracker.py
