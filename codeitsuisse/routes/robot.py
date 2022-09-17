import math

from flask import request, make_response

from codeitsuisse import app

TARGET = "CODEITSUISSE"

def get_coordinates(map):
    index_row = 0
    coordinates = {}
    for row in map:
        index_col = 0
        for col in row:
            if col != " " and col != "\n":
                if col in coordinates:
                    coordinates[col].append([index_row, index_col])
                else:
                    coordinates[col] = [[index_row, index_col]]
            index_col += 1
        index_row += 1
    
    return coordinates

def shortest(player, coordinates):
    distance = math.dist(player, coordinates[0])
    coordinate = coordinates[0]
    index = 0
    for i in range(1,len(coordinates)):
        temp = math.dist(player, coordinates[i])
        if temp < distance:
            coordinate = coordinates[i]
            distance = temp
            index = i

    return coordinate, index

#not yet optimazied
@app.route("REST/message", methods=['POST'])
def message():
    headers = {"Content-Type": "text/plain", "Accept": "text/plain"}
    return make_response(request.data.decode(), 200, headers=headers)

@app.route('/cryptocollapz', methods=['POST'])
def robot():
    output = ""
    map = message()
    coordinates = get_coordinates(map)

    facing = 'up'
    for char in TARGET:
        player = coordinates['X'][0]
        target = coordinates[char][0]
        target_index = 0
        if len(coordinates[char]) != 1:
            target,target_index = shortest(player ,coordinates[char])
        travel = True
        while travel:
            if facing == "up":
                if target[0] > player[0]:
                    output += "R" * 2
                    facing = "down"
                    continue
                elif target[0] < player[0]:
                    # player need to get closer vertically
                    output += "S" * (player[0] - target[0])
                    player[0] = target[0]
               
                if player[1] < target[1]:
                    output += "R"
                    facing = "right"
                elif player[1] > target[1]:
                    output += "L"
                    facing = "left"
                if player == target:
                    output += "P"
                    travel = False
            elif facing == "down":
                if target[0] > player[0]:
                    output += "S" * (target[0] - player[0])
                    player[0] = target[0]
                elif target[0] < player[0]:
                    # player need to get closer vertically
                    output += "R" * 2
                    facing = "up"
                    continue
                  
                if player[1] < target[1]:
                    output += "L"
                    facing = "right"
                elif player[1] > target[1]:
                    output += "R"
                    facing = "left"
                        
                if player == target:
                    output += "P"
                    travel = False

            elif facing == "right":
                if target[0] > player[0]:
                    output += "R"
                    facing = "down"
                    continue
                elif target[0] < player[0]:
                    output += "L"
                    facing = "up"
                    continue
                  
                if player[1] < target[1]:
                    output += "S" * (target[1] - player[1])
                    player[1] = target[1]
                elif player[1] > target[1]:
                    output += "R" * 2
                    facing = "left"
                        
                if player == target:
                    output += "P"
                    travel = False

            elif facing == "left":
                if target[0] > player[0]:
                    output += "L"
                    facing = "down"
                    continue
                elif target[0] < player[0]:
                    output += "R"
                    facing = "up"
                    continue
                  
                if player[1] < target[1]:
                    output += "R" * 2
                    facing = "right"
                elif player[1] > target[1]:
                    output += "S" * (player[1] - target[1])
                    player[1] = target[1]
                        
                if player == target:
                    output += "P"
                    travel = False
        
        coordinates['X'][0] = player
        coordinates[char].pop(target_index)
            
    return output

#SSPSSPSSPRSSSSSSPSSSSSSSPRSSSSPSSSSRSSSSSSSSSSSSSSSSSSSSSSSPRRSSSSSSSSSSSSSSSSSSPRRSSSSSSPSSSSSSSSPRRSSSSSSSSSSSSSSSSSSSPRRSSSSSSSSSSSSSSSSSSSSSSSSSP