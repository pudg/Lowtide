from requests_html import HTMLSession
from datetime import datetime
session = HTMLSession()

LOCATIONS = [
    "https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest",
    "https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest",
    "https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest",
    "https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest"
]

"""
Converts time from 12h to 24h format.
Args:
    time: 12h format time stamp.
Returns:
    24h format time stamp.
"""
def convert(time):
    if len(time) == 6:
        time = '0' + time
    time = time[:5] + ' ' + time[5:]
    if time[:2] == "00":
        return time[:5]
    return datetime.strptime(time, "%I:%M %p").strftime("%H:%M")

"""
Extracts sunrise and sunset times from tide information.

args:
    data: Array of tide table row information.

Returns:
    sunrise and sunset 12h format time stamps.
"""

def sun_rise_set(data):
    sunrise, sunset = "", ""
    for dat in data:
        if "Sunrise" in dat:
            sunrise = dat
        if "Sunset" in dat:
            sunset = dat
    return sunrise.split(' ')[1], sunset.split(' ')[1]

"""
Extracts low tide imformation times(s).

args:
    data: Array of tide table row information.

Returns:
    All low tide information from given table row.
"""
def get_tides(data):
    tides = [data[idx:idx+3] for (idx, dat) in enumerate(data) if dat == 'Low Tide']
    return tides


def main():
    for location in LOCATIONS:
        resp = session.get(location)
        table = resp.html.find(".tide_flex_start")
        if len(table) != 0:
            tides = table[0].find(".tide-day")
            for tide in tides:
                data = tide.text.split("\n")
                sunrise, sunset = sun_rise_set(data)
                sunrise, sunset = convert(sunrise), convert(sunset)
                lowtides = get_tides(data)
                print(data[0])
                if len(lowtides) == 1:
                    lt_time1 = convert(lowtides[0][1].split('(')[0].replace(' ', ''))
                    if lt_time1 >= sunrise and lt_time1 <= sunset:
                        print(f"Daylight Tide: {lowtides[0][2]}")
                else:
                    lt_time1 = convert(lowtides[0][1].split('(')[0].replace(' ', ''))
                    lt_time2 = convert(lowtides[1][1].split('(')[0].replace(' ', ''))
                    if lt_time1 >= sunrise and lt_time1 <= sunset:
                        print(f"Daylight Tide1: {lowtides[0][2]}")
                    if lt_time2 >= sunrise and lt_time2 <= sunset:
                        print(f"Daylight Tide2: {lowtides[1][2]}")
                print("\n")

if __name__ == "__main__":
    main()