import folium
import time


# Laptop Location: 23.7854103,90.4309706
current_location = [23.783724898550883,90.42016804218294]

# Create a map object
map = folium.Map(location=current_location, zoom_start=18)
# Show my current location
folium.Marker(location=current_location).add_to(map)

# Create an empty list to store the polyline coordinates
# coordinates = []
# # Add an initial point to the coordinates list
# coordinates.append(current_location)
# # Create a polyline object with the initial coordinates
# polyline = folium.PolyLine(locations=coordinates, color='red')
# polyline.add_to(map)

map.add_child(folium.ClickForMarker(popup="Waypoint"))
map.add_child(folium.LatLngPopup().add_to(map))




# Display the map
map.save("index.html")
