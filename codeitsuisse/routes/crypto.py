import json

from flask import request, jsonify
import logging
from codeitsuisse import app

history = {1:4}

def get_highest_value(num):
    original_number = num

    if num in history:
        return history[num]

    highest_price = num

    if num % 2 == 0:
        num = num // 2
    else:
        num = num * 3 + 1

    temp = get_highest_value(num)
    if highest_price < temp:
        history[original_number] = temp
        return temp
    else:
        history[original_number] = highest_price
        return highest_price

def solve(arr):
    output = []
    for num in arr:
        if num not in history:
            get_highest_value(num)
        output.append(history[num])

    return output

@app.route('/cryptocollapz', methods=['POST'])
def crypo_fall():
    data = request.get_json()

    output = []
    for arr in data:
        output.append(solve(arr))
    
    return json.dumps(output)