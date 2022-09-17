import numpy as np
import json

from flask import request

from codeitsuisse import app

# rubiks = {  
#             "u": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
#             "l": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
#             "f": [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
#             "r": [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
#             "b": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
#             "d": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
#         }

"""
INDEX = [][0]
U:  r -> f
    f -> l
    l -> b
    b -> r

Ui: l -> f
    f -> r
    r -> b
    b -> l

INDEX = [][2]
D: l -> f
    f -> r
    r -> b
    b -> l

Di:  r -> f
    f -> l
    l -> b
    b -> r

INDEX = [2][]
R:  f -> u
    u -> b
    b -> d
    d -> f

Ri: f -> d
    d -> b
    b -> u
    u -> f

INDEX = [0][]
L: f -> d
    d -> b
    b -> u
    u -> f

Li:  f -> u
    u -> b
    b -> d
    d -> f

INDEX = [0][]
F: l -> u
    u -> r
    r -> d
    d -> l

Fi: l -> d
    d -> r
    r -> u
    u -> l

INDEX = [0][]
B: r -> u
    u -> l
    l -> d
    d -> r

Bi: r -> d
    d -> l
    l -> u
    u -> r


"""

def get_operation(ops):
    operations = []
    index = -1
    for i in ops:
        if i == 'i':
            operations[index] += 'i'
        else:
            operations.append(i)
            index += 1
    
    return operations

def rotate(rubiks, operation):
    print(operation)
    if operation == "U":
        temp = rubiks['r'][0]
        rubiks['r'][0] = rubiks['b'][0]
        rubiks['b'][0] = rubiks['l'][0]
        rubiks['l'][0] = rubiks['f'][0]
        rubiks['f'][0] = temp

        #rotate upper
        temp = rubiks['u'][0]
        rubiks['u'][0] = rubiks['u'][2]
        rubiks['u'][2] = temp
        rubiks['u'] = np.transpose(rubiks['u']).tolist()
    
    elif operation == "Ui":
        temp = rubiks['l'][0]
        rubiks['l'][0] = rubiks['b'][0]
        rubiks['b'][0] = rubiks['r'][0]
        rubiks['r'][0] = rubiks['f'][0]
        rubiks['f'][0] = temp
        
        #rotate upper
        rubiks['u'][0] = rubiks['u'][0][::-1]
        rubiks['u'][1] = rubiks['u'][1][::-1]
        rubiks['u'][2] = rubiks['u'][2][::-1]
        rubiks['u'] = np.transpose(rubiks['u']).tolist()

    elif operation == "Di":
        temp = rubiks['r'][2]
        rubiks['r'][2] = rubiks['b'][2]
        rubiks['b'][2] = rubiks['l'][2]
        rubiks['l'][2] = rubiks['f'][2]
        rubiks['f'][2] = temp

        #rotate down
        temp = rubiks['d'][0]
        rubiks['d'][0] = rubiks['d'][2]
        rubiks['d'][2] = temp
        rubiks['d'] = np.transpose(rubiks['d']).tolist()
    
    elif operation == "D":
        temp = rubiks['l'][2]
        rubiks['l'][2] = rubiks['b'][2]
        rubiks['b'][2] = rubiks['r'][2]
        rubiks['r'][2] = rubiks['f'][2]
        rubiks['f'][2] = temp
        
        #rotate down
        rubiks['d'][0] = rubiks['d'][0][::-1]
        rubiks['d'][1] = rubiks['d'][1][::-1]
        rubiks['d'][2] = rubiks['d'][2][::-1]
        rubiks['d'] = np.transpose(rubiks['d']).tolist()
   
    elif operation == "L":
        rubiks['f'] = np.transpose(rubiks['f'])
        rubiks['d'] = np.transpose(rubiks['d'])
        rubiks['b'] = np.transpose(rubiks['b'])
        rubiks['u'] = np.transpose(rubiks['u'])

        temp = rubiks['f'][0]
        rubiks['f'][0] = rubiks['u'][0]
        rubiks['u'][0] = rubiks['b'][0]
        rubiks['b'][0] = rubiks['d'][0]
        rubiks['d'][0] = temp

        rubiks['f'] = np.transpose(rubiks['f']).tolist()
        rubiks['d'] = np.transpose(rubiks['d']).tolist()
        rubiks['b'] = np.transpose(rubiks['b']).tolist()
        rubiks['u'] = np.transpose(rubiks['u']).tolist()

        #rotate left
        temp = rubiks['l'][0]
        rubiks['l'][0] = rubiks['l'][2]
        rubiks['l'][2] = temp
        rubiks['l'] = np.transpose(rubiks['l']).tolist()

    elif operation == "Li":
        rubiks['f'] = np.transpose(rubiks['f'])
        rubiks['d'] = np.transpose(rubiks['d'])
        rubiks['b'] = np.transpose(rubiks['b'])
        rubiks['u'] = np.transpose(rubiks['u'])

        temp = rubiks['f'][0]
        rubiks['f'][0] = rubiks['d'][0]
        rubiks['d'][0] = rubiks['b'][0]
        rubiks['b'][0] = rubiks['u'][0]
        rubiks['u'][0] = temp

        rubiks['f'] = np.transpose(rubiks['f']).tolist()
        rubiks['d'] = np.transpose(rubiks['d']).tolist()
        rubiks['b'] = np.transpose(rubiks['b']).tolist()
        rubiks['u'] = np.transpose(rubiks['u']).tolist()

        #rotate left
        rubiks['l'][0] = rubiks['l'][0][::-1]
        rubiks['l'][1] = rubiks['l'][1][::-1]
        rubiks['l'][2] = rubiks['l'][2][::-1]
        rubiks['l'] = np.transpose(rubiks['l']).tolist()

    elif operation == "R":
        rubiks['f'] = np.transpose(rubiks['f'])
        rubiks['d'] = np.transpose(rubiks['d'])
        rubiks['b'] = np.transpose(rubiks['b'])
        rubiks['u'] = np.transpose(rubiks['u'])

        temp = rubiks['f'][2]
        rubiks['f'][2] = rubiks['d'][2]
        rubiks['d'][2] = rubiks['b'][2]
        rubiks['b'][2] = rubiks['u'][2]
        rubiks['u'][2] = temp

        rubiks['f'] = np.transpose(rubiks['f']).tolist()
        rubiks['d'] = np.transpose(rubiks['d']).tolist()
        rubiks['b'] = np.transpose(rubiks['b']).tolist()
        rubiks['u'] = np.transpose(rubiks['u']).tolist()

        temp = rubiks['r'][0]
        rubiks['r'][0] = rubiks['r'][2]
        rubiks['r'][2] = temp
        rubiks['r'] = np.transpose(rubiks['r']).tolist()

    elif operation == "Ri":
        rubiks['f'] = np.transpose(rubiks['f'])
        rubiks['d'] = np.transpose(rubiks['d'])
        rubiks['b'] = np.transpose(rubiks['b'])
        rubiks['u'] = np.transpose(rubiks['u'])

        temp = rubiks['f'][2]
        rubiks['f'][2] = rubiks['u'][2]
        rubiks['u'][2] = rubiks['b'][2]
        rubiks['b'][2] = rubiks['d'][2]
        rubiks['d'][2] = temp

        rubiks['f'] = np.transpose(rubiks['f']).tolist()
        rubiks['d'] = np.transpose(rubiks['d']).tolist()
        rubiks['b'] = np.transpose(rubiks['b']).tolist()
        rubiks['u'] = np.transpose(rubiks['u']).tolist()

        #rotate left
        rubiks['r'][0] = rubiks['r'][0][::-1]
        rubiks['r'][1] = rubiks['r'][1][::-1]
        rubiks['r'][2] = rubiks['r'][2][::-1]
        rubiks['r'] = np.transpose(rubiks['r']).tolist()

    elif operation == "F":
        rubiks['l'] = np.transpose(rubiks['l'])
        rubiks['r'] = np.transpose(rubiks['r'])

        temp = rubiks['l'][2]
        rubiks['l'][2] = rubiks['d'][0]
        rubiks['d'][0] = rubiks['r'][0].tolist()
        rubiks['r'][0] = rubiks['u'][2]
        rubiks['u'][2] = temp.tolist()

        rubiks['l'] = np.transpose(rubiks['l']).tolist()
        rubiks['r'] = np.transpose(rubiks['r']).tolist()

        #rotate front
        temp = rubiks['f'][0]
        rubiks['f'][0] = rubiks['f'][2]
        rubiks['f'][2] = temp
        rubiks['f'] = np.transpose(rubiks['f']).tolist()

    elif operation == "Fi":
        rubiks['l'] = np.transpose(rubiks['l'])
        rubiks['r'] = np.transpose(rubiks['r'])

        temp = rubiks['l'][2]
        rubiks['l'][2] = rubiks['u'][2]
        rubiks['u'][2] = rubiks['r'][0].tolist()
        rubiks['r'][0] = rubiks['d'][0]
        rubiks['d'][0] = temp.tolist()

        rubiks['l'] = np.transpose(rubiks['l']).tolist()
        rubiks['r'] = np.transpose(rubiks['r']).tolist()

        #rotate front
        rubiks['f'][0] = rubiks['f'][0][::-1]
        rubiks['f'][1] = rubiks['f'][1][::-1]
        rubiks['f'][2] = rubiks['f'][2][::-1]
        rubiks['f'] = np.transpose(rubiks['f']).tolist()

    elif operation == "B":
        rubiks['l'] = np.transpose(rubiks['l'])
        rubiks['r'] = np.transpose(rubiks['r'])

        temp = rubiks['r'][0]
        rubiks['r'][0] = rubiks['d'][0]
        rubiks['d'][2] = rubiks['l'][2].tolist()
        rubiks['l'][2] = rubiks['u'][2]
        rubiks['u'][2] = temp.tolist()

        rubiks['l'] = np.transpose(rubiks['l']).tolist()
        rubiks['r'] = np.transpose(rubiks['r']).tolist()

        #rotate back
        temp = rubiks['b'][0]
        rubiks['b'][0] = rubiks['b'][2]
        rubiks['b'][2] = temp
        rubiks['b'] = np.transpose(rubiks['b']).tolist()

    elif operation == "Bi":
        rubiks['l'] = np.transpose(rubiks['l'])
        rubiks['r'] = np.transpose(rubiks['r'])

        temp = rubiks['r'][0]
        rubiks['r'][0] = rubiks['u'][2]
        rubiks['u'][2] = rubiks['l'][2].tolist()
        rubiks['l'][2] = rubiks['d'][0]
        rubiks['d'][0] = temp.tolist()

        rubiks['l'] = np.transpose(rubiks['l']).tolist()
        rubiks['r'] = np.transpose(rubiks['r']).tolist()

        rubiks['b'][0] = rubiks['b'][0][::-1]
        rubiks['b'][1] = rubiks['b'][1][::-1]
        rubiks['b'][2] = rubiks['b'][2][::-1]
        rubiks['b'] = np.transpose(rubiks['b']).tolist()
    else:
        print("Invalid Operation")
        return -1

@app.route('/rubiks', methods=['POST'])
def rubiks_cube():

    data = request.get_json()
    ops = data.get("ops")
    operations = get_operation(ops)
    rubiks = data.get("state")
    for op in operations:
        rotate(rubiks, op)

    return rubiks

    # for i in rubiks.values():
    #     print(i)
