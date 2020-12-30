import pickle
# load the previous score if it exists
try:
    with open('score.dat', 'rb') as file:
        record = pickle.load(file)
        file.close()
except:
    record = 0
print(record)
with open('score.dat', 'wb') as file:
    pickle.dump(0, file)