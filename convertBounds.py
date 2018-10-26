import csv
import json

def createGeoJSON(read_str, output_str):
    with open(read_str, 'r') as myfile:
        data=myfile.read().replace('\n', '')

        r = {
              "type": "Feature",
              "geometry": data
        }

        with open(output_str,'wb') as file:
            file.write(json.dumps(r))


def main():
    json_file = 'shenzhen_boundary_gps.geojson'
    output = 'new_shenzhen_boundary.txt'
    createGeoJSON(json_file, output)


main()
