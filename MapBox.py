import csv
import json

def getMean(read_str):
    record_high = 0.0
    record_total = 0.0
    with open(read_str) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        row_list = []
        for row in csv_reader:

            if line_count > 0:
                record_total += float(row[2])

            line_count += 1

    print(str(record_total/line_count))

    return record_total/line_count

def scanData(read_str):
    record_high = 0.0
    record_total = 0.0
    with open(read_str) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        row_list = []
        for row in csv_reader:
            if line_count > 0:
                record_total += float(row[2])
                record_high = max(float(record_high), float(row[2]))

            line_count += 1

    return record_high

def createGeoJSON(read_str, output_str):
    with open(read_str) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        row_list = []
        record_high = 0
        for row in csv_reader:
            if line_count > 0:
                r = {
                      "type": "Feature",
                      "geometry": {
                        "type": "Point",
                        "coordinates": [float(row[0]), float(row[1])]
                      },
                      "properties": {
                        "record": float(row[2])
                      }
                }
                row_list.append(r)

            line_count += 1

        feature = {
            "type": "FeatureCollection",
            "features": row_list
        }

        with open(output_str,'wb') as file:
            file.write(json.dumps(feature))

class Row:
    lon = 0.0
    lat = 0.0
    rec = 0.0

    def __init__(self, longitude, latitude, record):
        self.lon = longitude
        self.lat = latitude
        self.rec = record

def main():
    heatmap_greatest = 0;
    heatmap_filename = "";

    total_avg_meanA = 0.0
    total_avg_meanB = 0.0
    record_highA = 0
    record_highB = 0

    for x in range(0, 144):

        # Create file-path for input and output
        # ten-mins dir contains raw csv files, geojson_data is output dir
        base_strA = 'tower-'+str(x)+'-network-a-10-mins'
        base_strB = 'tower-'+str(x)+'-network-b-10-mins'

        read_strA = "./ten-mins/"+base_strA+".csv"
        outp_strA = "./mapbox-gl-js/geojson_data/"+base_strA+".geojson"

        read_strB = "./ten-mins/"+base_strB+".csv"
        outp_strB = "./mapbox-gl-js/geojson_data/"+base_strB+".geojson"

        # Use for finding average record data (density)
        # total_avg_meanA += getMean(read_strA)
        # total_avg_meanB += getMean(read_strB)

        # Use for finding max data value in CSV files
        # record_highA = max(scanData(read_strA), record_highA)
        # record_highB = max(scanData(read_strB), record_highB)

        createGeoJSON(read_strA, outp_strA)
        createGeoJSON(read_strB, outp_strB)

main()
