# Write your awesome code here
from collections import defaultdict
import json
import re



def load_data():
    bus_id = []
    stop_id = []
    stop_name = []
    next_stop = []
    stop_type = []
    a_time = []

    json_data = input()
    datas = json.loads(json_data)
    bus_id_error = 0
    stop_id_error = 0
    stop_name_error = 0
    next_stop_error = 0
    stop_type_error = 0
    a_time_error = 0
    for data in datas:
        if type(data["bus_id"]) not in [128, 256, 512]:
            bus_id_error += 1
        if type(data["stop_id"]) not in range(1, 8):
            stop_id_error += 1
        if type(data["stop_name"]) is not str or re.match(r'[A-Z].+ (Road|Avenue|Boulevard|Street)$', data['stop_name']) is None:
            stop_name_error += 1
        if type(data["next_stop"]) not in range(1, 8):
            next_stop_error += 1
        if type(data["stop_type"]) is not str or data["stop_type"] not in ["S", "O", "F", '']:
            stop_type_error += 1
        if type(data["a_time"]) is not str or re.match(r'([0-1][0-9]|2[0-4]):[0-5][0-9]$', data["a_time"]) is None:
            a_time_error += 1
    verify_lines(datas)


def line_info(datas):
    stops = defaultdict(int)
    for data in datas:
        stops[data['bus_id']] += 1
    print("Line names and number of stops:")
    for bus_id, freq in stops.items():
        print("bus_id: {}, stops: {}".format(bus_id, freq))


def verify_lines(datas):
    buses = set()
    start = set()
    end = set()
    for data in datas:
        buses.add(data['bus_id'])
        if data['stop_type'] == 'S':
            if data['bus_id'] in start:
                print("There is more than one start or end stop for the line: {}.".format(data['bus_id']))
                return
            start.add(data['bus_id'])
        if data['stop_type'] == 'F':
            if data['bus_id'] in end:
                print("There is more than one start or end stop for the line: {}.".format(data['bus_id']))
                return
            end.add(data['bus_id'])
    total_miss = (buses - (start | end)) | (end - start) | (start - end)
    for miss in total_miss:
        print(f"There is no start or end stop for the line: {miss}.")
        return

    start.clear()
    end.clear()
    midway = set()
    transfer = set()

    for data in datas:
        if data['stop_type'] == 'S':
            start.add(data['stop_name'])
        elif data['stop_type'] == 'F':
            end.add(data['stop_name'])
        if data['stop_name'] in midway:
            transfer.add(data['stop_name'])
        else:
            midway.add(data['stop_name'])
    on_demand_check(datas, start, end, transfer)
    # print("Start stops: {} {}".format(len(start), sorted(start)))
    # print("Transfer stops: {} {}".format(len(transfer), sorted(transfer)))
    # print("Finish stops: {} {}".format(len(end), sorted(end)))


def time_check(first, second):
    first_h, first_m = first.split(":")
    second_h, second_m = second.split(":")
    if first_h < second_h or (first_h == second_h and first_m < second_m):
        return True
    return False


def chronological_check(datas):
    wrong_id = []
    wrong_name = []
    time = defaultdict(lambda : "00:00")
    for data in datas:
        if data['bus_id'] not in wrong_id:
            if time_check(time[data['bus_id']], data['a_time']):
                time[data['bus_id']] = data['a_time']
            else:
                wrong_id.append(data['bus_id'])
                wrong_name.append(data['stop_name'])
    print('Arrival time test:')
    if len(wrong_id) == 0:
        print('OK')
    else:
        for id, name in zip(wrong_id, wrong_name):
            print(f'bus_id line {id}: wrong time on station {name}')


def on_demand_check(datas, start, end, transfer):
    wrong = []
    for data in datas:
        stop_name = data['stop_name']
        if data['stop_type'] == 'O' and (stop_name in start or stop_name in end or stop_name in transfer):
            wrong.append(data['stop_name'])
    print("On demand stops test:")
    if len(wrong) != 0:
        print(sorted(wrong))
    else:
        print("OK")


if __name__ == "__main__":
    load_data()

# [{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Prospekt Avenue", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:12"},
# {"bus_id" : 128, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 5, "stop_type" : "O", "a_time" : "08:19"},
# {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:25"},
# {"bus_id" : 128, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:37"},
# {"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "09:20"},
# {"bus_id" : 256, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 6, "stop_type" : "", "a_time" : "09:45"},
# {"bus_id" : 256, "stop_id" : 6, "stop_name" : "Abbey Road", "next_stop" : 7, "stop_type" : "O", "a_time" : "09:59"},
# {"bus_id" : 256, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"},
# {"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "S", "a_time" : "08:13"},
# {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Abbey Road", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:16"}]
