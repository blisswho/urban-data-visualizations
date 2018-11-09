# Urban Data Visualizations

### Usage Instructions

1. Input your csv files inside of directory ten-mins. 

2. Run "python MapBox.py" to create geojson files which are taken from ten-mins and outputted into mapbox-gl-js/geojson_data

Optional: Run "python convertBounds.py" for converting Shenzhen boundary file

3. Open up terminal, change directory into mapbox-gl-js and run "python -n SimpleHTTPServer"

4. Network A: localhost:8000/network-a.html, Network B: localhost:8000/network-b.html

5. Enjoy heatmap visualizations for Shenzhen from Networks A and B!
