import json
from flask import request
from codeitsuisse import app

def check_insertion_condition(data_is_integer, array, index):
  if data_is_integer:
    return array[index] < array[index//2]
  else:
    return array[index][1].lower() < array[index//2][1].lower()
    
def insertion(array: list, data, data_is_integer: bool = True):
  array.append(data)
  index = len(array) - 1
  condition = check_insertion_condition(data_is_integer, array, index)
    
  while condition and index > 0:
    array[index], array[index//2] = array[index//2], array[index]
    index = index//2
    condition = check_insertion_condition(data_is_integer, array, index)

def check_extract_min_condition(data_is_integer, array, index):
  if data_is_integer:
    current = array[index]
    index = 2 * index
    if index == 0:
      index = 1
    left, right = array[index], array[index + 1]

    return (current, left, index) if left < right else (current, right, index + 1)
  else:
    current = array[index][1].lower()
    index = 2 * index
    if index == 0:
      index = 1
    left, right = array[index][1].lower(), array[index + 1][1].lower()

    return (current, left, index) if left < right else (current, right, index + 1)



def extract_min(array: list, data_is_integer: bool = True):
  pop, array[0] = array[0], array[len(array) - 1]
  array.pop() 

  if len(array) == 1:
    if pop > array[0] and data_is_integer:
      pop, array[0] = array[0], pop
    elif not data_is_integer:
      if pop[1] > array[0][1]:
        pop, array[0] = array[0], pop

  index = 0

  try:
    current, smallest, swap_index = check_extract_min_condition(data_is_integer, array, index)
  except IndexError:
    return pop

  while current > smallest:
    array[index], array[swap_index] = array[swap_index], array[index]
    index = swap_index
    try:
        current, smallest, swap_index = check_extract_min_condition(data_is_integer, array, index)
    except IndexError:
        return pop

  return pop


def heapsort(array: list):
  hashmap = {}
  trees = []
    
  # --- heapsort based on timestamp and ticker ---
  for line in array:
    line = line.split(',')
    try:
      timestamp = int(line[0][:2]+line[0][3:])
      if timestamp in hashmap:                
        insertion(hashmap[timestamp], line, False)
      else:
        hashmap[timestamp] = []
        hashmap[timestamp].append(line)
        insertion(trees, timestamp)

    except ValueError:
      print("Error data format")

  return trees, hashmap

@app.route('/tickerStreamPart1', methods=['POST'])
def to_cumulative():
  data = request.get_json()
  stream = data.get("stream")
  output = []
  history = {}
  sorted_timestamp, sorted_ticker = heapsort(stream)
  for _ in range(len(sorted_timestamp)):
    timestamp = extract_min(sorted_timestamp)
    temp = f"{sorted_ticker[timestamp][0][0]},"
    encounter = []
    for _ in range(len(sorted_ticker[timestamp])):
      data = extract_min(sorted_ticker[timestamp], False)
      try:
        quantity, price = int(data[2]), float(data[3])
        if data[1] in history:
          history[data[1]][0] += quantity
          history[data[1]][1] += round(quantity * price, 1)
          history[data[1]][1] = round(history[data[1]][1], 1)
        else:
          history[data[1]] = [quantity, round(quantity * price, 1)]
      except ValueError:
        print("Error during Conversion Process")
        return -1
      
      if data[1] not in encounter:
        encounter.append(data[1])

    for ticker in encounter:
      temp += f"{ticker},{history[ticker][0]},{history[ticker][1]},"
      
    temp = temp[:-1]
    output.append(temp)

  return {"output": output}

@app.route('/tickerStreamPart2', methods=['POST'])
def to_cumulative_delayed():
  data = request.get_json()
  stream = data.get("stream")
  quantity_block = data.get("quantityBlock")
  output = []
  history = {}
  sorted_timestamp, sorted_ticker = heapsort(stream)
  for _ in range(len(sorted_timestamp)):
    timestamp = extract_min(sorted_timestamp)
    encounter = []
    for _ in range(len(sorted_ticker[timestamp])):
      data = extract_min(sorted_ticker[timestamp], False)
      try:
        quantity, price = int(data[2]), float(data[3])
        if data[1] in history:
          cumulative_notional = 0
          while history[data[1]][0] + quantity >= quantity_block:
            room_to_fill = quantity_block - history[data[1]][0]
            cumulative_notional = history[data[1]][1] + round(room_to_fill * price, 1)
            history[data[1]][3] += quantity_block
            history[data[1]][2] += round(room_to_fill * price, 1)
            history[data[1]][2] = round(history[data[1]][2], 1)
            history[data[1]][0] = 0
            history[data[1]][1] = 0
            quantity -= room_to_fill

          history[data[1]][0] += quantity
          history[data[1]][1] += round(quantity * price, 1)
          history[data[1]][1] = round(history[data[1]][1], 1)
          
        else:
          cumulative_notional = 0
          digest = 0
          while quantity >= quantity_block:
            cumulative_notional += round(quantity_block * price, 1)
            digest += quantity_block
            quantity -= quantity_block

          history[data[1]] = [quantity, round(quantity * price, 1), cumulative_notional, digest]

      except ValueError:
        print("Error during Conversion Process")
        return -1

      if data[1] not in encounter:
        encounter.append(data[1])

    for ticker in encounter:
      temp = f"{timestamp},{ticker},{history[ticker][3]},{history[ticker][2]}"
      output.append(temp)

  return {"output": output}