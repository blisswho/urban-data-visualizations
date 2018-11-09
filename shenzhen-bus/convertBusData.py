

from cpstime import CPSTime
import csv
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


pd.set_option('display.max_row', 1000)
pd.set_option('display.max_columns', 50)

def createGeoJSONFile(values, timeslot_num):

    # Cut longitude to 6 digits, count record
    # Cut latitude to 5 digits, count record

    row_list = []

    for x in values:
        r = {
             "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [float(x[1]), float(x[2])]
              },
              "properties": {
                "record": float(x[2])
              }
        }

        row_list.append(r)

    feature = {
        "type": "FeatureCollection",
        "features": row_list
    }
    output_str = "./mapbox-gl-js/geojson_data/bus-data-"+str(timeslot_num)+".geojson"

    with open(output_str,'wb') as file:
        file.write(json.dumps(feature))


def separateBySlots(read_str):
    csv_df = pd.read_csv(read_str)

    csv_df['mlon_str'] = csv_df.mlon.astype(str)
    csv_df.mlon_str = csv_df.mlon_str.str.slice(0, 7)
    csv_df['mlat_str'] = csv_df.mlat.astype(str)
    csv_df.mlat_str = csv_df.mlat_str.str.slice(0, 6)
    # print(csv_df[['mlon','mlon_str','mlat', 'mlat_str', 'timeslot']][:100])

    csv_df_agg = csv_df.groupby(['mlon_str','mlat_str', 'timeslot']).size().reset_index(name='counts')

    unique_timeslots = csv_df_agg.timeslot.unique()

    for x in unique_timeslots:
        timeslot_temp = csv_df_agg[csv_df_agg['timeslot'] == x]
        new_array = timeslot_temp[['timeslot','mlon_str','mlat_str','counts']].values
        createGeoJSONFile(new_array, x)


def createTimeSlots(read_str, output_str):
    with open(read_str) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        row_strings = []
        row_timeslots = []
        for row in csv_reader:

            if line_count == 0:
                headers = ",".join(row)+",timeslot"
                row_strings.append(headers)
                row_timeslots.append("null")

            if line_count > 0:
                parse_time = CPSTime().parseTime(row[4])
                timeslot = CPSTime().timeSlot(parse_time, t_min=5)
                new_line = ",".join(row)+","+str(timeslot)
                row_strings.append(new_line)
                row_timeslots.append(timeslot)

            line_count += 1

        with open(output_str,'wb') as file:
            for x in row_strings:
                file.write(x+"\n")

def main():
    # Uncomment below to add timeslot column

    # read_str = "./bus.csv"
    # output_str = "./bus-added-time.csv"
    # createTimeSlots(read_str, output_str)

    # Use below to separate by timeslots into new csv files
    separateBySlots("./bus-added-time.csv")



main()
